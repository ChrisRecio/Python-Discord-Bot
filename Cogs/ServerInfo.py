import discord
from discord.ext import commands

embedColor = 0xff8400  # (255, 132, 0)


class ServerInfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('ServerInfo Cog Loaded')

    @commands.command(name="Ping")
    async def Ping(self, ctx):
        target = ctx.author.display_name
        embed = discord.Embed(
            title=f"Message For {target}", description=f"Ping time for bot is {round(self.client.latency * 1000)} ms", color=embedColor)
        await ctx.send(embed=embed)

    @commands.command(name="ServerInfo")
    async def ServerInfo(self, ctx):
        server = ctx.message.guild

        embed = discord.Embed(title=f"{server.name}'s Info", color=embedColor)
        embed.add_field(name='Owner', value=server.owner, inline=False)
        embed.add_field(name='Members', value=server.member_count)
        embed.add_field(name='Region', value=server.region)
        embed.add_field(name='Created At', value=server.created_at.__format__(
            '%A, %d. %B %Y @ %H:%M:%S'))

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ServerInfo(client))
