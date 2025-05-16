from game.entity import *


class Projectile(Entity):
    def __init__(self, pos, speed, color, vector, power):
        super().__init__(pos, speed, color)

        self.vector = vector

        self.in_bound = False   # Les projectiles peuvent sortir des limites du terrain
        # (traverser les cases pas accessibles, mais pas les murs)

        self.height = 1

        self.power = power

        self.marked = []        # List contains all entities already damaged by the projectile (Only 1 touch)

    def actualise(self, engine, frame_rate, world):
        super().actualise(engine, frame_rate, world)

        self.move(self.vector, frame_rate, world)

        grid_pos = (int(self.pos[0]), int(self.pos[1]))
        if world.in_map(grid_pos, self.pos):
            if world[grid_pos].get_wall():
                self.active = False
        else:
            self.active = False

    def get_map_trajectory(self):
        return self.last_pos, self.pos

    def get_absolute_trajectory(self, engine):
        trajectory = self.get_map_trajectory()

        return engine.screen_coordinates(trajectory[0]), engine.screen_coordinates(trajectory[1])


class Player_Projectile(Projectile):
    def __init__(self, pos, speed, vector, power):
        super().__init__(pos, speed, BLUE, vector, power)

    def actualise(self, engine, frame_rate, world):
        super().actualise(engine, frame_rate, world)

        for entity in engine.entities:
            if isinstance(entity, Living_Entity) and entity.bad:
                rect = entity.get_pygame_rect(engine)

                trajectory = self.get_absolute_trajectory(engine)

                print(rect.clipline(trajectory))

                if rect.clipline(trajectory):
                    self.marked.append(entity)
                    entity.remove_health(self.power)

                    self.active = not self.active


class Enemy_Projectile(Projectile):
    def __init__(self, pos, speed, vector, power):
        super().__init__(pos, speed, LIGHT_RED, vector, power)

    def actualise(self, engine, frame_rate, world):
        super().actualise(engine, frame_rate, world)

        if not self.marked:
            rect = engine.player.get_pygame_rect(engine.screen)

            line_start = engine.screen_coordinates(self.pos)
            line_end = engine.screen_coordinates(self.last_pos)


            if rect.clipline(line_start, line_end):
                # Player is touched by the projectile
                engine.player.remove_health(self.power)
                self.active = not self.active

                self.marked.append(engine.player)


