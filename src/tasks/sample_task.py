import time
from discord.ext import tasks
from src.client_ import client
from src.tasks.test import unordinary, message1, message2

@tasks.loop(seconds=0.5)
async def sendpm_custom():
    current_time = time.localtime()
    match time.strftime("%H:%M:%S", current_time):
        case "04:30:00":
            user = await client.fetch_user(unordinary)
            await user.send(message1)
            print(time.strftime("%H:%M:%S", current_time), " | MORNING MESSAGE")
        case "21:00:00":
            user = await client.fetch_user(unordinary)
            await user.send(message2)
            print(time.strftime("%H:%M:%S", current_time), " | EVENING MESSAGE")
        case _:
            print(time.strftime("%H:%M:%S", current_time))