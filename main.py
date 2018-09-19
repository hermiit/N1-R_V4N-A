#// init
import discord
import asyncio
import time
from datetime import datetime, date, time
import requests as reqs
import json
client = discord.Client()

#/ vars
TOKEN = 'NDg4MTA3OTIyMDg2NDI4Njcz.DoQaYw.sC9d5FYEifRKVGUUlLNiQRnnA34'
api = 'https://api.roblox.com/'

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

#// Functions
def checkrbx(msg):
    if msg[:10] != '**rbxinfo ':
        return False
    plrid = int(msg[10:])
    newreq = reqs.get(api + 'users/' + str(plrid))
    if newreq.status_code == 200:
        print('Sending info of id %d...' % plrid)
        reqjs = newreq.json()
        print(type(reqjs))
        return reqjs
    else:
        print('error' + str(newreq))
        return False

def getthumb(id):
    thumbapi = 'https://www.roblox.com/headshot-thumbnail/image'
    newthumb = reqs.get(thumbapi,params={'userId': [id],'width': 420,'height': 420,'format': 'png'})
    if newthumb.status_code < 400:
        return newthumb.url
    else:
        return False

def primgrp(id):
    groupapi = 'https://www.roblox.com/Groups/GetPrimaryGroupInfo.ashx'
    usrgrp = reqs.get(groupapi,params={'users': id['Username']})
    user = id['Username']
    print(usrgrp)
    if usrgrp.status_code < 400:
        usrjs = usrgrp.json()
        if usrjs == {}:
            print('User %s has no primary group!' % user)
            return 'N/A'
        else:
            return usrjs['Username']['GroupName']
    else:
        return False

#// main
@client.async_event
def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('**hello'):
        msg = 'Hey, {0.author.mention}.'.format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('**embtest'):
        embedo=discord.Embed( description="Testing embed description.", color=0x832297)
        embedo.set_author(name="Jill", icon_url=julico)
        yield from client.send_message(message.channel, embed=embedo)

    if message.content.startswith('**rbxinfo '):
        checkthis = checkrbx(message.content)
        if checkthis and checkthis['Username'] != 'ROBLOX':
            infostr = '**Username**: %s\n**User ID**: %d' % (checkthis['Username'],checkthis['Id'])
            embed=discord.Embed(title="Quick Info for %s:" % checkthis['Username'], color=0xf02b39)
            embed.set_author(name="Jill", url="https://roblox.com/users/" + str(checkthis['Id']), icon_url=julico)
            embed.set_thumbnail(url=getthumb(checkthis['Id']))
            embed.add_field(name='Username', value=checkthis['Username'], inline=True)
            embed.add_field(name='User ID', value=str(checkthis['Id']), inline=True)
            embed.add_field(name='Primary Group', value=primgrp(checkthis), inline=True)
            yield from client.send_message(message.channel, embed=embed)
        else:
            infostr = 'Incorrect syntax! Correct usage: `**rbxinfo 261`'
            yield from client.send_message(message.channel, content=infostr)

    if message.content.startswith('**drinktionary'): # UNFINISHED
        embedo=discord.Embed(title="Drinktionary", url=dnkurl, description="Here are the ingredients, please post with which number you want to use. (emoji :one:-:five:)", color=0x832297)
        embedo.set_author(name="Jill", url=julirl, icon_url=julico)
        embedo.set_image(url=mixgif)
        embedo.add_field(name=(1), value="Adelhyde", inline=True)
        embedo.add_field(name=(2), value="Bronson Extract", inline=True)
        embedo.add_field(name=(3), value="Powdered Delta", inline=True)
        embedo.add_field(name=(4), value="Flanergide", inline=True)
        embedo.add_field(name=(5), value="Karmotrine", inline=True)
        embedo.set_footer(icon_url=julico,text='Generated via N1-R V4N-A | ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        embmsg = yield from client.send_message(message.channel, embed=embedo)
        res = client.wait_for_message(author=message.author,content='1')
        yield from client.send_message(message.channel,content=res.content)



@client.async_event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Time to mix drinks and save lives.')
    print('------')

client.run(TOKEN)
