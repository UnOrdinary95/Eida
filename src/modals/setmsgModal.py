import discord
import logging
from src.models.Reminder import Reminder
from src.database.ReminderDAO import ReminderDAO

logger = logging.getLogger(__name__)


class SetMsgModal(discord.ui.Modal, title="Edit Reminder Message"):
    """Modal for editing existing reminder messages."""

    def __init__(self, reminder_name: str):
        super().__init__()
        self.reminder_name = reminder_name
        self.embeds_submit = {
            "success": discord.Embed(
                title="✅ Reminder Message Updated",
                description="Reminder message updated successfully!",
            ),
            "error": discord.Embed(
                title="❌ Reminder Message Update",
                description="An error occurred while updating the reminder message.",
            ),
            "warning": discord.Embed(
                title="⚠️ Reminder Message Update",
                description="Unexpected error occurred. Please try again later.",
            ),
        }

    message_input = discord.ui.TextInput(
        label="Message",
        placeholder="Hello world!\nI'm a reminder!",
        style=discord.TextStyle.long,
        max_length=1024,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        """
        Process message update with validation.
        Client-side validation provides immediate feedback for single-field update.
        """

        # Validate message content before database interaction
        if not Reminder.validate_message(self.message_input.value):
            await interaction.response.send_message(
                "Invalid message or no message provided. Maximum 1024 characters allowed.",
                ephemeral=True,
            )
            return

        try:
            success = ReminderDAO.set_reminder_message(
                interaction.user.id, self.reminder_name, self.message_input.value
            )
            if success:
                await interaction.response.send_message(
                    embed=self.embeds_submit["success"], ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=self.embeds_submit["error"], ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(
                embed=self.embeds_submit["warning"], ephemeral=True
            )
            logger.error(
                f"Unexpected error occurred while setting reminder message: {e}"
            )
