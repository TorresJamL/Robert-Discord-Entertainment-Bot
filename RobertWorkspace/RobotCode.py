import discord
import asyncio
import sys
import random
import tracemalloc
import logging

tracemalloc.start()

# Cog imports 
from tokenStorage import *
from text_to_speech_cog import *
from moderation_cog import *
from fun_cog import *
from music_cog import *
from discord.ext import commands, tasks

sys.path.insert(0, FILE_PATH)

# Message to future me: 
## Increment the amount of problems you've had with imports here: 7

from BotGame import gameCog as GameCog

intents = discord.Intents.all()
client = commands.Bot(command_prefix='-', intents=intents)
default_channel = None

# TODO: 
#   Move some functions to a new cog, "funCog."
#   
#   Some functions use other functions that would make sense to leave in this file.
#   Decide on what to do with those.

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

@client.command(name = "VC?")
async def VC(ctx)->None:
    """
    Makes the bot join the VC the user is in.
    """
    print(type(ctx))
    await join(ctx)

@client.command(name='blacklist')
async def blacklistUser(ctx, user_ID):
    processed_user_ID = user_ID[2:-1]
    try:
        if not check_string_in_file("blacklist.txt", processed_user_ID):
            await ctx.send(f"User: {user_ID}, has been blacklisted. Do you feel safe though? Cause you shouldn't")
            with open("blacklist.txt", 'a') as file:
                file.write(f"{processed_user_ID} ")
        else:
            await ctx.send(f"User: {user_ID}, is already on the blacklist!")
    except Exception as e:
        await ctx.send("An error occured while parsing file. Blame Jamil's incompetence")
        print(f"An error occured: {e}")

@client.command()
async def unBlacklistUser(ctx, user_ID):
    processed_user_ID = user_ID[2:-1]
    if check_string_in_file("blacklist.txt", processed_user_ID):
        with open("blacklist.txt", 'r') as file:
            file_data = file.read()

        file_data = file_data.replace(f"{processed_user_ID} ", "")
        with open("blacklist.txt", 'w') as file:
            file.write(file_data)
        await ctx.send(f"Removed User: {user_ID} from blacklist")
    else:
        await ctx.send(f"User: {user_ID} is not on the blacklist!")

@client.event
async def on_message(message):
    await client.process_commands(message)

@client.command(name='request')
async def add_to_game(ctx, submission_type, *, text: str):
    if submission_type == "enemy":
        # Enemy addition format -->| Enemy Type | name | hp | dmg | def | speed | description |
        await send_submission(ctx, 6, text)
    elif submission_type == "item":
        # Item addition format -->| Item Type | name | durability | dmg (None if not a weapon) | effect (None if not a potion) | def (None if not armor) | description |
        await send_submission(ctx, 6, text)
    else:
        await ctx.send(f'```Invalid argument, "{submission_type}": \n Try "enemy" or "item" instead.```')

@client.event
async def on_reaction_add(reaction, user):
    if user.id == BOT_OWNER_ID:  # Check if the reaction is from you
        message_id = reaction.message.id
        if message_id in client.submissions:
            submission_user, submission_text = client.submissions[message_id]
            if reaction.emoji == '✅':
                await submission_user.send(f'```Your submission,"{submission_text}" has been approved! Please be considerate that addition and implementation may take several days. So hold your horses or be filled by one. Thanks!```')
            elif reaction.emoji == '❌':
                await submission_user.send(f'```Your submission,"{submission_text}" has been rejected after not so careful consideration. It was plain out horrendous. Next time use those wrinkles on yo brain.\n\nFor future reference make sure your submission meets the desired format and/or is simply better.```')
            # Remove the submission from the dictionary after reacting
            del client.submissions[message_id]

@client.command(name='feedback')
async def send_user_feedback(self, ctx, *, text: str):
    sender = await client.fetch_user(ctx.author.id)
    client_owner = await client.fetch_user(BOT_OWNER_ID)
    await client_owner.send(f"```Feedback from {sender}:\n{text}```")
    await ctx.send("```Thank you for your feedback!```")

