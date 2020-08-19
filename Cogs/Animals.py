import discord
from discord.ext import commands
import requests

embedColor = 0xf98e1d  # (249, 142, 29)


class Animals(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Animals Cog Loaded')

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
    client.add_cog(Animals(client))
