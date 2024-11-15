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

def println(string):
    print(string)
    print()

item = Item(name= "Cup", durability= 5)
box = Inventory(10)


while item.has_durability():
    print(item)
    item.lose_durability()