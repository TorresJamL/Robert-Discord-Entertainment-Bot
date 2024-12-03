import discord
import asyncio
import sys
import random
import tracemalloc
import logging
from discord.ext import commands, tasks

tracemalloc.start()
class RobertLib(commands.Cog):
    def __init__(self) -> None:
        super().__init__()

# async def join(ctx):
#     if (ctx.author.voice):
#         channel = ctx.message.author.voice.channel
#         await channel.connect()
#     else:
#         await ctx.send('goofy')

# connection_terminated: str = ""
# async def leave(ctx):
#     if (ctx.voice_client):
#         await ctx.guild.voice_client.disconnect()
#     else:
#         await ctx.send('goofy')

# async def disconnect(vc_member):
#     await vc_member.move_to(None)

# async def get_member(member_id):
#     for user in client.get_all_members():
#         if user.id == member_id:
#             return user

# async def send_submission(ctx, inputs_length, text: str)->None:
#     client_owner = await client.fetch_user(JAMIL_ID)
#     user_input_submission = text.split()
#     if len(user_input_submission) == inputs_length:
#         await ctx.send("```Submission sent: Check for submission details in your DMs!```")
#         user = await client.fetch_user(ctx.author.id)
#         await user.send("```Your submission is being reviewed. Keep checking this DM conversation for updates on your submission!```")
#         owner_dm = await client_owner.send(f"`User: {user} Submission: {text}`")
        
#         # Add reactions to the message
#         await owner_dm.add_reaction('✅')
#         await owner_dm.add_reaction('❌')

#         # Store submission details in a dictionary
#         client.submissions[owner_dm.id] = (user, text)
#     else:
#         await ctx.send("```Your submission does not fit the submission format. The format for enemy submission is : \nEnemy addition format -->| Enemy Type | name | hp | dmg | def | speed |```")          
