import pyttsx3
import discord
from discord.ext import commands, tasks
import asyncio
import tracemalloc

tracemalloc.start()

class TextToSpeech(commands.Cog):
    engine = pyttsx3.init()
    def __init__(self, client):
        self.client = client
        self.TTS_queue = []

    async def text_to_speech(rate, volume, speakGender, text):
        '''
        Converts text to speech costumized by the given parameters.
        '''
        engine = TextToSpeech.engine
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume) 
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[speakGender].id)
        
        # Use pyttsx3 to convert text to speech
        engine.save_to_file(text, "tts_output.wav")
        engine.runAndWait()
    
    async def speak(self, ctx, voice_rate: int, voice_volume: float, voice_gender: int, *, text: str):
        # Get the voice channel the user wants the bot to join
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
        else:
            await ctx.send('goofy')

        if not channel:
            await ctx.send("Voice channel not found.")
            return

        # Join the voice channel
        voice_client = await channel.connect()

        # Play the user's text in the voice channel
        await self.text_to_speech(voice_rate, voice_volume, voice_gender, text)

        # Get the bot's voice state
        voice_state = ctx.guild.voice_client

        if voice_state:
            # Play the generated speech in the voice channel
            voice_state.play(discord.FFmpegPCMAudio("tts_output.wav"))

        # Wait until the audio is finished playing
        while voice_client.is_playing():
            await asyncio.sleep(1)
        if self.TTS_queue != []:
            self.speak(ctx, voice_rate, voice_volume, voice_gender, text)
        # Disconnect from the voice channel
        await voice_client.disconnect()

    @commands.command(name = "Dspeak")
    async def speak_base(self, ctx, *, text):
        try:
            await self.speak(self, ctx, 200, 1.0, 0, text)
        except Exception as e:
            print(e)
        finally:
            await ctx.send("An error has occured.")
        # TODO: 
        #   Fix input from discord client.

    @commands.command(name= "say")
    async def say(self, ctx, rate: int, volume: float, gender: int, *, text: str)->None:
        print("Active")
        try:
            self.TTS_queue.append(text)
            await self.speak(ctx, rate, volume, gender, text)
        except Exception as e:
            print(e)
        finally:
            await ctx.send("Something went wrong while running this command.")
        # TODO:
        #   Implement a queue system to allow multiple consective inputs to go through

