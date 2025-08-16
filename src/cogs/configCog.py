import logging
import discord
from discord import app_commands
from discord.ext import commands
from src.database.AccountDAO import AccountDAO
from src.views.setzView import SetzView

logger = logging.getLogger(__name__)


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embeds_create_account = {
            "success": discord.Embed(
                title="✅ Account Creation", description="Account created successfully!"
            ),
            "error": discord.Embed(
                title="❌ Account Creation",
                description="You already have an account or an error occurred.",
            ),
            "warning": discord.Embed(
                title="⚠️ Account Creation",
                description="Unexpected error occurred. Please try again later.",
            ),
        }
        self.embeds_set_timezone = {
            "url": discord.Embed(
                title="🕰️ Timezone Setup",
                description="You can see the complete list of timezones in the link below ⬇️\n"
                "https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568\n\n"
                "Please enter your timezone.",
            ),
            "error": discord.Embed(
                title="❌ Timezone Setup",
                description="You need to create an account!\nPlease use **/c**.",
            ),
        }

    @app_commands.command(
        name="c", description="Create your personal reminder account."
    )
    async def create_account(self, interaction: discord.Interaction):
        try:
            success = AccountDAO.add_account(interaction.user.id)
            if success:
                await interaction.response.send_message(
                    embed=self.embeds_create_account["success"], ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=self.embeds_create_account["error"], ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                embed=self.embeds_create_account["warning"], ephemeral=True
            )
            logger.error(f"Unexpected error occurred while creating account: {e}")

    @app_commands.command(
        name="settimezone", description="Set your timezone for accurate reminders."
    )
    async def set_timezone(self, interaction: discord.Interaction):
        if AccountDAO.account_exists(interaction.user.id):
            await interaction.response.send_message(
                embed=self.embeds_set_timezone["url"], view=SetzView(), ephemeral=True
            )
        else:
            await interaction.response.send_message(
                embed=self.embeds_set_timezone["error"], ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Config(bot))
