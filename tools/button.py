# Button management Module

# Import
from tools.colors import *
from tools.basics import *
from tools.text_style import *

pygame.font.init()


# --------- #


class Button:
    lmb_pressed = False

    def __init__(self, x: float, y: float, width: int, height: int, name: str, action=lambda: None):

        self.x = x
        self.y = y

        self.name = name
        self.rect = pygame.Rect([x, y, width, height])  # Rectangle position
        self.action = action

        self.pressed = False

    def draw(self, window: pygame.Surface):

        if self.rect.collidepoint(input_info["M_POS"]):
            if not input_info["LMB"]:
                pygame.draw.rect(window, LIGHT_YELLOW, self.rect, 6)
            else:
                pygame.draw.rect(window, GREEN, self.rect, 6)
        else:
            pygame.draw.rect(window, RED, self.rect, 6)

        pygame.draw.rect(window, DARK_GREY, self.rect, 3)

    def is_pressed(self):
        return self.rect.collidepoint(input_info["M_POS"]) and input_info["LMB"]

    def actualise(self):

        if self.is_pressed():
            if not self.pressed:
                self.pressed = True
                return self.action()
        else:
            self.pressed = False


class TextButton(Button):
    def __init__(self, x: float, y: float, width: int, height: int, name: str, style: TextStyle, text: str, center=True,
                 action=lambda: None):
        super().__init__(x, y, width, height, name, action)

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
