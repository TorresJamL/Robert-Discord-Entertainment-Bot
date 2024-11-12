import asyncio
import discord
import random
from discord.ext import commands

from PlayerCog import Player

from EnemyCog import Enemy
from EnemyCog import Grunt
from EnemyCog import Fighter
from EnemyCog import Boss

from ItemsCog import Weapon
from ItemsCog import Potion
from ItemsCog import Armor
from ItemsCog import Item

import json

import tracemalloc
tracemalloc.start()

def print_line(string):
    print(string)
    print()

player1 = Player("Jamil", "Clerk")
enemy1 = Grunt("grunt", None)

print_line(player1.get_player_stats())
print_line(enemy1.get_enemy_stats())

player1.deal_damage(enemy1)

print_line(enemy1.get_enemy_stats())
