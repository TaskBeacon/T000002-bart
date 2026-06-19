import random


def _condition_hash(condition: str) -> int:
    return sum((idx + 1) * ord(ch) for idx, ch in enumerate(condition))


def sample_explosion_point(settings, condition: str, block_idx: int | None, max_pumps: int) -> int:
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
