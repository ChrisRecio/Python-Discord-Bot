import random
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType

embedColor = 0x42b0ff #  (66, 176, 255)


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Misc Cog Loaded')

    
    @commands.command()
    async def ping(self, ctx):
        target = ctx.author
        embed = discord.Embed(title = f"Message For {target}", description = f"Ping time for bot is {round(self.client.latency * 1000)} ms", color = embedColor)
        await ctx.send(embed=embed)
    

def setup(client):
    client.add_cog(Misc(client))

