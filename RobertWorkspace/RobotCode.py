import discord
import asyncio
import sys
import random
import tracemalloc
tracemalloc.start()

# Cog imports 
from tokenStorage import *
from text_to_speech_cog import *
from moderation_cog import *
from fun_cog import *
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import requests

sys.path.insert(0, FILE_PATH) 

from BotGame import GameCog

intents = discord.Intents.all()
client = commands.Bot(command_prefix='-', intents=intents)

# TODO: 
#   Replace every instance of "JAMIL_ID" with a new role specifically for who's managing the bot.
#   Make a function that assigns the new 'bot manager' role to any ONE, person. Allow only 
#   people with administration permissions to use said command.
#   Remove certain inside jokes
#   Move some functions to a new cog, "funCog."
#   
#   Some functions use other functions that would make sense to leave in this file.
#   Decide on what to do with those.
#   In some cases, it's faster to re-implement a new function with the same purpose in each cog rather than import it from this one.

async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send('goofy')

connection_terminated: str = ""
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
    client_owner = await client.fetch_user(JAMIL_ID)
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

@client.command()
async def randSCP(ctx):
    scpNum = ''
    num = random.randint(1, 8000)
    if (num < 100):
        scpNum = f"0{num}"
    else:
        scpNum = num
    url_link = f'https://scp-wiki.wikidot.com/scp-{scpNum}'
    try:
        pass
    except Exception:
        print()
    await ctx.send(url_link)

# Add to new funCog
def check_string_in_file(filename, target_string):
    with open(filename, 'r') as file:
        for line in file:
            if target_string in line:
                return True
    return False

# Add to new funCog
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

# Add to new funCog
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

# Add to new funCog
@client.command(name = 'sacrifice')
async def randVC(ctx):
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
        
        print(f"Member list: {str(members)}")
        print()
        print(type(random_member))
        print()

        '''await ctx.send(f'```Random User ID from the voice channel: {random_member}```')
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

        await ctx.send("```Function ran too many time, try again later...```")'''
        await leave(ctx)
        
    
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send('An error occurred while trying to disconnect a member of the voice channel.')
        await leave(ctx)

@client.event
async def on_message(message):
    await client.process_commands(message)

@client.command(name='request')
async def add_to_game(ctx, args, *, text: str):
    if args == "enemy":
        # Enemy addition format -->| Enemy Type | name | hp | dmg | def | speed | description |
        await send_submission(ctx, 6, text)
    elif args == "item":
        # Item addition format -->| Item Type | name | durability | dmg (None if not a weapon) | effect (None if not a potion) | def (None if not armor) | description |
        await send_submission(ctx, 6, text)
    else:
        await ctx.send(f'```Invalid argument, "{args}": \n Try "enemy" or "item" instead.```')

@client.event
async def on_reaction_add(reaction, user):
    if user.id == JAMIL_ID:  # Check if the reaction is from you
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
    client_owner = await client.fetch_user(JAMIL_ID)
    await client_owner.send(f"```Feedback from {sender}:\n{text}```")
    await ctx.send("```Thank you for your feedback!```")

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

@client.command(name = 'VoiceChannels')
async def get_voice_channels(ctx):
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
    finally:
        await ctx.send("```Unfortunatly, an error occured. If you'd like to report this error, do not, as   does not care about the bug and especially not you.```")

# Undecided
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
        user = await get_member(JAMIL_ID)

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

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Initialize a dictionary to store submissions
    client.submissions = {}  
    if (vc_move.is_running):
        vc_move.stop()

# Create instances of the game cog, tts cog, and moderation cog
game_cog = GameCog.Game(client)
tts_cog = TextToSpeech(client)
mod_cog = ModerationCog(client)
fun_cog = FunCog(client)


#mc = MusicCog(client)
# Run the bot
async def main():
    await client.add_cog(game_cog)
    await client.add_cog(tts_cog)
    await client.add_cog(mod_cog)
    await client.add_cog(fun_cog)    
    #await client.add_cog(mc) 
    await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
