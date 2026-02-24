from __future__ import annotations

import random
from typing import Any


COLORS = ["RED", "GREEN", "BLUE", "YELLOW"]
SHAPES = ["CIRCLE", "TRIANGLE", "STAR", "SQUARE"]
NUMBERS = [1, 2, 3, 4]
VALID_RULES = ("color", "shape", "number")


def normalize_rule(rule: str) -> str:
    value = str(rule).strip().lower()
    if value not in VALID_RULES:
        raise ValueError(f"Unsupported sorting rule: {rule!r}")
    return value


def _target_image_path(*, color: str, shape: str, number: int) -> str:
    return (
        f"assets/cards/targets/target_color-{color.lower()}"
        f"_shape-{shape.lower()}_number-{int(number)}.png"
    )


def sample_card_trial_spec(rule: str, *, key_list: list[str], seed: int) -> dict[str, Any]:
    """Generate one target-card trial spec from a rule label and seeded RNG."""
    rule = normalize_rule(rule)
    keys = [str(k) for k in key_list]
    if len(keys) != 4:
        raise ValueError(f"Card-sorting task requires exactly 4 response keys, got {keys!r}")

    rng = random.Random(int(seed))

    # Use distinct feature indices so the active rule uniquely determines the correct key.
    indices = [0, 1, 2, 3]
    rng.shuffle(indices)
    color_idx, shape_idx, number_idx = indices[:3]

    if rule == "color":
        correct_idx = color_idx
    elif rule == "shape":
        correct_idx = shape_idx
    else:
        correct_idx = number_idx

    target_color = COLORS[color_idx]
    target_shape = SHAPES[shape_idx]
    target_number = NUMBERS[number_idx]

    return {
        "rule": rule,
        "condition_id": f"{rule}|{target_color}|{target_shape}|{target_number}",
        "target_color": target_color,
        "target_shape": target_shape,
        "target_number": target_number,
        "correct_key": keys[correct_idx],
        "target_image": _target_image_path(
            color=target_color,
            shape=target_shape,
            number=target_number,
        ),
    }
