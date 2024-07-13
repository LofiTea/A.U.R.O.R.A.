import nextcord

from nextcord import Interaction
from nextcord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="test", description="Introduction to Slash Commands")
    async def test(self, interaction: Interaction):
        await interaction.response.send_message("Hello! A.U.R.O.R.A. here!")

    @nextcord.slash_command(name="hello", description="Say hello")
    async def hello(self, interaction: Interaction):
        player_name = interaction.user.global_name
        await interaction.response.send_message(f"Hi there, {player_name}! Did Charlie Brown finally hit that football?")

    @nextcord.slash_command(name="goodbye", description="Say goodbye")
    async def goodbye(self, interaction: Interaction):
        await interaction.response.send_message("Goodbye. Always remember cereal is a soup!")

    @nextcord.slash_command(name="embed", description="Send an embed message")
    async def embed(self, interaction: Interaction):
        embed = nextcord.Embed(title="LofiTea Friends", description="Take a look at the members", color=0x00ff00)
        author_avatar_url = interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url
        embed.set_author(name=interaction.user.global_name, url="https://www.youtube.com/channel/UCuiVwtzLsd0npFIUkFD-LdA", icon_url=author_avatar_url)
        embed.set_thumbnail(url="https://i.postimg.cc/XN2SYsS5/LofiTea.png")
        embed.add_field(name="Henry", value="Programmer", inline=True)
        embed.add_field(name="Harmon", value="DJ", inline=True)
        embed.add_field(name="Melody", value="Idol", inline=True)
        embed.add_field(name="Orion", value="Guitarist", inline=True)
        embed.add_field(name="Aurora", value="Painter", inline=True)
        embed.add_field(name="Cyprus", value="Gamer", inline=True)
        embed.add_field(name="Raella", value="Reader", inline=True)
        embed.set_footer(text="Time to sleep...")
        await interaction.response.send_message(embed=embed)

def setup(client):
    client.add_cog(Greetings(client))