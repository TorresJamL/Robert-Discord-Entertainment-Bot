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

# inv = Inventory(8)
# for i in range(8):
#     inv.add_item(item= item)
# print(item)
# print(inv)

# while (player1.is_player_alive() and enemy1.is_enemy_alive()):
#     player1.deal_damage(enemy1)
#     println(player1.get_stats())
#     enemy1.deal_damage(player1)
#     println(enemy1.get_stats())
#     if run_count > 100:
#         print("Exceeded Run Limit")
#         StupidError
#         break
#     run_count += 1
def do(something):
    print((f"did {something}"))

board = [[' ' for i in range(8)] for j in range(8)]
spaces = {
    'wall' : do('wall')

}
spaces['wall']

def initializeBoard(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            rand_num = random.randint(0, 100)

def displayBoard(grid):
    for row in grid:
        print(row)

displayBoard(board)

class WeightedDict(dict[str : int]):
    """A type of dictionary meant to be used for weighted random chances. Where the value must be an integer.
    """ 

    def get_total_weight(self):
        return sum(list(self.values()))

    def get_random_key(self):
        cumulative_weights = []
        total_weight = 0
        for weight in list(self.values()):
            total_weight += weight
            cumulative_weights.append(total_weight)

        rand_num = random.randint(0, total_weight)

        for i, cumulative_weight in enumerate(cumulative_weights):
            if rand_num <= cumulative_weight:
                return list(self.keys())[i]
        
        return

D = WeightedDict({
    'A': 1,
    'B': 2,
    'C': 8
})

for _ in range(10):
    print(D.get_random_key())