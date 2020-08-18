from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands import command, cooldown, BucketType

embedColor = 0x74ff38  # (116, 255, 56)


class UserInfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('UserInfo Cog Loaded')

    # Returns mentioned user's avatar or sender if none provided
    @commands.command(name="avatar")
    async def Avatar(self, ctx, target: Optional[discord.Member] = None):
        if target is None:
            target = ctx.author

        embed = discord.Embed(
            title=f"{target.display_name}'s Profile Picture", color=embedColor)
        embed.set_image(url='{}'.format(target.avatar_url))
        await ctx.send(embed=embed)

    # Returns mentioned user's profile info or sender if none provided
    @commands.command(name="userInfo", aliases=["accountInfo"])
    async def AccountInfo(self, ctx, target: Optional[discord.Member] = None):
        if target is None:
            target = ctx.author

        embed = discord.Embed(
            title=f"{target.display_name}'s Account Information", color=embedColor)
        embed.set_thumbnail(url='{}'.format(target.avatar_url))
        embed.add_field(name='Nick', value=target.nick, inline=True)
        embed.add_field(name='Status', value=target.status, inline=True)
        embed.add_field(name='Game', value=target.activity, inline=True)
        embed.add_field(name='Account Created', value=target.created_at.__format__(
            '%A, %d. %B %Y @ %H:%M:%S'))
        embed.add_field(name='Join Date', value=target.joined_at.__format__(
            '%A, %d. %B %Y @ %H:%M:%S'))
        embed.set_footer(
            text=f'Requested by {ctx.message.author.nick}')

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(UserInfo(client))
