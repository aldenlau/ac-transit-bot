# This example requires the 'message_content' intent.
from os import environ
import discord
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
BOT_TOKEN = environ.get('AC_TRANSIT_BOT_TOKEN')
AC_TRANSIT_TOKEN = environ.get('AC_TRANSIT_API_TOKEN')
BASE_URL = 'https://api.actransit.org/transit'

@client.event
async def on_ready():
    print(f'Bot ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!bus'):
        payload = {'token': AC_TRANSIT_TOKEN, 'unixTime': True}
        r = requests.get(BASE_URL + '/actrealtime/time', params=payload)
        time = int(r.json()['bustime-response']['tm'])
        spruce_stop_id = 51173
        payload = {'token': AC_TRANSIT_TOKEN, 'stpid': spruce_stop_id, 'rt': ['52', 'F'], 'top': 3, 'tmres': 'm'}
        r = requests.get(BASE_URL + '/actrealtime/prediction', params = payload)
        await message.channel.send(r.json())
        # times = [arrival[''] for arrival in r.json()['bustime-response']['prd']]
client.run(BOT_TOKEN)
