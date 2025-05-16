import random
from typing import Callable

from game.particle import *

import pygame


class Build:

    def __init__(self, name: str, walkable: bool = False, wall: bool = True, texture: pygame.Surface = None):
        self.name = name

        self.initiated = False
        self.active = True

        self.walkable = walkable
        self.wall = wall

        self.texture = texture
        if self.texture is not None:
            self.small_texture = pygame.transform.scale(self.texture, (15, 15))

        self.interaction = None
        self.interaction_range = None

        self.pos = (0, 0)
        self.height = 0

        self.resistance = None

    def interact(self, engine):
        pass

    def display(self, window: pygame.Surface, pos_conversion: Callable):
        pos = pos_conversion(self.pos)

        cell_size = abs(pos_conversion((1, 0))[0] - pos_conversion((0, 0))[0])

        texture_size = self.texture.get_size()

        window.blit(self.texture, (pos[0] + (cell_size - texture_size[0])/2,
                                   pos[1] - (texture_size[1] - cell_size)))

    def actualise(self, engine):
        pass


class Interaction_Build(Build):
    def __init__(self, name: str, walkable: bool = False, wall: bool = True, texture: pygame.Surface = None,
                 interaction_range: float = 1.15):
        super().__init__(name, walkable, wall, texture)

        self.interaction = 1
        self.interaction_range = interaction_range


class Breakable_Build(Build):
    def __init__(self, name: str, walkable: bool = False, wall: bool = True, texture: pygame.Surface = None,
                 resistance: int = 20):
        super().__init__(name, walkable, wall, texture)

        self.resistance = resistance

    def remove_resistance(self, amount):
        self.resistance -= amount

        if self.resistance <= 0:
            self.active = False


class Chest(Interaction_Build):
    def __init__(self):
        name = "Chest"

        walkable = False
        wall = True

        texture = pygame.image.load("assets/builds/chest.png").convert_alpha()

        super().__init__(name, walkable, wall, texture)

        self.texture_open = pygame.image.load("assets/builds/chest_opened.png").convert_alpha()

        self.height = 0.7

    def interact(self, engine):
        self.texture = self.texture_open


class Strelitzia(Interaction_Build):
    def __init__(self):
        name = "Strelitzia"
        walkable = True
        wall = False

        texture = pygame.image.load("assets/builds/strelitzia/main.png").convert_alpha()

        super().__init__(name, walkable, wall, texture)

        self.height = 0.9


class Workbench(Interaction_Build):
    def __init__(self):
        name = "Workbench"

        walkable = False
        wall = False

        texture = pygame.image.load("assets/builds/workbench.png").convert_alpha()

        super().__init__(name, walkable, wall, texture)

        self.height = 0.7


class Vending_Machine(Interaction_Build):
    def __init__(self):
        name = "Vending Machine"
        walkable = False
        wall = True

        texture = pygame.image.load("assets/builds/vending_machine.png").convert_alpha()

        super().__init__(name, walkable, wall, texture)

        self.height = 1


class Fire_Camp(Interaction_Build):
    def __init__(self):
        name = "Fire camp"
        walkable = False
        wall = False

        texture = pygame.image.load("assets/builds/fire_camp.png").convert_alpha()

        super().__init__(name, walkable, wall, texture)

        self.height = 0.8

        self.flow = None

    def actualise(self, engine):
        if self.flow is None:
            self.flow = Particle_Flow(0.015, (self.pos[0] + 0.57, self.pos[1] + 0.43), 6,
                                      RED, 100, (1, 6),
                                      ((-0.2, 0.35), (-0.2, 0.1)), Particle.BURNING_PARTICLES,
                                      True, True)
        else:
            self.flow.actualise(engine)


class Cactus(Interaction_Build):
    def __init__(self):
        name = "Cactus"
        walkable = False
        wall = True

        texture = pygame.image.load("assets/builds/cactus/main.png").convert_alpha()

        super().__init__(name, walkable, wall, texture)

        self.height = 1


class Boat(Interaction_Build):
    def __init__(self):
        name = "Boat"
        walkable = False
        wall = True

        texture = pygame.image.load("assets/builds/boat.png").convert_alpha()

        super().__init__(name, walkable, wall, texture)

        self.height = 0.8


class Bandit_Camp(Interaction_Build):
    def __init__(self):
        name = "Bandits camp"
        walkable = False
        wall = True

        texture = pygame.image.load("assets/builds/bandit_camp.png").convert_alpha()

        super().__init__(name, walkable, wall, texture)

        self.height = 1


class Crystal(Interaction_Build):
    def __init__(self):
        name = "Crystal"
        walkable = False
        wall = True

        texture = pygame.image.load("assets/builds/crystal/main.png").convert_alpha()

        super().__init__(name, walkable, wall, texture)

        self.height = 1


ALL_BUILDS = [Chest, Strelitzia, Workbench, Vending_Machine, Fire_Camp, Cactus, Bandit_Camp, Boat, Crystal]

