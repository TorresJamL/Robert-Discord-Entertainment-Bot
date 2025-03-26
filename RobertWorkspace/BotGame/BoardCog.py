import asyncio
import discord
import random
import tracemalloc
import numpy
tracemalloc.start()

from PlayerCog import *
from discord.ext import commands
from enum import Flag, auto
from extraslib import extras as EX

#? All players on a layer should be dragged into an enemy battle on that layer.
class Cell:
    """Class representing each board cell."""
    #* A cell can be in 5 states, open:O, enemy:E, item:I, traverse: T, boss:B
    def __init__(self, players:list[Player] = [], weights:list[int] = [70, 30, 10]):
        states = EX.WeightedDict([("O", weights[0]), ("E", weights[1]), ("I", weights[2])])
        self.__state = states.random()
        self.__players = players

    def get_cell_state(self):
        return self.__state
    
    def get_players_on_cell(self):
        return (self.__players, len(self.__players))
    
    def get_complete_cell_status(self) -> tuple[str | bool]:
        return (self.__state, True if self.__players != None else False)

    def set_cell_state(self, cell_state):
        self.__state = cell_state

    def add_players_to_cell(self, player: Player):
        self.__players.append(player)

    def __str__(self):
        return self.__state
class Board:
    def __init__(self, length: int, width: int, next = None, prev = None):
        self.__board = [[ Cell() for i in range(length)] for j in range(width)]
        self.length = length
        self.width = width
        self.next = next
        self.prev = prev
        #! Item space should be a shop encounter while open spaces have a random chance of dropping an item. As do enemies.
        
    def initialize_board(self):
        traversal_space = (random.randint(0, self.length), random.randint(0, self.width))
        boss_space = (random.randint(0, self.length), random.randint(0, self.width))
        while (boss_space == traversal_space):
            boss_space = (random.randint(0, self.length), random.randint(0, self.width))
        for i in range(self.length):
            for j in range(self.width):
                if (i, j) == (0, 0):
                    self.__board[i][j].set_cell_state("O")
                elif traversal_space == (i,j):
                    self.__board[i][j].set_cell_state("T")
                elif boss_space == (i,j):
                    self.__board[i][j].set_cell_state("B")

    def __str__(self):
        """
        Displays the board in its current state.
        """
        display_board = ""
        for row in self.__board:
            for col in row:
                display_board += str(col) + " "
            display_board += '\n'
        return display_board
