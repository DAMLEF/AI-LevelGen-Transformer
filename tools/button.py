# Button management Module
import pygame
from typing import Callable

# Import
from tools.colors import *
from tools.basics import *
from tools.text_style import *

pygame.font.init()


# --------- #


class Button:
    lmb_pressed = False

    def __init__(self, x: float, y: float, width: int, height: int, name: str, base_color: tuple = LIGHT_YELLOW,
                 action=lambda: None):

        self.x = x
        self.y = y

        self.name = name
        self.rect = pygame.Rect([x, y, width, height])  # Rectangle position

        self.color = base_color
        self.on_color = RED
        self.pressed_color = GREEN

        self.action = action

        self.pressed = False

    def draw(self, window: pygame.Surface):

        if self.rect.collidepoint(input_info["M_POS"]):
            if not input_info["LMB"]:
                pygame.draw.rect(window, self.on_color, self.rect, 5)
            else:
                pygame.draw.rect(window, self.pressed_color, self.rect, 5)
        else:
            pygame.draw.rect(window, self.color, self.rect, 5)

    def is_pressed(self):
        return self.rect.collidepoint(input_info["M_POS"]) and input_info["LMB"]

    def is_on(self):
        return self.rect.collidepoint(input_info["M_POS"])

    def actualise(self):
        if self.is_pressed():
            if not self.pressed:
                self.pressed = True
                return self.action()
        else:
            self.pressed = False


class TextButton(Button):
    def __init__(self, x: float, y: float, width: int, height: int, name: str, style: TextStyle, text: str, center=True,
                 base_color: tuple = LIGHT_YELLOW, action=lambda: None):
        super().__init__(x, y, width, height, name, base_color, action)

        self.text = text
        self.style = style
        self.render = style.render(text)

        self.center = center

        if center:
            self.text_pos = (self.rect.x + abs(self.rect.width - self.render.get_width()) // 2,
                             self.rect.y + abs(self.rect.height - self.render.get_height()) // 2)
        else:
            self.text_pos = (self.rect.x + 5,
                             self.rect.y + abs(self.rect.height - self.render.get_height()) // 2)

    def actualise_text_pos(self):
        if self.x != self.rect.x or self.rect.y != self.y:
            if self.center:
                self.text_pos = (self.rect.x + abs(self.rect.width - self.render.get_width()) // 2,
                                 self.rect.y + abs(self.rect.height - self.render.get_height()) // 2)
            else:
                self.text_pos = (self.rect.x + 5,
                                 self.rect.y + abs(self.rect.height - self.render.get_height()) // 2)

    def actualise(self):
        super().actualise()
        self.actualise_text_pos()

    def draw(self, window: pygame.Surface):
        super().draw(window)

        window.blit(self.render, self.text_pos)


class BoolButton(TextButton):
    def __init__(self, x: float, y: float, width: int, height: int, name: str, style: TextStyle, text: str, center=True,
                 start_value: bool = False):
        act = lambda: self.change_value()
        super().__init__(x, y, width, height, name, style, text, center, action=act)

        self.color = LIGHT_RED
        self.on_color = LIGHT_BLUE2
        self.pressed_color = PURPLE

        self.value = start_value

    def change_value(self):
        self.value = not self.value

        if self.value:
            self.color = GREEN
        else:
            self.color = RED


class SelectionButton(TextButton):
    HEIGHT = 50

    def __init__(self, x: float, y: float, name: str, text: str, selection: Callable,
                 base_color: tuple = LIGHT_YELLOW, action=lambda: None):
        style = DefaultStyle(20, LIGHT_YELLOW, True)

        width = 140
        height = 50
        super().__init__(x, y, width, height, name, style, text, False, base_color, action)

        self.selection = selection
        self.text_pos = (self.text_pos[0] + 40, self.text_pos[1])


class CellSelectorButton(SelectionButton):
    HEIGHT = 50

    def __init__(self, x: float, y: float, name: str, text: str, cell_color: tuple, selection: Callable,
                 base_color: tuple = LIGHT_YELLOW, action=lambda: None):

        super().__init__(x, y, name, text, selection, base_color, action)

        self.cell_color = cell_color

    def draw(self, window: pygame.Surface):
        super().draw(window)

        pygame.draw.rect(window, self.cell_color, (self.rect.x + 10, self.rect.y + 10, 30, 30))


class BuildSelectorButton(SelectionButton):
    HEIGHT = 50

    def __init__(self, x: float, y: float, name: str, text: str, build_texture: pygame.Surface, selection: Callable,
                 base_color: tuple = LIGHT_YELLOW, action=lambda: None):

        super().__init__(x, y, name, text, selection, base_color, action)

        self.build_texture = build_texture

    def draw(self, window: pygame.Surface):
        super().draw(window)

        window.blit(self.build_texture, (self.rect.x + 10, self.rect.y + 10))