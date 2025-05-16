# Bibliothèques
import math
import copy
import time

import pygame

from game.player import *
from game.engine import *
from game.projectile import *
from game.pathfinding import *
from game.build import *
from game.enemy import *
from game.item import *

import sys

# --- #

# Zone de test
M = Map()

M.create(30, 20)

M[(3, 3)].reverse_walkable()
M[(3, 3)].set_color(DARK_GREY)

M[(8, 8)].reverse_walkable()
M[(8, 8)].reverse_wall()
M[(8, 8)].set_color(DARK_GREY)

M[(9, 9)] = Water()
M[(8, 8)] = Sand()
M[(9, 10)] = Water()

M[(15, 15)] = Grass()



# ---------------- #

# Game parameters
MAP_EDITOR = True
DEVELOPER_MODE = True

interaction_key = pygame.K_e

left_key = pygame.K_q
right_key = pygame.K_d
up_key = pygame.K_z
down_key = pygame.K_s

# ---------------- #

# On génère notre moteur de jeu
E = Engine(DARK_GREY, None, M)

E.player = Player()
E.camera = E.player.get_camera()

a = Chest()

E.map[(3, 3)].build = a

# On génère une horloge qui va gérer le taux de rafraichissement du jeu
Clock = pygame.time.Clock()
FPS = 144

# Zone de test 2

E.player.get_inventory().consumable = Apple()

E.add_item((8.5, 8.5), Money_It4())

# ----------------- #

E.initiate_map()


