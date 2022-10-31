from os import environ
import discord
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
BOT_TOKEN = environ.get('AC_TRANSIT_BOT_TOKEN')
AC_TRANSIT_TOKEN = environ.get('AC_TRANSIT_API_TOKEN')
BASE_URL = 'https://api.actransit.org/transit'
STOPS = {'52': 50400, 'F': 52848}

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

        payload = {'token': AC_TRANSIT_TOKEN, 'stpid': ','.join([str(stpid) for stpid in STOPS.values()]), 'rt': ','.join([route for route in STOPS.keys()]), 'top': 3, 'tmres': 'm'}
        r = requests.get(BASE_URL + '/actrealtime/prediction', params = payload)
        
        times = [f"**{arrival['rt']} Line** arriving in **{arrival['prdctdn']} minutes** at **{arrival['stpnm']}**" for arrival in r.json()['bustime-response']['prd']]
        await message.channel.send('\n'.join(times))

client.run(BOT_TOKEN)