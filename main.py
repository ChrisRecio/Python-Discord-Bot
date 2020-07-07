import discord
from discord.ext import commands
import json


try:
    with open('BotConfig.json', 'r') as json_file:
        data = json.load(json_file)

        TOKEN = data['Token']
        json_file.close()

except IOError:
    print('Please Enter Your Bot Token')
    TOKEN = input()
    data = {'Token': TOKEN}
    with open('BotConfig.json', 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Ready')


@client.command()
async def ping(ctx):
    await ctx.send('pong')



client.run(TOKEN)
