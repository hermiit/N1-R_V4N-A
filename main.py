#// init
import discord
import requests
client = discord.Client()

#/ vars
TOKEN = "NDg4MTA3OTIyMDg2NDI4Njcz.DnYIOg.rhIw0g63U2JygBTxCBeJTVhxhTw"
iconu = "https://cdn.discordapp.com/avatars/488107922086428673/ac74d4af50b36a915400bcb648addb8a.png"
testu = "https://google.com"

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

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
