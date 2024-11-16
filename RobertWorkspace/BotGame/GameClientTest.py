import asyncio
import discord
import random
from discord.ext import commands

from PlayerCog import Player

from EnemyCog import Enemy, Grunt, Fighter, Boss
from EnemyCog import Grunt
from EnemyCog import Fighter
from EnemyCog import Boss

from ItemsCog import Weapon, Potion, Armor, Item
from ItemsCog import Potion
from ItemsCog import Armor
from ItemsCog import Item

from InventoryCog import Inventory

import json

import tracemalloc
tracemalloc.start()

class StupidError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self):
        return "Exception: 'Stupid Drug' occured."

def println(string):
    print(string)
    print()

item = Item(name= "Cup", durability= 5)

player1 = Player("J",
                 "Definitely a building",
                 2)

enemy1 = Grunt("Poo", "Fresh meat")
run_count = 0

inv = Inventory(8)
for i in range(8):
    inv.add_item(item= item)
print(item)
print(inv)

# while player1.is_player_alive():
#     player1.deal_damage(enemy1)
#     println(player1.get_stats())
#     enemy1.deal_damage(player1)
#     println(enemy1.get_stats())
#     if run_count > 100:
#         print("Exceeded Run Limit")
#         StupidError
#         break
#     run_count += 1
 