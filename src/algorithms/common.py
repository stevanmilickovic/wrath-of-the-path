from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from ..core.grid import Grid, Pos
from ..core.result import SearchResult


@dataclass(frozen=True)
class AlgorithmConfig:
    emit_trace: bool = True


def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from: dict[Pos, Pos | None], start: Pos, goal: Pos) -> list[Pos]:
    if goal not in came_from:
        return []
    cur: Pos | None = goal
    path: list[Pos] = []
    while cur is not None:
        path.append(cur)
        cur = came_from.get(cur)
    path.reverse()
    if not path or path[0] != start:
        return []
    return path


def new_result(start: Pos, goal: Pos) -> SearchResult:
    r = SearchResult(found=False, start=start, goal=goal)
    r.came_from[start] = None
    return r


def emit(res: SearchResult, cfg: AlgorithmConfig, event: str, payload=None) -> None:
    if cfg.emit_trace:
        res.trace.append((event, payload))


NeighborsFn = Callable[[Grid, Pos], Iterable[Pos]]


def neighbors4(grid: Grid, p: Pos) -> Iterable[Pos]:
    return grid.neighbors4(p)
