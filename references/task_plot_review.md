# Task Plot Review

Review checklist source: `E:/Taskbeacon/skills/task-plot/references/review_checklist.md`.

## Evidence Match

- Pass: task name matches `Balloon Analogue Risk Task (BART)`.
- Pass: rows match blue, yellow, and orange balloon conditions.
- Pass: phase order matches `src/run_trial.py`: fixation, pump/cash decision loop, cash/pop outcome, feedback.
- Pass: timing labels match config for fixation and outcome/feedback durations.
- Pass: response mapping is correct: `space` pumps and `right` cashes out.
- Pass: reward increments and max pump profiles are shown as +5/max 24, +10/max 12, and +20/max 6.

## Visual Quality

- Pass: fixed title and `Construct: risk taking / decision making` subtitle are centered in the header.
- Pass: fixed TaskBeacon logo lockup is borderless in the top-right corner and does not overlap content.
- Pass: feedback avoids invented fixed score examples and uses `earned score`.
- Pass: text is readable and no generated extra title, subtitle, logo, watermark, people, or devices are present.
- Pass: `references/task_plot_timeline_raw.png` preserves the generated timeline before header/logo post-processing.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the first image under `## 2. Task Flow` is exactly `![Task Flow](task_flow.png)`.
- Pass: final image is saved at the task root as `task_flow.png`.
