import asyncio
import discord
import random
import tracemalloc
tracemalloc.start()

from PlayerCog import *
from discord.ext import commands

#? All players on a layer should be dragged into an enemy battle on that layer.
class Cell:
    """Class representing the state of every cell in the board."""
    def __init__(self, cell_state:str = 'WALLS', players:list[Player] = None):
        self.__state = cell_state
        self.__players = players

    def get_cell_state(self):
        return self.__state
    
    def get_player_on_cell(self):
        return self.__players

    def get_complete_cell_status(self) -> tuple[str | bool]:
        return (self.__state, True if self.__players != None else False)

    def set_cell_state(self, cell_state):
        self.__state = cell_state

    def set_player_on_cell(self, player):
        if self.__players == None:
            self.__players = player
        elif player == None:
            self.__players = player
class Board:
    def __init__(self, width, height):
        self.__board = [[ Cell() for i in range(width)] for j in range(height)]

    def initialize_board(self):
        encounters: list[str] = ['W', 'E', 'I', 'O'] # W: Wall, E: Enemy, I: Item Encounter, O: Open space
        one_time: list[str] = ['T', 'B'] # T: Layer travel space, B: boss
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (row, col) == (0, 0):
                    self.__board[row][col] = 'P' # P: Player occupied space
                else:
                    pass              

    def __str__(self):
        """
        Displays the board in its current state.
        """
        display_board:str
        for row in self.board:
            for col in row:
                display_board += str(col)
            s += '\n'
        return display_board
    
class Level:
    def __init__(self, boards_per_lvl):
        self.boards = []