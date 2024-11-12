import asyncio
import discord
import random
import time
from discord.abc import Connectable
from discord.ext import commands
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
import traceback

class VoiceClient(discord.voice_client.VoiceClient):
    def __init__(self, client: discord.Client, channel: Connectable) -> None:
        super().__init__(client, channel)

class Context(discord.ext.commands.context.Context):
    def __init__(self, client) -> None:
        self.client = client
        super().__init__()

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'options': '-vn'}
        self.vc: VoiceClient = None
        self.ytdl = YoutubeDL(self.YDL_OPTIONS)

    @commands.command(pass_context=True)
    async def clearQueue(self, ctx):
        self.music_queue = []

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            data = await self.ytdl.extract_info(m_url, download=False)
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.ensure_future(self.play_next()))
                           
    async def play_music(self, ctx: Context):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            voice_channel = self.music_queue[0][1]
            if not ctx.voice_client or not ctx.voice_client.is_connected():
                self.vc = await voice_channel.connect()
            self.music_queue.pop(0)
            try:
                data = self.ytdl.extract_info(m_url, download=False)
                song = data['url']
                self.vc.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.ensure_future(self.play_next()))
            except Exception as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()
                raise e

    def search_yt(self, item):
        if item.startswith("https://"):
            try:
                title = self.ytdl.extract_info(item, download=False)["title"]
                info_dict: dict = self.ytdl.extract_info(item, download=False)
                print(f"\n{list(info_dict.values())}\n")
                return {'source': item, 'title': title}
            except Exception as error:
                print(f"AN ERROR HAS OCCURED: {error}")
                traceback.print_exc
                raise error
            
        search = VideosSearch(item, limit=1)
        return {'source': search.result()["result"][0]["link"], 'title': search.result()["result"][0]["title"]}

    @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from youtube")
    async def play(self, ctx: Context, *args):
        query = " ".join(args)
        if not ctx.author.voice:
            await ctx.send('You need to be in a voice channel to use this command.')
            return
        voice_channel = ctx.author.voice.channel
        if self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("```Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.```")
            else:
                if self.is_playing:
                    await ctx.send(f"**#{len(self.music_queue)+2} -'{song['title']}'** added to the queue")
                else:
                    await ctx.send(f"**'{song['title']}'** added to the queue")
                self.music_queue.append([song, voice_channel])
                if not self.is_playing:
                    await self.play_music(ctx)
                    traceback.print_exc()
