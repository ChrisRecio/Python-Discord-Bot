import discord
from discord.ext import commands
import lavalink
from typing import Optional
import os
import time
import re
from dotenv import load_dotenv

load_dotenv()
LavaLinkIP = os.environ['LavaLinkIP']
LavaLinkPort = os.environ['LavaLinkPort']
LavaLinkPassword = os.environ['LavaLinkPassword']

embedColor = 0x7a34eb  # (122, 52, 235)

# LavaLink Docs
# https://discordpy.readthedocs.io/en/latest/api.html


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
                return True
        else:
            await ctx.send('You are not currently connected to a voice channel!')
            return False

    # Plays Requested Song
    @commands.command(name='Play')
    @commands.max_concurrency(1, commands.BucketType.user)
    async def Play(self, ctx, *, query=None):

        if not query:
            embed = discord.Embed(
                title='**Missing Argument**', description='The query argument is required.', color=embedColor)
            embed.add_field(
                name='Usage', value='```.play <song name or url>```')
            await ctx.channel.send(embed=embed)
            return

        if await self.Join(ctx):

            try:
                player = self.client.music.player_manager.get(ctx.guild.id)

                query = f'ytsearch:{query}'
                results = await player.node.get_tracks(query)
                tracks = results['tracks'][0:1]
                track = tracks[0]

                ytVideoID = re.match('^[^v]+v=(.{11}).*', track["info"]["uri"])

                embed = discord.Embed(
                    title=f'**Now Playing**', description=track["info"]["uri"], color=embedColor)
                embed.set_thumbnail(
                    url=f'http://img.youtube.com/vi/{ytVideoID.group(1)}/0.jpg')
                embed.set_footer(
                    text=f'Requested by: {ctx.message.author.display_name}')
                await ctx.channel.send(embed=embed)

                time.sleep(1.5)

                player.add(requester=ctx.author.id, track=track)

                # TODO have bot wait 5 ish mins before leaving

                if not player.is_playing:
                    await player.play()

            except Exception as error:
                print(error)

        else:
            pass

    # Pause current song
    @commands.command(name='Pause')
    async def Pause(self, ctx):
        # TODO Pause song
        pass

    # Resumes playback of song
    @commands.command(name='Resume', aliases=['unpause'])
    async def Resume(self, ctx):
        # TODO resume playback of song
        # TODO check if song is currently paused
        pass

    # Skips current song
    @commands.command(name='Skip', aliases=['next'])
    async def Skip(self, ctx):
        player = self.client.music.player_manager.get(ctx.guild.id)

        # TODO Check if bot is in vc

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voice channel!')
        else:
            await player.skip()
            await ctx.send('✅ Skipped current track.')
        # TODO Check if bot is playing and if the ctx.author is in the voice channel with bot

    # Shows songs in queue
    @commands.command(name='Queue')
    async def Queue(self, ctx):
        # TODO WORKING JUST NEED TO FORMAT IN AN EMBED
        player = self.client.music.player_manager.get(ctx.guild.id)

        queue = []

        for song in player.queue:
            queue.append(song)

        # if not queue:
        #     await ctx.send('Music queue is empty.')
        # else:
        #     embed = discord.Embed(title='Songs In Queue', color=embedColor)

        await ctx.send(queue)

    # Leaves Voice Channel
    @commands.command(name='Disconnect', aliases=['leave', 'stop'])
    async def Disconnect(self, ctx):
        player = self.client.music.player_manager.get(ctx.guild.id)

        # TODO fix if bot is not connected

        if not player.is_connected:
            return await ctx.send('Bot is not in a voice channel!')

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
