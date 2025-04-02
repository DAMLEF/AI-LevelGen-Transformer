import pygame


class Displayer:
    def __init__(self, surface: pygame.Surface, x: int, y: int):
        self.surface = surface

        self.x = x
        self.y = y

    def draw(self, window: pygame.Surface):
        window.blit(self.surface, (self.x, self.y))

