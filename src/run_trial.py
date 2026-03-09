import random
from functools import partial

from psyflow import StimUnit, next_trial_id, set_trial_context


def _condition_hash(condition: str) -> int:
    return sum((idx + 1) * ord(ch) for idx, ch in enumerate(condition))


def _sample_explosion_point(settings, condition: str, block_idx: int | None, max_pumps: int) -> int:
    mode = str(getattr(settings, "explosion_sampling_mode", "without_replacement_cycle"))
    state = getattr(settings, "_bart_explosion_state", None)
    if state is None:
        state = {}
        setattr(settings, "_bart_explosion_state", state)

    block_index = int(block_idx or 0)
    key = (block_index, str(condition))
    sampler = state.get(key)
    if sampler is None:
        block_seed = 0
        block_seeds = getattr(settings, "block_seed", None)
        if isinstance(block_seeds, list) and 0 <= block_index < len(block_seeds):
            seed_value = block_seeds[block_index]
            if seed_value is not None:
                block_seed = int(seed_value)
        rng_seed = block_seed + _condition_hash(str(condition))
        sampler = {"rng": random.Random(rng_seed), "bag": []}
        state[key] = sampler

    rng = sampler["rng"]
    bag = sampler["bag"]

    if mode == "with_replacement":
        return int(rng.randint(1, max_pumps))
    if mode == "without_replacement_cycle":
        if not bag:
            bag.extend(range(1, max_pumps + 1))
            rng.shuffle(bag)
        return int(bag.pop())

    raise ValueError(
        f"Unsupported explosion_sampling_mode={mode!r}. "
        "Use 'without_replacement_cycle' or 'with_replacement'."
    )


# trial stages use task-specific phase labels via set_trial_context(...)
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
    """Run a single BART trial with a deterministic explosion sampler."""
    trial_id = next_trial_id()
    trial_data = {"condition": condition}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    continue_pump = True
    pump_count = 0
    score_bank = 0
    delta = getattr(settings, f"{condition}_delta")
    max_pumps = getattr(settings, f"{condition}_max_pumps")
    initial_scale = settings.initial_balloon_scale
    max_scale = settings.max_balloon_scale
    balloon_base_deg = settings.balloon_size_deg
    size_step = (max_scale - initial_scale) / max_pumps

    decision_timeout_enabled = bool(getattr(settings, "decision_timeout_enabled", True))
    decision_window_s = (
        float(settings.balloon_duration)
        if decision_timeout_enabled
        else float(getattr(settings, "decision_timeout_fallback_s", 600.0))
    )
    decision_deadline_s = float(settings.balloon_duration) if decision_timeout_enabled else None

    explosion_point = _sample_explosion_point(settings, str(condition), block_idx, max_pumps)
    trial_data["explosion_point"] = explosion_point
    trial_data["explosion_sampling_mode"] = str(
        getattr(settings, "explosion_sampling_mode", "without_replacement_cycle")
    )
    trial_data["decision_timeout_enabled"] = decision_timeout_enabled

    # phase: pre_pump_fixation
    fixation = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="pre_pump_fixation",
        deadline_s=settings.fixation_duration,
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
        balloon.add_stim(stim_bank.get_and_format("score_bank_text", score_bank=score_bank))
        set_trial_context(
            balloon,
            trial_id=trial_id,
            phase="pump_decision",
            deadline_s=decision_deadline_s,
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
            duration=decision_window_s,
            onset_trigger=settings.triggers.get(f"{condition}_balloon_onset"),
            response_trigger={
                settings.pump_key: settings.triggers.get(f"{condition}_pump_press"),
                settings.cash_key: settings.triggers.get(f"{condition}_cash_press"),
            },
            timeout_trigger=settings.triggers.get(f"{condition}_timeout") if decision_timeout_enabled else None,
            terminate_on_response=True,
        ).to_dict(trial_data)
        response = balloon.get_state("response", None)

        if response == settings.pump_key:
            pump_count += 1
            if pump_count >= explosion_point:
                pop = (
                    make_unit(unit_label="pop")
                    .add_stim(stim_bank.get(f"{condition}_pop"))
                    .add_stim(stim_bank.get("pop_sound"))
                )
                set_trial_context(
                    pop,
                    trial_id=trial_id,
                    phase="pop_outcome",
                    deadline_s=settings.response_feedback_duration,
                    valid_keys=[],
                    block_id=block_id,
                    condition_id=str(condition),
                    task_factors={
                        "condition": str(condition),
                        "stage": "pop_outcome",
                        "pump_count": int(pump_count),
                        "score_bank": float(score_bank),
                        "block_idx": block_idx,
                    },
                    stim_id=f"{condition}_pop+pop_sound",
                )
                pop.show(
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
            cash = (
                make_unit(unit_label="cash")
                .add_stim(stim_bank.get("cash_screen"))
                .add_stim(stim_bank.get("cash_sound"))
            )
            set_trial_context(
                cash,
                trial_id=trial_id,
                phase="cash_outcome",
                deadline_s=settings.response_feedback_duration,
                valid_keys=[],
                block_id=block_id,
                condition_id=str(condition),
                task_factors={
                    "condition": str(condition),
                    "stage": "cash_outcome",
                    "pump_count": int(pump_count),
                    "score_bank": float(score_bank),
                    "block_idx": block_idx,
                },
                stim_id="cash_screen+cash_sound",
            )
            cash.show(
                duration=settings.response_feedback_duration,
                onset_trigger=settings.triggers.get(f"{condition}_cash"),
            ).to_dict(trial_data)
            fb_type = "cash"
            continue_pump = False
            fb_score = score_bank
        else:
            timeout = make_unit(unit_label="timeout").add_stim(stim_bank.get("timeout_screen"))
            set_trial_context(
                timeout,
                trial_id=trial_id,
                phase="timeout_outcome",
                deadline_s=settings.response_feedback_duration,
                valid_keys=[],
                block_id=block_id,
                condition_id=str(condition),
                task_factors={
                    "condition": str(condition),
                    "stage": "timeout_outcome",
                    "pump_count": int(pump_count),
                    "score_bank": float(score_bank),
                    "block_idx": block_idx,
                },
                stim_id="timeout_screen",
            )
            timeout.show(
                duration=settings.response_feedback_duration,
                onset_trigger=settings.triggers.get(f"{condition}_timeout"),
            ).to_dict(trial_data)
            continue_pump = False
            fb_type = "timeout"
            fb_score = 0

    # outcome display
    fb_stim = "win_feedback" if fb_type == "cash" else "lose_feedback"
    feedback = make_unit(unit_label="feedback").add_stim(stim_bank.get_and_format(fb_stim, fb_score=fb_score))
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="trial_feedback",
        deadline_s=settings.feedback_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=str(condition),
        task_factors={
            "condition": str(condition),
            "stage": "trial_feedback",
            "fb_type": str(fb_type),
            "fb_score": float(fb_score),
            "pump_count": int(pump_count),
            "block_idx": block_idx,
        },
        stim_id=fb_stim,
    )
    feedback.show(
        duration=settings.feedback_duration,
        onset_trigger=settings.triggers.get("feedback_onset"),
    )
    feedback.set_state(fb_type=fb_type, fb_score=fb_score, pump_count=pump_count)
    feedback.to_dict(trial_data)

    return trial_data
