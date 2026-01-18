from __future__ import annotations

import heapq

from ..core.grid import Grid, Pos
from ..core.result import SearchResult
from .common import AlgorithmConfig, emit, manhattan, neighbors4, new_result, reconstruct_path


def run(grid: Grid, start: Pos, goal: Pos, cfg: AlgorithmConfig | None = None) -> SearchResult:
    cfg = cfg or AlgorithmConfig()

    res = new_result(start, goal)
    emit(res, cfg, "init", {"algo": "A*", "start": start, "goal": goal})

    if start == goal:
        res.found = True
        res.path = [start]
        res.stats.path_length = 1
        emit(res, cfg, "goal_found", goal)
        emit(res, cfg, "path", res.path)
        emit(res, cfg, "done", {"found": True})
        return res

    g_score: dict[Pos, int] = {start: 0}

    open_heap: list[tuple[int, int, Pos]] = []
    tie = 0
    heapq.heappush(open_heap, (manhattan(start, goal), tie, start))
    emit(res, cfg, "frontier_add", start)

    in_open: set[Pos] = {start}
    closed: set[Pos] = set()

    while open_heap:
        _, _, current = heapq.heappop(open_heap)
        if current in closed:
            continue

        in_open.discard(current)
        emit(res, cfg, "frontier_pop", current)

        res.stats.expanded += 1
        res.visited_order.append(current)
        emit(res, cfg, "visit", current)

        if current == goal:
            res.found = True
            emit(res, cfg, "goal_found", goal)
            break

        closed.add(current)

        for nb in neighbors4(grid, current):
            if nb in closed:
                continue

            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(nb, 10**9):
                res.came_from[nb] = current
                g_score[nb] = tentative_g
                f = tentative_g + manhattan(nb, goal)
                tie += 1
                heapq.heappush(open_heap, (f, tie, nb))
                if nb not in in_open:
                    in_open.add(nb)
                    emit(res, cfg, "frontier_add", nb)

    res.stats.visited = len(g_score)
    if res.found:
        res.path = reconstruct_path(res.came_from, start, goal)
        res.stats.path_length = len(res.path)
        emit(res, cfg, "path", res.path)

    emit(res, cfg, "done", {"found": res.found})
    return res
