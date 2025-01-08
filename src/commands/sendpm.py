import discord
from discord import app_commands


@app_commands.command(name="sendpm", description="Send you message immediately")
async def sendpm(interaction: discord.Interaction, message: str):
    await interaction.user.send(message)
    await interaction.response.send_message("Message sent!", ephemeral=True)
