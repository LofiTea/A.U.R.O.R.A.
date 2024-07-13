import nextcord

from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord.utils import get
from apikeys import *

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="kick", description="Kick a member")
    @has_permissions(kick_members=True)
    async def kick(self, interaction: Interaction, member: nextcord.Member, reason: str = None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f'{member.global_name} has been yeeted from the server for {reason}.')

    @kick.error
    async def kick_error(self, interaction: Interaction, error):
        if isinstance(error, nextcord.errors.Forbidden):
            await interaction.response.send_message("Hey! Stop trying to kick people out! Only I can do that!", ephemeral=True)

    @nextcord.slash_command(name="ban", description="Ban a member")
    @has_permissions(ban_members=True)
    async def ban(self, interaction: Interaction, member: nextcord.Member, reason: str = None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f'{member.global_name} has been terminated for {reason}')

    @ban.error
    async def ban_error(self, interaction: Interaction, error):
        if isinstance(error, nextcord.errors.Forbidden):
            await interaction.response.send_message("Hey! Stop trying to ban people! Are you trying to get banned?", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if "https://www.youtube.com/watch?v=dQw4w9WgXcQ" in message.content:
            await message.delete()
            await message.channel.send("Nice try, buddy. Don't do that again.")
        if any(word in message.content for word in ["fuck", "shit", "bitch"]):
            await message.delete()
            await message.channel.send("Please do not cuss. THIS IS YOUR FINAL WARNING.")

    @nextcord.slash_command(name="message", description="Send a message to a user")
    async def message(self, interaction: Interaction, user: nextcord.Member, *, message: str = "Welcome to the LT Friends Server!"):
        embed = nextcord.Embed(title=message)
        await user.send(embed=embed)
        await interaction.response.send_message(f"Message sent to {user.global_name}.", ephemeral=True)

    @nextcord.slash_command(name="add_role", description="Add a role to a member")
    @has_permissions(manage_roles=True)
    async def add_role(self, interaction: nextcord.Interaction, member: nextcord.Member, *, role_name: str):
        guild = interaction.guild
        role_object = nextcord.utils.get(guild.roles, name=role_name)
        
        if role_object is None:
            await interaction.response.send_message(f"The role '{role_name}' does not exist.", ephemeral=True)
        elif role_object in member.roles:
            await interaction.response.send_message(f"{member.global_name} already has the role {role_name}.", ephemeral=True)
        else:
            if interaction.user == guild.owner:
                await member.add_roles(role_object)
                await interaction.response.send_message(f"You assigned the role '{role_name}' to {member.global_name}.", ephemeral=True)
            else:
                if member != interaction.user:
                    await interaction.response.send_message("No.", ephemeral=True)
                elif role_object.name in ["Friend", "Best Friend"]:
                    await interaction.response.send_message("Hah, nice try.", ephemeral=True)
                else:
                    await member.add_roles(role_object)
                    await interaction.response.send_message(f"You now have the role '{role_object.name}'!", ephemeral=True)

    @add_role.error
    async def add_role_error(self, interaction: Interaction, error):
        if isinstance(error, nextcord.errors.Forbidden):
            await interaction.response.send_message("You are not allowed to have a role in this play, baka!", ephemeral=True)

    @nextcord.slash_command(name="remove_role", description="Remove a role from a member")
    @has_permissions(manage_roles=True)
    async def remove_role(self, interaction: nextcord.Interaction, member: nextcord.Member, *, role_name: str):
        guild = interaction.guild
        role_object = nextcord.utils.get(guild.roles, name=role_name)
        
        if role_object is None:
            await interaction.response.send_message(f"The role '{role_name}' doesn't exist.", ephemeral=True)
        elif role_object not in member.roles:
            await interaction.response.send_message(f"{member.global_name} doesn't have the role {role_name}.", ephemeral=True)
        else:
            if interaction.user == guild.owner:
                await member.remove_roles(role_object)
                await interaction.response.send_message(f"You removed the role '{role_name}' from {member.global_name}.", ephemeral=True)
            else:
                if member != interaction.user:
                    await interaction.response.send_message("No.", ephemeral=True)
                elif role_object.name in ["Friend", "Best Friend"]:
                    await interaction.response.send_message("What do you think you are doing?", ephemeral=True)
                else:
                    await member.remove_roles(role_object)
                    await interaction.response.send_message(f"You removed the role '{role_name}'.", ephemeral=True)

    @remove_role.error
    async def remove_role_error(self, interaction: Interaction, error):
        if isinstance(error, nextcord.errors.Forbidden):
            await interaction.response.send_message("Oh, come on! Why are you trying to quit the play?", ephemeral=True)

def setup(client):
    client.add_cog(Admin(client))