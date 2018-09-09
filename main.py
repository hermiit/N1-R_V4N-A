#// init
import discord
import time
import requests
import datetime
client = discord.Client()

#/ vars
TOKEN = "no"
iconu = "https://cdn.discordapp.com/avatars/488107922086428673/ac74d4af50b36a915400bcb648addb8a.png"
testu = "https://google.com"
mixurl = "https://vignette.wikia.nocookie.net/va11halla/images/5/51/Mixing.gif"
julirl = "http://va11halla.wikia.com/wiki/Julianne_Stingray"
dnkurl = "http://va11halla.wikia.com/wiki/Drinktionary"



dnums = {
    ":one:"  : "Adelhyde",
    ":two:"  : "Bronson Extract",
    ":three:": "Powdered Delta",
    ":four:" : "Flanergide",
    ":five:" : "Karmotrine"
}

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
        embedo.set_author(name="Jill", icon_url=iconu)
        await client.send_message(message.channel, embed=embedo)

    if message.content.startswith('**drinktionary'):
        embedo=discord.Embed(title="Drinktionary", url=dnkurl, description="Here are the ingredients, please react with which number you want to use. (emoji :one:-:five:)", color=0x832297)
        embedo.set_author(name="Jill", url=julirl, icon_url=iconu)
        embedo.set_thumbnail(url=mixurl)
        embedo.add_field(name=(1), value="Adelhyde", inline=True)
        embedo.add_field(name=(2), value="Bronson Extract", inline=True)
        embedo.add_field(name=(3), value="Powdered Delta", inline=True)
        embedo.add_field(name=(4), value="Flanergide", inline=True)
        embedo.add_field(name=(5), value="Karmotrine", inline=True)
        embmsg = await client.send_message(message.channel, embed=embedo)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Time to mix drinks and save lives.')
    print('------')

client.run(TOKEN)