def map_editor(default_size: tuple[int, int] = (0, 0)):
    if default_size == (0, 0):
        print("Size of the map : ")
        width = int(input("\t - WIDTH : "))
        height = int(input("\t - HEIGHT : "))

        ms = width, height
    else:
        ms = default_size

    # In editor Mode, user can go outside the map box
    E.player.in_bound = False
    E.camera.in_bound = False

    # Creation of the new map
    edit_map = Map()
    edit_map.create(ms[0], ms[1])

    # Put the map in the engine
    E.change_map(edit_map)
    E.initiate_edit_mode()

    # Selector definition section
    selector = None
    selector_type = None
    selector_menu_buttons = []

    selector_options = []

    button_pressed = False
    button_on = False

    def active_cells_menu():
        nonlocal selector, selector_type, selector_menu_buttons
        if selector_type != "Cells":
            selector = None
            selector_type = "Cells"

            selector_menu_buttons = []

            for i, cell in enumerate(ALL_CELLS_TYPE):
                selector_menu_buttons.append(CellSelectorButton(1120, 30 + (CellSelectorButton.HEIGHT + 10) * i, f"CS_{i}",
                                                                cell.__name__, cell().color, cell()))
        else:
            selector_type = None

    def active_builds_menu():
        nonlocal selector, selector_type, selector_menu_buttons, selector_options
        if selector_type != "Builds":
            selector = None
            selector_type = "Builds"

            selector_menu_buttons = []
            selector_options = []

            for i, build in enumerate(ALL_BUILDS):
                texture = pygame.transform.scale(build().texture, (30, 30))
                selector_menu_buttons.append(BuildSelectorButton(1100, 30 + (SelectionButton.HEIGHT + 10) * i,
                                                                 f"CS_{i}", build().name, texture, build()))
        else:
            selector_type = None

    def add_selector_options(name: str):
        selector_options.append(BoolButton(options_start_pos[0] + 120 * len(selector_options), options_start_pos[1],
                                           100, 40, name, data_text_style, f"{name[0].upper()}{name[1:]}"))

    # Buttons section management
    buttons = [TextButton(1150, 660, 120, 40, "Play", DefaultStyle(25, GOLD), "Play",
                          True, base_color=GOLD, action=lambda: active_cells_menu()),
                TextButton(640, 660, 100, 40, "Cells_choice_menu", DefaultStyle(25, LIGHT_YELLOW), "Cells",
                          True, base_color=LIGHT_YELLOW, action=lambda: active_cells_menu()),
               TextButton(750, 660, 100, 40, "Builds_choice_menu", DefaultStyle(25, LIGHT_YELLOW), "Builds",
                          True, base_color=LIGHT_YELLOW, action=lambda: active_builds_menu()),
               TextButton(860, 660, 100, 40, "Enemies_choice_menu", DefaultStyle(25, LIGHT_YELLOW), "Enemies",
                          True, base_color=LIGHT_YELLOW),
               TextButton(10, 660, 180, 40, "Save Map", DefaultStyle(25, LIGHT_BLUE2), "Save Map",
                          True, base_color=LIGHT_BLUE2),
               TextButton(10, 600, 180, 40, "Load Map", DefaultStyle(25, PURPLE), "Load Map",
                          True, base_color=PURPLE),
               TextButton(200, 660, 180, 40, "Map Tweaker", DefaultStyle(25, GOLD), "Map Tweaker",
                          True, base_color=GOLD),
               TextZone(390, 660, 150, 40, "Map Name", DefaultStyle(25, WHITE), True, False)
               ]

    # Style section
    data_text_style = DefaultStyle(20, LIGHT_YELLOW, True)

    options_start_pos = (400, 10)
    edit_info_start_pos = (10, 10)

    def display_hud_em(window: pygame.surface):
        info_data = f"MOUSE COORDINATES : {mc} / {E.map_coordinates_round(mc)} "

        info_data_render = data_text_style.render(info_data)
        window.blit(info_data_render, edit_info_start_pos)

        info_data = f"MAP SIZE : {E.map.size} "

        info_data_render = data_text_style.render(info_data)
        window.blit(info_data_render, (edit_info_start_pos[0], edit_info_start_pos[1] + 20))

        if selector is not None:
            info_data = f"SELECTOR : {selector_type}"

            info_data_render = data_text_style.render(info_data)
            window.blit(info_data_render, (edit_info_start_pos[0], edit_info_start_pos[1] + 50))

            if isinstance(selector, Cell):
                pygame.draw.rect(window, selector.color, (edit_info_start_pos[0], edit_info_start_pos[0] + 65, 30, 30))
            if isinstance(selector, Build):
                texture = pygame.transform.scale(selector.texture, (30, 30))
                window.blit(texture, (edit_info_start_pos[0], edit_info_start_pos[0] + 65))

                render_extra_build_info = data_text_style.render(f" (Walkable : {selector.walkable} | Wall : {selector.wall})")
                window.blit(render_extra_build_info, (edit_info_start_pos[0], edit_info_start_pos[1] + 100))

            pygame.draw.rect(window, LIGHT_YELLOW, (edit_info_start_pos[0], edit_info_start_pos[0] + 65, 30, 30), 3)

            selector_name = selector.__class__.__name__
            selector_name_render = data_text_style.render(selector_name)
            window.blit(selector_name_render, (edit_info_start_pos[0] + 35, edit_info_start_pos[1] + 72))

            for option in selector_options:
                option.draw(window)

        for b in buttons:
            b.draw(window)

        if selector_type is not None:
            for b in selector_menu_buttons:
                b.draw(window)

    while True:
        mc = pygame.mouse.get_pos()
        wheel_relative = get_relative_mouse_wheel_value()
        input_actualise()

        if button_on:
            show_target_cell = False
        else:
            show_target_cell = True

        E.display(True, False, False, show_target_cell, display_hud_em)
        E.actualise()

        button_pressed = False
        button_on = False

        for button in buttons:
            button.actualise()

            if button.is_pressed():
                button_pressed = True

            if button.is_on():
                button_on = True

        for button in selector_menu_buttons:
            button.actualise()

            if button.is_on():
                button_on = True

            if button.is_pressed():
                button_pressed = True

                selector_options = []
                selector = button.selection

                if isinstance(selector, Grass):
                    add_selector_options("blades")
                    add_selector_options("strelitzia")
                    add_selector_options("bush")
                    add_selector_options("rock")
                elif isinstance(selector, Sand):
                    add_selector_options("shells")
                    add_selector_options("cactus")
                    add_selector_options("desert_bush")
                    add_selector_options("rock")
                elif isinstance(selector, Stone):
                    add_selector_options("stone")
                    add_selector_options("crystal")
                    add_selector_options("crack")
                    add_selector_options("bone")
                elif isinstance(selector, Water):
                    add_selector_options("lilypad")

        if selector is not None:
            for button in selector_options:
                button.actualise()

                if button.is_on():
                    button_on = True

                if button.is_pressed():
                    button_pressed = True

        if button_pressed:
            input_info["LMB"] = False

        # Editor interface
        if input_info["LMB"]:
            map_coordinates = E.map_coordinates(mc)
            if isinstance(selector, Cell) and E.map.in_map(get_cell_pos(map_coordinates)):
                cell = copy.deepcopy(selector)

                if isinstance(cell, Grass) and selector_options[0].value:
                    cell.generate_blades()
                if isinstance(cell, Grass) and selector_options[1].value:
                    cell.generate_flowers()
                if isinstance(cell, Grass) and selector_options[2].value:
                    cell.generates_bush()
                if isinstance(cell, Grass) and selector_options[3].value:
                    cell.generates_rocks()

                if isinstance(cell, Sand) and selector_options[0].value:
                    cell.generates_shells()
                if isinstance(cell, Sand) and selector_options[1].value:
                    cell.generates_cactus()
                if isinstance(cell, Sand) and selector_options[2].value:
                    cell.generates_desert_bush()
                if isinstance(cell, Sand) and selector_options[3].value:
                    cell.generates_rocks()

                if isinstance(cell, Stone) and selector_options[0].value:
                    cell.generates_rocks()
                if isinstance(cell, Stone) and selector_options[1].value:
                    cell.generates_crystals()
                if isinstance(cell, Stone) and selector_options[2].value:
                    cell.generates_cracks()
                if isinstance(cell, Stone) and selector_options[3].value:
                    cell.generates_bones()

                if isinstance(cell, Water) and selector_options[0].value:
                    cell.generates_lilypad()

                E.modif_map(map_coordinates, cell)
            if isinstance(selector, Build) and E.map.in_map(get_cell_pos(map_coordinates)):
                build = copy.copy(selector)

                E.add_build(map_coordinates, build)

        if input_info.get(pygame.K_f):
            E.map.save_map("saves/map.txt")

        # Camera movement
        # Vector
        camera_v = [0., 0.]
        if input_info.get(left_key):
            camera_v[0] -= 1.
        if input_info.get(right_key):
            camera_v[0] += 1.
        if input_info.get(down_key):
            camera_v[1] += 1.
        if input_info.get(up_key):
            camera_v[1] -= 1.

        E.player.move(tuple(camera_v), FPS, M)

        if input_info.get(interaction_key):
            return

        if wheel_relative != 0:
            if wheel_relative < 0:
                E.change_zoom(-1)
            else:
                E.change_zoom(1)

        for event in pygame.event.get():
            check_input(event)

            if event.type == pygame.QUIT:
                sys.exit()


