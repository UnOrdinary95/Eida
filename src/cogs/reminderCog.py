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
        self.embeds_sett = {
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
        self.embeds_setd = {
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

    @app_commands.command(name="sett", description="Set the time for a reminder.")
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
                    embed=self.embeds_sett["success"], ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=self.embeds_sett["error"], ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                embed=self.embeds_sett["warning"], ephemeral=True
            )
            logger.error(f"Unexpected error occurred while setting reminder time: {e}")

    @app_commands.command(name="setd", description="Set the date for a reminder.")
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
                    embed=self.embeds_setd["success"], ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=self.embeds_setd["error"], ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                embed=self.embeds_setd["warning"], ephemeral=True
            )
            logger.error(f"Unexpected error occurred while setting reminder date: {e}")


async def setup(bot):
    await bot.add_cog(ReminderCog(bot))
