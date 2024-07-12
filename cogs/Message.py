import nextcord
import requests

from nextcord import Interaction
from nextcord.ext import commands
from apikeys import *

class Message(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        url = "https://icanhazdadjoke.com/"
        headers = {
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        joke_data = response.json()
        joke_text = joke_data.get("joke", "Couldn't fetch a joke!")

        channel = self.client.get_channel(CHANNEL_ID)
        await channel.send(f"Hello, {member.display_name}! Did you find Waldo?")
        await channel.send(joke_text)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(CHANNEL_ID)
        await channel.send(f"{member.display_name} has been kicked from the server.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(user.display_name + " added: " + reaction.emoji)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(user.display_name + " removed: " + reaction.emoji)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
    
        if "happy" in message.content:
            emoji = '😄'
            await message.add_reaction(emoji)

    @nextcord.slash_command(name="henry", description="Send a message about Henry")
    async def henry(self, interaction: Interaction):
        await interaction.response.send_message("Stop playing Genshin Impact!")

    @nextcord.slash_command(name="harmon", description="Send a message about Harmon")
    async def harmon(self, interaction: Interaction):
        await interaction.response.send_message("When will he get a boyfriend?")

    @nextcord.slash_command(name="melody", description="Send a message about Melody")
    async def melody(self, interaction: Interaction):
        await interaction.response.send_message("Ah, yes, the wanna-be idol.")

    @nextcord.slash_command(name="orion", description="Send a message about Orion")
    async def orion(self, interaction: Interaction):
        await interaction.response.send_message("What did he do this time?")

    @nextcord.slash_command(name="aurora", description="Send a message about Aurora")
    async def aurora(self, interaction: Interaction):
        await interaction.response.send_message("My alter-ego is probably talking about Marxism again...")

    @nextcord.slash_command(name="cyprus", description="Send a message about Cyprus")
    async def cyprus(self, interaction: Interaction):
        await interaction.response.send_message("Quick! Someone take away his sword!")

    @nextcord.slash_command(name="raella", description="Send a message about Raella")
    async def raella(self, interaction: Interaction):
        await interaction.response.send_message("She's been sleeping for 16 hours now...")

    @nextcord.slash_command(name="among_us", description="Send a message about Among Us")
    async def among_us(self, interaction: Interaction):
        await interaction.response.send_message("SUS.")

    @nextcord.slash_command(name="lofi", description="Send a message about Lofi")
    async def lofi(self, interaction: Interaction):
        await interaction.response.send_message("Time to chill...")

    @nextcord.slash_command(name="october_31st", description="Send a message about October 31st")
    async def october_31st(self, interaction: Interaction):
        await interaction.response.send_message("Is it my birthday or is it Aurora's birthday?")

    @nextcord.slash_command(name="slap", description="Send a message about Slap")
    async def slap(self, interaction: Interaction):
        await interaction.response.send_message("Stop! It hurts!")

    @nextcord.slash_command(name="coffee_over_tea", description="Send a message about Coffee over Tea")
    async def coffee_over_tea(self, interaction: Interaction):
        await interaction.response.send_message("YOU MONSTER. YOU MUST DIE NOW.")

def setup(client):
    client.add_cog(Message(client))