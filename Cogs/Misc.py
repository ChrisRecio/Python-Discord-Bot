import random
import time
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType

embedColor = 0x42b0ff  # (66, 176, 255)

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Misc Cog Loaded')

    @commands.command(name="Ping")
    async def Ping(self, ctx):
        target = ctx.author.display_name
        embed = discord.Embed(
            title=f"Message For {target}", description=f"Ping time for bot is {round(self.client.latency * 1000)} ms", color=embedColor)
        await ctx.send(embed=embed)

    @commands.command(name="SlowClap", aliases=["clap"])
    async def SlowClap(self, ctx):
        await ctx.send(':clap:')
        time.sleep(1)
        await ctx.send(':clap:')
        time.sleep(1)
        await ctx.send(':clap:')

    # @commands.command()
    # async def lmgtfy(self, ctx, *, input_str: str):

    #     search_terms = input_str.replace("+", "%2B").replace(" ", "+"), mass_mentions=True
    #     await ctx.send("https://lmgtfy.com/?q={}".format(search_terms))


def setup(client):
    client.add_cog(Misc(client))
