from discord.abc import Connectable
import pyttsx3
import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands.context import Context
import asyncio
import tracemalloc

tracemalloc.start()

class TextToSpeech(commands.Cog):
    engine = pyttsx3.init()
    def __init__(self, client):
        self.client = client
        self.is_playing = False
        self.TTS_queue : list[str] = []

    async def join_vc(self, ctx: Context) -> VoiceClient:
        """Joins the voice channel of the author of the message

        Args:
            ctx (_type_): _description_

        Returns:
            VoiceClient: _description_
        """
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
        else:
            await ctx.send('User was not found in any voice channel.')

        if not channel:
            await ctx.send("Voice channel not found.")
            return 
        return await channel.connect()

    async def text_to_speech(self, rate: int = 200, volume: float = 1.0, voice_gender: bool = None, text: str = ""):
        """Converts text to audible speech contained in "tts_output.wav" 

        Args:
            rate (int): Integer speech rate in words per minute. Defaults to 200 words per minute.
            volume (float): Floating point volume in the range of 0.0 to 1.0 inclusive. Defaults to 1.0.
            voice_gender (bool): Boolean speaking voice gender. 1 for male, 0 for female. Defaults to None
            text (str): String text to be converted. Defaults to "".
        """
        engine = TextToSpeech.engine
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume) 
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_gender].id)
        
        engine.save_to_file(text, "RobertWorkspace\\tts_output.wav")
        engine.runAndWait()
    
    async def speak(self, ctx: Context, voice_client: VoiceClient, text: str = "", voice_rate: int = 200, voice_volume: float = 1.0, voice_gender: bool = None) -> None:
        """Plays the text as audio in a voice channel

        Args:
            ctx (Context): The context in which the funcion was invoked.
            voice_client (VoiceClient): Represents a discord voice connection.
            text (str, optional): String text to be converted. Defaults to "".
            voice_rate (int, optional): Integer speech rate in words per minute. Defaults to 200 words per minute.
            voice_volume (float, optional): Floating point volume in the range of 0.0 to 1.0 inclusive. Defaults to 1.0.
            voice_gender (bool, optional): Boolean speaking voice gender. 0 for male, 1 for female. Defaults to None
        """
        try:
            if self.TTS_queue == []:
                await voice_client.disconnect()
                return
            else:
                # Generate the audio
                await self.text_to_speech(voice_rate, voice_volume, voice_gender, text)
                # Get the bot's voice state and play the generated audio in the voice channel
                voice_state = ctx.guild.voice_client
                if voice_state:
                    with open("RobertWorkspace\\tts_output.wav", "rb") as file:
                        await ctx.send("Here's your audio file!", file=discord.File(file, "robert TTS.wav"))
                    voice_state.play(discord.FFmpegPCMAudio("RobertWorkspace\\tts_output.wav"))
                while voice_client.is_playing():
                    await asyncio.sleep(1)

                print(f"Queue Length: {len(self.TTS_queue)} \nQueue: {self.TTS_queue}")
                self.TTS_queue = self.TTS_queue[1:]
                await self.speak(ctx, voice_client, self.TTS_queue[0], voice_rate, voice_volume, voice_gender)
            
        except Exception as error:
            print(f"(Speak) An error has occured: {error}")

    @commands.command(name= "say")
    async def say(self, ctx: Context, rate: int, volume: float, gender: int, *, text: str):
        """Format: {rate: int} {volume: float between 0.0 and 1.0} {gender: int, either 1(female) or 0(male)} {text: string} 
            A more customizable form of Dspeak. If nothing happens, presume an error occured. Otherwise, feedback should always be provided.
        """
        self.TTS_queue.append(text)
        await ctx.send(f"Text appended to queue. Queue position {len(self.TTS_queue) - 1}")
        if not self.is_playing:
            print("TTS intiated...  \n")
            await ctx.send("```Text To Speech Initaited...```")
            print(f"Queue Length: {len(self.TTS_queue)} \nQueue: {self.TTS_queue}")
        try:
            voice_client = await self.join_vc(ctx)
            print(f"voice client is a {type(voice_client)}")
            if not voice_client.is_playing():
                self.is_playing = True
                await self.speak(ctx, voice_client, text, rate, volume, gender)
        except Exception as error:
            print(f"(say) An error has occured: {error}")

    @commands.command(name = "Dspeak")
    async def default_say(self, ctx: Context, *, text: str):
        print("TTS intiated...  \n")
        self.TTS_queue.append(text)
        print(f"Queue Length: {len(self.TTS_queue)} \nQueue: {self.TTS_queue}")
        try:
            voice_client = await self.join_vc(ctx)
            await self.speak(ctx, voice_client, 200, 1.0, 0, text)
        except Exception as error:
            print(f"(speak_base) An error has occured: {error}")

    @commands.command(name = "queue")
    async def queue(self, ctx: Context):
        print(f"Queue Length: {len(self.TTS_queue)} \nQueue: {self.TTS_queue}")
        await ctx.send(self.TTS_queue)