import time
import discord
from discord.ext import tasks
from src.server import client

@tasks.loop(seconds=0.9)
async def sendpm_custom():
    current_time = time.localtime()
    if time.strftime("%H:%M:%S", current_time) == '22:12:00':
        user = get_user(768823850951376896)
        await user.send('Hi !')

async def get_user(user_id):
    user = await client.fetch_user(user_id)
    return user