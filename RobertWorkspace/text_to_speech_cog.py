from discord.abc import Connectable
import pyttsx3
import discord
from discord.ext import commands
import asyncio
import tracemalloc

tracemalloc.start()
class VoiceClient(discord.voice_client.VoiceClient):
    def __init__(self, client: discord.Client, channel: Connectable) -> None:
        super().__init__(client, channel)

class TextToSpeech(commands.Cog):
    engine = pyttsx3.init()
    def __init__(self, client):
        self.client = client
        self.TTS_queue : list[str] = []

    async def join_vc(self, ctx) -> VoiceClient:
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

    async def text_to_speech(self, rate: int, volume: float, speakGender: bool, text: str):
        """Converts text to audible speech contained in "tts_output.wav" 

        Args:
            rate (_type_): _description_
            volume (_type_): _description_
            speakGender (_type_): _description_
            text (_type_): _description_
        """
        engine = TextToSpeech.engine
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume) 
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[speakGender].id)
        
        # Use pyttsx3 to convert text to speech
        engine.save_to_file(text, "tts_output.wav")
        engine.runAndWait()
    
    async def speak(self, ctx, voice_client: VoiceClient, voice_rate, voice_volume, voice_gender, text):
        try:
            await self.text_to_speech(voice_rate, voice_volume, voice_gender, text)

            # Get the bot's voice state and play the generated audio in the voice channel
            voice_state = ctx.guild.voice_client
            if voice_state:
                voice_state.play(discord.FFmpegPCMAudio("tts_output.wav"))
            while voice_client.is_playing():
                await asyncio.sleep(1)

            print(f"Queue Length: {len(self.TTS_queue)} \nQueue: {self.TTS_queue}")
            if len(self.TTS_queue) > 1:
                self.TTS_queue.pop(0)
                await self.speak(ctx, voice_client, voice_rate, voice_volume, voice_gender, self.TTS_queue[0])
            
            await voice_client.disconnect()
            self.TTS_queue.clear()

        except Exception as error:
            print(f"An error has occured: {error}")

    @commands.command(name= "say")
    async def say(self, ctx, rate: int, volume: float, gender: int, *, text: str):
        print("TTS intiated...  \n")
        self.TTS_queue.append(text)
        print(f"Queue Length: {len(self.TTS_queue)} \nQueue: {self.TTS_queue}")
        try:
            voice_client = await self.join_vc(ctx)
            print(f"voice client is a {type(voice_client)}")
            if not voice_client.is_playing():
                await self.speak(ctx, voice_client, rate, volume, gender, text)
        except Exception as error:
            print(error)

    @commands.command(name = "Dspeak")
    async def speak_base(self, ctx, *, text):
        print("TTS intiated...  \n")
        self.TTS_queue.append(text)
        print(f"Queue Length: {len(self.TTS_queue)} \nQueue: {self.TTS_queue}")
        try:
            voice_client = await self.join_vc(ctx)
            await self.speak(ctx, voice_client, 200, 1.0, 0, text)
        except Exception as error:
            print(error)

    @commands.command(name = "queue")
    async def queue(self, ctx, ):
        await ctx.send(self.TTS_queue)