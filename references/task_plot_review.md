# Task Plot Review

Review checklist source: `E:/Taskbeacon/skills/task-plot/references/review_checklist.md`.

Generated image:
- `E:/Taskbeacon/T000002-bart/task_flow.png`

## Evidence Match

- Pass: task is labeled as BART / Balloon Analogue Risk Task.
- Pass: condition rows are present for Blue, Yellow, and Orange balloons.
- Pass: condition parameters match config: Blue `+5` max 24, Yellow `+10` max 12, Orange `+20` max 6.
- Pass: phase order matches `run_trial.py`: fixation, decision, pump loop, outcome, feedback.
- Pass: response mapping is correct: `space` pumps, `right` cashes out.
- Pass: outcome branch shows Cash versus Pop, matching the cash-out and explosion branches.
- Pass: timing labels show 0.8 s fixation and 1.0 s outcome/feedback where relevant.

## Visual Quality

- Pass: text is readable at normal preview size.
- Pass: rows and arrows clearly show temporal order.
- Pass: gray screen boxes, row separators, and restrained condition colors match the TaskBeacon figure style.
- Pass: pump-loop arrows make repeated pumping clear without drawing every pump.
- Pass: the image model did not generate its own logo, watermark, or brand text.
- Pass: the fixed TaskBeacon logo lockup was applied in post-processing and appears in the top-right corner without overlapping timeline content.
- Pass: README embeds `![Task Flow](task_flow.png)` under `## 2. Task Flow`.

## Decision

Accepted regenerated `task_flow.png` from the upgraded `task-plot` skill template and fixed logo overlay workflow. No further regeneration required.
