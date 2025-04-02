import pygame
import time

from tools.other import *

input_info = {"M_POS": (0, 0), "LMB": False, "MW": 0}
input_stack = []
input_last_time = {}
input_check = {}


def input_actualise():
    input_info["M_POS"] = pygame.mouse.get_pos()


INPUT_DELAY = 0.5
REPETITION_RATE = 15      # Hz
def input_repetition_check(key: int) -> bool:
    state = input_check.get(key)
    if state is None or state[0] is False:
        input_check[key] = (True, 1)
        return True
    else:
        if time.time() - input_last_time[key] - INPUT_DELAY - state[1] * (1/REPETITION_RATE) > 0:
            input_check[key] = (True, state[1] + 1)
            return True
        else:
            return False


# Function in event main loop
def check_input(py_event: pygame.event) -> None:  # For each key pressed, we turn a key in a dict
    # The value of the key is in index and a boolean who indicate if the key is pressed or not
    global input_info

    if py_event.type == pygame.KEYDOWN:
        input_info[py_event.key] = True
        input_last_time[py_event.key] = time.time()
        input_stack.append(py_event.key)
        input_check[py_event.key] = (False, 0)
    elif py_event.type == pygame.KEYUP:
        input_info[py_event.key] = False
        input_stack.remove(py_event.key)
    elif py_event.type == pygame.MOUSEBUTTONDOWN:
        if py_event.button == 1:
            input_info["LMB"] = True
        elif py_event.button == 2:
            input_info["MWB"] = True
        if py_event.button == 3:
            input_info["RMB"] = True
    elif py_event.type == pygame.MOUSEBUTTONUP:
        if py_event.button == 1:
            input_info["LMB"] = False
        elif py_event.button == 2:
            input_info["MWB"] = False
        elif py_event.button == 3:
            input_info["RMB"] = False
    elif py_event.type == pygame.MOUSEWHEEL:
        input_info["MW"] += py_event.y

def input_is_letters_or_numbers(key: int):
    if key_input.get(key) is not None:
        return True
    return False


def input_is_letters(key: int):
    if letters_key.get(key_input[key]) is not None:
        return True
    return False


def input_is_numbers(key: int):
    if numbers_key.get(key_input[key]) is not None:
        return True
    return False


def capslock() -> bool:
    return bool(pygame.key.get_mods() & pygame.KMOD_CAPS)


key_dict = {"space": pygame.K_SPACE, "esc": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
            "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "return": pygame.K_RETURN,
            "backspace": pygame.K_BACKSPACE,
            "a": pygame.K_a,
            "b": pygame.K_b,
            "c": pygame.K_c,
            "d": pygame.K_d,
            "e": pygame.K_e,
            "f": pygame.K_f,
            "g": pygame.K_g,
            "h": pygame.K_h,
            "i": pygame.K_i,
            "j": pygame.K_j,
            "k": pygame.K_k,
            "l": pygame.K_l,
            "m": pygame.K_m,
            "n": pygame.K_n,
            "o": pygame.K_o,
            "p": pygame.K_p,
            "q": pygame.K_q,
            "r": pygame.K_r,
            "s": pygame.K_s,
            "t": pygame.K_t,
            "u": pygame.K_u,
            "v": pygame.K_v,
            "w": pygame.K_w,
            "x": pygame.K_x,
            "y": pygame.K_y,
            "z": pygame.K_z,
            "1": pygame.K_1,
            "2": pygame.K_2,
            "3": pygame.K_3,
            "4": pygame.K_4,
            "5": pygame.K_5,
            "6": pygame.K_6,
            "7": pygame.K_7,
            "8": pygame.K_8,
            "9": pygame.K_9,
            "0": pygame.K_0}

letters_key = {"A": pygame.K_a,
               "B": pygame.K_b,
               "C": pygame.K_c,
               "D": pygame.K_d,
               "E": pygame.K_e,
               "F": pygame.K_f,
               "G": pygame.K_g,
               "H": pygame.K_h,
               "I": pygame.K_i,
               "J": pygame.K_j,
               "K": pygame.K_k,
               "L": pygame.K_l,
               "M": pygame.K_m,
               "N": pygame.K_n,
               "O": pygame.K_o,
               "P": pygame.K_p,
               "Q": pygame.K_q,
               "R": pygame.K_r,
               "S": pygame.K_s,
               "T": pygame.K_t,
               "U": pygame.K_u,
               "V": pygame.K_v,
               "W": pygame.K_w,
               "X": pygame.K_x,
               "Y": pygame.K_y,
               "Z": pygame.K_z}

numbers_key = {"1": pygame.K_1,
               "2": pygame.K_2,
               "3": pygame.K_3,
               "4": pygame.K_4,
               "5": pygame.K_5,
               "6": pygame.K_6,
               "7": pygame.K_7,
               "8": pygame.K_8,
               "9": pygame.K_9,
               "0": pygame.K_0}

letters_and_numbers_key = dict_add(letters_key, numbers_key)

key_input = {pygame.K_SPACE: " ",
             pygame.K_a: "A",
             pygame.K_b: "B",
             pygame.K_c: "C",
             pygame.K_d: "D",
             pygame.K_e: "E",
             pygame.K_f: "F",
             pygame.K_g: "G",
             pygame.K_h: "H",
             pygame.K_i: "I",
             pygame.K_j: "J",
             pygame.K_k: "K",
             pygame.K_l: "L",
             pygame.K_m: "M",
             pygame.K_n: "N",
             pygame.K_o: "O",
             pygame.K_p: "P",
             pygame.K_q: "Q",
             pygame.K_r: "R",
             pygame.K_s: "S",
             pygame.K_t: "T",
             pygame.K_u: "U",
             pygame.K_v: "V",
             pygame.K_w: "W",
             pygame.K_x: "X",
             pygame.K_y: "Y",
             pygame.K_z: "Z",
             pygame.K_1: "1",
             pygame.K_2: "2",
             pygame.K_3: "3",
             pygame.K_4: "4",
             pygame.K_5: "5",
             pygame.K_6: "6",
             pygame.K_7: "7",
             pygame.K_8: "8",
             pygame.K_9: "9",
             pygame.K_0: "10"}
