import discord

from discord.ext import commands # Cogs commands
from discord import app_commands # Slash commands

from src.database.AccountDAO import AccountDAO

class CreateAccountCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="c", description="Create a new account to start using Eida's reminder features.")
    async def create_account(self, interaction: discord.Interaction):
        try:
            success = AccountDAO.addAccount(interaction.user.id)

            if success:
                await interaction.response.send_message("✔️ Account created successfully !", ephemeral=True)
            else:
                await interaction.response.send_message("✖️ You already have an account or an error occurred during creation.", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message("⚠️ Unexpected error occurred. Please try again later.", ephemeral=True)
            print(f"Unexpected error: {e}")
