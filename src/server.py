import discord
import os
from dotenv import load_dotenv
import logging
from src.Eida import bot
from src.tasks import reminderTask

# Load environment variables from .env file for secure token storage
load_dotenv()

# Configure logging to both file and console for debugging and monitoring
# File logging preserves history, console logging provides real-time feedback
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


@bot.event
async def on_ready():
    # Set bot's Discord status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="👁️ Eida's clairvoyance"
        )
    )
    logger.info(f"{bot.user} is now running.")
    try:
        # Sync slash commands with Discord's API to make them available
        synced_commands = await bot.tree.sync()
        logger.info(f"Synced {len(synced_commands)} commands.")

        # Start reminder task only if not already running to avoid duplicates
        if not reminderTask.check_reminders.is_running():
            # Wait until next minute boundary for consistent reminder timing
            await reminderTask.wait_until_next_minute()
            reminderTask.check_reminders.start()
            logger.info("Reminder task started")
    except Exception as e:
        logger.error("An error with syncing commands has occurred: ", e)


bot.run(os.getenv("TOKEN"))
