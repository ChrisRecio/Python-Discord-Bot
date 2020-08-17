import random
import time
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType
import urllib.parse
import requests
from Utils import Responses

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
    async def Mock(self, ctx, *input):

        inputString = ' '.join(input)
        inputStringAsList = [c for c in inputString]
        result = ''
        flip = True

        for i in inputStringAsList:
            if flip:
                result += i.lower()
            else:
                result += i.upper()
            flip = not flip

        await ctx.send(result)

    # Magic 8 ball
    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question: commands.clean_content):
        answer = random.choice(Responses.eightballAnswers)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    # Coin Flip
    @commands.command(aliases=['flip', 'coin'])
    async def coinflip(self, ctx):
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    # Creates let me google this for you link
    @commands.command(pass_context=True, name="lmgtfy", aliases=['google'])
    async def lmgtfy(self, ctx, *, msg: str):
        lmgtfy = 'http://lmgtfy.com/?q='
        await ctx.send(lmgtfy + urllib.parse.quote_plus(msg.lower().strip()))

    # Gets a picture of a cat
    @commands.command(name="Cat", aliases=['randomCat', 'Random Cat'])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def Cat(self, ctx):
        url = "https://api.thecatapi.com/v1/images/search"
        r = requests.get(url)
        data = r.json()
        imgURL = data[0]["url"]

        embed = discord.Embed(
            title="Random Cat", color=embedColor)
        embed.set_image(url=imgURL)
        await ctx.send(embed=embed)

    # Gets a cat fact
    @commands.command(name="Cat Fact", aliases=["CatFact", "CatFacts", "Cat Facts"])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def CatFact(self, ctx):
        url = "https://catfact.ninja/fact"
        r = requests.get(url)
        data = r.json()
        fact = data['fact']

        embed = discord.Embed(
            title="Random Cat Fact", color=embedColor, description=fact)
        await ctx.send(embed=embed)

    # Gets a picture of a dog
    @commands.command(name="Dog", aliases=['randomDog', 'Random Dog'])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def Dog(self, ctx):
        url = "https://dog.ceo/api/breeds/image/random"
        r = requests.get(url)
        data = r.json()
        imgURL = data["message"]

        embed = discord.Embed(
            title="Random Dog", color=embedColor)
        embed.set_image(url=imgURL)
        await ctx.send(embed=embed)

    # Gets a picture of a dog
    @commands.command(name="Doge", aliases=['randomDoge', 'Random Doge', 'adam'])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def Doge(self, ctx):
        url = "http://shibe.online/api/shibes?count=1"
        r = requests.get(url)
        data = r.json()
        imgURL = data[0]

        embed = discord.Embed(
            title="Random Doge", color=embedColor)
        embed.set_image(url=imgURL)
        await ctx.send(embed=embed)

    # Gets a picture of a bird
    @commands.command(name="Birb", aliases=['randomBird', 'Random Bird', 'randomBirb', 'Random Birb'])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def Birb(self, ctx):
        url = "https://api.alexflipnote.dev/birb"
        r = requests.get(url)
        data = r.json()
        imgURL = data['file']

        embed = discord.Embed(
            title="Random Birb", color=embedColor)
        embed.set_image(url=imgURL)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Misc(client))
