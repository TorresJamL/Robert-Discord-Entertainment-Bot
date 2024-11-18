import asyncio
import discord
import random
from discord.ext import commands
from enum import Enum

class Enemy:
    """Enemy class
    """
    def __init__(self, name: str, hp: float, damage: float, defense: float, speed: float, description: str = "An enemy...") -> None:
        self.name = name
        self.health_points = hp
        self.damage = damage
        self.defense = defense
        self.speed = speed
        self.is_alive = True
        self.ult_percent = 0.0
        self.description = description
    
    def get_name(self):
        return self.name

    def take_damage(self, dmg):
        damage_dealt = dmg - self.defense
        if damage_dealt <= 0:
            damage_dealt = 0
        if damage_dealt > self.health_points:
            self.is_alive = False
        else:
            self.health_points -= damage_dealt
        print(f"Player strikes for: {damage_dealt} damage!")

    def deal_damage(self, player):
        player.take_damage(self.damage)

    def get_stats(self):
        return f"Enemy: {self.name} \n HP: {self.health_points}\n Defense: {self.defense}\n Speed: {self.speed}\n Damage: {self.damage}\n Description: {self.description}"

    def get_description(self):
        return self.description
    
    def __str__(self):
        return Enemy.get_stats(self)

class Grunt(Enemy):
    def __init__(self, name, description: str) -> None:
        hp = random.randint(5, 10)
        damage = random.randint(1, 2)
        defense = random.randint(0, 2)
        speed = random.randint(1, 2)
        super().__init__(name, hp, damage, defense, speed, description)
    
    def stealItem(self, player):
        return NotImplementedError

class Fighter(Enemy):
    def __init__(self, name, description: str) -> None:
        hp = random.randint(7, 15)
        damage = random.randint(2, 4)
        defense = random.randint(1, 2)
        speed = random.randint(3, 10)
        super().__init__(name, hp, damage, defense, speed, description)

    #deals major damage and sends a special attack specific message
    def special_attack(self, name : str = "↑←↓↓↓"):
        is_crit = bool(random.getrandbits(1))
        if is_crit:
            pass
        else:
            pass

class Boss(Enemy):
    def __init__(self, name, description: str) -> None:
        hp = random.randint(50, 150)
        damage = random.randint(5, 20)
        defense = random.randint(5, 10)
        speed = random.randint(1, 20)
        super().__init__(name, hp, damage, defense, speed, description)

    def special_attack(self):
        pass

    def ultimate_attack(self):
        pass
