import discord
from discord.ext import commands, tasks
from discord import Member, User
from datetime import datetime, timedelta
import asyncio
import tracemalloc

tracemalloc.start()

class Context(discord.ext.commands.context.Context):
    def __init__(self, client) -> None:
        self.client = client
        super().__init__()

class ModerationCog(commands.Cog):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
    
    @commands.command(name = "ban")
    @commands.has_guild_permissions(administrator=True)
    async def user_ban(self, ctx: Context, user: Member, days_of_messages: int = 0, ban_reason: str = "") -> None:
        """Permenantly bans user. Format: -ban{user}{days_of_messages: defaults to 0}{ban reason}
        If an number is entered into the 'days of messages' spot, any message sent by the user within that 'days of messages' 
        amount of time from their ban, will be deleted.

        Args:
            ctx (Context): Context the command is being called in.
            user (Member): The user to be banned.
            days_of_messages (int, optional): The days worth of messages to delete IF ANY. Defaults to 0.
            ban_reason (str, optional): Reason for user being banned. Defaults to "".
        Examples:
            "ban @user": @user will be kicked and prevented from joining the server until unbanned.
        """
        try:
            await user.ban(delete_message_days = days_of_messages, reason = ban_reason)
        except Exception as error:
            print(f"An error has occured: {error}")
            await ctx.send(f'Something went wrong. User: "{user}" may not exist.')            

    @commands.command(name = "kick")
    @commands.has_guild_permissions(administrator=True)
    async def user_kick(self, ctx: Context, user: Member, *, reason: str) -> None:
        """Kicks user. Format: -kick{user}{reason}
        """
        try:
            await user.kick(reason)
        except Exception as error:
            print(f"An error occured: {error}")
        finally:
            await ctx.send(f"Something went wrong. User: {user} : may not exist.")

    @commands.command(name = "timeout")
    @commands.has_guild_permissions(administrator=True)
    async def user_timeout(self, ctx: Context,  member: Member, duration_amount: int, timeout_reason: str) -> None:
        try:
            # TODO add a time duration to .timeout() using deltatime or datetime. Refer to appropriate documentation
            await member.timeout(reason= timeout_reason)
        except TypeError as error:
            print()

    @commands.command(name = "toggleAutoMod")
    @commands.has_guild_permissions(administrator=True)
    async def toggleAutoMod(self, ctx: Context, feature: str = "all") -> None:
        match feature:
            case "all":
                pass
            case "anti-spam":
                pass
            case "language-filter":
                pass
    
    async def antiSpam():
        pass