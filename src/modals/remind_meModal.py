import discord
import logging
from datetime import datetime
from src.models.Reminder import Reminder
from src.database.ReminderDAO import ReminderDAO

logger = logging.getLogger(__name__)


class RemindMeModal(discord.ui.Modal, title="New Reminder"):
    embeds_remind_me = {
        "success": discord.Embed(
            title="✅ Reminder Creation", description="Reminder created successfully!"
        ),
        "error": discord.Embed(
            title="❌ Reminder Creation",
            description="A reminder with this name already exists, or an error occurred.",
        ),
        "warning": discord.Embed(
            title="⚠️ Reminder Creation",
            description="Unexpected error occurred. Please try again later.",
        ),
    }
    name_input = discord.ui.TextInput(
        label="Name",
        placeholder="My reminder",
        style=discord.TextStyle.short,
        max_length=50,
        required=True,
    )
    time_input = discord.ui.TextInput(
        label="Time",
        placeholder="07:53",
        style=discord.TextStyle.short,
        max_length=5,
        required=True,
    )
    date_input = discord.ui.TextInput(
        label="Date (default: today)",
        placeholder=datetime.now().strftime("%d/%m/%Y"),
        style=discord.TextStyle.short,
        max_length=10,
        required=False,
    )
    intervals_input = discord.ui.TextInput(
        label="Intervals (default: None)",
        placeholder="e15m2h1d | w:* | w:tue,fri,mon,sat",
        style=discord.TextStyle.short,
        max_length=30,
        required=False,
    )
    message_input = discord.ui.TextInput(
        label="Message",
        placeholder="Hello world!\nI'm a reminder!",
        style=discord.TextStyle.long,
        max_length=1024,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Validate all inputs using the Reminder model validation methods
        if not Reminder.validate_reminder_name(self.name_input.value):
            await interaction.response.send_message(
                "Invalid reminder name. Maximum 50 characters allowed.", ephemeral=True
            )
            return

        if not Reminder.validate_time(self.time_input.value):
            await interaction.response.send_message(
                "Invalid time format. Please use HH:MM format.", ephemeral=True
            )
            return

        if not Reminder.validate_date(self.date_input.value) and self.date_input.value != "":
            await interaction.response.send_message(
                "Invalid date format. Please use DD/MM/YYYY format.", ephemeral=True
            )
            return

        if not Reminder.validate_intervals(self.intervals_input.value):
            await interaction.response.send_message(
                "Invalid intervals format. Please check your input.", ephemeral=True
            )
            return

        if not Reminder.validate_message(self.message_input.value):
            await interaction.response.send_message(
                "Invalid message or no message provided. Maximum 1024 characters allowed.", ephemeral=True
            )
            return

        # If all validations pass, send success response
        reminder = Reminder(
            interaction.user.id,
            self.name_input.value,
            self.time_input.value,
            datetime.now().strftime("%d/%m/%Y") if self.date_input.value == "" else self.date_input.value,
            self.intervals_input.value,
            self.message_input.value,
        )
        try:
            success = ReminderDAO.add_reminder(reminder)
            if success:
                await interaction.response.send_message(
                    embed=self.embeds_remind_me["success"], ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=self.embeds_remind_me["error"], ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                embed=self.embeds_remind_me["warning"], ephemeral=True
            )
            logger.error(f"Unexpected error occurred while creating reminder: {e}")
