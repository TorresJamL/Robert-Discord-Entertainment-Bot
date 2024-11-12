import asyncio
import discord
import random
import json

import tracemalloc
tracemalloc.start()

from discord.ext import commands

from EnemyCog import Enemy, Grunt, Fighter, Boss
from ItemsCog import Item, Weapon, Potion, Armor

# Idea: An adventure game about traversing a "map" full of items and random encounters occur 
# Traversing: When it's a player's turn and they are not in a battle, they can 'traverse' for a random encounter.

# Enemies and Players: Have stats such as attack damage, defense, armor and speed.
# Players can get items: weapons, armor, currency, and etc.

# The winner is determined by the amount of "tokens" gained by players. 
# Tokens can be gained through mainly enemy kills. (possibly through trading items of equal value aswell)  

# Items & enemies are contained within a json file (CogData.json)

# Players will be able to name themselves after selection sequence
class Context(discord.ext.commands.context.Context):
    def __init__(self, client) -> None:
        self.client = client
        super().__init__()

class Game(commands.Cog):
    
    THEBOOLEAN: bool
    def __init__(self, client) -> None:
        self.prompt_message = None
        self.is_getting_players = False
        self.item_list: Item = []
        self.client = client
        self.enemy_list: Enemy = []
        # player list dictionary. Key is the user ID, value is the user's inputted name
        self.player_list = {} # ID : user nickname
    
    @commands.command(name = "Placeholder-Text")
    async def game_start(self, ctx: Context):
        self.is_getting_players = True
        self.enemy_list, self.item_list = self.load_game_data("BotGame/CogData.json")
        await self.prompt_for_players(self, ctx)

    @commands.command(name = "nickname")
    async def change_name(self, ctx: Context, *, new_name: str):
        try:
            if self.is_getting_players:
                user_id = ctx.author.id
                user = await self.client.fetch_user(ctx.author.id)
                self.player_list[user_id] = new_name
                print(f"{user} has updated their name {self.player_list}")
                await ctx.send(f"```Your name in game has been updated: {self.player_list}```")
            else:
                await ctx.send("Name changing is only available during player selection.")
        except Exception as error:
            print(f"An error has occured: {error}")
        finally:
            await ctx.send(f"An error occured while processing {error}")

    # Returns an item from the item list
    def get_item(self, item):
        if item in self.item_list:
            return item
        else:
            return "GameCog Error: Item not found"
    
    # Returns an enemy from the enemy list
    def get_enemy(self, enemy):
        if enemy in self.enemy_list:
            return enemy
        else:
            return "GameCog Error: Enemy not found"
    
    async def prompt_for_players(self, ctx: Context):
        self.prompt_message = await ctx.send("```React with ✅ if you wish to be a player. Once everyone who wants to play has reacted, react with #️⃣ to end player selection sequence.```")
        await self.prompt_message.add_reaction('✅')
        await self.prompt_message.add_reaction('#️⃣')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel = message.channel
        
        # Checks if the message is the prompt message, if the reactions aren't from the bot and if the Game is still selecting players
        if (message == self.prompt_message) and (user != self.client.user) and self.is_getting_players:
            print(f"User: {user}, User id: {user.id}, reaction added.")
            if reaction.emoji == '✅':
                self.player_list[user.id] = ""
                print(f"A player has joined the game:\n User: {user}\n Players: {self.player_list}\n")
            elif reaction.emoji == '#️⃣':
                await channel.send('Selection Ended')
                self.is_getting_players = False

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        message = reaction.message

        # Checks if the message is the prompt message and if the reactions aren't from the bot 
        if (message == self.prompt_message) and (user != self.client.user):
            print(f"User: {user}, User id: {user.id}, reaction removed")
            if reaction.emoji == '✅':
                self.player_list.pop(user.id)
                print(f"A player has left the game:\n User: {user}\n Remaining Players: {self.player_list}\n")

    # Returns enemies and items from the CogData.json file. 
    def load_game_data(self, data_file):
        enemies = []
        items = []


        with open(data_file, 'r') as file:
            data = json.load(file)

            # Append each enemy from the json file to the list of enemies to be returned
            for enemy in data["enemies"]:
                if enemy['type'] == "Grunt":
                    enemies.append(Grunt(enemy['name'], enemy['description']))
                elif enemy['type'] == "Figther":
                    enemies.append(Fighter(enemy['name'], enemy['description']))
                elif enemy['type'] == "Boss":
                    enemies.append(Boss(enemy['name'], enemy['description']))
                elif enemy['type'] == "Enemy":
                    enemies.append(Enemy(enemy['name'], enemy['hp'], enemy['damage'], enemy['defense'], enemy['speed'], enemy['description']))

            # Append each item from the json file to the list of items to be returned
            for item in data["items"]:
                if item['type'] == "Weapon":
                    items.append(Weapon(item['name'], item['damage'], item['durability']))
                elif item['type'] == "Potion":
                    items.append(Potion(item['name'], item['effect'], item['durability']))
                elif item['type'] == "Armor":
                    items.append(Armor(item['name'], item['defense'], item['durability']))
        # Returns both list
        return enemies, items