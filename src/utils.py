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


def generate_card_sorting_conditions(
    n_trials: int,
    condition_labels: list[Any] | None = None,
    *,
    seed: int = 0,
    key_list: list[str] | None = None,
) -> list[tuple[str, str, str, str, int, str, str]]:
    """Build concrete card-sorting trial specs during block scheduling."""
    labels = [normalize_rule(str(label)) for label in (condition_labels or [])]
    if not labels:
        raise ValueError("Card-sorting condition_labels cannot be empty.")
    keys = [str(key) for key in (key_list or [])]
    if len(keys) != 4:
        raise ValueError(f"Card-sorting task requires exactly 4 response keys, got {keys!r}")

    rng = random.Random(int(seed))
    rule_schedule: list[str] = []
    while len(rule_schedule) < int(n_trials):
        rule_schedule.extend(labels)
    rule_schedule = rule_schedule[: int(n_trials)]
    if len(labels) > 1:
        rng.shuffle(rule_schedule)

    scheduled: list[tuple[str, str, str, str, int, str, str]] = []
    for rule in rule_schedule:
        trial_seed = rng.randrange(1, 2**31)
        spec = sample_card_trial_spec(rule, key_list=keys, seed=trial_seed)
        scheduled.append(
            (
                str(spec["rule"]),
                str(spec["condition_id"]),
                str(spec["target_color"]),
                str(spec["target_shape"]),
                int(spec["target_number"]),
                str(spec["correct_key"]),
                str(spec["target_image"]),
            )
        )
    return scheduled


def card_condition_to_trial_spec(condition: Any) -> dict[str, Any]:
    """Decode a scheduled card-sorting condition tuple."""
    if isinstance(condition, (tuple, list)) and len(condition) >= 7:
        rule, condition_id, target_color, target_shape, target_number, correct_key, target_image = condition[:7]
        return {
            "rule": normalize_rule(str(rule)),
            "condition_id": str(condition_id),
            "target_color": str(target_color),
            "target_shape": str(target_shape),
            "target_number": int(target_number),
            "correct_key": str(correct_key),
            "target_image": str(target_image),
        }
    raise ValueError(f"Expected scheduled card-sorting condition tuple, got {condition!r}")
