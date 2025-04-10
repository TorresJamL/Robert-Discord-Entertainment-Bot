import discord
import asyncio
import sys
import random
import tracemalloc
from discord.ext import commands, tasks
from tokenStorage import BOT_OWNER_ID

tracemalloc.start()

client = None
def init(bot_client): ### Must be called in the main running file ###
    global client
    client = bot_client

def within_range(num, lower_bound, upper_bound):
    return (num > lower_bound and num < upper_bound)

def check_string_in_file(filename, target_string):
    with open(filename, 'r') as file:
        for line in file:
            if target_string in line:
                return True
    return False

async def join(ctx):
    """Joins the voice channel of the user who called the command.

    Returns:
        True if it successfully joined, false otherwise
    """
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        return True
    else:
        await ctx.send('goofy')
        return False

async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send('goofy')

async def disconnect(vc_member):
    await vc_member.move_to(None)

async def get_member(member_id):
    for user in client.get_all_members():
        if user.id == member_id:
            return user

async def send_submission(ctx, inputs_length, text: str)->None:
    client_owner = await client.fetch_user(BOT_OWNER_ID)
    user_input_submission = text.split()
    if len(user_input_submission) == inputs_length:
        await ctx.send("```Submission sent: Check for submission details in your DMs!```")
        user = await client.fetch_user(ctx.author.id)
        await user.send("```Your submission is being reviewed. Keep checking this DM conversation for updates on your submission!```")
        owner_dm = await client_owner.send(f"`User: {user} Submission: {text}`")
        
        # Add reactions to the message
        await owner_dm.add_reaction('✅')
        await owner_dm.add_reaction('❌')

        # Store submission details in a dictionary
        client.submissions[owner_dm.id] = (user, text)
    else:
        await ctx.send("```Your submission does not fit the submission format. The format for enemy submission is : \nEnemy addition format -->| Enemy Type | name | hp | dmg | def | speed |```")          

async def get_occupied_voice_channels():
    try:
        voice_channels_with_members = []
        for channel in client.get_all_channels():
            if (type(channel) is discord.channel.VoiceChannel) and len(channel.members) > 0:
                voice_channels_with_members.append(channel)

        if not voice_channels_with_members:
            return False
        else:
            print(type(voice_channels_with_members[0]))
            return voice_channels_with_members
    except Exception as error:
        return f'An error has occured: {error} :\n get_occupied_voice_channels(ctx)'
    
async def is_member_in_voice(member: discord.Member):
    pass

async def get_member_info(member: discord.Member):
    return {
        "name": member.name,
        "nick": member.nick,
        "raw_status": member.raw_status,
        "activity": member.activity,
        "activities": member.activities
    }