import discord
from src.server import intents

# Create bot client
client_status = "Seeing everything that is currently happening"
client = discord.Client(intents=intents)