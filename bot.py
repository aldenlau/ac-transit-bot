from os import environ
import discord
import requests
import xmltodict

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
BOT_TOKEN = environ.get('AC_TRANSIT_BOT_TOKEN')
AC_TRANSIT_TOKEN = environ.get('AC_TRANSIT_API_TOKEN')
BASE_URL = 'https://api.actransit.org/transit'
BEAR_TRANSIT_URL = 'https://retro.umoiq.com/service/publicXMLFeed?command=predictions&a=ucb&r=peri&s='
NORTHSIDE_BEAR_TRANSIT_STOP_NAME = 'oxfouniv'
SOUTHSIDE_BEAR_TRANSIT_STOP_NAME = 'sprouhall'
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
        
        northside_times = [(arrival['rt'], arrival['prdctdn'], arrival['stpnm']) for arrival in r.json()['bustime-response']['prd']]

        r = requests.get(BEAR_TRANSIT_URL+NORTHSIDE_BEAR_TRANSIT_STOP_NAME)
        dict_data = xmltodict.parse(r.content)
        for item in dict_data['body']['predictions']['direction']['prediction']:
            minutes = item['@minutes']
            northside_times.append(('P', minutes, 'Oxford St & University Av'))
        northside_times.sort(key=(lambda x: x[1]))
        northside_times = northside_times[:5]
        
        northside_times = [f"**{route} Line** arriving in **{time} minutes** at **{stop}**" for route, time, stop in northside_times]



        payload = {'token': AC_TRANSIT_TOKEN, 'stpid': ','.join([str(stpid) for stpid in SOUTHSIDE_STOPS.values()]), 'rt': ','.join([route for route in SOUTHSIDE_STOPS.keys()]), 'top': 3, 'tmres': 'm'}
        r = requests.get(BASE_URL + '/actrealtime/prediction', params = payload)

        southside_times = [(arrival['rt'], arrival['prdctdn'], arrival['stpnm']) for arrival in r.json()['bustime-response']['prd']]

        r = requests.get(BEAR_TRANSIT_URL+SOUTHSIDE_BEAR_TRANSIT_STOP_NAME)
        dict_data = xmltodict.parse(r.content)
        for item in dict_data['body']['predictions']['direction']['prediction']:
            minutes = item['@minutes']
            southside_times.append(('P', minutes, 'Bancroft Way & Telegraph Av'))
        southside_times.sort(key=(lambda x: x[1]))
        southside_times = southside_times[:5]

        southside_times = [f"**{route} Line** arriving in **{time} minutes** at **{stop}**" for route, time, stop in southside_times]
        
        output = f'__**Northside buses:**__\n' + '\n'.join(northside_times) + f'\n\n__**Southside buses:**__\n' + '\n'.join(southside_times)
        await message.channel.send(output)

client.run(BOT_TOKEN)