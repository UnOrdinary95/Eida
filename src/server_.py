import os
import discord
from discord import app_commands
from src.commands.sendpm import sendpm
from src.tasks.sample_task import sendpm_custom
from src.client_ import client, client_status

# Create commandtree
tree = app_commands.CommandTree(client)
tree.add_command(sendpm)

# Event triggered when the bot is ready and connected to Discord
@client.event
async def on_ready():
    print(f"{client.user} is now running !")
    await client.change_presence(activity=discord.CustomActivity(client_status))
    try:
        print("Synchronizing commandss...")
        await tree.sync()
        print("Commands synchronized!")
        sendpm_custom.start()
        print("TASK IS RUNNING!")
    except Exception as e:
        print(f"Error syncing commandss: {e}")


# Run the bot
client.run(os.getenv("TOKEN"))