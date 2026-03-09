# Task Plot Audit

- generated_at: 2026-03-10T00:00:16
- mode: existing
- task_path: E:\Taskbeacon\T000002-bart

## 1. Inputs and provenance

- E:\Taskbeacon\T000002-bart\README.md
- E:\Taskbeacon\T000002-bart\config\config.yaml
- E:\Taskbeacon\T000002-bart\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | Fixation | `fixation` stimulus before each trial. |
- | Pump Decision | Balloon + dynamic score text (`score_bank_text`) and pump/cash response. |
- | Outcome | Pop / cash / timeout outcome branch. |
- | Feedback | Numeric trial score display. |

## 3. Evidence extracted from config/source

- blue: phase=pre pump fixation, deadline_expr=settings.fixation_duration, response_expr=n/a, stim_expr='fixation'
- blue: phase=pump decision, deadline_expr=decision_deadline_s, response_expr=n/a, stim_expr=f'{condition}_balloon'
- blue: phase=pop outcome, deadline_expr=settings.response_feedback_duration, response_expr=n/a, stim_expr=f'{condition}_pop+pop_sound'
- blue: phase=trial feedback, deadline_expr=settings.feedback_duration, response_expr=n/a, stim_expr=fb_stim
- yellow: phase=pre pump fixation, deadline_expr=settings.fixation_duration, response_expr=n/a, stim_expr='fixation'
- yellow: phase=pump decision, deadline_expr=decision_deadline_s, response_expr=n/a, stim_expr=f'{condition}_balloon'
- yellow: phase=pop outcome, deadline_expr=settings.response_feedback_duration, response_expr=n/a, stim_expr=f'{condition}_pop+pop_sound'
- yellow: phase=trial feedback, deadline_expr=settings.feedback_duration, response_expr=n/a, stim_expr=fb_stim
- orange: phase=pre pump fixation, deadline_expr=settings.fixation_duration, response_expr=n/a, stim_expr='fixation'
- orange: phase=pump decision, deadline_expr=decision_deadline_s, response_expr=n/a, stim_expr=f'{condition}_balloon'
- orange: phase=pop outcome, deadline_expr=settings.response_feedback_duration, response_expr=n/a, stim_expr=f'{condition}_pop+pop_sound'
- orange: phase=trial feedback, deadline_expr=settings.feedback_duration, response_expr=n/a, stim_expr=fb_stim

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 4
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.031, right=0.033, blank=0.128
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.031, 'right_ratio': 0.0331, 'blank_ratio': 0.1278}
- validator_warnings:
  - timelines[0].phases[1] missing duration_ms; renderer will annotate as n/a.

## 7. Output files and checksums

- E:\Taskbeacon\T000002-bart\references\task_plot_spec.yaml: sha256=2fb0cb93c9093592bf33ef9cd049591592802a1d6ba26b12f6fc464862534fb4
- E:\Taskbeacon\T000002-bart\references\task_plot_spec.json: sha256=c6af625290325353e7a790a1cb956cc92a882020ad4c360a1f04bbba78d298d0
- E:\Taskbeacon\T000002-bart\references\task_plot_source_excerpt.md: sha256=bab5ed8015dd0e3b10648bf2211ceee4da61c49aab69e5055bc087628f0a1cf4
- E:\Taskbeacon\T000002-bart\task_flow.png: sha256=78c9d652b3248226bf4760abafc161e3d290ae3cb5eaadf86fe84564db292529

## 8. Inferred/uncertain items

- blue:pump decision:unable to resolve duration from 'float(settings.balloon_duration) if decision_timeout_enabled else None'
- yellow:pump decision:unable to resolve duration from 'float(settings.balloon_duration) if decision_timeout_enabled else None'
- orange:pump decision:unable to resolve duration from 'float(settings.balloon_duration) if decision_timeout_enabled else None'
- collapsed equivalent condition logic into representative timeline: blue, yellow, orange
- unparsed if-tests defaulted to condition-agnostic applicability: pump_count >= explosion_point; response == settings.cash_key; response == settings.pump_key
