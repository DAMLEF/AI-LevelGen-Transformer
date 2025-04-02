from tools.basics import *


class ScrollBar:
    def __init__(self, items: list, side: bool, mi: int, ma: int, power: int):
        self.items = items

        self.extreme_pos = (mi, ma)

        self.side = side    # True: y-axis, False: x-axis

        self.power = power
        self.ref = input_info["MW"] * power

    def actualise(self):
        for item in self.items:
            if self.side:
                item.rect.y = item.y + (input_info["MW"]*self.power - self.ref)
            else:
                item.rect.x = item.x + (input_info["MW"]*self.power - self.ref)
