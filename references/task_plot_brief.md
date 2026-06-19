# Task Plot Brief

Task: Balloon Analogue Risk Task (BART)

Goal measured: risk taking and reward-risk tradeoff.

Primary evidence:
- `README.md`: task overview, flow, color conditions, and timing.
- `config/config.yaml`: condition list, reward increments, max pumps, keys, timing, and stimuli.
- `src/run_trial.py`: participant-visible trial sequence and branch logic.

Conditions:
- Blue balloon: lower reward increment, `+5` per pump, maximum pump profile `24`.
- Yellow balloon: medium reward increment, `+10` per pump, maximum pump profile `12`.
- Orange balloon: higher reward increment, `+20` per pump, maximum pump profile `6`.

Trial phases:
- Fixation: `+`, 0.8 s.
- Pump decision: colored balloon plus temporary score `+{score_bank}`. Participant can press `space` to pump or `right` to cash out.
- Pump loop: each `space` pump increases temporary reward by the condition increment, grows the balloon, and repeats unless the explosion point is reached.
- Pop outcome: if pump count reaches the sampled explosion point, show popped balloon and play pop sound for 1.0 s; temporary reward is lost.
- Cash outcome: if participant presses `right`, show cash-out screen and play cash sound for 1.0 s; temporary reward is banked.
- Timeout outcome: possible in QA/SIM profiles when timeout is enabled; not enabled for human config.
- Trial feedback: show earned score for 1.0 s, `0` after pop/timeout or banked score after cash.

Participant-visible response rule:
- Press `space` to pump and increase temporary reward.
- Press `right` to cash out and bank the current temporary reward.

Block context:
- Human profile: 3 blocks, 10 trials per block, 30 trials total.
- Conditions are blue, yellow, and orange balloons.

Image simplification:
- Use three timeline rows: Blue, Yellow, Orange.
- Show a loop/branch structure for pump/cash/pop rather than drawing every repeated pump.
- Omit timeout from the main row flow, but include a small QA-only note if space allows.
