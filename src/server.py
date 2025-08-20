import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
from src.Eida import bot
from src.tasks import reminderTask

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="👁️ Eida's clairvoyance"
        )
    )
    logger.info(f"{bot.user} is now running.")
    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Synced {len(synced_commands)} commands.")
        if not reminderTask.check_reminders.is_running():
            await reminderTask.wait_until_next_minute()
            reminderTask.check_reminders.start()
            logger.info("Reminder task started")
    except Exception as e:
        logger.error("An error with syncing commands has occurred: ", e)


@bot.hybrid_command()
async def hello(ctx):
    await ctx.send("Hello !")


bot.run(os.getenv("TOKEN"))
