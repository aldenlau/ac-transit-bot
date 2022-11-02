from os import environ
import discord
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
BOT_TOKEN = environ.get('AC_TRANSIT_BOT_TOKEN')
AC_TRANSIT_TOKEN = environ.get('AC_TRANSIT_API_TOKEN')
BASE_URL = 'https://api.actransit.org/transit'
NORTHSIDE_STOPS = {'52': 50400, 'F': 52848}
SOUTHSIDE_STOPS = {'51B': 54455}

@client.event
async def on_ready():
    print(f'Bot ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!bus'):
        payload = {'token': AC_TRANSIT_TOKEN, 'stpid': ','.join([str(stpid) for stpid in NORTHSIDE_STOPS.values()]), 'rt': ','.join([route for route in NORTHSIDE_STOPS.keys()]), 'top': 3, 'tmres': 'm'}
        r = requests.get(BASE_URL + '/actrealtime/prediction', params = payload)
        
        northside_times = [f"**{arrival['rt']} Line** arriving in **{arrival['prdctdn']} minutes** at **{arrival['stpnm']}**" for arrival in r.json()['bustime-response']['prd']]

        payload = {'token': AC_TRANSIT_TOKEN, 'stpid': ','.join([str(stpid) for stpid in SOUTHSIDE_STOPS.values()]), 'rt': ','.join([route for route in SOUTHSIDE_STOPS.keys()]), 'top': 3, 'tmres': 'm'}
        r = requests.get(BASE_URL + '/actrealtime/prediction', params = payload)

        southside_times = [f"**{arrival['rt']} Line** arriving in **{arrival['prdctdn']} minutes** at **{arrival['stpnm']}**" for arrival in r.json()['bustime-response']['prd']]
        output = f'__**Northside buses:**__\n' + '\n'.join(northside_times) + f'\n\n__**Southside buses:**__\n' + '\n'.join(southside_times)
        await message.channel.send(output)

client.run(BOT_TOKEN)