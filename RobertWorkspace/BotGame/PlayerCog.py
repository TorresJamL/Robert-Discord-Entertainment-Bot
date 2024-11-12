import asyncio
import discord
import random

from ItemsCog import *
from EnemyCog import *
from InventoryCog import Inventory
from discord.ext import commands

class Player:
    def __init__(self, name: str, 
                 description: str,
                 damage: int = 1,
                 defense: int = 1,
                 speed: int = 2,
                 weapon: Weapon = None, 
                 armor: Armor = None
                 ) -> None:
        self.name = name
        self.description = description
        self.damage = 1
        self.defense = 1
        self.speed = 2
        self.health_points = 10
        self.weapon = None
        self.armor = None
        self.is_alive = True
        self.inventory = Inventory(size= 10)
        # TODO: Initialize values within constructor parameters.

    def is_player_alive(self):
        return self.is_alive

    def get_player_stats(self):
        return f"Player: {self.name} \n HP: {self.health_points}\n Weapon: {self.weapon}\n Armor: {self.armor} \n Defense: {self.defense}\n Speed: {self.speed}\n Damage: {self.damage}"

    def take_damage(self, dmg):
        if self.is_alive:
            damage_dealt = dmg - self.defense
            if damage_dealt <= 0:
                damage_dealt = 0
            if damage_dealt > self.health_points:
                self.is_alive = False
            else:
                self.health_points -= damage_dealt
            print(f"Enemy strikes for: {damage_dealt} damage!")

    def deal_damage(self, enemy: Enemy):
        enemy.take_damage(self.damage)

    def add_to_inv(self, item):
        if len(self.inventory) < 5:
            self.inventory.append(item)
        else:
            return "Inventory is full"
        
    # def remove_from_inv(self, item):
    #     if len(self.inventory) > 0:
    #         self.inventory.remove(item)
    #     else:
    #         return "Inventory is empty"
        
    # def use_item(self, item: Item):
    #     if item in self.inventory:
    #         should_delete = item.lose_durability()
    #         if should_delete:
    #             self.remove_from_inv(item)
    #             del item  # This ensures the item is properly deleted
    #     else:
    #         return f"Item: {item}, could not be found."

#TODO: Make the Vanguard, Warrior, Harbinger, and Liferbinder classes. Give them character descriptions.
#* Lifebinder: Includes a team heal and individual heal ability. Possibly passive regeneration. 
#* Warrior: Includes battle buffs.
#* Harbinger: Includes abilities like foresight (sees the probability of an encounter).
#* Vanguard: Includes higher natural health/armor, armor is more effective (In return weapons are less effective), and they can taunt the 
#* enemy to make them target themselves.
#! All abilities need a cooldown (Likely implemented in GameCog)

#? Dunce class that is almost always useless but can land a super heavy hit 1 / 1000 times.
class Vanguard(Player):
    def __init__(self, _name):
        super().__init__(name= _name, description= "place-holder-text")

class Warrior(Player):
    def __init__(self, _name):
        super().__init__(name= _name, description= "place-holder-text")

class Harbinger(Player):
    def __init__(self, _name):
        super().__init__(name= _name, description= "place-holder-text")

class LifeBinder(Player):
    def __init__(self, _name):
        super().__init__(name= _name, description= "place-holder-text")