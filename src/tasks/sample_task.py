from datetime import datetime, time
from discord.ext import tasks
from src.client_ import client
from src.tasks.test import unordinary, message1, message2, list_str_time, time_format


@tasks.loop(seconds=1)
async def sendpm_custom():
    current_time = datetime.now().time() # Extracts only the time part (HH:MM:SS)

    if current_time > time(5, 30):
        user = await client.fetch_user(unordinary)
        await user.send(message1)
        print(current_time, " | MORNING MESSAGE")

    if current_time > time(22, 00):
        user = await client.fetch_user(unordinary)
        await user.send(message2)
        print(current_time, " | EVENING MESSAGE")