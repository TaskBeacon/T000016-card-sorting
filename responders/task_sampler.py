from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import random as _py_random

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Task-specific sampler for WCST-style card sorting.

    - For non-choice phases, responds with `continue_key` when allowed.
    - For choice phase, chooses correct key with probability `hit_rate`.
    """

    continue_key: str = "space"
    hit_rate: float = 0.72
    rt_mean_s: float = 0.48
    rt_sd_s: float = 0.08
    rt_min_s: float = 0.18

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.hit_rate = max(0.0, min(1.0, float(self.hit_rate)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _sample_choice(self, values: list[str]) -> str:
        rng = self._rng
        if hasattr(rng, "choice"):
            return str(rng.choice(values))
        return str(values[int(rng.randrange(len(values)))])

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        rng = self._rng
        if rng is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "rng_missing"})

        factors = dict(obs.task_factors or {})
        phase = str(obs.phase or factors.get("stage") or "").strip().lower()
        if phase != "card_choice_response":
            if self.continue_key in valid_keys:
                rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))
                return Action(key=self.continue_key, rt_s=rt, meta={"source": "task_sampler", "phase": phase})
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "phase": phase})

        correct_key = str(factors.get("correct_key", "")).strip()
        if not correct_key or correct_key not in valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "missing_correct_key"})

        if self._sample_random() > self.hit_rate:
            wrong = [k for k in valid_keys if k != correct_key]
            if not wrong:
                return Action(key=None, rt_s=None, meta={"source": "task_sampler", "outcome": "miss"})
            rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))
            return Action(
                key=self._sample_choice(wrong),
                rt_s=rt,
                meta={"source": "task_sampler", "outcome": "error", "correct_key": correct_key},
            )

        rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))
        return Action(
            key=correct_key,
            rt_s=rt,
            meta={"source": "task_sampler", "outcome": "hit", "correct_key": correct_key},
        )
