import random
import time

import pygame


# todo: moves away ?
class Modifier_Display:

    # This class brings a standard content to help understand the player what an item does
    def __init__(self, modifier_type: str, amount: str):
        self.md_type = modifier_type
        self.amount = amount


class Health_MD(Modifier_Display):
    def __init__(self, amount: str):
        md_type = "Health"
        super().__init__(md_type, amount)


class Money_MD(Modifier_Display):
    def __init__(self, amount: str):
        md_type = "Money"
        super().__init__(md_type, amount)


class Item:
    GCD = 0.5  # Global cooldown to every item

    def __init__(self, name: str, description: str, item_type: str, rarity: int, texture: pygame.Surface):
        self.name = name
        self.description = description
        self.item_type = item_type

        self.rarity = rarity

        self.texture = texture

        self.cooldown = Item.GCD
        self.last_use = time.time() - self.cooldown - 1

        self.modifiers = []

    def use(self, player):
        pass


class Tool(Item):
    def __init__(self, name: str, description: str, rarity: int, texture: pygame.Surface):
        item_type = "TOOL"
        super().__init__(name, description, item_type, rarity, texture)


class Money_Item(Item):
    LUMUS_TEXTURE = pygame.image.load("assets/items/money.png").convert_alpha()

    def __init__(self, rarity: int, amount: int):
        item_type = "MONEY"

        name = "Money"
        description = ("Lumus are a foundational cryptocurrency — the only reliable currency: untraceable, resistant "
                       "to magnetic fields, and mysteriously accepted by all merchant AIs.")

        super().__init__(name, description, item_type, rarity, Money_Item.LUMUS_TEXTURE)

        self.amount = amount

        self.modifiers.append(Money_MD(f"+{self.amount}"))


class Mask(Item):
    def __init__(self, name: str, description: str, rarity: int, texture: pygame.Surface):
        item_type = "MASK"
        super().__init__(name, description, item_type, rarity, texture)


class Consumable(Item):
    def __init__(self, name: str, description: str, charges: int, rarity: int, texture: pygame.Surface):
        item_type = "CONSUMABLE"
        super().__init__(name, description, item_type, rarity, texture)

        self.charges = charges

    def use(self, player):
        self.charges -= 1


class Apple(Consumable):
    TEXTURE = pygame.image.load("assets/items/Apple.png").convert_alpha()

    def __init__(self):
        name = "Apple"
        description = "Restores 10% of the player's maximum health"
        charges = 15
        rarity = 1

        texture = Apple.TEXTURE
        super().__init__(name, description, charges, rarity, texture)

        self.modifiers.append(Health_MD("+10%"))

    def use(self, player):
        super().use(player)
        player.give_health(player.max_health / 10)


class Money_It1(Money_Item):
    M_RANGE = [1, 6]

    def __init__(self):
        rarity = 1
        money = random.randint(Money_It1.M_RANGE[0], Money_It1.M_RANGE[1])

        super().__init__(rarity, money)


class Money_It2(Money_Item):
    M_RANGE = [5, 10]

    def __init__(self):
        rarity = 2
        money = random.randint(Money_It2.M_RANGE[0], Money_It2.M_RANGE[1])

        super().__init__(rarity, money)


class Money_It3(Money_Item):
    M_RANGE = [12, 15]

    def __init__(self):
        rarity = 3
        money = random.randint(Money_It3.M_RANGE[0], Money_It3.M_RANGE[1])

        super().__init__(rarity, money)


class Money_It4(Money_Item):
    M_RANGE = [20, 25]

    def __init__(self):
        rarity = 4
        money = random.randint(Money_It4.M_RANGE[0], Money_It4.M_RANGE[1])

        super().__init__(rarity, money)



ALL_CONSUMABLES = [Apple]
ALL_TOOLS = []
