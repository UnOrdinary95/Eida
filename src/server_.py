import os
import logging
import discord
from discord import app_commands
# from src.commands.sendpm import sendpm
from src.tasks.sample_task import morning_task, evening_task, test_task
from src.client_ import client, client_status

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# Create commandtree
tree = app_commands.CommandTree(client)
# tree.add_command(sendpm)

# Event triggered when the bot is ready and connected to Discord
@client.event
async def on_ready():
    print(f"{client.user} is now running !")
    await client.change_presence(activity=discord.CustomActivity(client_status))
    try:
        print("Synchronizing commands...")
        await tree.sync()
        print("Commands synchronized.")

        morning_task.start()
        evening_task.start()
        # test_task.start()
        print("Task is running.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Run the bot
client.run(os.getenv("TOKEN"))