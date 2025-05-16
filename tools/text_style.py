import pygame

pygame.font.init()


# todo Shadow Style
class TextStyle:
    def __init__(self, font: str, size: int, color: tuple, bold=False, antialiasing=True):
        self.f = font
        self.s = size
        self.c = color

        self.b = bold
        self.al = antialiasing

        #todo
        self.font = pygame.font.SysFont(self.f, self.s, self.b)

    def render(self, text):
        return self.font.render(text, self.al, self.c)


class BaseStyle(TextStyle):
    def __init__(self, size: int, color: tuple, bold: bool = False):
        super().__init__("Consolas", size, color, bold)


class DefaultStyle(TextStyle):
    def __init__(self, size: int, color: tuple, bold: bool = False):
        super().__init__(None, size, color, bold)