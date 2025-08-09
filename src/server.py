import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Eida(commands.Bot):
    async def setup_hook(self):
        extensions = ["config", "dashboard", "help", "reminder"]
        for extension in extensions:
            await self.load_extension(f"src.cogs.{extension}")

bot = Eida(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="👁️ Eida's clairvoyance"))
    logger.info(f"{bot.user} is now running.")
    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        logger.error("An error with syncing commands has occurred: ", e)

@bot.hybrid_command()
async def hello(ctx):
    await ctx.send("Hello !")

bot.run(os.getenv("TOKEN"))