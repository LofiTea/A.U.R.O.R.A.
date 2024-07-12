import nextcord
import yt_dlp
import os

from nextcord import Interaction
from nextcord.ext import commands
from nextcord import FFmpegOpusAudio

queues = {}

async def check_queue(interaction, client, guild_id):
    if queues[guild_id]:
        voice = interaction.guild.voice_client
        source = queues[guild_id].pop(0)
        voice.play(source, after=lambda x=None: client.loop.create_task(check_queue(interaction, client, guild_id)))

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="join", description="Join the voice channel")
    async def join(self, interaction: nextcord.Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
            mp3_path = '/Users/henrylee/Desktop/Python Stuff/DiscordBot/venv/audio/fire-in-the-hole.mp3'
            source = FFmpegOpusAudio(mp3_path)
            voice.play(source)
            await interaction.response.send_message("FIRE IN THE HOLE!")
        else:
            await interaction.response.send_message("Are you dumb? You're not in a voice channel!")

    @nextcord.slash_command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: nextcord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Bye nerds! I left the voice channel!")
        else:
            await interaction.response.send_message("Aww. I'm not in a voice channel.")

    @nextcord.slash_command(name="pause", description="Pause the current audio")
    async def pause(self, interaction: nextcord.Interaction):
        voice = nextcord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice and voice.is_playing():
            voice.pause()
            await interaction.response.send_message("Audio paused.")
        else:
            await interaction.response.send_message("Stop it! It hurts!")

    @nextcord.slash_command(name="resume", description="Resume the paused audio")
    async def resume(self, interaction: nextcord.Interaction):
        voice = nextcord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice and voice.is_paused():
            voice.resume()
            await interaction.response.send_message("Audio resumed.")
        else:
            await interaction.response.send_message("Bah humbug! No audio is being played!")

    @nextcord.slash_command(name="stop", description="Stop the current audio")
    async def stop(self, interaction: nextcord.Interaction):
        voice = interaction.guild.voice_client
        if voice is None:
            await interaction.response.send_message("I'm not playing anything, idiot!")
        else:
            voice.stop()
            await interaction.response.send_message("Audio stopped.")

    @nextcord.slash_command(name="play", description="Play audio from a URL or local file")
    async def play(self, interaction: nextcord.Interaction, arg: str):
        if interaction.user.voice:
            voice_channel = interaction.user.voice.channel
            voice = interaction.guild.voice_client

            if voice is None:
                voice = await voice_channel.connect()
            elif not voice.is_connected():
                await voice.move_to(voice_channel)

            if "youtube.com" in arg or "youtu.be" in arg:
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(arg, download=False)
                    audio_url = info['url']
                source = FFmpegOpusAudio(audio_url)
            else:
                audio_folder = 'audio'
                file_path = os.path.join(audio_folder, arg)
                if not os.path.isfile(file_path):
                    await interaction.response.send_message(f"The file `{arg}` does not exist!!! Stupid!")
                    return
                source = FFmpegOpusAudio(file_path)

            if voice.is_playing():
                guild_id = interaction.guild.id
                if guild_id in queues:
                    queues[guild_id].append(source)
                else:
                    queues[guild_id] = [source]
                await interaction.response.send_message("The song has been added!")
            else:
                voice.play(source, after=lambda x=None: self.client.loop.create_task(check_queue(interaction, interaction.guild.id)))
                await interaction.response.send_message("Now playing greatness.")
        else:
            await interaction.response.send_message("I'm not in a voice channel, stupid!")

    @nextcord.slash_command(name="queue", description="Queue audio from a URL or local file")
    async def queue(self, interaction: nextcord.Interaction, arg: str):
        if interaction.user.voice:
            voice_channel = interaction.user.voice.channel
            voice = interaction.guild.voice_client

            if voice is None:
                voice = await voice_channel.connect()
            elif not voice.is_connected():
                await voice.move_to(voice_channel)

            if "youtube.com" in arg or "youtu.be" in arg:
                ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(arg, download=False)
                    audio_url = info['url']
                source = FFmpegOpusAudio(audio_url)
            else:
                audio_folder = 'audio'
                file_path = os.path.join(audio_folder, arg)
                if not os.path.isfile(file_path):
                    await interaction.response.send_message(f"The file `{arg}` does not exist! Sigh.")
                    return
                source = FFmpegOpusAudio(file_path)

            guild_id = interaction.guild.id
            if guild_id in queues:
                queues[guild_id].append(source)
            else:
                queues[guild_id] = [source]

            await interaction.response.send_message("The song has been added to the queue!")
        else:
            await interaction.response.send_message("I'm not in a voice channel, stupid!")

def setup(client):
    client.add_cog(Music(client))