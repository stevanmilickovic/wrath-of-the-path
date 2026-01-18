from __future__ import annotations

import random
from dataclasses import dataclass

from .grid import Grid, Pos


@dataclass(frozen=True)
class MazeConfig:
    seed: int | None = None


class MazeGenerator:

    @staticmethod
    def generate(grid: Grid, start: Pos, goal: Pos, cfg: MazeConfig | None = None) -> None:
        rnd = random.Random(cfg.seed if cfg else None)

        for y in range(grid.height):
            for x in range(grid.width):
                grid.walls[y][x] = True

        def clamp_odd(v: int, max_v: int) -> int:
            v = max(1, min(v, max_v - 2))
            if v % 2 == 0:
                v = v - 1 if v > 1 else v + 1
            return max(1, min(v, max_v - 2))

        sx, sy = clamp_odd(start[0], grid.width), clamp_odd(start[1], grid.height)
        gx, gy = clamp_odd(goal[0], grid.width), clamp_odd(goal[1], grid.height)

        cell_stack: list[Pos] = [(sx, sy)]
        visited_cells: set[Pos] = {(sx, sy)}
        grid.set_wall((sx, sy), False)

        def cell_neighbors(c: Pos) -> list[Pos]:
            x, y = c
            opts = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
            res: list[Pos] = []
            for nx, ny in opts:
                if 1 <= nx < grid.width - 1 and 1 <= ny < grid.height - 1:
                    if (nx, ny) not in visited_cells:
                        res.append((nx, ny))
            return res

        while cell_stack:
            current = cell_stack[-1]
            nbs = cell_neighbors(current)
            if not nbs:
                cell_stack.pop()
                continue

            nxt = rnd.choice(nbs)
            cx, cy = current
            nx, ny = nxt
            between = ((cx + nx) // 2, (cy + ny) // 2)
            grid.set_wall(between, False)
            grid.set_wall(nxt, False)

            visited_cells.add(nxt)
            cell_stack.append(nxt)

        grid.set_wall(start, False)
        grid.set_wall(goal, False)

        for p in (start, goal):
            if not grid.is_walkable(p):
                grid.set_wall(p, False)
            if all(grid.is_wall(q) for q in _neighbors_in_bounds(grid, p)):
                q = rnd.choice(_neighbors_in_bounds(grid, p))
                grid.set_wall(q, False)


def _neighbors_in_bounds(grid: Grid, p: Pos) -> list[Pos]:
    x, y = p
    candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [q for q in candidates if grid.in_bounds(q)]