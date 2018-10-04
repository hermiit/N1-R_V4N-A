#// Modules
import discord
import asyncio
import sys
import os
import time
import random
import math
from datetime import datetime, date
import requests as reqs
import json
client = discord.Client()

#// Variables
TOKEN = 'NDkzMzQxNzgzODc5ODQzODQw.DpJ5tA.3NsrBR1Ujix4VTDxsBr086eWCAs'
owner = '213839777840103426'
api = 'https://api.roblox.com/'
data = './data/'

approved = {
   '213839777840103426': '213839777840103426', # crabb
   '481168580541415425': '481168580541415425' # hermit
}

#/ urls
urljs = open(data+'urls.json')
urls = json.load(urljs)

mixgif = urls['Media']['mixgif']
julico = urls['Media']['julico']
bossico = urls['Media']['bossico']
testu = urls['Pages']['testu']
julirl = urls['Pages']['julirl']
dnkurl = urls['Pages']['dnkurl']

#// Functions
random.seed()

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
   if approved[author.id]:
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

#/ EXP
def addxp(user):
   usdict = None
   with open(data+'users.json') as users:
      usdict = json.load(users)
      id = user.id
      if id in usdict:
         usdict[id]['exp'] += 1
         usdict[id]['name'] = user.name
         usdict[id]['cap'] = round( 0.04 * (pow(usdict[id]['lvl'],3)) + 0.8 * (pow(usdict[id]['lvl'],2)) + 2 * usdict[id]['lvl'])
         if usdict[id]['exp'] >= usdict[id]['cap']:
            usdict[id]['lvl'] += 1
            usdict[id]['cap'] = round( 0.04 * (pow(usdict[id]['lvl'],3)) + 0.8 * (pow(usdict[id]['lvl'],2)) + 2 * usdict[id]['lvl'])
            usdict[id]['exp'] = 0
      else:
         usdict[id] = {
            'exp': 0,
            'lvl': 1,
            'cap': 3,
            'name': user.name
         }
   with open(data+'users.json', 'w') as users:
      json.dump(usdict,users,sort_keys=True,indent=3)

def xparray(id):
   usdict = None
   with open(data+'users.json') as users:
      usdict = json.load(users)
   try:
      lvl = usdict[id]['lvl']
      exp = usdict[id]['exp']
      cap = usdict[id]['cap']

      return [exp,lvl,cap]
   except KeyError:
      return False

