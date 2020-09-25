import os
import labelmaker
import datetime


import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
lp = None
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'bclp,' in message.content:
        response = message.content
        labelstr = message.content
        print(len(labelstr))
        #backfill up to 6 commas
        for i in range(0,6-len(message.content.split(','))):
            labelstr + ','
        labelstr = labelstr.split(',')
        lp.printlabel(labelstr[1],labelstr[2],labelstr[3],labelstr[4],labelstr[5])
        await message.channel.send(response)


if __name__ == "__main__":
    if TOKEN != '':
        global lp
        lp = labelprinter(os.getenv('PRINTER_IP')
        lp.printlabel('Discoball Power-On Self-Test', 'Bot started:', datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), barcodedata=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        client.run(TOKEN)
    else:
        print('%s Bot Failed: No Token'%datetime.datetime.now())
