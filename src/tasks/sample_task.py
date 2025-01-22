import time
from datetime import datetime
from discord.ext import tasks
from src.client_ import client
from src.tasks.test import unordinary, message1, message2, list_str_time, time_format


@tasks.loop(seconds=0.5)
async def sendpm_custom():
    current_time = datetime.now()

    if (list_str_time[0] > current_time):
        user = await client.fetch_user(unordinary)
        await user.send(message1)
        print(datetime.strftime(current_time, time_format), " | MORNING MESSAGE")
        pass






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