#// main
@client.async_event
def on_message(message):
   # we do not want the bot to reply to itself
   if message.author == client.user:
      return

   addxp(message.author)

   # Normal
   if message.content.startswith('--cmds') or message.content.startswith('--commands'):
      yield from client.send_typing(message.channel)
      embedo=discord.Embed(title="Commands", url=dnkurl, description="```Here's the commands for N1RV Ann-a v0.2. Prefix: '--'```", color=0x832297)
      embedo.set_author(name="Jill", url=julirl, icon_url=julico)
      embedo.set_image(url=mixgif)
      def addcmds():
         embfile = None
         with open(data+'cmds.json') as openfile:
            embfile = json.load(openfile)
         for i in embfile:
            print(type(i))
            if i.get('usage'):
               descstr = i.get('description') + ("\nUsage: `{}`".format(i.get('usage')))
               embedo.add_field(name=i.get('command'), value=descstr, inline=False)
            else:
               embedo.add_field(name=i.get('command'), value=i.get('description'), inline=False)
      addcmds()
      yield from client.send_message(message.channel,embed=embedo)

   if message.content.startswith('--chance '):
      chances = parse(message.content)
      authid = message.author.id
      try:
         cho1 = int(chances[1])
         cho2 = int(chances[2])
         
         newint = random.randint(cho1,cho2)
         chomsg = ('<@{}> :8ball: `Selected: {}`').format(authid,newint)
         printf('Random int: %d',newint)
         yield from client.send_message(message.channel,chomsg)
      except ValueError:
         errmsg = ('<@{}> Please use an integer for your range! Example: `--chance 1 50`').format(authid)
         yield from client.send_message(message.channel,errmsg)
      except IndexError:
         errmsg = ('<@{}> Please use an integer for your range! Example: `--chance 1 50`').format(authid)
         yield from client.send_message(message.channel,errmsg)

   # API
   if message.content.startswith('--rbxinfo '):
      yield from client.send_typing(message.channel)
      checkthis = checkstr(message.content)
      if checkthis and checkthis['Username'] != 'ROBLOX':
         infostr = '--Username--: %s\n--User ID--: %d' % (checkthis['Username'],checkthis['Id'])
         embed=discord.Embed(title="Quick Info for %s:" % checkthis['Username'], color=0xf02b39)
         embed.set_author(name="Jill", url="https://roblox.com/users/" + str(checkthis['Id']), icon_url=julico)
         embed.set_thumbnail(url=getthumb(checkthis['Id']))
         embed.add_field(name='Username', value=checkthis['Username'], inline=True)
         embed.add_field(name='User ID', value=str(checkthis['Id']), inline=True)
         embed.add_field(name='Primary Group', value=primgrp(checkthis), inline=True)
         embed.add_field(name='Presence', value=checkthis['Presence'], inline=True)
         yield from client.send_message(message.channel, embed=embed)
      else:
         infostr = 'Incorrect syntax! Correct usage: `--rbxinfo 261`'
         yield from client.send_message(message.channel, content=infostr)

   # Moderation
   if message.content.startswith('--clean ') and checkowner(message.author):
      pmsg = parse(message.content)
      cmd = pmsg[1]
      if cmd == 'self':
         def is_me(m):
            return m.author == client.user
         
         def is_metoo(m):
            return m.author == message.author

         yield from client.send_typing(message.channel)

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
      elif cmd == 'all':
         yield from client.send_typing(message.channel)

         deltree = yield from client.purge_from(message.channel, limit=5000)
         delmsg = '*Deleted {} messages.*'.format(len(deltree))
         printf(delmsg)
         
         if len(pmsg) > 2:
            snd = yield from client.send_message(message.channel,content=delmsg)
            time.sleep(float(pmsg[2]))
            yield from client.delete_message(snd)

   if message.content.startswith('--exit') and checkowner(message.author):
      yield from client.delete_message(message)
      print('Logging out...')
      print('-----------------------------------')
      logmsg = 'Alright <@%s>, logging out.' % message.author.id
      sendlog = yield from client.send_message(message.channel,content=logmsg)
      time.sleep(2)
      yield from client.delete_message(message=sendlog)
      yield from client.logout()

   # Levels
   if message.content.startswith('--levels'):
      yield from client.send_typing(message.channel)
      
      msgpars = parse(message.content)
      if len(msgpars) > 1:
         usrid = msgpars[1]
         userarr = xparray(usrid)
         if userarr:
            exp = userarr[0]
            lvl = userarr[1]
            cap = userarr[2]

            embedo=discord.Embed(title='Level info for <@{}>:'.format(usrid), color=0x934ac4)
            embedo.add_field(name='*EXP*', value=str(exp), inline=True)
            embedo.add_field(name='*Level*', value=str(lvl), inline=True)
            embedo.add_field(name='*EXP until next level*', value='({0} / {1})'.format(exp,cap), inline=True)
            embedo.set_footer(text='N1RV Ann-a 0.3 | ' + str(datetime.utcnow()),icon_url = bossico)
            yield from client.send_message(message.channel,embed=embedo)
         else:
            errmsg = 'User <@{}> has no level! Maybe they haven\'t posted recently?'.format(usrid)

            yield from client.send_message(message.channel,errmsg)
      else:
         usrid = message.author.id
         userarr = xparray(usrid)
         exp = userarr[0]
         lvl = userarr[1]
         cap = userarr[2]

         embedo=discord.Embed(title='Stats:', color=0x934ac4)
         embedo.set_author(name="Jill", url=julirl, icon_url=julico)
         embedo.add_field(name='*EXP*', value=str(exp), inline=False)
         embedo.add_field(name='*Level*', value=str(lvl), inline=False)
         embedo.add_field(name='*EXP until next level*', value='({0} / {1})'.format(exp,cap), inline=False)
         embedo.set_footer(text='N1RV Ann-a 0.3 | ' + str(datetime.utcnow()),icon_url = bossico)
         yield from client.send_message(message.channel,content=('Level info for <@{}>:'.format(usrid)),embed=embedo)
         




@client.async_event
def on_ready():
   print('Logged in as')
   print(client.user.name)
   print(client.user.id)
   print('Time to mix drinks and save lives.')
   print('-----------------------------------')

client.run(TOKEN)