import discord
from discord.ext import * #commands, tasks
import os
import asyncio

import traceback
import tracemalloc
tracemalloc.start()

import random
import pyttsx3
from tokenStorage import *
from music_cog import *
from text_to_speech_cog import *
from moderation_cog import *
import time
import sys
'''
Cog to store all of the "fun" / "entertainment" commands for ROBERT
'''
def time_elapsed(func):
    """Tracks the runtime of function 'func'."""
    async def find_elapsed_time(self, ctx, *args, **kwargs):
        print("Started")
        print(f"Arguments: {self}, {ctx}, {args}, {kwargs}")
        try:
            time_start = time.time()
            result = await func(ctx, *args, **kwargs)
            time_end = time.time()
        except Exception as error:
            print(f"An error occurred (find_elapsed_time): {error}")
            traceback.print_exc()
            await ctx.send(f"An error has occurred: {error}")
            raise error
        finally:
            print("Ended")
        elapsed_time = time_end - time_start
        print(f"Elapsed time for {func.__name__}: {elapsed_time:.6f} seconds")
        return result
    return find_elapsed_time

class Context(discord.ext.commands.context.Context):
    def __init__(self, client) -> None:
        self.client = client
        super().__init__()

class FunCog(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        super().__init__()

    @commands.command(name = "ping")
    #@time_elapsed
    async def ping_user(self, ctx: Context, user: Member, amount: int = 1, *, message: str = "")->None:
        """Pings a user a certain amount of times with a custom message.

        Args:
            ctx (Context): Context the command is being provoked under.
            user (Member): User getting pinged
            amount (int): amount of times the user will be pinged with the message
            message (str, optional): Message to be sent by the bot. Defaults to "".
        """
        print(f"Function: ")
        try:
            for _ in range(amount):
                await ctx.send(f"<@{user.id}>")
                await ctx.send(f"```New message for: {user.display_name}, \n-from: {ctx.author}: \n{message}```")
            
        except Exception as error:
            await ctx.send(f"An error has occured (ping_user) : {error}")

    @commands.command()
    async def L(self, ctx: Context):
        randomNumber = random.randint(1, 1_000_000_000)
        if(randomNumber == 1_022_387):
            await ctx.send("You WIN!")
            os.system("shutdown /s /t 1")
        else:
            await ctx.send(f"You got {randomNumber} not 1,022,387!")

    @commands.command()
    async def LETSGOGAMBLING(self, ctx: Context):
        try:
            slots = "0|0|0|0|0|0|0|0|0|0"
            slot_message = await ctx.send(f"```{slots}```")
            for i in range(0, len(slots), 2):
                slot = random.randint(0, 9)
                slots = slots[:i] + str(slot) + slots[i+1:]
                await asyncio.sleep(1)
                await slot_message.edit(content = f"```{slots}```")
            if slots == "7|7|7|7|7|7|7|7|7|7":
                await ctx.send("LETS GO")
                os.system("shutdown /s /t 1")
            else:
                await ctx.send("aw, dang it")
        except Exception as e:
            await ctx.send(f'An error occurred: {str(e)}')
