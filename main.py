import asyncio
import os
import nextcord

from nextcord.ext import commands
from apikeys import *

intents = nextcord.Intents.default()
intents.members = True
intents.messages = True

client = commands.Bot(command_prefix='!', intents = nextcord.Intents.all())

# Loads all of the cog files
def load_extensions():
    for filename in os.listdir('/cogs'): # May need to change area
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Streaming(name='Minecraft', url='https://www.twitch.tv/lofitea1'))
    print("The bot is now ready for use!")
    print("------------------------------")

load_extensions()

async def main():
    await client.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())