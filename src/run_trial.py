import random
from functools import partial

from psychopy.visual import TextStim

from psyflow import StimUnit, set_trial_context

# trial stages use task-specific phase labels via set_trial_context(...)
_TRIAL_COUNTER = 0


def _next_trial_id() -> int:
    global _TRIAL_COUNTER
    _TRIAL_COUNTER += 1
    return _TRIAL_COUNTER


def _deadline_s(value) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run a single BART trial with a predetermined explosion point."""
    trial_id = _next_trial_id()
    trial_data = {"condition": condition}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    continue_pump = True
    pump_count = 0
    score_bank = getattr(settings, f"{condition}_delta")
    delta = getattr(settings, f"{condition}_delta")
    max_pumps = getattr(settings, f"{condition}_max_pumps")
    initial_scale = settings.initial_balloon_scale
    max_scale = settings.max_balloon_scale
    balloon_base_deg = settings.balloon_size_deg
    size_step = (max_scale - initial_scale) / max_pumps

    explosion_point = random.randint(1, max_pumps)
    trial_data["explosion_point"] = explosion_point

    # phase: pre_pump_fixation
    # phase: pre_pump_fixation
    fixation = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="pre_pump_fixation",
        deadline_s=_deadline_s(settings.fixation_duration),
        valid_keys=[settings.pump_key, settings.cash_key],
        block_id=block_id,
        condition_id=str(condition),
        task_factors={"condition": str(condition), "stage": "pre_pump_fixation", "block_idx": block_idx},
        stim_id="fixation",
    )
    fixation.show(duration=settings.fixation_duration, onset_trigger=settings.triggers.get("fixation_onset")).to_dict(trial_data)

    # phase: pump_decision
    while continue_pump:
        current_scale = initial_scale + pump_count * size_step
        balloon_size = [current_scale * balloon_base_deg[0], current_scale * balloon_base_deg[1]]

        balloon = make_unit(unit_label=f"pump_{pump_count}")
        balloon.add_stim(stim_bank.rebuild(f"{condition}_balloon", size=balloon_size))
        balloon.add_stim(TextStim(win, text=f"+{score_bank}", pos=[0, -4], color="white"))
        set_trial_context(
            balloon,
            trial_id=trial_id,
            phase="pump_decision",
            deadline_s=_deadline_s(settings.balloon_duration),
            valid_keys=[settings.pump_key, settings.cash_key],
            block_id=block_id,
            condition_id=str(condition),
            task_factors={
                "condition": str(condition),
                "stage": "pump_decision",
                "pump_count": int(pump_count),
                "score_bank": float(score_bank),
                "block_idx": block_idx,
            },
            stim_id=f"{condition}_balloon",
        )
        balloon.capture_response(
            keys=[settings.pump_key, settings.cash_key],
            correct_keys=[],
            duration=settings.balloon_duration,
            onset_trigger=settings.triggers.get(f"{condition}_balloon_onset"),
            response_trigger={
                settings.pump_key: settings.triggers.get(f"{condition}_pump_press"),
                settings.cash_key: settings.triggers.get(f"{condition}_cash_press"),
            },
            timeout_trigger=settings.triggers.get(f"{condition}_balloon_onset"),
            terminate_on_response=True,
        ).to_dict(trial_data)
        response = balloon.get_state("response", None)

        if response == settings.pump_key:
            pump_count += 1
            if pump_count >= explosion_point:
                make_unit(unit_label="pop").add_stim(stim_bank.get(f"{condition}_pop")).add_stim(stim_bank.get("pop_sound")).show(
                    duration=settings.response_feedback_duration,
                    onset_trigger=settings.triggers.get(f"{condition}_pop"),
                ).to_dict(trial_data)
                fb_type = "pop"
                continue_pump = False
                fb_score = 0
            else:
                continue_pump = True
                score_bank += delta
        elif response == settings.cash_key:
            make_unit(unit_label="cash").add_stim(stim_bank.get("cash_screen")).add_stim(stim_bank.get("cash_sound")).show(
                duration=settings.response_feedback_duration,
                onset_trigger=settings.triggers.get(f"{condition}_cash"),
            ).to_dict(trial_data)
            fb_type = "cash"
            continue_pump = False
            fb_score = score_bank
        else:
            make_unit(unit_label="timeout").add_stim(stim_bank.get("timeout_screen")).show(
                duration=settings.response_feedback_duration,
                onset_trigger=settings.triggers.get(f"{condition}_timeout"),
            ).to_dict(trial_data)
            continue_pump = False
            fb_type = "timeout"
            fb_score = 0

    # outcome display
    fb_stim = "win_feedback" if fb_type == "cash" else "lose_feedback"
    feedback = make_unit(unit_label="feedback").add_stim(stim_bank.get_and_format(fb_stim, fb_score=fb_score)).show(
        duration=settings.feedback_duration,
        onset_trigger=settings.triggers.get("feedback_onset"),
    )
    feedback.set_state(fb_type=fb_type, fb_score=fb_score, pump_count=pump_count)
    feedback.to_dict(trial_data)

    return trial_data
