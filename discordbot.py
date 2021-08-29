import os
import datetime
import io
import discord
import logging

from PIL.Image import Image
from labelmaker import labelprinter
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
maxqty = 10

startuplines = [ 'Goliath Online', 'Reactor Online\nSensors Online\nWeapons Online\nAll Systems Functional']

@client.event
async def on_ready():
    logging.debug(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        await message.channel.send('Current commands:\n\nLabel Commands:```!lp [qty \#] Bigtext,LittleText,LittleTextRight,BarcodeData,BarcodeType```')

    if message.content.startswith('!lp '):
        qty = 1
        preview = False
        labelstr = message.content.replace('!lp ','').strip()
#        labelstr = pf.censor(message.content.replace('!lp ','').strip())

        #this is a range check.
        def checkforquantity(lstr):
            inspectstr = None
            qtystr = None
            if len(lstr.split(' ')) > 1:
                inspectstr = lstr.split(' ')[0]
                qtystr = lstr.split(' ')[1]
            return inspectstr, qtystr

        inspectstr, qtystr = checkforquantity(labelstr)

        if inspectstr is not None:
            if inspectstr.startswith('qty'):
                if len(inspectstr.replace('qty','')) > 0 and inspectstr.replace('qty','').isdigit():
                    qty = min(max(int(inspectstr.replace('qty','').strip()),1),maxqty)
                    labelstr = labelstr.replace(f'{inspectstr} ','')
                elif qtystr.isdigit():
                    qty = min(max(int(qtystr.strip()),1),maxqty)
                    labelstr = labelstr.replace(f'qty {qtystr} ','')
            if inspectstr.startswith('preview'):
                preview = True

        #backfill up to 6 commas
        for i in range(5-len(labelstr.split(','))):
            labelstr += ','
        labelstr = labelstr.split(',')
        report = lp.printlabel(labelstr[0],labelstr[1].strip(),labelstr[2].strip(),labelstr[3].strip(),labelstr[4].strip(), quantity=qty, preview=preview)
        if type(report) is bool:
            await message.channel.send(f'Printing label x {qty}:\n\t{labelstr}')
        elif type(report) is bytes:
            image = Image.frombytes(report)
            await message.channel.send(file=discord.File(image, 'preview.png'))

def osBooltoPyBool(str):
    if 'true' in str.lower(): return True
    return False

if __name__ == "__main__":
    if TOKEN != '':
        global lp
        lp = labelprinter(os.getenv('PRINTER_IP'),
                          width=float(os.getenv('LABELWIDTH')),
                          height=float(os.getenv('LABELHEIGHT')),
                          imperialunits=osBooltoPyBool(os.getenv('IMPERIALUNITS')))
        lp.printlabel('Discoball Power On Self Test',
                      'Bot started:',
                      datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"),
                      barcodedata=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        client.run(TOKEN)
    else:
        logging.warning('%s Bot Failed: No Token'%datetime.datetime.now())
