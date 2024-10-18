import discord
from discord.ext import commands, tasks
from discord import Member, User
import asyncio
import tracemalloc

tracemalloc.start()

class ModerationCog(commands.Cog):
    def __init__(self, client) -> None:
        super().__init__()
        self.client =  client
    
    @commands.command(name = "ban")
    @commands.has_guild_permissions(administrator=True)
    async def user_ban(ctx, user: Member, days_of_messages, reason):
        """
        Permenantly bans user. Upon calling "ban @user", the pinged user will be kicked and prevented from joining the server ever.

        :param user: Accepts a user as parameter.
        """
        try:
            await user.ban()
        except Exception as error:
            print(f"An error has occured: {error}")
        finally:
            await ctx.send(f"Something went wrong. User: {user} : may not exist.")

    @commands.command(name = "kick")
    @commands.has_guild_permissions(administrator=True)
    async def user_kick(ctx, user: Member, *, reason: str):
        """
        Kicks user from guild. 
        """
        try:
            await user.kick(reason)
        except Exception as error:
            print(f"An error occured: {error}")
        finally:
            await ctx.send(f"Something went wrong. User: {user} : may not exist.")

