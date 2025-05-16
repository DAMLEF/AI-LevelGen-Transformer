from typing import Callable
import pygame

from tools.colors import *
from tools.animation import *
from game.map import *

pygame.display.init()


class Entity:
    def __init__(self, pos, speed, color: tuple = LIGHT_BLUE) -> None:
        self.pos = pos
        self.last_pos = pos
        self.speed = speed

        self.last_vector = (0, 0)

        self.reverse_speed = True

        self.active = True

        # La couleur d'affichage de l'entité
        self.color = color

        # Ce paramètre précise si l'entité doit rester dans les limites du terrain
        self.in_bound = True

        # Ce paramètre permet d'aider à l'affichage en renseignant la hauteur de l'entité
        self.height = 0

    # The function take a vector and apply few transformations to move the entity
    def move(self, v: tuple[float, float], frame_rate: int, world: Map):
        reset_move = False
        self.last_pos = tuple(self.pos)

        speed = self.speed if not (not self.reverse_speed and self.speed < 0) else 0
        norm = distance(v)

        if norm == 0:  # Pas de déplacement
            return
        vector = (v[0] / norm, v[1] / norm)

        self.pos = (self.pos[0] + (vector[0] * speed) / frame_rate, self.pos[1] + (vector[1] * speed) / frame_rate)

        if self.in_bound:
            grid_pos = (int(self.pos[0]), int(self.pos[1]))
            if world.in_map(grid_pos, self.pos):
                if not world[grid_pos].get_walkable():
                    reset_move = True
            else:
                reset_move = True

        if reset_move:
            self.reset_move()

    def reset_move(self):
        self.pos = self.last_pos

    def move_to(self, pos: tuple) -> None:  # Move entity (teleportation)
        self.pos = pos

    def display(self, window: pygame.Surface, pos_conversion: Callable):
        # Par défaut le jeu affiche un cercle à la position de l'entité
        pygame.draw.circle(window, self.color, pos_conversion(self.pos), 3)

    def actualise(self, engine, frame_rate: int, world: Map):
        self.last_vector = (self.pos[0] - self.last_pos[0], self.pos[1] - self.last_pos[1])

    def change_speed(self, amount):
        self.speed += amount  # La speed est appliquée sur le vecteur dans move

    def set_speed(self, new_speed: float):
        self.speed = new_speed

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True


class Living_Entity(Entity):
    def __init__(self, pos, speed, max_health: int, damage: int, attack_speed: float, color: tuple = LIGHT_BLUE):
        super().__init__(pos, speed, color)
        self.health = max_health
        self.max_health = max_health

        self.damage = damage
        self.attack_speed = attack_speed
        self.last_attack_time = time.time()

        self.bad = False  # This attribute informs if the entity is susceptible to attack a good entity
        # (player, PNJ, ...)

    def remove_health(self, amount: int):
        self.health -= amount

        if self.health <= 0:
            self.active = False

    def give_health(self, amount: int):
        self.health += amount

        if self.health > self.max_health:
            self.health = self.max_health

    def get_damage(self):
        return self.damage

    def get_rect(self, engine):
        pos = engine.screen_coordinates(self.pos)

        return pos[0] - 15, pos[1] - 30, 30, 30

    def get_pygame_rect(self, engine):
        return pygame.Rect(self.get_rect(engine))
