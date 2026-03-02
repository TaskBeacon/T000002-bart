# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `trial_count` | `task.total_blocks`, `task.trial_per_block`, `task.total_trials` | Human `3 x 10 = 30`; QA/SIM `1 x 9 = 9` | `W2146196757` | Canonical BART protocols typically use around 30 balloons for stable behavior metrics. | `adapted` | Human profile aligned to canonical scale; QA/SIM remains reduced for runtime validation only. |
| `condition_set` | `task.conditions` | `['blue', 'yellow', 'orange']` | `W2005240523` | Modified BART variants use color-coded balloon types with distinct burst distributions. | `adapted` | Uses `orange` as high-risk condition label. |
| `max_pumps_profile` | `task.blue_max_pumps`, `task.yellow_max_pumps`, `task.orange_max_pumps` | `24`, `12`, `6` | `W2005240523` | Modified BART studies define color-specific burst ranges. | `adapted` | Current ranges are task-specific adaptation and should be reported explicitly in methods. |
| `reward_increment` | `task.blue_delta`, `task.yellow_delta`, `task.orange_delta` | `5`, `10`, `20` per successful pump | `W2005240523` | Modified variants use fixed point increments tied to condition. | `adapted` | Condition-dependent deltas are implementation-specific and documented. |
| `action_mapping` | `task.pump_key`, `task.cash_key`, `task.key_list` | pump=`space`, cash=`right` | `W2146196757` | Core action pair is inflate-versus-collect. | `inferred` | Key labels remain config-defined for hardware/localization portability. |
| `response_deadline_policy` | `task.decision_timeout_enabled`, `timing.balloon_duration` | Human `false` (self-paced target), QA/SIM `true` + `2.0s` | `W2146196757` | Canonical BART is generally self-paced in human sessions. | `adapted` | QA/SIM keeps bounded window to avoid hanging automated runs. |
| `explosion_sampling_method` | `task.explosion_sampling_mode` + `src/run_trial.py` sampler | `without_replacement_cycle` (deterministic by block/condition seed) | `W2005240523` | Modified protocols describe bounded burst sampling per color. | `adapted` | Replaced global per-trial RNG draw for reproducibility and explicit policy. |
| `score_bank_initialization` | `src/run_trial.py` | Trial bank starts at `0`; increases only after successful pump | `W2146196757` | Pumping is the action that accrues temporary reward. | `direct` | Removes prior non-zero pre-pump bank behavior. |
| `primary_metric_support` | trial output columns (`feedback_fb_score`, `pump_count`, `fb_type`) | Per-trial metrics emitted; adjusted pumps can be derived offline | `W2029537564` | BART validation emphasizes non-exploded pump behavior metrics. | `inferred` | Derivation script can compute adjusted-pump metrics from logged rows. |
