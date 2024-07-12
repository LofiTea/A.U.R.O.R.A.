import nextcord
import yt_dlp
import os

from nextcord import Interaction
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio

queues = {}

async def check_queue(interaction, client, guild_id):
    if queues[guild_id]:
        voice = interaction.guild.voice_client
        source = queues[guild_id].pop(0)
        voice.play(source, after=lambda x=None: client.loop.create_task(check_queue(interaction, client, guild_id)))

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="join", description="Join a voice channel")
    async def join(self, interaction: Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice = await channel.connect()
            mp3_path = '/audio/fire-in-the-hole.mp3'
            source = FFmpegPCMAudio(mp3_path)
            voice.play(source)
            await interaction.response.send_message(f"Joined {channel.name} and started playing sound!")
        else:
            await interaction.response.send_message("Are you dumb? You're not in a voice channel!", ephemeral=True)

    @nextcord.slash_command(name="leave", description="Leave the voice channel")
    async def leave(self, interaction: Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Bye nerds! I left the voice channel!")
        else:
            await interaction.response.send_message("Aww. I'm not in a voice channel.", ephemeral=True)

    @nextcord.slash_command(name="play", description="Play a song from YouTube or local file")
    async def play(self, interaction: Interaction, arg: str):
        if not interaction.user.voice:
            await interaction.response.send_message("I'm not in a voice channel, stupid!", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel
        voice = interaction.guild.voice_client
        if voice is None:
            voice = await voice_channel.connect()
        elif not voice.is_connected():
            await voice.move_to(voice_channel)

        if "youtube.com" in arg or "youtu.be" in arg:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(arg, download=False)
                audio_url = info['url']
            source = FFmpegPCMAudio(audio_url)
        else:
            audio_folder = '/Users/henrylee/Desktop/Python Stuff/DiscordBot/venv/audio'
            file_path = os.path.join(audio_folder, arg)
            if not os.path.isfile(file_path):
                await interaction.response.send_message(f"The file `{arg}` does not exist!!! Stupid!", ephemeral=True)
                return
            source = FFmpegPCMAudio(file_path)

        if voice.is_playing():
            guild_id = interaction.guild.id
            if guild_id in queues:
                queues[guild_id].append(source)
            else:
                queues[guild_id] = [source]
            await interaction.response.send_message("The song has been added to the queue!")
        else:
            voice.play(source, after=lambda x=None: self.client.loop.create_task(check_queue(interaction, self.client, interaction.guild.id)))
            await interaction.response.send_message("Started playing the song!")

    @nextcord.slash_command(name="pause", description="Pause the current song")
    async def pause(self, interaction: Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("Be in a voice channel first, idiot!", ephemeral=True)
            return

        voice = nextcord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice and voice.is_playing():
            voice.pause()
            await interaction.response.send_message("Paused the current song.")
        else:
            await interaction.response.send_message("Stop it! It hurts!", ephemeral=True)

    @nextcord.slash_command(name="resume", description="Resume the paused song")
    async def resume(self, interaction: Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("Be in a voice channel first, idiot!", ephemeral=True)
            return

        voice = nextcord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if voice and voice.is_paused():
            voice.resume()
            await interaction.response.send_message("Resumed the song.")
        else:
            await interaction.response.send_message("Bah humbug! No audio is being played!", ephemeral=True)

    @nextcord.slash_command(name="stop", description="Stop the current song")
    async def stop(self, interaction: Interaction):
        voice = interaction.guild.voice_client
        if voice is None:
            await interaction.response.send_message("I'm not playing anything, idiot!", ephemeral=True)
            return
        voice.stop()
        await interaction.response.send_message("Stopped the song.")

def setup(client):
    client.add_cog(Music(client))