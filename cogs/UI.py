import nextcord

from nextcord.ext import commands
from nextcord import Interaction

class CoffeeOrTea(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
        self.value = None

    @nextcord.ui.button(label = "Coffee", style = nextcord.ButtonStyle.red)
    async def coffee(self, button: nextcord.ui.Button, interaction = Interaction):
        await interaction.response.send_message('Inferior.', ephemeral=True)
        self.value = True

    @nextcord.ui.button(label = "Tea", style = nextcord.ButtonStyle.green)
    async def tea(self, button: nextcord.ui.Button, interaction = Interaction):
        await interaction.response.send_message('Superior!', ephemeral=True)
        self.value = False

class Dropdown(nextcord.ui.Select):
    def __init__(self):
        select_options = [
            nextcord.SelectOption(label="Henry", description="LT Friend 1"),
            nextcord.SelectOption(label="Harmon", description="LT Friend 2"),
            nextcord.SelectOption(label="Melody", description="LT Friend 3"),
            nextcord.SelectOption(label="Orion", description="LT Friend 4"),
            nextcord.SelectOption(label="Aurora", description="LT Friend 5"),
            nextcord.SelectOption(label="Cyprus", description="LT Friend 6"),
            nextcord.SelectOption(label="Raella", description="LT Friend 7")
        ]
        super().__init__(placeholder="LT Friends Options", min_values=1, max_values=1, options=select_options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "Henry":
            return await interaction.response.send_message("Error 404 again?")
        elif self.values[0] == "Harmon":
            return await interaction.response.send_message("No more Gatorade!")
        elif self.values[0] == "Melody":
            return await interaction.response.send_message("Totally not a cat")
        elif self.values[0] == "Orion":
            return await interaction.response.send_message("Secretly simping on Melody")
        elif self.values[0] == "Aurora":
            return await interaction.response.send_message("Stop spraypainting on my stuff...")
        elif self.values[0] == "Cyprus":
            return await interaction.response.send_message("No, you are not waking up Raella!")
        elif self.values[0] == "Raella":
            return await interaction.response.send_message("Zzz...")

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class UI(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name = "coffee_or_tea_button", description = "Coffee VS Tea button")
    async def coffee_or_tea_button(self, interaction = Interaction):
        view = CoffeeOrTea()
        await interaction.response.send_message("Choose a drink: ", view = view)
        await view.wait()

        if view.value is None:
            return

    @nextcord.slash_command(name = "lt_friends_dropdown", description = "Meet the LT Friends!")
    async def drop(self, interaction: Interaction):
        view = DropdownView()
        await interaction.response.send_message("Which LT Friend do you want to meet? ", view = view)

def setup(client):
    client.add_cog(UI(client))