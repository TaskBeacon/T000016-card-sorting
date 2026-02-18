from __future__ import annotations

import random
from typing import Any, Dict, List

from psychopy import logging


class Controller:
    """Trial generator and performance tracker for a WCST-style task.

    The task cycles sorting rules (color/shape/number) across blocks.
    On each trial, a target card is generated from mixed feature indices so that
    each rule maps to a different correct response key.
    """

    COLORS = ["RED", "GREEN", "BLUE", "YELLOW"]
    SHAPES = ["CIRCLE", "TRIANGLE", "STAR", "SQUARE"]
    NUMBERS = [1, 2, 3, 4]

    def __init__(self, seed: int | None = None, enable_logging: bool = True):
        self._rng = random.Random(seed)
        self.enable_logging = bool(enable_logging)
        self.histories: Dict[str, List[bool]] = {}

    @classmethod
    def from_dict(cls, config: dict | None = None) -> "Controller":
        config = config or {}
        return cls(
            seed=config.get("seed", None),
            enable_logging=config.get("enable_logging", True),
        )

    def _ensure_rule(self, rule: str) -> None:
        if rule not in self.histories:
            self.histories[rule] = []

    def sample_trial(self, rule: str) -> Dict[str, Any]:
        """Generate one target card and rule-specific correct key."""
        indices = [0, 1, 2, 3]
        self._rng.shuffle(indices)
        color_idx, shape_idx, number_idx = indices[:3]

        if rule == "color":
            correct_idx = color_idx
        elif rule == "shape":
            correct_idx = shape_idx
        elif rule == "number":
            correct_idx = number_idx
        else:
            raise ValueError(f"Unsupported sorting rule: {rule!r}")

        return {
            "rule": rule,
            "target_color": self.COLORS[color_idx],
            "target_shape": self.SHAPES[shape_idx],
            "target_number": self.NUMBERS[number_idx],
            "correct_key": str(correct_idx + 1),
            "target_image": (
                f"assets/cards/targets/target_color-{self.COLORS[color_idx].lower()}"
                f"_shape-{self.SHAPES[shape_idx].lower()}_number-{self.NUMBERS[number_idx]}.png"
            ),
        }

    def update(self, hit: bool, rule: str) -> None:
        self._ensure_rule(rule)
        self.histories[rule].append(bool(hit))
        if self.enable_logging:
            hits = sum(self.histories[rule])
            n = len(self.histories[rule])
            logging.data(
                f"[CardSortController] rule={rule} trials={n} hits={hits} accuracy={hits / max(n,1):.2%}"
            )

    def rule_accuracy(self, rule: str) -> float:
        hist = self.histories.get(rule, [])
        if not hist:
            return 0.0
        return float(sum(hist) / len(hist))

    def overall_accuracy(self) -> float:
        all_values: List[bool] = []
        for values in self.histories.values():
            all_values.extend(values)
        if not all_values:
            return 0.0
        return float(sum(all_values) / len(all_values))
