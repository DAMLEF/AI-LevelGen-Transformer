from tools.all import *
from game.map import *


class Engine:
    RESOLUTION = (1280, 720)

    def __init__(self, background_color: tuple, camera, world_map: Map):
        self.screen = pygame.display.set_mode(Engine.RESOLUTION)

        self.map = world_map

        self.background_color = background_color

    def display(self):
        self.screen.fill(self.background_color)

        self.display_map(True)

        pygame.display.update()

    def display_map(self, display_cell_border: bool = False):

        for y in range(self.map.size[1]):
            for x in range(self.map.size[0]):
                pos = self.screen_coordinates((x, y))

                pygame.draw.rect(self.screen, self.map[(x, y)].color, (pos, (Cell.SIZE, Cell.SIZE)))
                if display_cell_border:
                    pygame.draw.rect(self.screen, WHITE, (pos, (Cell.SIZE, Cell.SIZE)), 1)

    def screen_coordinates(self, pos: tuple):
        return (10 + pos[0] * Cell.SIZE, 10 + pos[1] * Cell.SIZE)
