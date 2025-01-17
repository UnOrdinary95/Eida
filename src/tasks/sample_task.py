import time
from discord.ext import tasks
from src.client_ import client

@tasks.loop(seconds=1)
async def sendpm_custom():
    current_time = time.localtime()
    if time.strftime("%H:%M:%S", current_time) == '19:06:30':
        user = await client.fetch_user(768823850951376896)
        await user.send('TEST SENDPM CUSTOM !')
        print("--CHECK--")
    else:
        print(time.strftime("%H:%M:%S", current_time))