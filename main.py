# Bibliothèques
import pygame

from tools.all import *
from game.engine import *
from game.map import *

import sys

# --- #

# Zone de test
M = Map()

M.create(30, 20)

print(M)

# ---------------- #

# On génère notre moteur de jeu
E = Engine(DARK_GREY, 0, M)

# On génère une horloge qui va gérer le taux de rafraichissement du jeu
Clock = pygame.time.Clock()
FPS = 144


while True:
    input_actualise()

    frame_rate = Clock.get_fps()
    print(f"FPS: {frame_rate}")

    E.display()

    for event in pygame.event.get():
        check_input(event)

        if event.type == pygame.QUIT:
            sys.exit()      # todo: Shutdown temporaire

    Clock.tick(FPS)



