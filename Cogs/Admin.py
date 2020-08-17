from typing import Optional
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord.ext.commands import Greedy, command, has_permissions, bot_has_permissions

embedColor = 0xff0000  # (255, 0, 0)


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin Cog Loaded')

    @commands.command(name="Clear", aliases=["purge"])
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def Clear(self, ctx, targets: Greedy[discord.Member], limit: Optional[int] = 1):
        def _check(message):
            return not len(targets) or message.author in targets

        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow() - timedelta(days=14),
                                                  check=_check)

                await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)

        else:
            await ctx.send("The limit provided is not within acceptable bounds.")


def setup(client):
    client.add_cog(Admin(client))
