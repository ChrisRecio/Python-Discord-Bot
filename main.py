import json
import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# DOCKER ENV VARIABLE
# ENV VARIABLE NAME: DiscordBotToken

# TOKEN = os.environ['DiscordBotToken']

# USE THIS LOCALLY
# Looks for BotConfig.json if doesnt exist creates one
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

client = commands.Bot(command_prefix='.', case_insensitive=True)


@client.event
async def on_ready():
    print('Bot Has Successfully Started')


# LOAD AND UNLOAD INDIVIDUAL COGS
# @client.command()
# async def load(ctx, extension):
#     client.load_extension(f'Cogs.{extension}')


# @client.command()
# async def unload(ctx, extension):
#     client.unload_extension(f'Cogs.{extension}')


# Command Not Found Error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


# Loads all Cog files on start
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')

client.run(TOKEN)
