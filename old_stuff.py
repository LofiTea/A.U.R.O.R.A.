import discord
import requests
import yt_dlp
import os

from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import FFmpegPCMAudio
from discord import Member
from apikeys import *

queues = {}

async def check_queue(ctx, guild_id):
    if queues[guild_id]:
        voice = ctx.guild.voice_client
        source = queues[guild_id].pop(0)
        voice.play(source, after=lambda x=None: client.loop.create_task(check_queue(ctx, guild_id)))

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name='Minecraft', url='https://www.twitch.tv/lofitea1'))
    print("The bot is now ready for use!")
    print("------------------------------")

@client.command()
async def hello(ctx):
    player_name = ctx.author.display_name
    await ctx.send(f"Hi there, {player_name}! Did Charlie Brown finally hit that football?")

@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye.  Always remember cereal is a soup!")

@client.event
async def on_member_join(member):
    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    joke_data = response.json()
    joke_text = joke_data.get("joke", "Couldn't fetch a joke!")

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(f"Hello, {member.display_name}! Did you find Waldo?")
    await channel.send(joke_text)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(f"{member.display_name} has been yeeted from the server.")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        mp3_path = '/Users/henrylee/Desktop/Python Stuff/DiscordBot/venv/audio/fire-in-the-hole.mp3'
        source = FFmpegPCMAudio(mp3_path)
        player = voice.play(source)
    else:
        await ctx.send("Are you dumb?  You're not in a voice channel!")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Bye nerds!  I left the voice channel!")
    else:
        await ctx.send("Aww.  I'm not in a voice channel.")

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild = ctx.guild)
    if (voice.is_playing()):
        voice.pause()
    else:
        await ctx.send("Stop it!  It hurts!")

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if (voice.is_paused()):
        voice.resume()
    else:
        await ctx.send("Bah hambug!  No audio is being played!")

@client.command(pass_context=True)
async def stop(ctx):
    voice = ctx.guild.voice_client
    if voice is None:
        await ctx.send("I'm not playing anything, idiot!")
        return
    voice.stop()

@client.command(pass_context=True)
async def play(ctx, *, arg):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("I'm not in a voice channel, stupid!")
        return

    voice = ctx.guild.voice_client
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
        audio_folder = 'audio'
        file_path = os.path.join(audio_folder, arg)
        if not os.path.isfile(file_path):
            await ctx.send(f"The file `{arg}` does not exist!!!  Stupid!")
            return
        source = FFmpegPCMAudio(file_path)

    if voice.is_playing():
        guild_id = ctx.message.guild.id
        if guild_id in queues:
            queues[guild_id].append(source)
        else:
            queues[guild_id] = [source]
        await ctx.send("The song has bene added!")
    else:
        voice.play(source, after=lambda x=None: client.loop.create_task(check_queue(ctx, ctx.message.guild.id)))

@client.command(pass_context=True)
async def queue(ctx, *, arg):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.send("I'm not in a voice channel, stupid!")
        return

    voice = ctx.guild.voice_client
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
        audio_folder = 'audio'
        file_path = os.path.join(audio_folder, arg)
        if not os.path.isfile(file_path):
            await ctx.send(f"The file `{arg}` does not exist!  Sigh.")
            return
        source = FFmpegPCMAudio(file_path)

    guild_id = ctx.message.guild.id
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]

    await ctx.send("The song has been!")

@client.event
async def on_message(message):
    if "https://www.youtube.com/watch?v=dQw4w9WgXcQ" in message.content:
        await message.delete()
        await message.channel.send("Nice try, buddy. Don't do that again.")
    if "fuck" in message.content:
        await message.delete()
        await message.channel.send("Please do not cuss.  THIS IS YOUR FINAL WARNING.")
    if "shit" in message.content:
        await message.delete()
        await message.channel.send("Please do not cuss.  THIS IS YOUR FINAL WARNING.")
    if "bitch" in message.content:
        await message.delete()
        await message.channel.send("Please do not cuss.  THIS IS YOUR FINAL WARNING.")
    await client.process_commands(message)

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.display_name} has been yeeted from the server for {reason}.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("Hey! Stop trying to kick people out! Only I can do that!")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.display_name} has been terminated for {reason}')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("Hey! Stop trying to ban people! Are you trying to get banned?")

@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Example Embed", description="This is an example embed", color=0x00ff00)
    author_avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    embed.set_author(name=ctx.author.display_name, url="https://www.youtube.com/channel/UCuiVwtzLsd0npFIUkFD-LdA", icon_url=author_avatar_url)
    embed.set_thumbnail(url="https://i.postimg.cc/XN2SYsS5/LofiTea.png")
    embed.add_field(name="Labradore", value="Cute dogs", inline=True)
    embed.add_field(name="Pugs", value="Cute dogs", inline=True)
    embed.set_footer(text="Thank you for reading")
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("What do you think you are doing?")

@ban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("What do you think you are doing?")

@client.command()
async def message(ctx, user:discord.Member, *, message=None):
    message = "Welcome to the LT Friends Server!"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

@client.command()
async def henry(ctx):
    await ctx.send("Stop playing Genshin Impact!")

@client.command()
async def harmon(ctx):
    await ctx.send("When will he get a boyfriend?")

@client.command()
async def melody(ctx):
    await ctx.send("Ah, yes, the wanna-be idol.")

@client.command()
async def orion(ctx):
    await ctx.send("What did he do this time?")

@client.command()
async def aurora(ctx):
    await ctx.send("My alter-ego is probably talking about Marxism again...")

@client.command()
async def cyprus(ctx):
    await ctx.send("Quick! Someone take away his sword!")

@client.command()
async def raella(ctx):
    await ctx.send("She's been sleeping for 16 hours now...")

@client.command()
async def amongus(ctx):
    await ctx.send("SUS.")

@client.command()
async def lofi(ctx):
    await ctx.send("Time to chill...")
    
@client.command()
async def october31st(ctx):
    await ctx.send("Is it my birthday or is it Aurora's birthday?")

@client.command()
async def slap(ctx):
    await ctx.send("Stop!  It hurts!")

@client.command()
async def coffeeovertea(ctx):
    await ctx.send("YOU MONSTER.  YOU MUST DIE NOW.")

client.run(BOT_TOKEN)