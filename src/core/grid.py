from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

Pos = tuple[int, int]


@dataclass
class Grid:
    width: int
    height: int
    walls: list[list[bool]]  # True = wall, False = walkable

    @classmethod
    def filled(cls, width: int, height: int, wall: bool = True) -> "Grid":
        walls = [[wall for _ in range(width)] for _ in range(height)]
        return cls(width=width, height=height, walls=walls)

    def in_bounds(self, p: Pos) -> bool:
        x, y = p
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, p: Pos) -> bool:
        x, y = p
        return self.walls[y][x]

    def set_wall(self, p: Pos, value: bool) -> None:
        x, y = p
        self.walls[y][x] = value

    def is_walkable(self, p: Pos) -> bool:
        return self.in_bounds(p) and (not self.is_wall(p))

    def neighbors4(self, p: Pos) -> Iterable[Pos]:
        x, y = p
        candidates = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
        for q in candidates:
            if self.is_walkable(q):
                yield q
