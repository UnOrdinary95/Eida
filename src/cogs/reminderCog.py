import logging
import discord
from discord import app_commands
from discord.ext import commands
from src.modals.remind_meModal import RemindMeModal
from src.database.AccountDAO import AccountDAO
from src.database.ReminderDAO import ReminderDAO
from src.modals.setmsgModal import SetMsgModal
from src.models.Reminder import Reminder
from datetime import datetime

logger = logging.getLogger(__name__)


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embeds_no_account = discord.Embed(
            title="❌ No Account",
            description="You need to create an account!\nPlease use **/c**.",
        )
        self.embeds_no_reminder = discord.Embed(
            title="❌ No Reminder",
            description="There is no reminder with this name.",
        )
        self.embeds_settime = {
            "success": discord.Embed(
                title="✅ Reminder Time Updated",
                description="Reminder time updated successfully!",
            ),
            "error": discord.Embed(
                title="❌ Reminder Time Update",
                description="An error occurred while updating the reminder time.",
            ),
            "warning": discord.Embed(
                title="⚠️ Reminder Time Update",
                description="Unexpected error occurred. Please try again later.",
            ),
        }
        self.embeds_setdate = {
            "success": discord.Embed(
                title="✅ Reminder Date Updated",
                description="Reminder date updated successfully!",
            ),
            "error": discord.Embed(
                title="❌ Reminder Date Update",
                description="An error occurred while updating the reminder date.",
            ),
            "warning": discord.Embed(
                title="⚠️ Reminder Date Update",
                description="Unexpected error occurred. Please try again later.",
            ),
        }
        self.embeds_setname = {
            "success": discord.Embed(
                title="✅ Reminder Name Updated",
                description="Reminder name updated successfully!",
            ),
            "error": discord.Embed(
                title="❌ Reminder Name Update",
                description="An error occurred while updating the reminder name.",
            ),
            "warning": discord.Embed(
                title="⚠️ Reminder Name Update",
                description="Unexpected error occurred. Please try again later.",
            ),
        }

    @app_commands.command(
        name="remindme", description="Remind yourself about something later."
    )
    async def remind_me(self, interaction: discord.Interaction):
        if not AccountDAO.account_exists(interaction.user.id):
            await interaction.response.send_message(
                embed=self.embeds_no_account, ephemeral=True
            )
            return

        await interaction.response.send_modal(RemindMeModal())

    @app_commands.command(name="setmsg", description="Edit your reminder message.")
    async def set_message(self, interaction: discord.Interaction, reminder_name: str):
        if not AccountDAO.account_exists(interaction.user.id):
            await interaction.response.send_message(
                embed=self.embeds_no_account, ephemeral=True
            )
            return

        if not ReminderDAO.reminder_exists(interaction.user.id, reminder_name):
            await interaction.response.send_message(
                embed=self.embeds_no_reminder, ephemeral=True
            )
            return

        await interaction.response.send_modal(SetMsgModal(reminder_name))

    @app_commands.command(name="settime", description="Set the time for a reminder.")
    async def set_time(
        self, interaction: discord.Interaction, reminder_name: str, time: str
    ):
        if not AccountDAO.account_exists(interaction.user.id):
            await interaction.response.send_message(
                embed=self.embeds_no_account, ephemeral=True
            )
            return

        if not ReminderDAO.reminder_exists(interaction.user.id, reminder_name):
            await interaction.response.send_message(
                embed=self.embeds_no_reminder, ephemeral=True
            )
            return

        if not Reminder.validate_time(time):
            await interaction.response.send_message(
                "Invalid time format. Please use HH:MM format.", ephemeral=True
            )
            return

        try:
            success = ReminderDAO.set_reminder_time(
                interaction.user.id, reminder_name, time
            )
            if success:
                await interaction.response.send_message(
                    embed=self.embeds_settime["success"], ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=self.embeds_settime["error"], ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                embed=self.embeds_settime["warning"], ephemeral=True
            )
            logger.error(f"Unexpected error occurred while setting reminder time: {e}")

    @app_commands.command(name="setdate", description="Set the date for a reminder.")
    async def set_date(
        self, interaction: discord.Interaction, reminder_name: str, date: str = ""
    ):
        if not AccountDAO.account_exists(interaction.user.id):
            await interaction.response.send_message(
                embed=self.embeds_no_account, ephemeral=True
            )
            return

        if not ReminderDAO.reminder_exists(interaction.user.id, reminder_name):
            await interaction.response.send_message(
                embed=self.embeds_no_reminder, ephemeral=True
            )
            return

        if date == "":
            date = datetime.now().strftime("%d/%m/%Y")
        if not Reminder.validate_date(date):
            await interaction.response.send_message(
                "Invalid date format. Please use DD/MM/YYYY format.", ephemeral=True
            )
            return

        try:
            success = ReminderDAO.set_reminder_date(
                interaction.user.id,
                reminder_name,
                datetime.strptime(date, "%d/%m/%Y").date(),
            )
            if success:
                await interaction.response.send_message(
                    embed=self.embeds_setdate["success"], ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=self.embeds_setdate["error"], ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                embed=self.embeds_setdate["warning"], ephemeral=True
            )
            logger.error(f"Unexpected error occurred while setting reminder date: {e}")

    @app_commands.command(name="setname", description="Set the name for a reminder.")
    async def set_name(
        self, interaction: discord.Interaction, reminder_name: str, new_name: str
    ):
        if not AccountDAO.account_exists(interaction.user.id):
            await interaction.response.send_message(
                embed=self.embeds_no_account, ephemeral=True
            )
            return

        if not ReminderDAO.reminder_exists(interaction.user.id, reminder_name):
            await interaction.response.send_message(
                embed=self.embeds_no_reminder, ephemeral=True
            )
            return

        try:
            success = ReminderDAO.set_reminder_name(
                interaction.user.id, reminder_name, new_name
            )
            if success:
                await interaction.response.send_message(
                    embed=self.embeds_setname["success"], ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=self.embeds_setname["error"], ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                embed=self.embeds_setname["warning"], ephemeral=True
            )
            logger.error(f"Unexpected error occurred while setting reminder name: {e}")


async def setup(bot):
    await bot.add_cog(ReminderCog(bot))
