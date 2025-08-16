import discord
from src.database.AccountDAO import AccountDAO

class SetzModal(discord.ui.Modal, title="Timezone Setup"):
    embeds_submit = {
        "success": discord.Embed(
            title="✅ Timezone Setup",
            description="Timezone changed successfully!"
        ),
        "error": discord.Embed(
            title="❌ Timezone Setup",
            description="You entered an invalid timezone or an unexpected error occurred. Please try again later."
        )
    }
    tz_input = discord.ui.TextInput(
        label="Timezone",
        placeholder="Europe/Paris",
        style=discord.TextStyle.short,
        max_length=40,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        if AccountDAO.set_timezone(interaction.user.id, self.tz_input.value):
            await interaction.response.send_message(embed=self.embeds_submit["success"], ephemeral=True)
        else:
            await interaction.response.send_message(embed=self.embeds_submit["error"], ephemeral=True)
