import os
import labelmaker
import time

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'bclp,' in message.content:
        disco_bigmessage = message.content.split(',')[1]
        disco_littlemessage = message.content.split(',')[2]
        disco_littlemessageright = message.content.split(',')[3]
        disco_barcodedata = message.content.split(',')[4]
        disco_barcodetype = message.content.split(',')[5]

        response = labelmaker.print(disco_bigmessage,
            littlemessageleft=disco_littlemessage,
            littlemessageright=disco_littlemessageright,
            barcodedata=disco_barcodedata,
            barcodetype=disco_barcodetype)

        await message.channel.send(response)


if __name__ == "__main__":
    if TOKEN != '':
        client.run(TOKEN)
        labelmaker.printlabel('Discoball Power-On Self-Test', 'Bot started:', datetime.now().strftime("%Y%m%d %H:%M:%S"), barcodedata=datetime.now().strftime("%Y%m%d%H%M%S"))
    else:
        print('%s Bot Failed: No Token'%datetime.now()
