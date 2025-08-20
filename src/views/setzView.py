import discord
from src.modals.setzModal import SetzModal


class SetzView(discord.ui.View):
    """Simple view for initiating timezone configuration through a modal"""
    
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Set timezone", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetzModal())
