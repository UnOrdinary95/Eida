import logging
import asyncio
from datetime import datetime
import discord
from discord.ext import tasks
from src.database.ReminderDAO import ReminderDAO
from src.models.Reminder import Reminder
from src.Eida import bot

logger = logging.getLogger(__name__)


@tasks.loop(minutes=1)
async def check_reminders():
    """
    Check for due reminders every minute and process them.
    1-minute interval ensures reminders are sent promptly without excessive database queries.
    """
    try:
        now = datetime.now()
        due_reminders = ReminderDAO.get_due_reminders(now)

        logger.info(f"Found {len(due_reminders)} due reminders")
        for reminder in due_reminders:
            await send_reminder_to_user(reminder)
            # Update recurring reminders to their next occurrence after successful send
            if reminder.intervals:
                ReminderDAO.update_reminder_date_time(reminder)
    except Exception as e:
        logger.error(f"Error checking reminders: {e}")


async def send_reminder_to_user(reminder: Reminder):
    """
    Send reminder message to user via DM.
    """
    try:
        user = await bot.fetch_user(reminder.user_id)
        if user:
            await user.send(reminder.message)
            logger.info(f"Reminder sent to {user.name} ({user.id})")
        else:
            logger.warning(f"User {reminder.user_id} not found")
    except discord.NotFound:
        # User account deleted or invalid ID - permanent failure
        logger.error(f"User {reminder.user_id} not found")
    except discord.Forbidden:
        # User has DMs disabled or blocked bot - expected behavior, not critical
        logger.error(f"Cannot send DM to user {reminder.user_id}")
    except Exception as e:
        # Unexpected errors that might indicate system issues
        logger.error(f"Error sending reminder to {reminder.user_id}: {e}")


async def wait_until_next_minute():
    """
    Synchronize task startup to minute boundaries for consistent reminder timing.
    Prevents reminders from being delayed by bot restart timing.
    """
    now = datetime.now()
    second_to_wait = 60 - now.second
    logger.info("Waiting until next minute...")
    await asyncio.sleep(second_to_wait)
    logger.info(f"Next minute reached -> {datetime.now()}")
