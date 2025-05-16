import time

import pygame

from game.player import *
from tools.all import *


def adapted_position(origin_position: int, sz: int, relative: int = 720):
    return origin_position * (sz / relative)


def cut_text_words(texte, mots_par_ligne=8):
    words = texte.split()
    lines = []
    for i in range(0, len(words), mots_par_ligne):
        line = ' '.join(words[i:i + mots_par_ligne])
        lines.append(line)
    return lines


class HUD:
    cursor_img = pygame.image.load("assets/other/cursor.png").convert_alpha()

    lumus_logo = pygame.image.load("assets/hud/lumus_logo.png").convert_alpha()
    word_logo = pygame.image.load("assets/hud/word_logo.png").convert_alpha()

    heart_item_modifier = pygame.image.load("assets/hud/heart_item_modifier.png").convert_alpha()
    money_item_modifier = pygame.image.load("assets/hud/lumus_logo.png").convert_alpha()

    hud_font = "assets/font/text.ttf"

    inventory_info_ts = TextStyle(hud_font, 22, BLACK)
    inventory_info_max_ts = TextStyle(hud_font, 22, GREEN)

    key_text = TextStyle(hud_font, 25, LIGHT_YELLOW, True)
    key_text_add = TextStyle(hud_font, 18, LIGHT_YELLOW, True)

    consumables_ts = TextStyle(hud_font, 20, WHITE, True)

    item_display_ts_0 = TextStyle(hud_font, 20, WHITE, True)
    item_display_ts_1 = TextStyle(hud_font, 20, GREEN2, True)
    item_display_ts_2 = TextStyle(hud_font, 20, BLUE, True)
    item_display_ts_3 = TextStyle(hud_font, 20, PURPLE, True)
    item_display_ts_4 = TextStyle(hud_font, 20, RED, True)

    item_display_ts_description = TextStyle(hud_font, 18, YELLOW, False)
    item_display_ts_modifier = TextStyle(hud_font, 18, WHITE, False)

    def __init__(self):
        pass

    def display(self, engine, window: pygame.Surface, player: Player):
        sz = window.get_size()
        t = time.time()
        mc = pygame.mouse.get_pos()

        # Health bar
        HEALTH_BAR_HEIGHT = 100
        if player.health > 0:
            health_state_height = HEALTH_BAR_HEIGHT * (player.health / player.max_health)
            pygame.draw.rect(window, LIGHT_RED, (65, adapted_position(580, sz[1]) +
                                                 (HEALTH_BAR_HEIGHT - health_state_height), 30, health_state_height))
        pygame.draw.rect(window, WHITE, (65, adapted_position(580, sz[1]), 30, HEALTH_BAR_HEIGHT), 4)

        ITEM_SQUARE_SIZE = 70
        # Tool item
        pygame.draw.rect(window, LIGHT_GREY, (115, adapted_position(610, sz[1]), ITEM_SQUARE_SIZE, ITEM_SQUARE_SIZE))
        pygame.draw.rect(window, WHITE, (115, adapted_position(610, sz[1]), ITEM_SQUARE_SIZE, ITEM_SQUARE_SIZE), 4)

        # Consumables item
        consumable_item = player.get_inventory().consumable

        pygame.draw.rect(window, LIGHT_GREY, (115 + ITEM_SQUARE_SIZE + 20,
                                              adapted_position(610, sz[1]), ITEM_SQUARE_SIZE, ITEM_SQUARE_SIZE))
        pygame.draw.rect(window, WHITE, (115 + ITEM_SQUARE_SIZE + 20,
                                         adapted_position(610, sz[1]), ITEM_SQUARE_SIZE, ITEM_SQUARE_SIZE), 4)

        if consumable_item is not None:
            item_image = consumable_item.texture
            it_im_sz = item_image.get_size()

            window.blit(item_image, (115 + ITEM_SQUARE_SIZE + 20 + (ITEM_SQUARE_SIZE - it_im_sz[0]) / 2,
                                     adapted_position(610, sz[1]) + + (ITEM_SQUARE_SIZE - it_im_sz[1]) / 2))

            render_charges_ic = HUD.consumables_ts.render(str(consumable_item.charges))
            window.blit(render_charges_ic, (115 + ITEM_SQUARE_SIZE + 20 + 8,
                                            adapted_position(610, sz[1]) + 8))

            render_ic_name = HUD.consumables_ts.render(str(consumable_item.name))
            it_name_sz = render_ic_name.get_size()
            window.blit(render_ic_name, (115 + ITEM_SQUARE_SIZE + 20 + (ITEM_SQUARE_SIZE - it_name_sz[0]) / 2,
                                         adapted_position(610, sz[1]) + ITEM_SQUARE_SIZE * 0.75))

            if t - player.last_item_use <= Player.GCD:
                height = (1 - (t - player.last_item_use) / Player.GCD) * ITEM_SQUARE_SIZE
                cooldown_displayer = pygame.surface.Surface((ITEM_SQUARE_SIZE, height), pygame.SRCALPHA)
                cooldown_displayer.fill(GOLD)
                cooldown_displayer.set_alpha(128)

                window.blit(cooldown_displayer, (115 + ITEM_SQUARE_SIZE + 20,
                                                 adapted_position(610, sz[1]) + (ITEM_SQUARE_SIZE - height)))

        # Player inventory (Money, words, ...)

        # Money
        money = player.get_inventory().money
        if money < player.get_inventory().max_money:
            money_render = HUD.inventory_info_ts.render(str(money))
        else:
            money_render = HUD.inventory_info_max_ts.render(str(money))
        window.blit(HUD.lumus_logo, (65, adapted_position(530, sz[1])))

        mr_sz = money_render.get_size()
        pygame.draw.rect(window, WHITE, (89, adapted_position(530, sz[1]), mr_sz[0] + 2, 20))
        window.blit(money_render, (90, adapted_position(534, sz[1])))

        # Words
        words = player.get_inventory().words
        if words < player.get_inventory().max_words:
            words_render = HUD.inventory_info_ts.render(str(words))
        else:
            words_render = HUD.inventory_info_max_ts.render(str(words))
        window.blit(HUD.word_logo, (65, adapted_position(500, sz[1])))

        wd_sz = words_render.get_size()
        pygame.draw.rect(window, WHITE, (89, adapted_position(500, sz[1]), wd_sz[0] + 2, 20))
        window.blit(words_render, (90, adapted_position(504, sz[1])))

        # Build Interaction interface
        p_pos = player.pos

        build_text_style = TextStyle(HUD.hud_font, 20, LIGHT_YELLOW, True)

        for build in engine.builds:

            # Interaction build interface
            if (build.interaction is not None and
                    distance2(p_pos[0], p_pos[1], build.pos[0] + 0.5, build.pos[1] + 0.5) < build.interaction_range):
                pos = engine.screen_coordinates((player.pos[0] + 1, player.pos[1] - 1))
                pygame.draw.rect(window, LIGHT_YELLOW, (pos[0], pos[1], 4, 50))

                pygame.draw.rect(window, LIGHT_YELLOW, (pos[0] + 10, pos[1] - 8, 15, 15), 2)
                window.blit(build.small_texture, (pos[0] + 10, pos[1] - 8))

                window.blit(build_text_style.render(build.__class__.__name__.upper()), (pos[0] + 28, pos[1] - 8))

                input_section_pos = (pos[0] + 10, pos[1] + 15)

                self.display_key_input(window, input_section_pos, "E", "USE")

        # Item on mouse displayer info
        item_to_displayer = None

        if item_to_displayer is None:
            for collectible in engine.items:
                if collectible.collide_mouse(engine.map_coordinates(mc)):
                    item_to_displayer = collectible.item
                    break

        if item_to_displayer is not None:
            start_item_display_pos = (mc[0] + 25, mc[1])
            pos_id = start_item_display_pos

            if item_to_displayer.rarity == 0:
                item_name_render = HUD.item_display_ts_0.render(item_to_displayer.name)
            elif item_to_displayer.rarity == 1:
                item_name_render = HUD.item_display_ts_1.render(item_to_displayer.name)
            elif item_to_displayer.rarity == 2:
                item_name_render = HUD.item_display_ts_2.render(item_to_displayer.name)
            elif item_to_displayer.rarity == 3:
                item_name_render = HUD.item_display_ts_3.render(item_to_displayer.name)
            elif item_to_displayer.rarity == 4:
                item_name_render = HUD.item_display_ts_4.render(item_to_displayer.name)

            description = item_to_displayer.description
            description_cut = cut_text_words(description)
            description_renders = []

            for line in description_cut:
                description_renders.append(HUD.item_display_ts_description.render(line))

            modifiers = item_to_displayer.modifiers
            modifiers_renders = []
            for modifier in modifiers:
                modifiers_renders.append(HUD.item_display_ts_modifier.render(modifier.amount))

            total_height = 5 + 40 + len(description_renders) * 20 + 5 + len(modifiers_renders) * 25

            all_lines = [description_renders[i].get_size()[0] for i in range(len(description_renders))]
            all_lines.append(item_name_render.get_size()[0])
            total_width = 30 + max(all_lines)

            if pos_id[0] + total_width >= sz[0]:
                pos_id = (pos_id[0] - (pos_id[0] + total_width - sz[0]), pos_id[1])

            if pos_id[1] + total_height >= sz[1]:
                pos_id = (pos_id[0], pos_id[1] - (pos_id[1] + total_height - sz[1]))

            # Item Displayer square
            pygame.draw.rect(window, DARK_GREY, (pos_id[0], pos_id[1], total_width, total_height), 0, 5, 5, 5, 5)
            pygame.draw.rect(window, LIGHT_RED2, (pos_id[0] + 5, pos_id[1] + 5, total_width - 10, total_height - 10), 4, 5, 5, 5, 5)

            window.blit(item_name_render, (pos_id[0] + 15, pos_id[1] + 15))
            for i, render in enumerate(description_renders):
                window.blit(render, (pos_id[0] + 15, pos_id[1] + 40 + i * 20))

            for j, render in enumerate(modifiers_renders):
                image = HUD.heart_item_modifier
                if modifiers[j].md_type == "Health":
                    image = HUD.heart_item_modifier
                elif modifiers[j].md_type == "Money":
                    image = HUD.money_item_modifier
                window.blit(image, (pos_id[0] + 15, pos_id[1] + 40 + j * 25 + len(description_renders) * 20 - 2))
                window.blit(render, (pos_id[0] + 36, pos_id[1] + 40 + j * 25 + len(description_renders) * 20))

        window.blit(HUD.cursor_img, mc)

    def display_key_input(self, window: pygame.Surface, pos: tuple, key: str, text_add: str = ""):
        SQUARE_SIZE = 20

        pygame.draw.rect(window, LIGHT_GREY, (pos[0], pos[1], SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(window, LIGHT_YELLOW, (pos[0], pos[1], SQUARE_SIZE, SQUARE_SIZE), 1)

        key_text_render = HUD.key_text.render(key)
        key_render_size = key_text_render.get_size()
        window.blit(key_text_render, (pos[0] + (SQUARE_SIZE - key_render_size[0]) / 2,
                                      pos[1] + (SQUARE_SIZE - key_render_size[1]) / 2,))

        if text_add != "":
            text_add_render = HUD.key_text_add.render(text_add)
            window.blit(text_add_render,
                        (pos[0] + SQUARE_SIZE + 2, pos[1] + (SQUARE_SIZE - text_add_render.get_size()[1]) / 2))

