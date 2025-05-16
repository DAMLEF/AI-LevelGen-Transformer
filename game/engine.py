import time

import pygame.transform

from tools.all import *
from game.map import *
from game.hud import *
from game.projectile import *
from game.particle import *
from game.item import *
from game.collectibles import *

import math


class Engine:
    RESOLUTION = (1280, 720)

    ROUND_DISPLAY_IG = (11, 7)
    ROUND_DISPLAY_EM = (45, 45)

    INTERACTION_DISTANCE = 1.15

    IN_GAME_ZOOM = 2
    MIN_ZOOM = 1
    MAX_ZOOM = 6

    def __init__(self, background_color: tuple, p, world_map: Map):
        self.screen = pygame.display.set_mode(Engine.RESOLUTION)
        self.sz = self.screen.get_size()

        self.map = world_map
        self.background_color = background_color

        self.zoom = 4
        self.round_display = Engine.ROUND_DISPLAY_IG

        # Entities list
        self.player = p
        # todo: getcamera player
        self.camera = None

        self.hud = HUD()

        self.entities = []
        self.entities_to_delete = []

        # Buildings list (Crystals, Distributor, etc...)
        self.builds = []
        self.builds_to_delete = []

        # Items list (On map)
        self.items = []
        self.items_to_delete = []

        # Projectiles list
        self.projectiles = []
        self.projectiles_to_delete = []

        # Extras list (blades, particles, ...)
        self.extras = []
        self.extras_to_delete = []

        # Screen of the map without extras, entities and builds (to speed up the display)
        self.map_image = None

    def display(self, display_cell_border: bool = False, display_player: bool = True, display_hud: bool = True,
                display_target_cell_special_border: bool = False, extra_display: Callable = None):
        self.screen.fill(self.background_color)
        self.display_map(display_cell_border, display_player, display_target_cell_special_border)

        # todo: manage zoom level
        if self.zoom != 1:
            screen_copy = self.screen.copy()
            sz_copy = screen_copy.get_size()

            screen_copy = pygame.transform.scale(screen_copy, (sz_copy[0] * self.zoom, sz_copy[1] * self.zoom))

            self.screen.blit(screen_copy, (-(sz_copy[0] / 2) * (self.zoom - 1), -(sz_copy[1] / 2) * (self.zoom - 1)))

        if display_hud:
            self.hud.display(self, self.screen, self.player)

        if extra_display is not None:
            extra_display(self.screen)

        pygame.display.update()

    def actualise(self):
        # todo: FPS

        self.player.actualise(self, 144, self.map)

        for entity in self.entities:
            entity.actualise(self, 144, self.map)

            if not entity.active:
                self.entities_to_delete.append(entity)

        for item in self.items:
            item.actualise(self, 144, self.map)

            if not item.active:
                self.items_to_delete.append(item)

        for projectile in self.projectiles:
            projectile.actualise(self, 144, self.map)

            if not projectile.active:
                self.projectiles_to_delete.append(projectile)

        for build in self.builds:
            build.actualise(self)

        particle_extra = [p for p in self.extras if isinstance(p, Particle)]

        for particle in particle_extra:
            particle.actualise(self, 144, self.map)

            if not particle.active:
                self.extras_to_delete.append(particle)

        self.delete_elements()

    def display_map(self, display_cell_border: bool = False, display_player: bool = True,
                    display_target_cell_special_border: bool = False):
        t = time.time()

        elements = [self.player]

        for e in self.entities:
            elements.append(e)
        for p in self.projectiles:
            elements.append(p)
        for b in self.builds:
            elements.append(b)
        for extra in self.extras:
            elements.append(extra)
        for item in self.items:
            elements.append(item)

        # We conserve only displayable elements around the player
        elements_to_display = []
        for e in elements:
            dx = abs(e.pos[0] - self.player.pos[0])
            dy = abs(e.pos[1] - self.player.pos[1])

            if dx <= self.round_display[0] and dy <= self.round_display[1]:
                elements_to_display.append(e)

        # We sort all displayable elements to ensure that the display fit for all map elements (Y-sorting)
        elements_to_display.sort(key=lambda element: element.pos[1] + element.height)

        if self.map_image is None:
            surface = pygame.surface.Surface((5000, 5000))
            surface.fill(self.background_color)
            for y in range(self.map.size[1]):
                for x in range(self.map.size[0] - 1, -1, -1):
                    pos = self.absolute_screen_coordinates((x, y))

                    pygame.draw.rect(surface, self.map[(x, y)].color, (pos, (Cell.SIZE, Cell.SIZE)))

                    if isinstance(self.map[(x, y)], Water):
                        if self.map.in_map((x - 1, y)) and not isinstance(self.map[(x - 1, y)], Water):
                            pygame.draw.rect(surface, SHADOW_LIGHT_BLUE, (pos[0], pos[1], Cell.SIZE // 8, Cell.SIZE))
                        if self.map.in_map((x, y - 1)) and not isinstance(self.map[(x, y - 1)], Water):
                            pygame.draw.rect(surface, SHADOW_LIGHT_BLUE, (pos[0], pos[1], Cell.SIZE, Cell.SIZE // 8))

                    if display_cell_border:
                        if self.map[(x, y)].get_wall():
                            pygame.draw.rect(surface, RED, (pos, (Cell.SIZE, Cell.SIZE)), 2)
                        else:
                            pygame.draw.rect(surface, LIGHT_YELLOW, (pos, (Cell.SIZE, Cell.SIZE)), 1)

                        if not self.map[(x, y)].get_walkable():
                            diagonal_pos1 = self.absolute_screen_coordinates((x + 1, y + 1))
                            pos2 = self.absolute_screen_coordinates((x + 1, y))
                            diagonal_pos2 = self.absolute_screen_coordinates((x, y + 1))

                            pygame.draw.line(surface, LIGHT_YELLOW, pos, diagonal_pos1, 2)
                            pygame.draw.line(surface, LIGHT_YELLOW, pos2, diagonal_pos2, 2)

            self.map_image = surface.copy()

        pos = self.screen_coordinates((0, 0))

        self.screen.blit(self.map_image, (pos[0] - self.sz[0] // 2, pos[1] - self.sz[1] // 2))

        if display_target_cell_special_border:
            grid_pos = get_cell_pos(self.map_coordinates(pygame.mouse.get_pos()))
            if self.map.in_map(grid_pos):
                pos = self.screen_coordinates(grid_pos)
                pygame.draw.rect(self.screen, GOLD, (pos[0] + 1, pos[1] + 1, Cell.SIZE, Cell.SIZE), 3)

        for e in elements_to_display:
            if isinstance(e, Player) and not display_player:
                pass
            else:
                e.display(self.screen, self.screen_coordinates)

    def initiate_map(self):
        for y in range(self.map.size[1]):
            for x in range(self.map.size[0]):
                cell = self.map[(x, y)]

                cell.initiate(x, y)

                b = cell.build
                if b is not None:
                    self.builds.append(b)

                for extra in cell.extras:
                    extra.define_absolute_pos(x, y)
                    self.extras.append(extra)

    def initiate_game(self):
        self.zoom = Engine.IN_GAME_ZOOM
        pygame.mouse.set_visible(False)
        self.round_display = Engine.ROUND_DISPLAY_IG

    def initiate_edit_mode(self):
        self.round_display = Engine.ROUND_DISPLAY_EM

    def reset_map_content(self):
        self.entities = []
        self.entities_to_delete = []

        self.builds = []
        self.builds_to_delete = []

        self.projectiles = []
        self.projectiles_to_delete = []

        self.extras = []
        self.extras_to_delete = []

        self.items = []
        self.items_to_delete = []

    def change_map(self, new_map: Map):
        self.reset_map_content()

        self.map = new_map
        self.initiate_map()

    def update_map(self):
        save_entities = self.entities

        self.reset_map_content()
        self.initiate_map()

        self.entities = save_entities
        self.add_item((8, 8), Apple())

        self.map_image = None

    def modif_map(self, pos: tuple, cell: Cell):
        # This method able users to modify a cell in the map in real time (edit mode only)
        self.map[get_cell_pos(pos)] = cell
        self.update_map()

        """        cell = self.map[get_cell_pos(pos)]
        if cell.build is not None:
            self.builds_to_delete.append(cell.build)

        for extra in cell.extras:
            self.extras_to_delete.append(extra)

        self.map[get_cell_pos(pos)] = cell

        self.map[get_cell_pos(pos)].initiate(int(pos[0]), int(pos[1]))
        self.map_image = None"""

    def add_build(self, pos: tuple, build):
        self.map[get_cell_pos(pos)].build = build

        self.update_map()

    def change_zoom(self, offset: int):
        if Engine.MIN_ZOOM <= self.zoom + offset <= Engine.MAX_ZOOM:
            self.zoom += offset

    def screen_map_offset(self) -> tuple[int, int]:
        return self.screen.get_width() // 2, self.screen.get_height() // 2

    def trigonometric_angle_of_cursor(self) -> float:
        # Return an angle in radian between the player and the cursor (for the projectiles mainly)
        player_pos = self.player.pos
        mouse_pos = self.map_coordinates(pygame.mouse.get_pos())
        position = (mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1])
        return math.atan2(position[1], position[0])

    def trigonometric_angle_of_object(self, obj: Entity, direction: Entity):
        obj_pos = obj.pos
        direction_pos = direction.pos

        vector = (direction_pos[0] - obj_pos[0], direction_pos[1] - obj_pos[1])

        return math.atan2(vector[1], vector[0])

    def screen_coordinates(self, pos: tuple):
        base_offset = self.screen_map_offset()
        camera_pos = self.camera.pos

        return (base_offset[0] + (pos[0] - camera_pos[0]) * Cell.SIZE,
                base_offset[1] + (pos[1] - camera_pos[1]) * Cell.SIZE)

    def absolute_screen_coordinates(self, pos: tuple):
        base_offset = self.screen_map_offset()

        return (base_offset[0] + pos[0] * Cell.SIZE,
                base_offset[1] + pos[1] * Cell.SIZE)

    def map_coordinates(self, pos: tuple):
        base_offset = self.screen_map_offset()
        camera_pos = self.camera.pos

        return (((1 / Cell.SIZE) * (pos[0] - base_offset[0]) / self.zoom + camera_pos[0]),
                ((1 / Cell.SIZE) * (pos[1] - base_offset[1]) / self.zoom + camera_pos[1]))

    def map_coordinates_round(self, pos: tuple, round_amount: int = 2):
        map_pos = self.map_coordinates(pos)

        return round(map_pos[0], round_amount), round(map_pos[1], round_amount)

    def add_projectile(self, projectile: Projectile):
        self.projectiles.append(projectile)

    def add_particle(self, particle: Particle):
        self.extras.append(particle)

    def add_item(self, pos: tuple, item: Item):
        self.items.append(Collectibles(pos, item.texture, item, item.rarity))

    def delete_elements(self):
        for entity in self.entities_to_delete:
            self.entities.remove(entity)

        for projectile in self.projectiles_to_delete:
            self.projectiles.remove(projectile)

        for build in self.builds_to_delete:
            self.builds.remove(build)

        for extra in self.extras_to_delete:
            self.extras.remove(extra)

        for item in self.items_to_delete:
            self.items.remove(item)

        self.entities_to_delete = []
        self.projectiles_to_delete = []
        self.builds_to_delete = []
        self.extras_to_delete = []
        self.items_to_delete = []