def game():
    E.initiate_game()
    E.entities.append(Mosquito((1.5, 1.5), E.player))
    while True:
        input_actualise()
        mouse_coordinates = pygame.mouse.get_pos()

        frame_rate = Clock.get_fps()
        # print(f"FPS: {frame_rate}")
        # print(len(E.projectiles))
        # print(M.get_neighbour_walkable(int(E.player.pos[0]), int(E.player.pos[1])))

        E.display()

        # Developer Mode extra functions
        if DEVELOPER_MODE:
            if input_info.get(pygame.K_F1):
                E.player.get_inventory().add_money(1, True)
            if input_info.get(pygame.K_F2):
                E.player.get_inventory().add_words(1, True)

        # Vecteur déplacement du joueur
        player_v = [0., 0.]
        if input_info.get(left_key):
            player_v[0] -= 1.
        if input_info.get(right_key):
            player_v[0] += 1.
        if input_info.get(down_key):
            player_v[1] += 1.
        if input_info.get(up_key):
            player_v[1] -= 1.

        # todo: test
        if input_info.get(pygame.K_f):
            E.player.remove_health(1)
            input_info[pygame.K_f] = False

        # Consumable Item
        if input_info.get(pygame.K_e):
            consumable_item = E.player.get_inventory().consumable
            if consumable_item is not None and time.time() - E.player.last_item_use >= Player.GCD:
                E.player.get_inventory().consumable.use(E.player)
                E.player.last_item_use = time.time()

                if consumable_item.charges <= 0:
                    E.player.get_inventory().consumable = None

        # Main attack
        if input_info.get("LMB") and E.player.can_attack():
            theta = E.trigonometric_angle_of_cursor()
            E.add_projectile(Player_Projectile(E.player.pos, 20, (math.cos(theta), math.sin(theta)), E.player.get_damage()))

            E.player.last_attack_time = time.time()

        # Loot Interaction
        if input_info.get("RMB"):
            for collectible in E.items:
                if collectible.collide_mouse(E.map_coordinates(mouse_coordinates)):
                    E.player.get_inventory().loot(collectible.item)
                    collectible.active = False
                    break

        # Move the player
        E.player.move(tuple(player_v), FPS, M)

        player_pos = E.player.pos
        for build in E.builds:
            if build.interaction is not None:
                b_pos = (build.pos[0] + 0.5, build.pos[1] + 0.5)
                d = distance2(player_pos[0], player_pos[1], b_pos[0], b_pos[1])

                if d <= Engine.INTERACTION_DISTANCE and input_info.get(interaction_key):
                    build.interact(E)
                    reset_key(interaction_key)

        E.actualise()

        for event in pygame.event.get():
            check_input(event)

            if event.type == pygame.QUIT:
                sys.exit()  # todo: Shutdown temporaire

        Clock.tick(FPS)


#    (25, 15)
if MAP_EDITOR:
    map_editor((25, 15))
game()
