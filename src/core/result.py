from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

Pos = tuple[int, int]


@dataclass
class SearchStats:
    expanded: int = 0
    visited: int = 0
    path_length: int = 0


@dataclass
class SearchResult:
    found: bool
    start: Pos
    goal: Pos

    path: list[Pos] = field(default_factory=list)          # final path (start..goal)
    visited_order: list[Pos] = field(default_factory=list)
    came_from: dict[Pos, Pos | None] = field(default_factory=dict)

    stats: SearchStats = field(default_factory=SearchStats)

    trace: list[tuple[str, Any]] = field(default_factory=list)
