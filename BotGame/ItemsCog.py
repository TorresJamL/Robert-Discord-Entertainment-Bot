import asyncio
import discord
import random
from discord.ext import commands
from enum import Enum

class Item:
    def __init__(self, name, durability: int = 1) -> None:
        self.name = name
        self.durability = durability
        self.state = "Working"

    def lose_durability(self):
        self.durability -= 1
        if self.durability <= 0:
            self.state = "broken"
            return True  # Indicate that the item should be deleted
        elif self.durability <= 2:
            self.state = "Almost broken"
        return False  # Indicate that the item is still usable

    def get_item_stats(self):
        return f"Item: {self.name}\n Durability: {self.durability}"

    def __str__(self):
        return Item.get_item_stats(self)

class Weapon(Item):
    def __init__(self, name, damage: int = 1, durability: int = 1) -> None:
        super().__init__(name, durability)
        self.damage = damage

    def __str__(self):
        return f"{super().__str__()}\n Damage: {self.damage}"

class Potion(Item):
    def __init__(self, name, effect, durability: int = 1) -> None:
        super().__init__(name, durability)
        self.effect = effect
        
    def __str__(self):
        return f"{super().__str__()}\n Effect: {self.effect}"

class Armor(Item):
    def __init__(self, name, defense, durability: int = 5) -> None:
        super().__init__(name, durability)
        self.defense = defense

    def __str__(self):
        return f"{super().__str__()}\n Defense: {self.defense}"