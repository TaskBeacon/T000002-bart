# CHANGELOG

All notable development changes for T000002-bart are documented here.

## [1.1.3] - 2026-03-10

### Changed
- Updated `src/run_trial.py` so every participant-visible outcome and feedback phase emits `set_trial_context(...)`, not just the response window.
- Regenerated task-plot artifacts under `references/task_plot_*` and `task_flow.png` using the updated task-plot skill.
- Updated `README.md` to embed the generated task-flow figure.
- Normalized `config/config.yaml` text encoding header.

### Fixed
- Restored audit visibility for BART pop, cash, timeout, and feedback screens in downstream task-plot inference.
- Updated the generated workflow figure to use participant-visible sample stimuli rather than abstract placeholders.

### Added
- Added comparison figure exports `task_flow_gemini3.png` and `task_flow_opus4.6.png`.

## [1.1.2] - 2026-02-23

### Changed
- Removed redundant `_TRIAL_COUNTER` and `_next_trial_id()` manually defined boilerplate in favor of native `psyflow.next_trial_id` synchronization.
- Removed redundant duration resolver (`_deadline_s()`) locally, since duration array parsing is now safely handled natively inside `set_trial_context(...)`.
- Refactored `src/run_trial.py` to maintain decoupled generalized tracking from `psyflow`.

## [1.1.1] - 2026-02-18

### Changed
- Refactored responder context phase names in `src/run_trial.py` to task-specific labels (removed generic MID-style phase naming).
- Updated stage comments in `src/run_trial.py` to phase-aligned labels for cleaner auditability.
- Updated `README.md` to keep runtime phase documentation aligned with the implemented trial context phases.

### Fixed
- Removed legacy stage comment patterns (`cue/anticipation/target/feedback`) from trial runtime code.

## [1.1.0] - 2026-02-17

### Added
- Added mode-aware main.py flow for human, qa, and sim modes.
- Added split runtime configs: config/config.yaml, config/config_qa.yaml, config/config_scripted_sim.yaml, and config/config_sampler_sim.yaml.
- Added task-local responder scaffold in 
esponders/task_sampler.py.
- Added outputs/.gitkeep and standardized output folders for human/qa/sim runs.

### Changed
- Aligned trigger config to structured schema (	riggers.map, 	riggers.driver, 	riggers.policy, 	riggers.timing).
- Aligned src/run_trial.py to set responder trial context via set_trial_context(...) at response windows.
- Added/updated 	askbeacon.yaml with contracts.psyflow_taps: v0.1.0.
- Updated .gitignore to match standardized task artifacts and output handling.

### Verified
- psyflow-validate <task> passes all contract checks (including artifacts).
- psyflow-qa <task> --config config/config_qa.yaml --no-maturity-update passes.
- python main.py sim --config config/config_scripted_sim.yaml runs successfully and writes sim outputs.
