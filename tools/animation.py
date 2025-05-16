import time

import pygame

_ = pygame.display.set_mode((1, 1))


class Animation:
    def __init__(self, images: list[pygame.Surface], frame_duration: float):
        self.images = images
        self.frame_duration = frame_duration

        self.last_time = time.time()
        self.state = 0

    def reset_state(self):
        self.state = 0

    def current_state(self):
        return self.state % len(self.images)

    def get_texture(self):
        return self.images[self.current_state()]

    def actualise(self):
        t = time.time()

        if t - self.last_time >= self.frame_duration:
            self.state += 1
            self.last_time = t
