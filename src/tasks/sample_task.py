from datetime import datetime, time, timedelta, timezone, tzinfo
import pytz
from discord.ext import tasks
from src.client_ import client
from src.tasks.test import unordinary, message1, message2


# Create a timezone object for UTC+1 (same as France/Paris)
FRANCE_TZ = timezone(timedelta(hours=1))

# Sample Tasks
@tasks.loop(time=time(5, 30, tzinfo=FRANCE_TZ))
async def morning_task():
    user = await client.fetch_user(unordinary)
    await user.send(message1)
    print(datetime.now(), " | MORNING MESSAGE")

@tasks.loop(time=time(22,00, tzinfo=FRANCE_TZ))
async def evening_task():
    user = await client.fetch_user(unordinary)
    await user.send(message2)
    print(datetime.now(), " | EVENING MESSAGE")


@tasks.loop(time=pytz.timezone("Europe/Paris").localize(datetime.combine(datetime.today(), time(11,36))).astimezone(pytz.utc).time())
async def test_task():
    user = await client.fetch_user(unordinary)
    await user.send("TEST TIME ZONE MESSAGE")
    print(datetime.now(), " | TEST TIME ZONE MESSAGE")

