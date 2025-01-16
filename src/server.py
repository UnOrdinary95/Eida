import os
import discord
from discord import app_commands
from commands.sendpm import sendpm
from src.client import client_status, client

# Define bot intents
intents = discord.Intents.default()
intents.message_content = True

# Create commandtree
tree = app_commands.CommandTree(client)
tree.add_command(sendpm)

# Event triggered when the bot is ready and connected to Discord
@client.event
async def on_ready():
    print(f"{client.user} is now running !")
    await client.change_presence(activity=discord.CustomActivity(client_status))
    try:
        print("Synchronizing commands...")
        await tree.sync()
        print("Commands synchronized!")

        user = await client.fetch_user(768823850951376896)
        await user.send('Hi !')

    except Exception as e:
        print(f"Error syncing commands: {e}")


# Run the bot
client.run(os.getenv("TOKEN"))