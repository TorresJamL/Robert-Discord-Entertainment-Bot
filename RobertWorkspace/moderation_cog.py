import discord
from discord.ext import commands, tasks
import asyncio
import tracemalloc

tracemalloc.start()

class ModerationCog(commands.Cog):
    def __init__(self, client) -> None:
        super().__init__()
        self.client =  client
