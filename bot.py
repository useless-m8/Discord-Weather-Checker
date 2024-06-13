import discord
from main import *

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.content.startswith('!weather'):
        if len(message.content.split(' ')) == 1: #if no city given, ask the user to give the prompt again
            await message.channel.send('Please specify city')
            return
        
        location = ' '.join(message.content.replace(',', ' ').split(' ')[1:])
        output = get_weather(location)

        if len(output) == 0:
            await message.channel.send('No data found.')
            return 
        
        if int(output['is_day']) > 0:
            time_of_day = 'day'
        else:
            time_of_day = 'night'

        output_string = f"Weather in **{output['city']}, {output['country']}** is currently: \n\n**Temperature**: {int(output['temperature'])},\n**Rain percentage**: {int(output['rain'])}%,\n**Showers percentage**: {int(output['showers'])}%,\n**Cloud coverage**: {int(output['cloud_cover'])}%,\n**Relative humidity**: {int(output['humidity'])}%,\nIt's **{time_of_day}**time."
        await message.channel.send(output_string)


client.run('') #bot token goes here (you must take it from discord dev portal)
