import random
import time
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType
import urllib.parse
import requests

embedColor = 0x42b0ff  # (66, 176, 255)


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Misc Cog Loaded')

    # Sends 3 claps
    @commands.command(name="SlowClap", aliases=["Clap"])
    async def SlowClap(self, ctx):
        await ctx.send(':clap:')
        time.sleep(1)
        await ctx.send(':clap:')
        time.sleep(1)
        await ctx.send(':clap:')

    # Alternates capitalizations
    @commands.command(name="Mock", aliases=["Sarcastic"])
    async def Mock(self, ctx, input: str):

        wordAsList = list(input)
        result = ''
        flip = True

        for i in wordAsList:
            if flip:
                result += i.lower()
            else:
                result += i.upper()
            flip = not flip

        await ctx.send(result)

    # Creates let me google this for you link
    @commands.command(pass_context=True, name="lmgtfy", aliases=['google'])
    async def lmgtfy(self, ctx, *, msg: str):
        lmgtfy = 'http://lmgtfy.com/?q='
        await ctx.send(lmgtfy + urllib.parse.quote_plus(msg.lower().strip()))

    # Gets a picture of a cat
    @commands.command(name="cat", aliases=['randomCat'])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cat(self, ctx):
        url = "https://api.thecatapi.com/v1/images/search"
        r = requests.get(url)
        data = r.json()
        imgURL = data[0]["url"]

        embed = discord.Embed(
            title="Random Cat", color=embedColor)
        embed.set_image(url=imgURL)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Misc(client))
