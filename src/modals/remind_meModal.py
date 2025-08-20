import discord
import logging
from datetime import datetime
from src.models.Reminder import Reminder
from src.database.ReminderDAO import ReminderDAO

logger = logging.getLogger(__name__)


class RemindMeModal(discord.ui.Modal, title="New Reminder"):
    """
    Modal form for reminder creation with comprehensive validation.
    Pre-validates input before database interaction for better user experience.
    """
    
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
    # Optional field with today's date as visual example
    date_input = discord.ui.TextInput(
        label="Date (default: today)",
        placeholder=datetime.now().strftime("%d/%m/%Y"),
        style=discord.TextStyle.short,
        max_length=10,
        required=False,
    )
    # Show examples of both interval patterns for user guidance
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
        """
        Process form submission with client-side validation before database interaction.
        Early validation provides immediate feedback and prevents unnecessary database calls.
        """
        
        # Validate each field individually to provide specific error messages
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

        # Special handling for optional date field - empty string is valid
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

        # Create reminder object only after all validations pass
        reminder = Reminder(
            interaction.user.id,
            self.name_input.value,
            self.time_input.value,
            # Apply default date logic consistently with Reminder model
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
