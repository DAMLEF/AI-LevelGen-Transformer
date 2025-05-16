from game.item import *

class Inventory:
    START_MAX_MONEY = 100
    START_MAX_WORDS = 15

    def __init__(self):
        self.money = 0
        self.max_money = Inventory.START_MAX_MONEY

        self.words = 0
        self.max_words = Inventory.START_MAX_WORDS

        self.tools = []
        self.consumable = None

        self.masks = []

    def loot(self, item: Item):
        if isinstance(item, Tool):
            pass
        elif isinstance(item, Consumable):
            self.consumable = item
        elif isinstance(item, Money_Item):
            self.add_money(item.amount)
        elif isinstance(item, Mask):
            # todo: gare au doublon avec les masques
            self.masks.append(item)

    def add_money(self, amount: int, allow_cheat: bool = False):
        self.money += amount

        if self.money >= self.max_money and not allow_cheat:
            self.money = self.max_money

    def remove_money(self, amount: int, allow_cheat: bool = False):
        self.money -= amount

    def enough_money(self, amount):
        return self.money >= amount

    def add_words(self, amount: int, allow_cheat: bool = False):
        self.words += amount

        if self.words >= self.max_words and not allow_cheat:
            self.words = self.max_words

    def remove_words(self, amount: int, allow_cheat: bool = False):
        self.words -= amount

    def enough_words(self, amount):
        return self.words >= amount





