import discord
import requests
client = discord.Client()

TOKEN = 'NDg4MTA3OTIyMDg2NDI4Njcz.DnXyqg.U4kD8T39b8UV8IfGaCCV3WkmANA'

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('**hello'):
        msg = 'Hey, {0.author.mention}.'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('**youok'):
        msg = 'Doing fine, {0.author.mention}.'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
