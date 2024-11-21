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
        self.damage = damage
        self.defense = defense
        self.speed = speed
        self.health_points = 10
        self.weapon = weapon
        self.armor = armor
        self.is_alive = True
        self.inventory = Inventory(size= 10)
        # TODO: Initialize values within constructor parameters.

    def is_player_alive(self):
        """Whether the player is alive
        Returns:
            bool: True if player is alive, false otherwise.
        """
        return self.is_alive

    def get_inventory(self):
        """Gets the inventory of the player.
        Returns:
            list: The inventory of the player as a list of items
        """
        return self.inventory

    def get_stats(self):
        return f"Player: {self.name} \n HP: {self.health_points}\n Weapon: {self.weapon}\n Armor: {self.armor} \n Defense: {self.defense}\n Speed: {self.speed}\n Damage: {self.damage}"

    def take_damage(self, dmg):
        if self.is_alive:
            damage_dealt = dmg - self.defense
            if damage_dealt <= 0:
                damage_dealt = 0
            if damage_dealt > self.health_points:
                self.is_alive = False
                print("Player down!")
            else:
                self.health_points -= damage_dealt
            print(f"Enemy strikes for: {damage_dealt} damage!")

    def deal_damage(self, enemy: Enemy):
        enemy.take_damage(self.damage)

    def add_to_inv(self, item):
        self.inventory.add_item(item)

    def use_item(self, item: Item):
        if self.inventory.has_item(item):
            self.inventory.use_item(item)

    def discard_item(self, item: Item):
        if self.inventory.has_item(item):
            self.inventory.remove_item(item)
