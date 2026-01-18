from __future__ import annotations

from dataclasses import dataclass

Pos = tuple[int, int]


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

    def contains(self, px: int, py: int) -> bool:
        return self.x <= px < self.x + self.w and self.y <= py < self.y + self.h


def clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(v, hi))


def grid_to_screen(cell: Pos, origin_xy: tuple[int, int], cell_size: int, cell_gap: int) -> tuple[int, int]:
    cx, cy = cell
    ox, oy = origin_xy
    x = ox + cx * (cell_size + cell_gap)
    y = oy + cy * (cell_size + cell_gap)
    return x, y


def screen_to_grid(px: int, py: int, origin_xy: tuple[int, int], cell_size: int, cell_gap: int) -> Pos | None:
    ox, oy = origin_xy
    dx = px - ox
    dy = py - oy
    if dx < 0 or dy < 0:
        return None

    step = cell_size + cell_gap
    cx = dx // step
    cy = dy // step

    # Ako si kliknuo u "gap" između ćelija, ignoriši
    if (dx % step) >= cell_size or (dy % step) >= cell_size:
        return None

    return int(cx), int(cy)
