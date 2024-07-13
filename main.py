import os
import nextcord

from nextcord.ext import commands
from apikeys import *

intents = nextcord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

def load_extensions():
    for filename in os.listdir('/Users/henrylee/Desktop/Python Stuff/DiscordBot/venv/cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Streaming(name='Minecraft', url='https://www.twitch.tv/lofitea1'))
    print("The bot is now ready for use!")
    print("------------------------------")

load_extensions()
client.run(BOT_TOKEN)