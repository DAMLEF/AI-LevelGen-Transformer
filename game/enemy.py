import math
import time

from game.entity import *

from game.pathfinding import *
from game.particle import *
from game.projectile import *


class Enemy(Living_Entity):
    TIME_BETWEEN_PATH_ACTUALISATION = 3  # In second

    DEFAULT_ATTACK_RANGE_CLOSE = 0.8  # In cell

    END_DISTANCE_WALK = 0.2

    def __init__(self, pos, speed, max_health: int, damage: int, attack_speed: float, target: Living_Entity,
                 distance_enemy: bool, attack_range: float):
        super().__init__(pos, speed, max_health, damage, attack_speed, LIGHT_RED)
        self.bad = True

        self.target = target
        self.distance = distance_enemy
        self.attack_range = attack_range

        # AI Enemy section
        self.path = None
        self.last_path_actualise = time.time()

    def is_in_attack_range(self) -> bool:
        vector = (self.pos[0] - self.target.pos[0], self.pos[1] - self.target.pos[1])
        return True if distance(vector) <= self.attack_range else False

    def get_new_path(self, world: Map):
        self.path = a_star(world, self.target.pos, self.pos)
        self.path.reverse()

        for i in range(len(self.path)):
            self.path[i] = (self.path[i].x, self.path[i].y)

        if self.path and not self.distance:
            self.path.append(self.target.pos)

    def can_attack(self) -> bool:
        t = time.time()
        return True if t - self.last_attack_time >= self.attack_speed and self.is_in_attack_range() else False

    def attack(self, engine):
        if self.distance:
            # todo:  projectile speed
            angle = engine.trigonometric_angle_of_object(self, self.target)
            vector = (math.cos(angle), math.sin(angle))
            engine.add_projectile(Enemy_Projectile(self.pos, 5, vector, self.get_damage()))
        else:
            self.target.remove_health(self.damage)

        self.last_attack_time = time.time()

    def actualise(self, engine, frame_rate: int, world: Map):
        super().actualise(engine, frame_rate, world)

        t = time.time()

        if (t - self.last_path_actualise >= Enemy.TIME_BETWEEN_PATH_ACTUALISATION or self.path is None) and not self.is_in_attack_range():
            self.path = []
            self.get_new_path(world)

            # Debug path trajectory
            for c in self.path:
                engine.add_particle(Particle((c[0], c[1]), 3, GOLD, 0))

            self.last_path_actualise = t

        if self.path is not None:
            if not self.path:
                self.path = None
            else:
                print(self.path)
                destination = self.path[0]

                vector = (destination[0] - self.pos[0], destination[1] - self.pos[1])
                # todo: normalize vector
                self.move(vector, frame_rate, world)

                dist = distance(vector)

                if dist < Enemy.END_DISTANCE_WALK:
                    self.path.pop(0)

        if self.can_attack():
            self.attack(engine)


class Mosquito(Enemy):
    def __init__(self, pos, target: Living_Entity):
        speed = 3
        distance_e = True

        max_health = 5
        damage = 1
        attack_speed = 0.5
        attack_range = 15

        textures = [pygame.image.load(f"assets/enemies/mosquito/{i}_left.png").convert_alpha() for i in range(6)]

        self.texture = Animation(textures, 0.01)

        super().__init__(pos, speed, max_health, damage, attack_speed, target, distance_e, attack_range)

    def actualise(self, engine, frame_rate: int, world: Map, ):
        super().actualise(engine, frame_rate, world)
        self.texture.actualise()

    def display(self, window: pygame.Surface, pos_conversion: Callable):
        pos = pos_conversion(self.pos)
        texture = self.texture.get_texture()

        t_size = texture.get_size()

        window.blit(texture, (pos[0] - t_size[0] / 2, pos[1] - t_size[1]))

    def get_rect(self, engine):
        pos = engine.screen_coordinates(self.pos)
        t_size = self.texture.get_texture().get_size()

        return pos[0] - t_size[0] / 2, pos[1] - t_size[1], t_size[0], t_size[1] / 2


ALL_ENEMIES = [Mosquito]

