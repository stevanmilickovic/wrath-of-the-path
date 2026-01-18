from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StepTimer:
    step_delay_ms: int
    _accum_ms: int = 0
    paused: bool = False

    def reset(self) -> None:
        self._accum_ms = 0

    def update(self, dt_ms: int) -> None:
        if self.paused:
            return
        self._accum_ms += dt_ms

    def is_ready(self) -> bool:
        return (not self.paused) and self._accum_ms >= self.step_delay_ms

    def consume(self) -> None:
        # potroši tačno jedan korak (ne sve)
        self._accum_ms = max(0, self._accum_ms - self.step_delay_ms)

    def step_once(self) -> None:
        if self.paused:
            self._accum_ms = self.step_delay_ms
