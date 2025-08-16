import logging
import discord
from discord import app_commands
from discord.ext import commands
from src.modals.remind_meModal import RemindMeModal

logger = logging.getLogger(__name__)


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="remindme", description="Remind yourself about something later.")
    async def remind_me(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RemindMeModal())
        
async def setup(bot):
    await bot.add_cog(ReminderCog(bot))