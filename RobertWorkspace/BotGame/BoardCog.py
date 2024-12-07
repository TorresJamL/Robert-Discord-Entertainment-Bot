import asyncio
import discord
import random
import tracemalloc
tracemalloc.start()

from discord.ext import commands

class Board:
    def __init__(self, width, height):
        self.board = [[ 0 for i in range(width)] for j in range(height)] # Creates a 3d array of dimensions x, y, z

    def __str__(self):
        display_board:str
        for row in self.board:
            for col in row:
                display_board += str(col)
            s += '\n'
        return display_board
    
class Level:
    def __init__(self, boards_per_lvl):
        self.boards = []