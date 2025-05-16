import random
import math
import time

import pygame

from typing import Callable
from tools.colors import *

from game.cell_detail import *


class Cell:
    # La taille des cellules qui composent le monde
    SIZE = 30

    Cell_Detail.CELL_SIZE = SIZE

    def __init__(self, walkable=True, color=(255, 0, 0), wall=False, build=None):
        self.walkable = walkable  # Paramètre pour dire si l'on peut ou non marcher sur la case (Joueur et entités)
        self.color = color  # Paramètre qui définie la couleur de la case

        self.wall = wall  # Paramètre pour dire s'il s'agit d'un mur (arrête net les projectiles)

        self.build = build

        self.extras: list[Cell_Detail] = []

    def initiate(self, x: int, y: int):
        if self.build is not None and not self.build.initiated:
            self.walkable = self.build.walkable
            self.wall = self.build.wall

            self.build.pos = (x, y)
            self.build.initiated = True

    def get_walkable(self):
        return self.walkable

    def get_wall(self):
        return self.wall

    def set_walkable(self, state: bool = True):
        self.walkable = state

    def set_wall(self, state: bool = True):
        self.wall = state

    def reverse_walkable(self):
        self.walkable = not self.walkable

    def reverse_wall(self):
        self.wall = not self.wall

    def set_color(self, color):
        self.color = color

    def generates_rocks(self, min_amount: int = 1, max_amount: int = 2):
        rocks = random.randint(min_amount, max_amount)

        for _ in range(rocks):
            self.extras.append(Rock(gen_relative_pos(), gen_relative_pos()))

    def generates_crystals(self, min_amount: int = 1, max_amount: int = 4):
        crystals = random.randint(min_amount, max_amount)

        for _ in range(crystals):
            self.extras.append(Crystal_Detail(gen_relative_pos(), gen_relative_pos()))

    def generate_blades(self, min_amount: int = 4, max_amount: int = 8):
        blades = random.randint(min_amount, max_amount)

        for _ in range(blades):
            self.extras.append(Blades(gen_relative_pos(), gen_relative_pos(), random.randint(3, 10),
                                      random.uniform(-0.2, 0.2)))

    def generate_flowers(self, min_amount: int = 1, max_amount: int = 2):
        flowers = random.randint(min_amount, max_amount)

        for _ in range(flowers):
            self.extras.append(Strelitzia_Detail(gen_relative_pos(), gen_relative_pos()))

    def generates_bush(self, min_amount: int = 1, max_amount: int = 2):
        flowers = random.randint(min_amount, max_amount)

        for _ in range(flowers):
            self.extras.append(Bush(gen_relative_pos(), gen_relative_pos()))

    def generates_shells(self, min_amount: int = 1, max_amount: int = 3):
        shells = random.randint(min_amount, max_amount)

        for _ in range(shells):
            self.extras.append(Shells(gen_relative_pos(), gen_relative_pos()))

    def generates_cactus(self, min_amount: int = 1, max_amount: int = 3):
        shells = random.randint(min_amount, max_amount)

        for _ in range(shells):
            self.extras.append(Cactus_Detail(gen_relative_pos(), gen_relative_pos()))

    def generates_desert_bush(self, min_amount: int = 1, max_amount: int = 3):
        bushs = random.randint(min_amount, max_amount)

        for _ in range(bushs):
            self.extras.append(Desert_Bush(gen_relative_pos(), gen_relative_pos()))

    def generates_cracks(self, min_amount: int = 1, max_amount: int = 2):
        cracks = random.randint(min_amount, max_amount)

        for _ in range(cracks):
            self.extras.append(Cracks(gen_relative_pos(), gen_relative_pos()))

    def generates_bones(self, min_amount: int = 1, max_amount: int = 3):
        bones = random.randint(min_amount, max_amount)

        for _ in range(bones):
            self.extras.append(Bone(gen_relative_pos(), gen_relative_pos()))

    def generates_lilypad(self, min_amount: int = 1, max_amount: int = 2):
        lp = random.randint(min_amount, max_amount)

        for _ in range(lp):
            self.extras.append(Lilypad(gen_relative_pos(), gen_relative_pos()))


class Water(Cell):
    def __init__(self):
        super().__init__(False, LIGHT_BLUE)


class Grass(Cell):
    def __init__(self):
        super().__init__(True, GREEN)


class Sand(Cell):
    def __init__(self):
        super().__init__(True, SAND)


class Stone(Cell):
    def __init__(self):
        super().__init__(True, SLATE_TWILIGHT)


class Snow(Cell):
    def __init__(self):
        super().__init__(True, SNOW)


class City(Cell):
    def __init__(self):
        super().__init__(True, ASPHALT)


ALL_CELLS_TYPE = [Grass, Water, Sand, Stone, Snow, City]
