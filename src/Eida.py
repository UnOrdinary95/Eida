import discord
from discord.ext import commands


class Eida(commands.Bot):
    async def setup_hook(self):
        extensions = ["configCog", "dashboardCog", "helpCog", "reminderCog"]
        for extension in extensions:
            await self.load_extension(f"src.cogs.{extension}")


bot = Eida(command_prefix="!", intents=discord.Intents.all())
