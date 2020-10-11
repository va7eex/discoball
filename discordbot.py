import os
import datetime
import discord

from labelmaker import labelprinter
from profanity_filter import ProfanityFilter
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
maxqty = 10

startuplines = [ 'Goliath Online', 'Reactor Online\nSensors Online\nWeapons Online\nAll Systems Functional']

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!lp '):
        qty = 1
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

        if inspectstr is not None and inspectstr.startswith('qty'):
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

        await message.channel.send(f'Printing label x {qty}:\n\t{labelstr}')

def osBooltoPyBool(str):
    if 'true' in str.lower(): return True
    return False

if __name__ == "__main__":
    if TOKEN != '':
        global lp
        global pf
        lp = labelprinter(os.getenv('PRINTER_IP'),
                          width=float(os.getenv('LABELWIDTH')),
                          height=float(os.getenv('LABELHEIGHT')),
                          imperialunits=osBooltoPyBool(os.getenv('IMPERIALUNITS')))
        lp.printlabel('Discoball Power-On Self-Test',
                      'Bot started:',
                      datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"),
                      barcodedata=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
#        pf = ProfanityFilter(languages=['en'])
        client.run(TOKEN)
    else:
        print('%s Bot Failed: No Token'%datetime.datetime.now())
