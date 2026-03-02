# Task Logic Audit: Balloon Analogue Risk Task (BART)

## 1. Paradigm Intent

- Task: `bart`
- Primary construct: behavioral risk taking under uncertain loss.
- Manipulated factors:
  - Balloon risk condition (`blue`, `yellow`, `orange`)
  - Repeated within-trial pump-versus-cash decisions.
- Dependent measures:
  - Pumps per trial
  - Pop/cash/timeout outcomes
  - Trial reward (`feedback_fb_score`)
  - Aggregate score across trials/blocks
- Key citations:
  - `W2146196757` (Lejuez et al., 2002)
  - `W2029537564` (Lejuez et al., 2003)
  - `W2005240523` (Rao et al., 2008)

## 2. Block/Trial Workflow

### Block Structure

- Total blocks:
  - Human config: `3`
  - QA/sim configs: `1`
- Trials per block:
  - Human config: `10`
  - QA/sim configs: `9`
- Randomization/counterbalancing:
  - Built-in `BlockUnit.generate_conditions()` with equal-weight condition labels.
- Condition generation method:
  - Built-in generator (`BlockUnit.generate_conditions(...)`), no custom generator.
- Runtime-generated trial values:
  - `explosion_point` is generated in `src/run_trial.py` with deterministic per-block/per-condition sampler.
  - Sampling mode is config-driven via `task.explosion_sampling_mode` (`without_replacement_cycle` by default).

### Trial State Machine

