import pygame.draw

from tools.button import *


class TextZone(Button):
    def __init__(self, x: float, y: float, width: int, height: int, name: str, style: TextStyle,
                 display_continuity: bool = True, simple_zone: bool = True, hide_entry: bool = False):

        self.writing = False
        self.entry = ""

        self.hide_entry = hide_entry

        super().__init__(x, y, width, height, name, self.inverse_writing)

        self.style = style

        self.display_continuity = display_continuity

        self.valid_button = TextButton(x + width + 3, y, height, height, "Valid_" + name, BaseStyle(70, BLACK), "",
                                       True, self.validation)
        self.valid = False

        self.simple_zone = simple_zone

    def inverse_writing(self):
        self.writing = not self.writing

    def len_without_space(self):  # todo : general function
        result = 0
        for letter in self.entry:
            if letter != " ":
                result += 1

        return result

    def validation(self):
        if self.len_without_space() >= 3:
            self.valid = True
        else:
            pass
            # todo: Error Message

    def get_max_in_render(self) -> int:
        for i in range(len(self.entry), -1, -1):
            if self.style.render(self.entry[0: i]).get_width() < self.rect.width - 5:
                return i

        return 0

    def get_min_in_render(self) -> int:
        for i in range(0, len(self.entry)):
            if self.style.render(self.entry[i:]).get_width() < self.rect.width - 5:
                return i

        return 0

    def get_render_style_height(self):
        return self.style.render("A").get_height()

    def draw(self, window: pygame.Surface):
        super().draw(window)

        if not self.simple_zone:
            self.valid_button.draw(window)

        if not self.hide_entry:
            text = self.entry
        else:
            text = "*" * len(self.entry)

        if self.display_continuity:
            render = self.style.render(text[self.get_min_in_render():])
        else:
            render = self.style.render(text[0: self.get_max_in_render()])
        size = render.get_size()

        start_x = self.rect.x + 5
        start_y = self.rect.y + (abs(self.rect.height - size[1])) // 2

        window.blit(render, (start_x, start_y))

        if self.writing:
            if int(time.time()) % 2 == 0:
                pygame.draw.rect(window, self.style.c, (start_x + render.get_width() + 5, start_y, 3,
                                                        self.get_render_style_height()))

    def actualise(self):
        if self.writing:
            for key in input_stack:
                if input_is_letters_or_numbers(key) and input_repetition_check(key):
                    if input_is_letters(key):
                        if capslock():
                            self.entry += key_input[key]
                        else:
                            self.entry += key_input[key].lower()
                    else:
                        self.entry += key_input[key]
                if key == pygame.K_BACKSPACE and input_repetition_check(key):
                    self.entry = self.entry[0: -1]

        self.valid_button.actualise()

        super().actualise()


class ConnexionIdZone:
    def __init__(self, x: float, y: float, width: int, height: int, name: str, style: TextStyle, offset: int,
                 valid_text: str, valid_action, display_continuity=True):

        self.id_zone = TextZone(x, y, width, height, name + "_id", style, display_continuity)
        self.password_zone = TextZone(x, y + height + offset, width, height, name + "_password", style,
                                      display_continuity, hide_entry=True)

        self.valid_button = TextButton(x, y + 2 * offset + 2 * height, width, height, name, style, valid_text, True,
                                       valid_action)

    def actualise(self):
        self.id_zone.actualise()

        if self.id_zone.writing and self.password_zone.writing:
            self.password_zone.inverse_writing()

        self.password_zone.actualise()

        if self.id_zone.writing and self.password_zone.writing:
            self.id_zone.inverse_writing()

        self.valid_button.actualise()

    def draw(self, window: pygame.Surface):
        self.id_zone.draw(window)
        self.password_zone.draw(window)
        self.valid_button.draw(window)