@client.command(name = 'VoiceChannels')
async def get_voice_channels(ctx):
    """Gives a list of occupied voice channels

    Args:
        ctx : The context the command is being called in. (Not important to users, ignore entirely)
    """
    vc_list = await get_occupied_voice_channels()
    await ctx.send(f"Occupied Voice Channels: {vc_list}")

# Command toggle to periodically move me between different occupied VCs
# Move to funCog
@client.command(name = 'VC_gamblecore')
async def VC_gamblecore(ctx):
    try:
        await toggle_vc_move(ctx)
        await ctx.send(f"VC hopping = {vc_move.is_running}")
    except Exception as e:
        print(f"Error occured: {e}")
        await ctx.send("```Unfortunatly, an error occured. If you'd like to report this error, do not, as Jamil does not care about the bug and especially not you.```")

# move to fun cog
async def toggle_vc_move(ctx):
    try:
        if vc_move.is_running():
            await vc_move.stop()
        else:
            await vc_move.start()
    except Exception as e:
        print(f"Error occured: {e}")

# Move me every 'seconds' seconds
# Move to funCog
@tasks.loop(seconds = 1.0)
async def vc_move():
    # Bot commands channel
    bot_commands = client.get_channel(848400178872713246)

    # Get a list of every channel's ID
    voice_channel_list = await get_occupied_voice_channels()\
    
    if len(voice_channel_list) > 1:
        # Get a random channel's ID 
        channel = random.choice(voice_channel_list)
        
        # User to be moved randomly
        user = await get_member(BOT_OWNER_ID)

        # Move user to that channel every inputted increment
        await user.move_to(channel)
        print(f"{user} has been moved")
    else:
        await bot_commands.send("```Not enough occupied voice channels, try again later```")
        await toggle_vc_move()

# Wait till start up
# Move to funCog
@vc_move.before_loop
async def before_vc_move():
    await client.wait_until_ready()

@client.command(name= "setDefaultChannel")
async def set_default_channel(ctx, channel_id: int):
    default_channel = discord.Guild.get_channel(channel_id)
    print(f"Gave result: {default_channel}")
    if default_channel == None:
        await ctx.send("Channel could not be found. Try again with a valid channel ID.")
    else:
        await ctx.send("Channel Default Set Successfully✅")

# @tasks.loop(seconds= 20.0)
# async def farm_merge_exterminator():
#     channel = client.get_channel(848400178872713246)
#     member_list = client.get_all_members()
#     for member in member_list:
#         if member.activities != ():
#             print(f"{member.name} \n\tstatus:{member.activities}")
#         if "league of legends" in str(member.activity).lower():
#             print(f"User {member.name} has been eradicated")
#             await channel.send("Peace has been restored...")
#             await member.ban(reason= "Be Better")

@client.event
async def on_ready():
    # 848400178872713246
    channel = default_channel
    print(channel)
    if channel != None:
        print("Condition Passed.")
        channel.send("Robert Online✅")
    else: 
        print("Condition Failed.")
    print(f'Logged in as {client.user}')
    # Initialize a dictionary to store submissions
    client.submissions = {}  
    if (vc_move.is_running):
        vc_move.stop()
    # try:
    #     await farm_merge_exterminator.start()
    # except Exception as err:
    #     print(f"An error occured: {err}")

game_cog = GameCog.Game(client)
tts_cog = TextToSpeech(client)
mod_cog = ModerationCog(client)
fun_cog = FunCog(client)
music_cog = MusicCog(client)

async def main():
    init(client)
    await client.add_cog(game_cog)
    await client.add_cog(tts_cog)
    await client.add_cog(mod_cog)
    await client.add_cog(fun_cog)    
    await client.add_cog(music_cog) 
    await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
