import asyncio
import discord
import random
import tracemalloc
import numpy
tracemalloc.start()

from PlayerCog import *
from discord.ext import commands

#? All players on a layer should be dragged into an enemy battle on that layer.
class Cell:
    """Class representing the state of every cell in the board."""
    def __init__(self, cell_state:str = 'Wall', players:list[Player] = []):
        self.__state = cell_state
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
    def __init__(self, width: int, height: int, ratios: list[int]):
        self.__board = [[ Cell() for i in range(width)] for j in range(height)]
        self.__encounters = {
            'Wall': 10,
            'Enemy': 15,
            'Item': 5,
            'Open': 20
        }
        #? Item space should be a shop encounter while open spaces have a random chance of dropping an item. As do enemies.
        """
        Each encounter should be ratios that total up to the amount of space of a layer.
        """
    def initialize_board(self):
        one_time: list[str] = ['T', 'B'] # T: Layer travel space, B: boss
        for i in range():
            for j in range():
                if (i, j) == (0, 0):
                    self.__board[i][j].set_cell_state("Open")

    def __str__(self):
        """
        Displays the board in its current state.
        """
        display_board:str
        for row in self.__board:
            for col in row:
                display_board += str(col)
            s += '\n'
        return display_board
    
class Level:
    def __init__(self, boards_per_lvl):
        self.boards = []