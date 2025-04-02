from game.cell import *

class Map:
    def __init__(self):
        self.size = (0, 0)

        self.map = {}

    def __str__(self):
        return f"* MAP :  \n\t - SIZE : {self.size} \n\t - CONTENT : {self.map}"

    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        self.map[key] = value

    def create(self, width: int, height: int):
        # ⚠️ Cette fonction détruit la map précédente

        self.size = (width, height)

        self.map = {}
        for y in range(height):
            for x in range(width):
                self.map[(x, y)] = Cell()

    def get_map(self):
        return self.map
