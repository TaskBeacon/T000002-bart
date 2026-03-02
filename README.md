# Balloon Analogue Risk Task (BART)

![Maturity: smoke_tested](https://img.shields.io/badge/Maturity-smoke_tested-d97706?style=for-the-badge&labelColor=c2410c)

| Field | Value |
|---|---|
| Name | Balloon Analogue Risk Task (BART) |
| Version | main (1.1) |
| URL / Repository | https://github.com/TaskBeacon/T000002-bart |
| Short Description | A risk-taking task based on BART with color-specific burst profiles. |
| Created By | Zhipeng Cao (zhipeng30@foxmail.com) |
| Date Updated | 2026/03/02 |
| PsyFlow Version | 0.1.0 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior/EEG |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |

## 1. Task Overview

BART measures risk-taking by requiring repeated choices between pumping a balloon for higher temporary reward and cashing out to bank reward safely. If a balloon explodes, that trial's temporary reward is lost.

This implementation uses deterministic explosion sampling with config-defined mode (`without_replacement_cycle` by default), three color conditions (`blue`, `yellow`, `orange`), and config-first participant-facing stimuli for localization portability.

## 2. Task Flow

### Controller Logic

- `main.py` runs one unified mode-aware flow (`human`, `qa`, `sim`).
- `BlockUnit.generate_conditions()` handles condition sequencing.
- `src/run_trial.py` handles trial states (`pre_pump_fixation`, `pump_decision`, outcome, feedback).
- Explosion points are sampled by a deterministic condition/block sampler, not global RNG.

### Block-Level Flow

| Step | Description |
|---|---|
| Load Config | Load mode-specific config from `config/`. |
| Collect Subject Info | Human uses `SubInfo`; QA/SIM use synthetic IDs. |
| Setup Trigger Runtime | Hardware in human mode, mock in QA/SIM. |
| Initialize Window/Input | Build PsychoPy window + keyboard. |
| Load Stimuli | Load from `StimBank` (`config`-defined). |
| Show Instructions | Show config-defined instruction text. |
| Loop Blocks | Run trial blocks and break screen. |
| Show Goodbye | Show final score and terminate. |
| Save Data | Save trial rows to CSV. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Fixation | `fixation` stimulus before each trial. |
| Pump Decision | Balloon + dynamic score text (`score_bank_text`) and pump/cash response. |
| Outcome | Pop / cash / timeout outcome branch. |
| Feedback | Numeric trial score display. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `pre_pump_fixation` | Pre-decision fixation stage. |
| `pump_decision` | Repeated pump-or-cash decision stage. |

## 3. Configuration Summary

### a. Subject Info

- Defined in `subinfo_fields` / `subinfo_mapping`.
- Includes `subject_id`, `subname`, `age`, `gender`.
- Participant-facing labels are config-defined for localization.

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1920, 1080]` |
| `units` | `deg` |
| `screen` | `1` |
| `bg_color` | `gray` |
| `fullscreen` | `True` |
| `monitor_width_cm` | `60` |
| `monitor_distance_cm` | `72` |

### c. Stimuli

| Name | Type | Notes |
|---|---|---|
| `fixation` | text | Pre-trial fixation cross |
| `[color]_balloon` | image | Balloon stimulus by condition |
| `score_bank_text` | text template | Dynamic `+{score_bank}` display |
| `[color]_pop` | image | Explosion outcome image |
| `cash_screen`, `timeout_screen` | text | Outcome text screens |
| `win_feedback`, `lose_feedback` | text template | Trial feedback with `{fb_score}` |
| `instruction_text`, `block_break`, `good_bye` | textbox/text | Participant-facing instructions and summaries |

### d. Timing

| Parameter | Value |
|---|---|
| `fixation_duration` | `0.8s` |
| `response_feedback_duration` | `1.0s` |
| `balloon_duration` | `2.0s` (used when `decision_timeout_enabled=true`) |
| `feedback_duration` | `1.0s` |

### e. Task Settings

| Parameter | Human | QA/SIM |
|---|---|---|
| `total_blocks` | 3 | 1 |
| `trial_per_block` | 10 | 9 |
| `total_trials` | 30 | 9 |
| `conditions` | `[blue, yellow, orange]` | `[blue, yellow, orange]` |
| `pump_key` | `space` | `space` |
| `cash_key` | `right` | `right` |
| `explosion_sampling_mode` | `without_replacement_cycle` | `without_replacement_cycle` |
| `decision_timeout_enabled` | `false` | `true` |

## 4. Methods (for academic publication)

Participants completed a Balloon Analogue Risk Task with color-coded balloon conditions (`blue`, `yellow`, `orange`) that differed in burst limits and reward increments. In each trial, participants could repeatedly pump (`space`) to increase temporary reward or cash out (`right`) to bank accumulated reward before explosion. If explosion occurred, that trial's temporary reward was lost. 

The human protocol uses 30 trials (3 blocks x 10 trials), while QA/SIM profiles are reduced for validation runtime. Explosion points are generated with a deterministic condition/block sampler configured by `explosion_sampling_mode`, and participant-facing text/stimuli are config-defined to support localization.

## 5. References

- Lejuez, C. W., Read, J. P., Kahler, C. W., Richards, J. B., Ramsey, S. E., Stuart, G. L., Strong, D. R., & Brown, R. A. (2002). *Evaluation of a behavioral measure of risk taking: The Balloon Analogue Risk Task (BART).* Journal of Experimental Psychology: Applied, 8(2), 75-84. https://doi.org/10.1037/1076-898X.8.2.75
- See `references/` for structured evidence artifacts and mapping tables.
