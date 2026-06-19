# Task Plot Brief

## Evidence Sources

- `README.md`
- `main.py`
- `config/config.yaml`
- `src/run_trial.py`
- `src/utils.py`

## Header

- Title: Balloon Analogue Risk Task (BART)
- Construct: risk taking / decision making

## Participant-Visible Flow

- Three balloon colors are presented: blue, yellow, and orange.
- Participant presses `space` to pump and `right` to cash out.
- Each pump increases temporary reward and balloon size.
- Pumping can lead to a pop outcome, which loses the temporary reward.
- Cashing out banks the temporary reward.
- Trial feedback shows earned score for the trial.

## Rows

- Blue balloon: `+5` per pump, max pump profile `24`.
- Yellow balloon: `+10` per pump, max pump profile `12`.
- Orange balloon: `+20` per pump, max pump profile `6`.

## Timings

- Fixation: 0.8 s.
- Decision window: no practical timeout in human config; participant chooses pump or cash.
- Cash or pop outcome: 1.0 s.
- Feedback: 1.0 s.

## Rendering Notes

- Use three rows and a compact pump loop/branch, not every repeated pump.
- The generated raw image must contain only timeline content below a blank header band.
- The final title, `Construct: risk taking / decision making` subtitle, and TaskBeacon logo are added by post-processing.
