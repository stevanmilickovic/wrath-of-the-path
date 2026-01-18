from __future__ import annotations

from core.grid import Grid, Pos
from core.result import SearchResult
from .common import AlgorithmConfig, emit, neighbors4, new_result, reconstruct_path


def run(grid: Grid, start: Pos, goal: Pos, cfg: AlgorithmConfig | None = None) -> SearchResult:
    cfg = cfg or AlgorithmConfig()

    res = new_result(start, goal)
    emit(res, cfg, "init", {"algo": "DFS", "start": start, "goal": goal})

    if start == goal:
        res.found = True
        res.path = [start]
        res.stats.path_length = 1
        emit(res, cfg, "goal_found", goal)
        emit(res, cfg, "path", res.path)
        emit(res, cfg, "done", {"found": True})
        return res

    stack: list[Pos] = [start]
    emit(res, cfg, "frontier_add", start)

    visited: set[Pos] = {start}

    while stack:
        current = stack.pop()
        emit(res, cfg, "frontier_pop", current)

        res.stats.expanded += 1
        res.visited_order.append(current)
        emit(res, cfg, "visit", current)

        if current == goal:
            res.found = True
            emit(res, cfg, "goal_found", goal)
            break

        for nb in neighbors4(grid, current):
            if nb in visited:
                continue
            visited.add(nb)
            res.came_from[nb] = current
            stack.append(nb)
            emit(res, cfg, "frontier_add", nb)

    res.stats.visited = len(visited)
    if res.found:
        res.path = reconstruct_path(res.came_from, start, goal)
        res.stats.path_length = len(res.path)
        emit(res, cfg, "path", res.path)

    emit(res, cfg, "done", {"found": res.found})
    return res