1. State name: `pre_pump_fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown: `fixation`
   - Valid keys: `pump_key`, `cash_key` are context-declared
   - Timeout behavior: fixed duration (`fixation_duration`)
   - Next state: `pump_decision`

2. State name: `pump_decision` (looped)
   - Onset trigger: `{condition}_balloon_onset`
   - Stimuli shown: `{condition}_balloon` + `score_bank_text`
   - Valid keys: `pump_key`, `cash_key`
   - Timeout behavior:
     - Human default: no planned timeout (`decision_timeout_enabled=false`)
     - QA/SIM: bounded window (`balloon_duration`) with `{condition}_timeout`
   - Next state:
     - `pump_decision` (if pump and no explosion)
     - `outcome_pop` (if pump reaches explosion point)
     - `outcome_cash` (if cash key pressed)
     - `outcome_timeout` (if no response in bounded mode)

3. State name: `outcome_pop` / `outcome_cash` / `outcome_timeout`
   - Onset trigger: condition-specific outcome trigger
   - Stimuli shown:
     - pop: `{condition}_pop` + `pop_sound`
     - cash: `cash_screen` + `cash_sound`
     - timeout: `timeout_screen`
   - Valid keys: none
   - Timeout behavior: fixed display duration (`response_feedback_duration`)
   - Next state: `feedback`

4. State name: `feedback`
   - Onset trigger: `feedback_onset`
   - Stimuli shown: `win_feedback` or `lose_feedback` with `fb_score`
   - Valid keys: none
   - Timeout behavior: fixed duration (`feedback_duration`)
   - Next state: trial end

## 3. Condition Semantics

- Condition ID: `blue`
  - Participant-facing meaning: low-risk balloon class in this implementation.
  - Concrete stimulus realization: `stimuli.blue_balloon`, `stimuli.blue_pop`.
  - Outcome rules: `blue_max_pumps=24`, `blue_delta=5`.

- Condition ID: `yellow`
  - Participant-facing meaning: medium-risk balloon class.
  - Concrete stimulus realization: `stimuli.yellow_balloon`, `stimuli.yellow_pop`.
  - Outcome rules: `yellow_max_pumps=12`, `yellow_delta=10`.

- Condition ID: `orange`
  - Participant-facing meaning: high-risk balloon class.
  - Concrete stimulus realization: `stimuli.orange_balloon`, `stimuli.orange_pop`.
  - Outcome rules: `orange_max_pumps=6`, `orange_delta=20`.

Participant-facing text/stimulus source:

- Participant-facing text source: `config/*.yaml -> stimuli.*`
- Why this source is appropriate for auditability: wording and labels are centralized in config.
- Localization strategy: language variants can be swapped via config without code edits.

## 4. Response and Scoring Rules

- Response mapping:
  - pump action: `pump_key` (default `space`)
  - cash action: `cash_key` (default `right`)
- Response key source:
  - Config-driven (`task.pump_key`, `task.cash_key`, `task.key_list`)
- Missing-response policy:
  - QA/SIM bounded mode can branch to timeout.
  - Human default is unbounded decision policy (`decision_timeout_enabled=false`).
- Correctness logic:
  - No hit/error classification; outcomes are `pop`, `cash`, `timeout`.
- Reward/penalty updates:
  - `score_bank` starts at `0`.
  - Successful non-explosive pump adds `delta`.
  - Pop sets trial score to `0`; cash uses current `score_bank`.
- Running metrics:
  - Per-trial `feedback_fb_score` logged; block/final score computed by sum.

## 5. Stimulus Layout Plan

- Screen name: `pre_pump_fixation`
  - Stimulus IDs shown together: `fixation`
  - Layout anchors (`pos`): center
  - Size/spacing: default text size
  - Readability/overlap checks: minimal load
  - Rationale: pre-decision visual anchor

- Screen name: `pump_decision`
  - Stimulus IDs shown together: `{condition}_balloon`, `score_bank_text`
  - Layout anchors (`pos`): balloon centered, score text at config-defined lower position
  - Size/spacing: balloon scales from `initial_balloon_scale` to `max_balloon_scale`
  - Readability/overlap checks: score text kept below balloon centerline
  - Rationale: explicit visualization of temporary reward growth and risk progression

- Screen name: `outcome_pop` / `outcome_cash` / `outcome_timeout`
  - Stimulus IDs shown together: outcome visual/text + optional sound
  - Layout anchors (`pos`): centered
  - Size/spacing: brief fixed-duration display
  - Readability/overlap checks: single outcome message per stage
  - Rationale: explicit state transition feedback

- Screen name: `feedback`
  - Stimulus IDs shown together: `win_feedback` or `lose_feedback`
  - Layout anchors (`pos`): centered text
  - Size/spacing: fixed `feedback_duration`
  - Readability/overlap checks: high-contrast color coding
  - Rationale: trial-level score reporting

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 98 | experiment start |
| `exp_end` | 99 | experiment end |
| `block_onset` | 100 | block start |
| `block_end` | 101 | block end |
| `fixation_onset` | 1 | fixation onset |
| `blue_balloon_onset` / `yellow_balloon_onset` / `orange_balloon_onset` | 36 / 16 / 26 | decision onset by condition |
| `blue_pump_press` / `yellow_pump_press` / `orange_pump_press` | 34 / 14 / 24 | pump key press |
| `blue_cash_press` / `yellow_cash_press` / `orange_cash_press` | 35 / 15 / 25 | cash key press |
| `blue_pop` / `yellow_pop` / `orange_pop` | 31 / 11 / 21 | explosion outcome onset |
| `blue_cash` / `yellow_cash` / `orange_cash` | 32 / 12 / 22 | cash outcome onset |
| `blue_timeout` / `yellow_timeout` / `orange_timeout` | 33 / 13 / 23 | timeout outcome onset |
| `feedback_onset` | 50 | final trial feedback onset |

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style:
  - One mode-aware flow (`human`, `qa`, `sim`) with shared setup and block loop.
- `utils.py` used?
  - No task-level utils module.
- Custom controller used?
  - No; uses `BlockUnit.generate_conditions(...)` and task-local `run_trial`.
- Why PsyFlow-native path is sufficient:
  - Built-in block scheduling and `StimUnit` response capture support required flow.
- Legacy/backward-compatibility fallback logic required?
  - No explicit legacy branch.

## 8. Inference Log

- Decision: keep three color conditions (`blue`, `yellow`, `orange`) with task-specific risk ranges.
  - Why inference was required: references use variant-specific color/range sets.
  - Citation-supported rationale: `W2005240523` modified BART color-condition workflow.

- Decision: human profile set to 30 total trials; QA/SIM remain reduced.
  - Why inference was required: QA/SIM runtime constraints conflict with full protocol length.
  - Citation-supported rationale: canonical BART literature emphasizes larger trial counts (`W2146196757`).

- Decision: bounded timeout kept for QA/SIM but disabled for default human run.
  - Why inference was required: automation needs bounded waits; canonical human protocol is typically self-paced.
  - Citation-supported rationale: `W2146196757` contingency logic and canonical task framing.
