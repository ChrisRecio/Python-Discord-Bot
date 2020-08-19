import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.environ['DiscordBotToken']
PREFIX = os.environ['DiscordBotPrefix']

client = commands.Bot(command_prefix=PREFIX, case_insensitive=True)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Walter'))
    print('Bot Has Successfully Started')


# LOAD AND UNLOAD INDIVIDUAL COGS
# @client.command()
# async def load(ctx, extension):
#     client.load_extension(f'Cogs.{extension}')


# @client.command()
# async def unload(ctx, extension):
#     client.unload_extension(f'Cogs.{extension}')

# @client.command()
# async def reload(ctx, extension):
    # client.unload_extension(f'Cogs.{extension}')
    # client.load_extension(f'Cogs.{extension}')


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
