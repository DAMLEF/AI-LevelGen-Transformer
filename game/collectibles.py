import random

import pygame

from game.entity import *
from game.particle import *
from game.item import *


class Collectibles(Entity):
    SHADOW = pygame.image.load("assets/other/shadow.png").convert_alpha()
    SHADOW_sz = SHADOW.get_size()

    def __init__(self, pos: tuple, texture: pygame.Surface, item: Item, rarity: int):
        super().__init__(pos, 0, WHITE)
        
        if rarity < 0:
            rarity = 0 
        elif rarity >= len(Particle.ITEM_PARTICLES):
            rarity = len(Particle.ITEM_PARTICLES) - 1   
        
        particle_color = [Particle.ITEM_PARTICLES[rarity]]

        self.texture = pygame.transform.scale(texture, (20, 20))
        self.flow = Particle_Flow(0.05, self.pos, 1, WHITE, 90, (1, 1),
                                  ((-0.2, 0.25), (-0.05, 0)), particle_color)
        self.height += 2.5

        self.item = item

    def actualise(self, engine, frame_rate: int, world: Map, ):
        self.flow.actualise(engine)

    def display(self, window: pygame.Surface, pos_conversion: Callable):
        pos = pos_conversion(self.pos)

        sz_t = self.texture.get_size()

        window.blit(Collectibles.SHADOW, (pos[0] - Collectibles.SHADOW_sz[0] / 2, pos[1] - Collectibles.SHADOW_sz[1]))
        window.blit(self.texture, (pos[0] - sz_t[0] / 2, pos[1] - sz_t[1]))

    def collide_mouse(self, mouse_in_map: tuple) -> bool:

        if ((self.pos[0] - 0.3) <= mouse_in_map[0] <= (self.pos[0] + 0.3) and
                (self.pos[1] - 0.6) <= mouse_in_map[1] <= self.pos[1]):
            return True
