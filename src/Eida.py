import discord
from discord.ext import commands


class Eida(commands.Bot):
    """Custom bot class extending commands.Bot to encapsulate initialization logic"""

    async def setup_hook(self):
        """
        Called after bot login but before on_ready event.
        Perfect timing for loading cogs without blocking the ready event.
        """
        # Define all cogs that provide the bot's core functionality
        extensions = ["configCog", "dashboardCog", "helpCog", "reminderCog"]

        # Load each cog asynchronously to avoid blocking startup
        for extension in extensions:
            await self.load_extension(f"src.cogs.{extension}")


# Create bot instance with all intents for full Discord API access
# Command prefix "!" maintained for hybrid command compatibility
bot = Eida(command_prefix="!", intents=discord.Intents.all())
