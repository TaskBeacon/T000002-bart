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
  - Human config: `2`
  - QA/sim configs: `1`
- Trials per block:
  - Human config: `5`
  - QA/sim configs: `9`
- Randomization/counterbalancing:
  - Uses built-in `BlockUnit.generate_conditions()` with condition labels from `task.conditions`.
  - No explicit `condition_weights` is currently defined, so generation is equal-weight by default.
- Condition generation method:
  - Built-in generator (`BlockUnit.generate_conditions(...)`), no custom generator.
- Runtime-generated trial values:
  - `explosion_point` is generated in `src/run_trial.py` using `random.randint(1, max_pumps)` each trial.
  - This draw is not explicitly linked to block/trial seed values, so exact burst sequences are not fully reproducible.

### Trial State Machine

1. State name: `pre_pump_fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown: `fixation`
   - Valid keys: `pump_key`, `cash_key` are context-declared; response not captured in this state
   - Timeout behavior: fixed duration (`fixation_duration`)
   - Next state: `pump_decision`

2. State name: `pump_decision` (looped)
   - Onset trigger: `{condition}_balloon_onset`
   - Stimuli shown: `{condition}_balloon` + dynamic score text
   - Valid keys: `pump_key`, `cash_key`
   - Timeout behavior: end decision loop on deadline (`balloon_duration`) and branch to timeout outcome
   - Next state:
     - `pump_decision` (if pump and no explosion)
     - `outcome_pop` (if pump reaches/exceeds explosion point)
     - `outcome_cash` (if cash key pressed)
     - `outcome_timeout` (if no response)

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
  - Participant-facing meaning: lowest-risk balloon class in this implementation.
  - Concrete stimulus realization: `stimuli.blue_balloon`, `stimuli.blue_pop`.
  - Outcome rules: `blue_max_pumps=24`, `blue_delta=5`.

- Condition ID: `yellow`
  - Participant-facing meaning: medium-risk balloon class.
  - Concrete stimulus realization: `stimuli.yellow_balloon`, `stimuli.yellow_pop`.
  - Outcome rules: `yellow_max_pumps=12`, `yellow_delta=10`.

- Condition ID: `orange`
  - Participant-facing meaning: highest-risk balloon class.
  - Concrete stimulus realization: `stimuli.orange_balloon`, `stimuli.orange_pop`.
  - Outcome rules: `orange_max_pumps=6`, `orange_delta=20`.

Participant-facing text/stimulus source:

- Participant-facing text source: mostly `config/*.yaml -> stimuli.*`
- Why this source is appropriate for auditability: wording is centralized and visible in config.
- Localization strategy: language-specific text can be swapped in config without editing code.
- Current exception: dynamic per-pump score text (`TextStim(text=f"+{score_bank}")`) is generated in `src/run_trial.py`.

## 4. Response and Scoring Rules

- Response mapping:
  - pump action: `pump_key` (default `space`)
  - cash action: `cash_key` (default `right`)
- Response key source:
  - Config-driven (`task.pump_key`, `task.cash_key`, `task.key_list`)
- Missing-response policy:
  - Timeout branch when no key before `balloon_duration`
- Correctness logic:
  - No hit/error correctness label; outcomes are `pop`, `cash`, `timeout`.
- Reward/penalty updates:
  - Current implementation initializes `score_bank` to condition delta before first pump.
  - On successful pump without explosion, `score_bank += delta`.
  - Pop sets trial score to `0`; cash sets trial score to current `score_bank`.
- Running metrics:
  - Per-trial `feedback_fb_score` logged; block and final score computed as sums.
  - Adjusted-pump metric (canonical BART analysis metric) is not computed in runtime.

## 5. Stimulus Layout Plan

- Screen name: `pre_pump_fixation`
  - Stimulus IDs shown together: `fixation`
  - Layout anchors (`pos`): center
  - Size/spacing: default text size for fixation
  - Readability/overlap checks: minimal screen load
  - Rationale: baseline visual anchor before decision loop

- Screen name: `pump_decision`
  - Stimulus IDs shown together: `{condition}_balloon`, dynamic score text
  - Layout anchors (`pos`): balloon default center; score text at `[0, -4]` (deg units)
  - Size/spacing: balloon scales from `initial_balloon_scale` to `max_balloon_scale`
  - Readability/overlap checks: score text remains below balloon footprint
  - Rationale: continuous risk accumulation visualization

- Screen name: `outcome_pop` / `outcome_cash` / `outcome_timeout`
  - Stimulus IDs shown together: outcome image/text + optional sound
  - Layout anchors (`pos`): centered outcome feedback
  - Size/spacing: brief fixed-duration presentation
  - Readability/overlap checks: single message per outcome state
  - Rationale: explicit outcome transition before summary feedback

- Screen name: `feedback`
  - Stimulus IDs shown together: `win_feedback` or `lose_feedback`
  - Layout anchors (`pos`): centered text
  - Size/spacing: fixed feedback duration
  - Readability/overlap checks: high contrast text color
  - Rationale: communicates trial-level gain/loss score

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 98 | experiment start |
| `exp_end` | 99 | experiment end |
| `block_onset` | 100 | block start |
| `block_end` | 101 | block end |
| `fixation_onset` | 1 | fixation onset |
| `blue_balloon_onset` | 36 | blue decision onset |
| `yellow_balloon_onset` | 16 | yellow decision onset |
| `orange_balloon_onset` | 26 | orange decision onset |
| `blue_pump_press` / `yellow_pump_press` / `orange_pump_press` | 34 / 14 / 24 | pump key press |
| `blue_cash_press` / `yellow_cash_press` / `orange_cash_press` | 35 / 15 / 25 | cash key press |
| `blue_pop` / `yellow_pop` / `orange_pop` | 31 / 11 / 21 | explosion outcome onset |
| `blue_cash` / `yellow_cash` / `orange_cash` | 32 / 12 / 22 | cash outcome onset |
| `blue_timeout` / `yellow_timeout` / `orange_timeout` | 33 / 13 / 23 | timeout outcome onset |
| `feedback_onset` | 50 | final trial feedback onset |

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style:
  - Single mode-aware execution path (`human`, `qa`, `sim`) with shared setup and block loop.
- `utils.py` used?
  - No task-level utils module in this task.
- Custom controller used?
  - No. Task uses `BlockUnit.generate_conditions(...)` + task-local `run_trial`.
- Why PsyFlow-native path is sufficient:
  - Condition scheduling and trial logging fit built-in `BlockUnit` and `StimUnit` abstractions.
- Legacy/backward-compatibility fallback logic required?
  - No explicit fallback branches in T000002 runtime.

## 8. Inference Log

- Decision: treat `orange` as high-risk color class analogous to red-coded variants.
  - Why inference was required: selected references use differing color labels across variants.
  - Citation-supported rationale: `W2005240523` documents color-coded risk classes in modified BART.

- Decision: mark current `total_trials=10` and `2s` response deadline as protocol adaptations.
  - Why inference was required: canonical protocol often uses larger trial counts and self-paced decisions.
  - Citation-supported rationale: `W2146196757` canonical task structure and contingency logic.

- Decision: flag explosion sampling implementation for manual review.
  - Why inference was required: current code uses per-trial independent RNG, while modified protocol literature describes bounded lists sampled without replacement.
  - Citation-supported rationale: `W2005240523` modified BART sampling description.

- Decision: flag score-bank initialization for manual review.
  - Why inference was required: current implementation starts temporary bank above zero before first successful pump.
  - Citation-supported rationale: `W2146196757` pump action is the mechanism that accrues temporary reward.
