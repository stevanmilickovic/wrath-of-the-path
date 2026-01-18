from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pygame

from ..utils.math2d import Rect
from . import colors


@dataclass
class Button:
    rect: Rect
    text: str
    on_click: Callable[[], None]
    enabled: bool = True
    _hover: bool = False

    def set_hover(self, mouse_x: int, mouse_y: int) -> None:
        self._hover = self.enabled and self.rect.contains(mouse_x, mouse_y)

    def handle_mouse_down(self, mouse_x: int, mouse_y: int) -> bool:
        if not self.enabled:
            return False
        if self.rect.contains(mouse_x, mouse_y):
            self.on_click()
            return True
        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        r = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)

        if not self.enabled:
            color = colors.BTN_DISABLED
        else:
            color = colors.BTN_HOVER if self._hover else colors.BTN

        pygame.draw.rect(surface, color, r, border_radius=10)

        label = font.render(self.text, True, colors.BTN_TEXT)
        lx = self.rect.x + (self.rect.w - label.get_width()) // 2
        ly = self.rect.y + (self.rect.h - label.get_height()) // 2
        surface.blit(label, (lx, ly))
