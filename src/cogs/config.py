import logging
import discord
from discord import app_commands
from discord.ext import commands
from src.database.AccountDAO import AccountDAO

logger = logging.getLogger(__name__)


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embeds_create_account = {
            "success": discord.Embed(title="✅ Account Creation", description="Account created successfully!"),
            "error": discord.Embed(title="❌ Account Creation", description="You already have an account or an error occurred."),
            "warning": discord.Embed(title="⚠️ Account Creation", description="Unexpected error occurred. Please try again later.")
        }
        
    @app_commands.command(name="c", description="Create your personal reminder account.")
    async def create_account(self, interaction: discord.Interaction):
        try:
            success = AccountDAO.addAccount(interaction.user.id)
            if success:
                await interaction.response.send_message(embed=self.embeds_create_account["success"], ephemeral=True)
            else:
                await interaction.response.send_message(embed=self.embeds_create_account["error"], ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(embed=self.embeds_create_account["warning"], ephemeral=True)
            logger.error(f"Unexpected error occurred while creating account: {e}")
            
    # @app_commands.command(name="setz", description="Set your timezone for accurate reminders.") 

async def setup(bot):
    await bot.add_cog(Config(bot))