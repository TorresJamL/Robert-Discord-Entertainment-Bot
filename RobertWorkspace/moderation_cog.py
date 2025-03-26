import discord
from discord.ext import commands, tasks
from discord import Member, User
from datetime import datetime, timedelta
import asyncio
import tracemalloc

tracemalloc.start()

class ModerationCog(commands.Cog):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
    
    @commands.command(name = "ban")
    @commands.has_guild_permissions(administrator=True)
    async def user_ban(self, ctx, member: Member, days_of_messages: int = 0, ban_reason: str = "") -> None:
        """Permenantly bans member. Format: -ban{member}{days_of_messages: defaults to 0}{ban reason}
        If an number is entered into the 'days of messages' spot, any message sent by the member within that 'days of messages' 
        amount of time from their ban, will be deleted.

        Args:
            ctx (Context): Context the command is being called in.
            member (Member): The member to be banned.
            days_of_messages (int, optional): The days worth of messages to delete IF ANY. Defaults to 0.
            ban_reason (str, optional): Reason for member being banned. Defaults to "".
        Examples:
            "ban @member": @member will be kicked and prevented from joining the server until unbanned.
        """
        try:
            await member.ban(delete_message_days = days_of_messages, reason = ban_reason)
        except Exception as error:
            print(f"An error has occured: {error}")
            await ctx.send(f'Something went wrong. member: "{member}" may not exist.')            

    @commands.command(name = "kick")
    @commands.has_guild_permissions(administrator=True)
    async def member_kick(self, ctx, member: Member, *, reason: str) -> None:
        """Kicks member. Format: -kick {member} {reason}
        """
        try:
            await member.kick(reason)
        except discord.Forbidden:
            await ctx.send("I do not have permission to timeout this member.")
        except Exception as error:
            print(f"An error occured: {error}")
            await ctx.send(f"Something went wrong. member: {member} : may not exist.")
        else:
            await ctx.send(f"Successful command execution, {member} has been kicked from the Guild")
        finally:
            await ctx.send("Command executed.")

    @commands.command(name = "timeout")
    @commands.has_guild_permissions(administrator=True)
    async def user_timeout(self, ctx,  member: Member, duration_amount: int, *, timeout_reason: str = None) -> None:
        """Timeouts a user for an amount of minutes. Format: -timeout {member} {minutes} {reason}

        Args:
            ctx (Context): _description_
            member (Member): _description_
            duration_amount (int): _description_
            timeout_reason (str, optional): _description_. Defaults to None.
        """
        try:
            timeout_duration = timedelta(minutes= duration_amount)
            await member.timeout(discord.utils.utcnow() + timeout_duration, reason= timeout_reason)
            await ctx.send(f"Member {member.name} was timed out for {duration_amount}")

        except discord.Forbidden as forbade:
            await ctx.send(f"```I do not have permission to timeout this user. Program Output :: {forbade}```")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to timeout the user. Error: {e}")
        except ValueError as error:
            await ctx.send("An error occured...")
            print(f"A value error occured: {error}")
        except TypeError as error:
            await ctx.send("An error occured...")
            print(f"A type error occured: {error}")
        except Exception as error:
            await ctx.send("An error occured...")
            print(f"An unexpected error occured: {error}")
        finally:
            print(f"member : {member} \nduration : {duration_amount} \nreason : {timeout_reason}")

    @commands.command(name = "toggleAutoMod")
    @commands.has_guild_permissions(administrator=True)
    async def toggleAutoMod(self, ctx, feature: str = "all") -> None:
        match feature:
            case "all":
                pass
            case "anti-spam":
                pass
            case "language-filter":
                pass
    
    async def antiSpam():
        pass