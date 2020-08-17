import discord
from discord.ext import commands
import requests


class NSFW(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('NSFW Cog Loaded')


def setup(client):
    client.add_cog(NSFW(client))
