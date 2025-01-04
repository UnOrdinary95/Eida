import os
import discord
from discord import app_commands


# Define bot intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot client
client_status = "Seeing everything that is currently happening in the world"
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Event triggered when the bot is ready and connected to Discord
@client.event
async def on_ready():
    print(f"{client.user} is now running !")
    await client.change_presence(activity=discord.CustomActivity(client_status))
    try:
        print("Synchronizing commands...")
        await tree.sync()
        print("Commands synchronized!")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Run the bot
client.run(os.getenv("TOKEN"))