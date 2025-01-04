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
from text_to_speech_cog import *
from moderation_cog import *
import time
import sys
from RobotCodelib import *

from bs4 import BeautifulSoup
import requests
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

    @commands.command(name= "DomainExpansion")
    async def disconnect_all(self, ctx: Context):
        """_summary_

        Args:
            ctx (Context): _description_
        """
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send('goofy')
            return
    
    @commands.command(name= 'sacrifice')
    async def randVC(self, ctx):
        try:
            await join(ctx)

            if ctx.guild.voice_client is None:
                return await ctx.send('I AINT EVEN THERE')

            voice_channel_id = ctx.guild.voice_client.channel.id
            await ctx.send(f'```Voice Channel ID: {voice_channel_id}```')
            
            voice_channel = discord.utils.get(ctx.guild.voice_channels, id=voice_channel_id)
            print(voice_channel)
            
            if not voice_channel:
                return await ctx.send('I give up')

            members = voice_channel.members

            random_member = random.choice(members)

            await ctx.send(f'```Random User ID from the voice channel: {random_member}```')
            for _ in range(20):
                print(str(random_member.id))
                print(not check_string_in_file("blacklist.txt", str(random_member.id)))
                if not check_string_in_file("blacklist.txt", str(random_member.id)):
                    await disconnect(random_member)
                    await ctx.send(f"```{random_member} has been sacrificed.```")
                    await leave(ctx)
                    return
                random_member = random.choice(members)
                await ctx.send(f'```Random User from the voice channel: {random_member}\nUser ID: {random_member.id}```')

            await ctx.send("```Function ran too many time, try again later...```")
            await leave(ctx)
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send('An error occurred while trying to disconnect a member of the voice channel.')
            await leave(ctx)

    @commands.command()
    async def scp(self, ctx, scp_num: int = None):
        """If given a scp number, it will link said scp. Otherwise, sends a link to a random SCP. 
        Also sends the description of said SCP presuming the author ain't quirky.
        Arguments:
            ctx (Context): The context of the client side function call. 
            scp_num (int): The number of the scp if one is desired to be searched for. Defaults to None
        """
        scpNum = ""
        if scp_num == None or not(within_range(scp_num, 0, 8000)):
            num = random.randint(1, 8000)
            if (num < 100):
                scpNum = f"0{num}"
            else:
                scpNum = num
        else: 
            scpNum = scp_num

        url_link = f'https://scp-wiki.wikidot.com/scp-{scpNum}'
        try:
            response = requests.get(url_link)
            data = response.text
            # Parse the HTML content
            soup = BeautifulSoup(data, 'html.parser')
            # Extract specific elements
            description = soup.find('strong', string='Description:').next_sibling.strip()
            await ctx.send(description)
        except Exception as error:
            print(f"An Error occured (SCP):\n {error}")
        finally:
            await ctx.send(url_link)