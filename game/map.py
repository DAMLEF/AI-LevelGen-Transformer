import math

from game.cell import *


def distance(vector: tuple[float, float]):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)


def distance2(x_1: float, y_1: float, x_2: float, y_2: float):
    return math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)


def get_cell_pos(pos: tuple[float, float]):
    return int(pos[0]), int(pos[1])


class Map:
    def __init__(self):
        self.size = (0, 0)

        self.map = {}

        self.name = ""

    def __str__(self):
        return f"* MAP {self.name}:  \n\t - SIZE : {self.size} \n\t - CONTENT : {self.map}"

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        self.map[key] = value

    def in_map(self, grid_pos: tuple[int, int], pos: tuple[float, float] = (0, 0)) -> bool:
        if pos[0] < 0 or pos[1] < 0:
            return False

        return True if self.map.get(grid_pos) is not None else False

    def change_name(self, name: str):
        self.name = name

    # todo : ?
    #def condition_over_neighbour(self, pos: tuple[int, int], side, condition):

    def create(self, width: int, height: int):
        # ⚠️ Cette fonction détruit la map précédente

        self.size = (width, height)

        self.map = {}
        for y in range(height):
            for x in range(width):
                self.map[(x, y)] = Grass()

    def get_map(self):
        return self.map

    def get_neighbour(self, x: int, y: int):
        result = []

        if self.in_map((x - 1, y - 1)):
            result.append((x - 1, y - 1))

        if self.in_map((x, y - 1)):
            result.append((x, y - 1))

        if self.in_map((x + 1, y - 1)):
            result.append((x + 1, y - 1))

        if self.in_map((x - 1, y + 1)):
            result.append((x - 1, y + 1))

        if self.in_map((x, y + 1)):
            result.append((x, y + 1))

        if self.in_map((x + 1, y + 1)):
            result.append((x + 1, y + 1))

        if self.in_map((x - 1, y)):
            result.append((x - 1, y))

        if self.in_map((x + 1, y)):
            result.append((x + 1, y))

        return result

    def get_neighbour_walkable(self, x: int, y: int):
        result = []

        if self.in_map((x - 1, y - 1)) and self[(x - 1, y - 1)].get_walkable():
            result.append((x - 1, y - 1))

        if self.in_map((x, y - 1)) and self[(x, y - 1)].get_walkable():
            result.append((x, y - 1))

        if self.in_map((x + 1, y - 1)) and self[(x + 1, y - 1)].get_walkable():
            result.append((x + 1, y - 1))

        if self.in_map((x - 1, y + 1)) and self[(x - 1, y + 1)].get_walkable():
            result.append((x - 1, y + 1))

        if self.in_map((x, y + 1)) and self[(x, y + 1)].get_walkable():
            result.append((x, y + 1))

        if self.in_map((x + 1, y + 1)) and self[(x + 1, y + 1)].get_walkable():
            result.append((x + 1, y + 1))

        if self.in_map((x - 1, y)) and self[(x - 1, y)].get_walkable():
            result.append((x - 1, y))

        if self.in_map((x + 1, y)) and self[(x + 1, y)].get_walkable():
            result.append((x + 1, y))

        return result

    def save_map(self, path: str):
        save = {}

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                grid_pos_data = (self[(x, y)].__class__.__name__, 0, self[(x, y)].build.__class__.__name__, 0)

                save[(x, y)] = grid_pos_data

        with open(path, "w") as f:
            f.write(str(save))
