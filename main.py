#// Mdoules
import discord
import asyncio
import sys
import os
import time
import random
from datetime import datetime, date
import requests as reqs
import json
client = discord.Client()

#// Variables
TOKEN = 'NDkzMzQxNzgzODc5ODQzODQw.Dosuuw.UVojAXDYaR8MQh50qGrtljNFE8M'
owner = '213839777840103426'
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
def printf(string,*argv):
   print(string % (argv))

def parse(string):
   return str.split(string)

def ifnum(string,pnt=False):
   try:
      float(string)
      if pnt:
         printf('%f can become a float',float(string))
      return True
   except ValueError:
      return False


def checkstr(msg):
   presapi = 'https://www.roblox.com/presence/user'
   usrapi  = 'https://api.roblox.com/users/'
   nameapi = 'https://api.roblox.com/users/get-by-username'
   msgpar = parse(msg)
   
   param = msgpar[1]

   if ifnum(param):
      plrid = param
      usrreq = reqs.get(usrapi + str(plrid))
      presreq = reqs.get(presapi,params={'userId': plrid})

      if usrreq.status_code == 200 and presreq.status_code == 200:
         printf ('Sending info of id %s...' % plrid)
         reqjs = usrreq.json()
         presjs = presreq.json()
         reqjs['Presence'] = presjs['LastLocation']
         print(type(reqjs))
         return reqjs
      else:
         print('User request: %s' % str(usrreq))
         print('Presence request: %s' % str(presreq))
         return False
   else:
      usrreq = reqs.get(nameapi,params={'username': param})

      if usrreq.status_code == 200:
         reqjs = usrreq.json()
         plrid = reqjs['Id']
         presreq = reqs.get(presapi,params={'userId': plrid})
         print('Sending info of id %s...' % plrid)
         presjs = presreq.json()
         reqjs['Presence'] = presjs['LastLocation']
         print(type(reqjs))
         return reqjs
      else:
         print('User request: %s' % str(usrreq))
         print('Presence request: %s' % str(presreq))
         return False

def checkowner(author):
   if author.id == owner:
      return True
   else:
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
         print(usrjs)
         return usrjs[user]['GroupName']
   else:
      return False

#// main
@client.async_event
def on_message(message):
   # we do not want the bot to reply to itself
   if message.author == client.user:
      return

   if message.content.startswith('**hello'):
      msg = 'Hey, <@%s>.' % message.author.id
      yield from client.send_message(message.channel, msg)

   if message.content.startswith('**embtest'):
      embedo=discord.Embed( description="Testing embed description.", color=0x832297)
      embedo.set_author(name="Jill", icon_url=julico)
      yield from client.send_message(message.channel, embed=embedo)

   if message.content.startswith('**rbxinfo '):
      checkthis = checkstr(message.content)
      if checkthis and checkthis['Username'] != 'ROBLOX':
         infostr = '**Username**: %s\n**User ID**: %d' % (checkthis['Username'],checkthis['Id'])
         embed=discord.Embed(title="Quick Info for %s:" % checkthis['Username'], color=0xf02b39)
         embed.set_author(name="Jill", url="https://roblox.com/users/" + str(checkthis['Id']), icon_url=julico)
         embed.set_thumbnail(url=getthumb(checkthis['Id']))
         embed.add_field(name='Username', value=checkthis['Username'], inline=True)
         embed.add_field(name='User ID', value=str(checkthis['Id']), inline=True)
         embed.add_field(name='Primary Group', value=primgrp(checkthis), inline=True)
         embed.add_field(name='Presence', value=checkthis['Presence'], inline=True)
         yield from client.send_message(message.channel, embed=embed)
      else:
         infostr = 'Incorrect syntax! Correct usage: `**rbxinfo 261`'
         yield from client.send_message(message.channel, content=infostr)

   if message.content.startswith('**clean ') and checkowner(message.author):
      pmsg = parse(message.content)
      cmd = pmsg[1]
      if cmd == 'self':
         def is_me(m):
            return m.author == client.user
         
         def is_metoo(m):
            return m.author == message.author

         deltree = yield from client.purge_from(message.channel, limit=100, check=is_metoo)
         printf('Deleted %d messages. (self)',len(deltree))
         delmsg2 = '*Deleted %s messages.* (self)' % len(deltree)

         deleted = yield from client.purge_from(message.channel, limit=100, check=is_me)
         printf('Deleted %d messages. (bot)',len(deleted))
         delmsg1 = '*Deleted %s messages.* (bot)' % len(deleted)

         snd1 = yield from client.send_message(message.channel,content=delmsg1)
         snd2 = yield from client.send_message(message.channel,content=delmsg2)
         time.sleep(float(pmsg[2]))
         yield from client.delete_messages([snd1,snd2])

   if message.content.startswith('**exit') and checkowner(message.author):
      print('Logging out...')
      logmsg = 'Alright <@%s>, logging out.' % message.author.id
      yield from client.send_message(message.channel,content=logmsg)
      yield from client.logout()

   """if message.content.startswith('**drinktionary'): # UNFINISHED
         embedo=discord.Embed(title="Drinktionary", url=dnkurl, description="Here are the ingredients, please post with which number you want to use. (emoji :one:-:five:)", color=0x832297)
         embedo.set_author(name="Jill", url=julirl, icon_url=julico)
         embedo.set_image(url=mixgif)
         embedo.add_field(name=(1), value="Adelhyde", inline=True)
         embedo.add_field(name=(2), value="Bronson Extract", inline=True)
         embedo.add_field(name=(3), value="Powdered Delta", inline=True)
         embedo.add_field(name=(4), value="Flanergide", inline=True)
         embedo.add_field(name=(5), value="Karmotrine", inline=True)
         embedo.set_footer(icon_url=julico,text='Generated via N1-R V4N-A | ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
         yield from client.send_message(message.channel, embed=embedo)
         res = client.wait_for_message(author=message.author,content='1')
         yield from client.send_message(message.channel,content=res.content)"""



@client.async_event
def on_ready():
   print('Logged in as')
   print(client.user.name)
   print(client.user.id)
   print('Time to mix drinks and save lives.')
   print('-----------------------------------')

client.run(TOKEN)