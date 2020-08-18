import discord
from discord.ext import commands
import lavalink
from typing import Optional
import os
import time
from dotenv import load_dotenv

load_dotenv()
LavaLinkIP = os.environ['LavaLinkIP']
LavaLinkPort = os.environ['LavaLinkPort']
LavaLinkPassword = os.environ['LavaLinkPassword']

embedColor = 0x7a34eb  # (122, 52, 235)


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Joins Voice Channel
    @commands.command(name="Join")
    @commands.max_concurrency(1, commands.BucketType.user)
    async def Join(self, ctx):
        member = discord.utils.find(
            lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.client.music.player_manager.create(
                ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))
        else:
            await ctx.send('You are not currently connected to a voice channel!')

    # Plays Requested Song
    @commands.command(name='Play')
    @commands.max_concurrency(1, commands.BucketType.user)
    async def Play(self, ctx, *, query):
        player = self.client.music.player_manager.get(ctx.guild.id)

        # TODO if bot isnt in channel, join

        try:

            query = f'ytsearch:{query}'
            results = await player.node.get_tracks(query)
            tracks = results['tracks'][0:1]
            track = tracks[0]
            print(track)

            embed = discord.Embed(
                title=f'**{track["info"]["title"]}**', url=f'{track["info"]["uri"]}', color=embedColor)
            embed.set_thumbnail(url=f'{track["info"]["uri"]}')
            embed.set_footer(text='Requested by {ctx.message.author.nick}')
            await ctx.channel.send(embed=embed)

            time.sleep(1.5)

            player.add(requester=ctx.author.id, track=track)

            # TODO add queue system here and have bot wait 5 ish mins before leaving

            if not player.is_playing:
                await player.play()

        except Exception as error:
            print(error)

    # Leaves Voice Channel
    @commands.command(aliases=['leave', 'stop'])
    async def disconnect(self, ctx):
        player = self.client.music.player_manager.get(ctx.guild.id)

        # TODO fix if bot is not connected

        if not player.is_connected:
            return await ctx.send('Bot is not in a voice channel!')

        # TODO Test other user not in channel disconnecting bot

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voice channel!')

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('✅ Stopped music playback and left the voice channel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.client._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.music = lavalink.Client(self.client.user.id)
        self.client.music.add_node(
            LavaLinkIP, LavaLinkPort, LavaLinkPassword, 'na', 'music-node')
        self.client.add_listener(
            self.client.music.voice_update_handler, 'on_socket_response')
        self.client.music.add_event_hook(self.track_hook)
        print('Music Cog Loaded')


def setup(client):
    client.add_cog(Music(client))
