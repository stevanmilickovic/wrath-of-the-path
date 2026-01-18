from __future__ import annotations

from dataclasses import dataclass, field

Pos = tuple[int, int]


@dataclass
class Player:
    pos: Pos
    path: list[Pos] = field(default_factory=list)
    _path_index: int = 0
    _accum_ms: int = 0

    def set_path(self, path: list[Pos]) -> None:
        self.path = path
        self._path_index = 0
        self._accum_ms = 0
        if self.path:
            self.pos = self.path[0]

    def is_done(self) -> bool:
        return (not self.path) or (self._path_index >= len(self.path) - 1)

    def update(self, dt_ms: int, step_delay_ms: int) -> None:
        if self.is_done():
            return

        self._accum_ms += dt_ms
        while self._accum_ms >= step_delay_ms and not self.is_done():
            self._accum_ms -= step_delay_ms
            self._path_index += 1
            self.pos = self.path[self._path_index]
