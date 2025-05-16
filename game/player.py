import time

import pygame.image

from game.camera import *
from game.particle import *
from game.inventory import *


class Player(Living_Entity):
    START_HEALTH = 15
    START_DAMAGE = 1

    START_SPEED = 15
    START_ATTACK_SPEED = 2  # Amount of attack per second
    START_ATTACK_SPEED = 150  # Amount of attack per second

    ANIMATION_SPEED = 0.4

    GCD = 0.5   # Global cooldown to every item

    HITBOX_TOP_OFFSET = 15

    def __init__(self):
        super().__init__((0, 0), Player.START_SPEED, Player.START_HEALTH, Player.START_DAMAGE,
                         Player.START_ATTACK_SPEED)
        self.IDLE_FRONT = [pygame.image.load(f"assets/player/animation/idle_front/{i}.png").convert_alpha() for i in
                           range(7)]
        self.particle_texture = pygame.image.load("assets/other/particle.png").convert_alpha()
        self.mask = pygame.image.load("assets/items/masks/utopex.png")
        self.mask = pygame.transform.scale(self.mask, (22, 22))
        # todo

        self.camera = Camera(self.pos, self.speed)

        # Inventory and Items gestion
        self.inventory = Inventory()

        self.last_item_use = time.time()

        # The pos of the player is at his feet
        self.height = 5

        # Animation gestion
        self.last_animation_time = time.time()
        self.animation_state = 0

        # Player modifiers
        # todo

    def move(self, v: tuple[float, float], frame_rate: int, world: Map):
        super().move(v, frame_rate, world)

        if self.pos != self.last_pos:
            self.camera.move(v, frame_rate, world)

    def actualise(self, engine, frame_rate: int, world: Map):
        super().actualise(engine, frame_rate, world)

        t = time.time()
        if t - self.last_animation_time >= Player.ANIMATION_SPEED:
            self.animation_state += 1

            self.last_animation_time = t

        particle_pos = (self.pos[0] + 0.05, self.pos[1] - 0.5)
        engine.add_particle(Evaporating_Particle(particle_pos, 2, LIGHT_BLUE, 100, (1, 3),
                                                 ((-0.2, 0.2), (-0.05, 0.1)), self.particle_texture,
                                                 gaussian_spawn_variation=True,
                                                 gaussian_inverse_height_spawn_propagation=True))

    def get_camera(self):
        return self.camera

    def can_attack(self):
        if time.time() - self.last_attack_time >= 1 / self.attack_speed:
            return True
        return False

    def remove_health(self, amount: int):
        super().remove_health(amount)

        if self.health <= 0:
            print("Le joueur est mort !")
            # todo

    def give_health(self, amount: int):
        super().give_health(amount)

    def get_damage(self):
        return super().get_damage()

    def get_texture(self):
        return self.IDLE_FRONT[self.animation_state % len(self.IDLE_FRONT)]

    def display(self, window: pygame.Surface, pos_conversion: Callable):
        sz = window.get_size()

        texture = self.get_texture()
        t_size = texture.get_size()

        mask = self.mask
        mask_sz = mask.get_size()

        window.blit(texture, (sz[0] / 2 - t_size[0] / 2, sz[1] / 2 - t_size[1] / 2))
        window.blit(mask, (sz[0] / 2 - t_size[0] / 2, sz[1] / 2 - t_size[1] / 2 - mask_sz[1] / 2))

        # Draw Hit box
        # pygame.draw.rect(window, RED, self.get_rect(window))

    def get_inventory(self):
        return self.inventory

    def get_rect(self, window):
        sz = window.get_size()

        texture = self.get_texture()
        t_size = texture.get_size()

        return (sz[0] / 2 - t_size[0] / 2, sz[1] / 2 - t_size[1] / 2 - Player.HITBOX_TOP_OFFSET, t_size[0],
                t_size[1] + Player.HITBOX_TOP_OFFSET)

    def get_pygame_rect(self, window):
        return pygame.Rect(self.get_rect(window))
