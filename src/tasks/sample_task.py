import time
import discord
from discord.ext import tasks
from src.client import client

@tasks.loop(seconds=0.9)
async def sendpm_custom():
    current_time = time.localtime()
    if time.strftime("%H:%M:%S", current_time) == '22:12:00':
        user = await client.fetch_user(768823850951376896)
        await user.send('TEST SENDPM CUSTOM !')