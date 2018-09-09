#// init
import discord
import time
import requests
from datetime import datetime, date, time
import json
client = discord.Client()

#/ vars
TOKEN = "lol no"

dnums = {
    ":one:"  : "Adelhyde",
    ":two:"  : "Bronson Extract",
    ":three:": "Powdered Delta",
    ":four:" : "Flanergide",
    ":five:" : "Karmotrine"
}

#/ urls
urls = {
   "Media": {
      "mixgif": "https://vignette.wikia.nocookie.net/va11halla/images/5/51/Mixing.gif",
      "julico": "https://cdn.discordapp.com/avatars/488107922086428673/ac74d4af50b36a915400bcb648addb8a.png"
   },
   "Pages": {
      "testu" : "https://google.com",
      "julirl": "http://va11halla.wikia.com/wiki/Julianne_Stingray",
      "dnkurl": "http://va11halla.wikia.com/wiki/Drinktionary"
   }
}

mixgif = urls['Media']['mixgif']
julico = urls['Media']['julico']
testu = urls['Pages']['testu']
julirl = urls['Pages']['julirl']
dnkurl = urls['Pages']['dnkurl']

#// main
@client.event

async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('**hello'):
        msg = 'Hey, {0.author.mention}.'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('**embtest'):
        embedo=discord.Embed( description="Testing embed description.", color=0x832297)
        embedo.set_author(name="Jill", icon_url=julico)
        await client.send_message(message.channel, embed=embedo)

    if message.content.startswith('**drinktionary'):
        embedo=discord.Embed(title="Drinktionary", url=dnkurl, description="Here are the ingredients, please react with which number you want to use. (emoji :one:-:five:)", color=0x832297)
        embedo.set_author(name="Jill", url=julirl, icon_url=julico)
        embedo.set_image(url=mixgif)
        embedo.add_field(name=(1), value="Adelhyde", inline=True)
        embedo.add_field(name=(2), value="Bronson Extract", inline=True)
        embedo.add_field(name=(3), value="Powdered Delta", inline=True)
        embedo.add_field(name=(4), value="Flanergide", inline=True)
        embedo.add_field(name=(5), value="Karmotrine", inline=True)
        embedo.set_footer(icon_url=julico,text='Generated via N1-R V4N-A | ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        embmsg = await client.send_message(message.channel, embed=embedo)
        res = client.wait_for_reaction([':one:',':two:',':three:',':four:',':five:'], user=message.author, timeout=5, message=embmsg)
        if res:
            if res.reaction.emoji == ':one:':
                print('ok man i see you like robbie')
            elif res['reaction']['emoji'] == ':two:':
                print('he was number 2')




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Time to mix drinks and save lives.')
    print('------')

client.run(TOKEN)
