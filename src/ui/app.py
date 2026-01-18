from __future__ import annotations

import pygame

from ..algorithms.common import AlgorithmConfig
from ..algorithms import bfs, dfs, astar

from ..core.grid import Grid, Pos
from ..core.maze import MazeConfig, MazeGenerator
from ..core.player import Player

from ..config import (
    APP_TITLE, FPS, GRID_W, GRID_H, CELL_SIZE, CELL_GAP, PANEL_W, MARGIN,
    WINDOW_W, WINDOW_H, START_POS, GOAL_POS, SEARCH_STEP_DELAY_MS,
    PLAYER_STEP_DELAY_MS, MAZE_SEED
)

from ..utils.math2d import Rect
from ..utils.timing import StepTimer

from .renderer import Renderer
from .widgets import Button


class AppState:
    EMPTY = "EMPTY"
    MAZE_READY = "MAZE_READY"
    SEARCHING = "SEARCHING"
    MOVING = "MOVING"
    WIN = "WIN"


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(APP_TITLE)

        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 26)
        self.small_font = pygame.font.SysFont(None, 20)

        self.grid_origin = (MARGIN, MARGIN)
        grid_px_w = GRID_W * (CELL_SIZE + CELL_GAP) - CELL_GAP
        self.panel_origin = (MARGIN + grid_px_w + MARGIN, 0)

        self.renderer = Renderer(
            surface=self.screen,
            font=self.font,
            small_font=self.small_font,
            grid_origin=self.grid_origin,
            panel_origin=self.panel_origin,
            cell_size=CELL_SIZE,
            cell_gap=CELL_GAP,
        )

        self.state = AppState.EMPTY

        self.start: Pos = START_POS
        self.goal: Pos = GOAL_POS

        self.grid: Grid | None = None
        self.player: Player | None = None

        # Visualization state
        self.visited: set[Pos] = set()
        self.frontier: set[Pos] = set()
        self.path: list[Pos] = []

        # Trace playback
        self.trace: list[tuple[str, object]] = []
        self.trace_i: int = 0
        self.search_timer = StepTimer(step_delay_ms=SEARCH_STEP_DELAY_MS)
        self.player_timer = StepTimer(step_delay_ms=PLAYER_STEP_DELAY_MS)

        # Buttons
        self.buttons: list[Button] = []
        self._build_buttons()

        self._update_button_enabled_states()

    def _build_buttons(self) -> None:
        px, _ = self.panel_origin
        x = px + 16
        y = 120
        w = PANEL_W - 32
        h = 36
        gap = 10

        def add(text: str, cb):
            nonlocal y
            self.buttons.append(Button(Rect(x, y, w, h), text, cb))
            y += h + gap

        add("Generate Maze", self.generate_maze)
        add("Run BFS", lambda: self.start_search("BFS"))
        add("Run DFS", lambda: self.start_search("DFS"))
        add("Run A*", lambda: self.start_search("A*"))

    def _update_button_enabled_states(self) -> None:
        # Generate uvijek može; algoritmi samo kad maze postoji i nije u toku animacija
        can_run_algo = self.grid is not None and self.state in (AppState.MAZE_READY, AppState.WIN)
        for b in self.buttons:
            if b.text == "Generate Maze":
                b.enabled = True
            else:
                b.enabled = can_run_algo

    def generate_maze(self) -> None:
        self.grid = Grid.filled(GRID_W, GRID_H, wall=True)
        MazeGenerator.generate(
            self.grid,
            start=self.start,
            goal=self.goal,
            cfg=MazeConfig(seed=MAZE_SEED),
        )

        self.player = Player(pos=self.start)
        self._reset_visuals()

        self.state = AppState.MAZE_READY
        self._update_button_enabled_states()

    def _reset_visuals(self) -> None:
        self.visited.clear()
        self.frontier.clear()
        self.path.clear()

        self.trace = []
        self.trace_i = 0
        self.search_timer.reset()
        self.search_timer.paused = False

        self.player_timer.reset()
        self.player_timer.paused = False

    def start_search(self, which: str) -> None:
        if self.grid is None:
            return

        self._reset_visuals()
        self.player = Player(pos=self.start)

        cfg = AlgorithmConfig(emit_trace=True)

        if which == "BFS":
            res = bfs.run(self.grid, self.start, self.goal, cfg)
        elif which == "DFS":
            res = dfs.run(self.grid, self.start, self.goal, cfg)
        else:
            res = astar.run(self.grid, self.start, self.goal, cfg)

        self.trace = res.trace
        self.trace_i = 0
        self.state = AppState.SEARCHING
        self._update_button_enabled_states()

    def _apply_trace_event(self, event: str, payload: object) -> None:
        if event == "frontier_add":
            if isinstance(payload, tuple):
                self.frontier.add(payload)  # type: ignore[arg-type]
        elif event == "frontier_pop":
            if isinstance(payload, tuple):
                self.frontier.discard(payload)  # type: ignore[arg-type]
        elif event == "visit":
            if isinstance(payload, tuple):
                p = payload  # type: ignore[assignment]
                self.visited.add(p)
                self.frontier.discard(p)
        elif event == "path":
            if isinstance(payload, list):
                self.path = payload  # type: ignore[assignment]
        elif event == "done":
            # Prelaz u MOVING ako postoji putanja
            if self.path and self.player is not None:
                self.player.set_path(self.path)
                self.state = AppState.MOVING
            else:
                self.state = AppState.MAZE_READY
            self._update_button_enabled_states()

    def _update_search(self, dt_ms: int) -> None:
        if self.trace_i >= len(self.trace):
            # Fallback (ako trace nema "done")
            if self.path and self.player is not None:
                self.player.set_path(self.path)
                self.state = AppState.MOVING
            else:
                self.state = AppState.MAZE_READY
            self._update_button_enabled_states()
            return

        self.search_timer.update(dt_ms)
        while self.search_timer.is_ready() and self.trace_i < len(self.trace):
            event, payload = self.trace[self.trace_i]
            self._apply_trace_event(event, payload)
            self.trace_i += 1
            self.search_timer.consume()

            # Ako smo dobili done, prekini dalje korake u ovom frame-u
            if event == "done":
                break

    def _update_player(self, dt_ms: int) -> None:
        if self.player is None:
            self.state = AppState.MAZE_READY
            self._update_button_enabled_states()
            return

        self.player.update(dt_ms, step_delay_ms=PLAYER_STEP_DELAY_MS)
        if self.player.pos == self.goal and self.player.is_done():
            self.state = AppState.WIN
            self._update_button_enabled_states()

    def run(self) -> None:
        running = True
        while running:
            dt_ms = self.clock.tick(FPS)

            # Events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                elif e.type == pygame.MOUSEMOTION:
                    mx, my = e.pos
                    for b in self.buttons:
                        b.set_hover(mx, my)

                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mx, my = e.pos
                    for b in self.buttons:
                        if b.handle_mouse_down(mx, my):
                            break

            # Updates
            if self.state == AppState.SEARCHING:
                self._update_search(dt_ms)
            elif self.state == AppState.MOVING:
                self._update_player(dt_ms)

            # Render
            state_label = self._state_label()
            stats_line = f"Visited: {len(self.visited)} | Frontier: {len(self.frontier)} | Path: {len(self.path)}"
            self.renderer.draw(
                grid=self.grid,
                start=self.start,
                goal=self.goal,
                player=self.player,
                visited=self.visited,
                frontier=self.frontier,
                path=self.path,
                state_label=state_label,
                stats_line=stats_line,
                buttons=self.buttons,
                panel_w=PANEL_W,
                window_h=WINDOW_H,
            )

        pygame.quit()

    def _state_label(self) -> str:
        if self.state == AppState.EMPTY:
            return "Status: no maze (click Generate)"
        if self.state == AppState.MAZE_READY:
            return "Status: maze ready (choose)"
        if self.state == AppState.SEARCHING:
            return "Status: searching..."
        if self.state == AppState.MOVING:
            return "Status: moving to goal..."
        return "Status: WIN"
