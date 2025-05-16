import random
import time
import pygame
import math

from tools.colors import *
from typing import Callable


def gen_relative_pos():
    return random.randint(0, 100)


class Cell_Detail:
    CELL_SIZE = 30

    def __init__(self, xr: int, yr: int):
        # Percentage position in the cell
        self.xr = xr
        self.yr = yr

        if not (0 <= xr <= 100):
            self.xr = 0

        if not (0 <= yr <= 100):
            self.yr = 0

        self.pos = (0, 0)
        self.height = 0

    def define_absolute_pos(self, x: int, y: int):
        self.pos = (x + self.xr/100, y + self.yr/100)

    def display(self, window: pygame.Surface, pos_converter: Callable):
        pass


class Texture_Cell_Detail(Cell_Detail):
    SHADOW = pygame.image.load("assets/other/shadow.png").convert_alpha()
    SHADOW_IMAGE_SIZE = SHADOW.get_size()

    def __init__(self, xr: int, yr: int, texture: pygame.Surface):
        super().__init__(xr, yr)

        self.texture = texture
        self.shadow = True

    def display(self, window: pygame.Surface, pos_converter: Callable):
        pos = pos_converter(self.pos)

        texture_size = self.texture.get_size()

        if self.shadow:
            window.blit(Texture_Cell_Detail.SHADOW, (pos[0] - Texture_Cell_Detail.SHADOW_IMAGE_SIZE[0]/2,
                                                   pos[1] - Texture_Cell_Detail.SHADOW_IMAGE_SIZE[1]/2))
        window.blit(self.texture, (pos[0] - texture_size[0]/2, pos[1] - texture_size[1]))


class Blades(Cell_Detail):
    BLADES_COLOR = DARK_GREEN

    def __init__(self, xr: int, yr: int, length: int = 6, base_angle: float = 0):
        # Percentage position in the cell
        super().__init__(xr, yr)

        self.length = length
        self.base_angle = base_angle

        if not (0 <= length <= 10):
            self.length = 6

        if not (-0.2 <= base_angle <= 0.2):
            self.base_angle = 0

    def display(self, window: pygame.Surface, pos_converter: Callable):
        t = time.time()
        pos = pos_converter(self.pos)

        angle = self.base_angle + 0.2 * math.sin(t)

        bx = pos[0]
        by = pos[1]

        dx = self.length * math.sin(angle)
        dy = self.length * math.cos(angle)

        pygame.draw.line(window, Blades.BLADES_COLOR, (bx, by), (bx + dx, by - dy), 2)


class Strelitzia_Detail(Texture_Cell_Detail):

    TEXTURES = [pygame.image.load(f"assets/builds/strelitzia/{i}.png").convert_alpha() for i in range(3)]

    def __init__(self, xr: int, yr: int):
        super().__init__(xr, yr, random.choice(Strelitzia_Detail.TEXTURES))


class Bush(Texture_Cell_Detail):
    TEXTURE = pygame.image.load(f"assets/builds/bush.png").convert_alpha()

    def __init__(self, xr: int, yr: int):
        super().__init__(xr, yr, Bush.TEXTURE)


class Rock(Texture_Cell_Detail):
    TEXTURES = [pygame.image.load(f"assets/builds/rock/{i}.png").convert_alpha() for i in range(3)]

    def __init__(self, xr: int, yr: int):
        super().__init__(xr, yr, random.choice(Rock.TEXTURES))


class Shells(Cell_Detail):
    def __init__(self, xr: int, yr: int,):
        super().__init__(xr, yr)

        self.right_add = False
        if random.randint(0, 1) == 1:
            self.right_add = True

    def display(self, window: pygame.Surface, pos_converter: Callable):
        pos = pos_converter(self.pos)

        pygame.draw.rect(window, GREY, (pos[0], pos[1], 2, 4), 2)
        if self.right_add:
            pygame.draw.rect(window, GREY, (pos[0], pos[1], 4, 2), 2)


class Cactus_Detail(Texture_Cell_Detail):
    TEXTURES = [pygame.image.load(f"assets/builds/cactus/{i}.png").convert_alpha() for i in range(4)]

    def __init__(self, xr: int, yr: int):
        super().__init__(xr, yr, random.choice(Cactus_Detail.TEXTURES))


class Desert_Bush(Texture_Cell_Detail):
    TEXTURE = pygame.image.load(f"assets/builds/desert_bush.png")

    def __init__(self, xr: int, yr: int):
        super().__init__(xr, yr, Desert_Bush.TEXTURE)


class Crystal_Detail(Texture_Cell_Detail):
    TEXTURES = [pygame.image.load(f"assets/builds/crystal/{i}.png").convert_alpha() for i in range(5)]

    def __init__(self, xr: int, yr: int):
        super().__init__(xr, yr, random.choice(Crystal_Detail.TEXTURES))


class Bone(Texture_Cell_Detail):
    TEXTURES = [pygame.image.load(f"assets/builds/bone/{i}.png").convert_alpha() for i in range(4)]

    def __init__(self, xr: int, yr: int):
        super().__init__(xr, yr, random.choice(Bone.TEXTURES))

        self.shadow = False


class Lilypad(Texture_Cell_Detail):
    TEXTURES = [pygame.image.load(f"assets/builds/lilypad/{i}.png").convert_alpha() for i in range(4)]

    def __init__(self, xr: int, yr: int):
        super().__init__(xr, yr, random.choice(Lilypad.TEXTURES))

        self.shadow = False


class Cracks(Cell_Detail):
    def __init__(self, xr: int, yr: int, zig_zag: int = 5):
        super().__init__(xr, yr)

        self.zig_zag = zig_zag

        self.offset = []
        for i in range(self.zig_zag):
            self.offset.append((random.choice([-5, -3, 3, 5]), random.choice([-5, -3, 3, 5])))

        sum_offset_height = 0
        for off in self.offset:
            sum_offset_height += off[1]

        self.height = sum_offset_height / Cell_Detail.CELL_SIZE

    def display(self, window: pygame.Surface, pos_converter: Callable):
        pos = pos_converter(self.pos)

        lines = [pos]
        for i in range(self.zig_zag):
            lines.append((lines[i][0] + self.offset[i][0], lines[i][1] + self.offset[i][1]))

        pygame.draw.lines(window, COLD_GREY, False, lines, 4)
