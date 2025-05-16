import time

import pygame

from game.entity import *


def gaussian_between(a, b, std_dev_factor=1 / 5):
    mean = (a + b) / 2
    std_dev = (b - a) * std_dev_factor  # 99.7% in [a, b] if std_dev = (b - a)/6
    value = random.gauss(mean, std_dev)
    return max(min(value, b), a)  # clip to [a, b]


def gaussian_weight(x, mean, std_dev, a, b):
    # Densité normale standard
    value = math.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    max_value = math.exp(-0.5 * ((a - mean) / std_dev) ** 2)
    return (value - max_value) / (1 - max_value) if value > max_value else 0


class Particle(Entity):
    IMAGES = [pygame.image.load("assets/other/particle_red.png").convert_alpha(),
              pygame.image.load("assets/other/particle_orange.png").convert_alpha(),
              pygame.image.load("assets/other/particle_dark_blue.png").convert_alpha(),
              pygame.image.load("assets/other/particle_purple.png").convert_alpha(),
              pygame.image.load("assets/other/particle_green2.png").convert_alpha(),
              pygame.image.load("assets/other/particle_white.png").convert_alpha(),
              ]

    BURNING_PARTICLES = [IMAGES[0], IMAGES[1]]
    ITEM_PARTICLES = [IMAGES[5], IMAGES[4], IMAGES[2], IMAGES[3], IMAGES[0]]

    def __init__(self, pos: tuple, radius: int, color: tuple, radius_removed_per_frame=0.5, image=None):
        super().__init__(pos, 1, color)
        self.radius = radius
        self.max_radius = radius
        self.radius_removed_per_frame = radius_removed_per_frame

        self.image = image
        self.color = color

        # The particle get a kind of priority display until 2 cells above the pos
        self.height = 2

        self.in_bound = False

    def actualise(self, engine, frame_rate: int, world: Map):
        self.radius -= self.radius_removed_per_frame
        if self.radius <= 0:
            self.active = False

    def display(self, window: pygame.Surface, pos_conversion: Callable):
        pos = pos_conversion(self.pos)
        if self.image is None:
            pygame.draw.circle(window, (self.color[0], self.color[1], self.color[2],
                                        int(255 * (self.radius / self.max_radius))), pos, self.radius)
        else:
            if self.radius >= 1:
                image = self.image if self.radius == self.max_radius else pygame.transform.scale(self.image,
                                                                                                 (self.radius,
                                                                                                  self.radius))

                window.blit(image, (pos[0] - image.get_width() // 2,
                                    pos[1] - image.get_width() // 2))


class Particle_Flow:
    def __init__(self, time_between_particle: float, ref_pos: tuple, radius: int, color: tuple, height_travel: int,
                 height_variation: tuple, spawn_variation: tuple = ((-0.5, 0.5), (-0.5, 0.5)), image: list[pygame.Surface]=None,
                 gaussian_spawn_variation: bool = False, gaussian_inverse_height_spawn_propagation: bool = False):
        self.time_between_particle = time_between_particle
        self.last_time = time.time()

        self.ref_pos = ref_pos
        self.radius = radius
        self.color = color

        self.height_to_travel = height_travel
        self.height_variation = height_variation

        self.spawn_variation = spawn_variation
        self.image = image

        self.option_gaussian_sv = gaussian_spawn_variation
        self.option_gaussian_ihsp = gaussian_inverse_height_spawn_propagation

    def actualise(self, engine):
        t = time.time()

        if t - self.last_time >= self.time_between_particle:
            if self.image is not None:
                engine.add_particle(Evaporating_Particle(self.ref_pos, self.radius, self.color, self.height_to_travel,
                                                         self.height_variation, self.spawn_variation, random.choice(self.image),
                                                         self.option_gaussian_sv, self.option_gaussian_ihsp))
            else:
                engine.add_particle(Evaporating_Particle(self.ref_pos, self.radius, self.color, self.height_to_travel,
                                                         self.height_variation, self.spawn_variation, None,
                                                         self.option_gaussian_sv, self.option_gaussian_ihsp))
            self.last_time = t


class Evaporating_Particle(Particle):
    def __init__(self, pos: tuple, radius: int, color: tuple, height_travel: int, height_variation: tuple,
                 spawn_variation: tuple = ((-0.5, 0.5), (-0.5, 0.5)), image=None,
                 gaussian_spawn_variation: bool = False, gaussian_inverse_height_spawn_propagation: bool = False):
        super().__init__(pos, radius, color, 1,
                         image)
        self.height_to_travel = height_travel
        self.actual_height = 0

        x = 1
        if not gaussian_spawn_variation:
            self.pos = (pos[0] + random.uniform(spawn_variation[0][0], spawn_variation[0][1]),
                        pos[1] + random.uniform(spawn_variation[1][0], spawn_variation[1][1]))
        else:
            x = gaussian_between(spawn_variation[0][0], spawn_variation[0][1])
            self.pos = (pos[0] - x,
                        pos[1] - gaussian_between(spawn_variation[1][0], spawn_variation[1][1]))

        self.height_variation = height_variation

        if gaussian_spawn_variation and gaussian_inverse_height_spawn_propagation:
            self.height_to_travel *= gaussian_weight(x, 0, 1/5, -0.2, 0.2)

    def actualise(self, engine, frame_rate: int, world: Map):
        if not world.in_map(get_cell_pos(self.pos)):
            self.active = False

        if self.actual_height < self.height_to_travel:
            height_upgrade = random.randint(self.height_variation[0], self.height_variation[1])
            self.move((0, -height_upgrade), frame_rate, world)

            if self.pos != self.last_pos:
                self.actual_height += height_upgrade
        else:
            super().actualise(engine, frame_rate, world)

