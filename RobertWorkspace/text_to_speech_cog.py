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

    async def join_vc(self, ctx):
        '''
        Joins the author's voice channel
        '''
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
        else:
            await ctx.send('User was not found in any voice channel.')

        if not channel:
            await ctx.send("Voice channel not found.")
            return 
        return await channel.connect()


    async def text_to_speech(self, rate, volume, speakGender, text):
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
    
    async def speak(self, ctx, voice_client, voice_rate, voice_volume, voice_gender, text):
        try:
            await self.text_to_speech(voice_rate, voice_volume, voice_gender, text)

            # Get the bot's voice state and play the generated audio in the voice channel
            voice_state = ctx.guild.voice_client
            if voice_state:
                voice_state.play(discord.FFmpegPCMAudio("tts_output.wav"))
            while voice_client.is_playing(): # Wait until the audio is finished playing
                await asyncio.sleep(1)

            if len(self.TTS_queue) > 1:
                await self.speak(ctx, voice_rate, voice_volume, voice_gender, self.TTS_queue[0])
                self.TTS_queue.pop(0)

            # Disconnect from the voice channel
            await voice_client.disconnect()

        except Exception as error:
            print(f"An error has occured: {error}")

    @commands.command(name= "say")
    async def say(self, ctx, rate: int, volume: float, gender: int, *, text: str):
        print("TTS intiated...  \n")
        try:
            voice_client = await self.join_vc(self, ctx)
            self.TTS_queue.append(text)
            if not voice_client.is_playing():
                await self.speak(ctx, voice_client, rate, volume, gender, text)
        except Exception as e:
            print(e)

    @commands.command(name = "Dspeak")
    async def speak_base(self, ctx, *, text):
        try:
            await self.speak(ctx, 200, 1.0, 0, text)
        except Exception as e:
            print(e)