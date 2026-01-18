from __future__ import annotations

import pygame

from core.grid import Grid, Pos
from core.player import Player
from utils.math2d import grid_to_screen
from . import colors


class Renderer:
    def __init__(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        small_font: pygame.font.Font,
        grid_origin: tuple[int, int],
        panel_origin: tuple[int, int],
        cell_size: int,
        cell_gap: int,
    ) -> None:
        self.surface = surface
        self.font = font
        self.small_font = small_font
        self.grid_origin = grid_origin
        self.panel_origin = panel_origin
        self.cell_size = cell_size
        self.cell_gap = cell_gap

    def draw(
        self,
        grid: Grid | None,
        start: Pos,
        goal: Pos,
        player: Player | None,
        visited: set[Pos],
        frontier: set[Pos],
        path: list[Pos],
        state_label: str,
        stats_line: str,
        buttons,
        panel_w: int,
        window_h: int,
    ) -> None:
        self.surface.fill(colors.BG)

        # Panel background
        px, py = self.panel_origin
        pygame.draw.rect(
            self.surface,
            colors.PANEL_BG,
            pygame.Rect(px, 0, panel_w, window_h),
        )

        # Title + status
        title = self.font.render("Wrath of the Path", True, colors.TEXT)
        self.surface.blit(title, (px + 16, 16))

        state_txt = self.small_font.render(state_label, True, colors.MUTED_TEXT)
        self.surface.blit(state_txt, (px + 16, 16 + title.get_height() + 6))

        stats_txt = self.small_font.render(stats_line, True, colors.MUTED_TEXT)
        self.surface.blit(stats_txt, (px + 16, 16 + title.get_height() + 6 + state_txt.get_height() + 4))

        # Buttons
        for b in buttons:
            b.draw(self.surface, self.small_font)

        # Grid draw
        if grid is not None:
            self._draw_grid(grid, start, goal, player, visited, frontier, path)

        pygame.display.flip()

    def _draw_grid(
        self,
        grid: Grid,
        start: Pos,
        goal: Pos,
        player: Player | None,
        visited: set[Pos],
        frontier: set[Pos],
        path: list[Pos],
    ) -> None:
        ox, oy = self.grid_origin
        cs, cg = self.cell_size, self.cell_gap

        for y in range(grid.height):
            for x in range(grid.width):
                p = (x, y)
                sx, sy = grid_to_screen(p, (ox, oy), cs, cg)
                rect = pygame.Rect(sx, sy, cs, cs)

                # Base tile
                if grid.is_wall(p):
                    color = colors.WALL
                else:
                    color = colors.FLOOR

                # Overlays
                if p in visited:
                    color = colors.VISITED
                if p in frontier:
                    color = colors.FRONTIER
                if p in path:
                    color = colors.PATH

                if p == start:
                    color = colors.START
                if p == goal:
                    color = colors.GOAL

                pygame.draw.rect(self.surface, color, rect)

        # Player on top
        if player is not None:
            sx, sy = grid_to_screen(player.pos, (ox, oy), cs, cg)
            rect = pygame.Rect(sx, sy, cs, cs)
            pygame.draw.rect(self.surface, colors.PLAYER, rect, border_radius=6)
