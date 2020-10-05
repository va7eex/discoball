import os
from labelmaker import labelprinter
import datetime


import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#lp = None
client = discord.Client()
maxqty = 10

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if '!lp ' in message.content:
        qty = 1
        labelstr = message.content.replace('!lp ','').strip()
        inspectstr, qtystr = labelstr.split(' ')[0], labelstr.split(' ')[1]


        if 'qty' in inspectstr:
            if len(inspectstr.replace('qty','')) > 0 and inspectstr.replace('qty','').isdigit():
                qty = min(max(int(inspectstr.replace('qty','').strip()),1),maxqty)
                labelstr = labelstr.replace(f'{inspectstr} ','')
            elif qtystr.isdigit():
                qty = min(max(int(qtystr.strip()),1),maxqty)
                labelstr = labelstr.replace(f'qty {qtystr} ','')

        #backfill up to 6 commas
        for i in range(5-len(labelstr.split(','))):
            labelstr += ','
        labelstr = labelstr.split(',')
        lp.printlabel(labelstr[0],labelstr[1],labelstr[2],labelstr[3],labelstr[4], quantity=qty)

        await message.channel.send(f'{message.content}')
        await message.channel.send(f'Printing label x {qty}')


if __name__ == "__main__":
    if TOKEN != '':
        global lp
        lp = labelprinter(os.getenv('PRINTER_IP'))
        lp.printlabel('Discoball Power-On Self-Test', 'Bot started:', datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), barcodedata=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        client.run(TOKEN)
    else:
        print('%s Bot Failed: No Token'%datetime.datetime.now())
