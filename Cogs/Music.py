import discord
from discord.ext import commands, tasks
import lavalink
import asyncio
import os
import re
from dotenv import load_dotenv
from validator_collection import checkers

load_dotenv()
LavaLinkIP = os.environ['LavaLinkIP']
LavaLinkPort = os.environ['LavaLinkPort']
LavaLinkPassword = os.environ['LavaLinkPassword']

embedColor = 0x7a34eb  # (122, 52, 235)

# LavaLink Docs
# https://lavalink.readthedocs.io/en/latest/lavalink.html

# TODO Try making bot wait 5 mins before leaving after finishing queue
# TODO Test to see if LavaNode Reconnects with activity after timing out


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
            player.store('channel', ctx.channel.id)

            if not player.is_playing:
                player.queue.clear()
                await player.stop()
                await ctx.send(f'Joined `{vc.name}` the `{vc.name}` voice channel.')
                await self.connect_to(ctx.guild.id, str(vc.id))
                await asyncio.sleep(300)
                if not player.is_playing:
                    await ctx.send(f'Left due to innactivity.')
                    await self.connect_to(ctx.guild.id, None)

            if player.is_connected and player.is_playing:
                await ctx.send(f'Moved to the `{vc.name}` voice channel.')
                await self.connect_to(ctx.guild.id, str(vc.id))
                await asyncio.sleep(300)
                if not player.is_playing:
                    await ctx.send(f'Left `{vc.name}` due to innactivity.')
                    await self.connect_to(ctx.guild.id, None)
        else:
            await ctx.send('You are not currently connected to a voice channel!', delete_after=10)

    # Plays Requested Song
    @commands.command(name='Play')
    @commands.max_concurrency(1, commands.BucketType.user)
    async def Play(self, ctx, *, query=None):

        if not query:
            embed = discord.Embed(
                title='**Missing Argument**', description='The query argument is required.', color=embedColor)
            embed.add_field(
                name='Usage', value='```.play <song name or url>```')
            await ctx.channel.send(embed=embed, delete_after=10)
            return

        player = self.client.music.player_manager.get(ctx.guild.id)

        if not player:
            await self.Join(ctx)
        elif not player.is_connected:
            await self.Join(ctx)

        try:
            player = self.client.music.player_manager.get(ctx.guild.id)

            if checkers.is_url(query):  # Checks if the user submitted a link or song name
                # Cleanse link in case it is a youtube list
                youtubeVideoId = re.match('^[^v]+v=(.{11}).*', query)
                ytSearch = f'https://www.youtube.com/watch?v={youtubeVideoId.group(1)}'
            else:
                ytSearch = query

            query = f'ytsearch:{ytSearch}'
            results = await player.node.get_tracks(query)
            tracks = results['tracks'][0:1]
            track = tracks[0]

            if player.is_playing:
                title = 'Added To Queue'
            else:
                title = 'Now Playing'

            embed = discord.Embed(
                title=f'**{title}**', description=track["info"]["uri"], color=embedColor)
            embed.set_thumbnail(
                url=f'http://img.youtube.com/vi/{track["info"]["identifier"]}/0.jpg')
            embed.set_footer(
                text=f'Requested by: {ctx.message.author.display_name}')
            await ctx.channel.send(embed=embed)

            player.add(requester=ctx.author.id, track=track)

            if not player.is_playing:
                await player.play()

        except Exception as error:
            print(error)

    # Shows current song
    @commands.command(name='NowPlaying', aliases=['Now Playing', 'Current', 'Current Track', 'Currently Playing'])
    async def NowPlaying(self, ctx):
        player = self.client.music.player_manager.get(ctx.guild.id)

        # Check if bot is connected to a voice channel
        if not player:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)
        elif not player.is_connected:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)

        # Check if bot is playing audio
        if not player.is_playing:
            return await ctx.send('Bot is not playing anything!', delete_after=10)

        currentSong = ''
        track = player.current
        currentSong = f'[**{track.title}**]({track.uri})'

        embed = discord.Embed(title='Currently Playing',
                              description=currentSong, color=embedColor)
        embed.set_thumbnail(
            url=f'http://img.youtube.com/vi/{track.identifier}/0.jpg')
        await ctx.send(embed=embed)

    # Pause current song
    @commands.command(name='Pause')
    async def Pause(self, ctx):
        player = self.client.music.player_manager.get(ctx.guild.id)

        # Check if bot is connected to a voice channel
        if not player:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)
        elif not player.is_connected:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)

        # Check if bot is playing audio
        if not player.is_playing:
            return await ctx.send('Bot is not playing anything!', delete_after=10)

        # Check if user calling skip is in the same voice channel as bot
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voice channel!', delete_after=10)
        else:
            await ctx.send('Song paused!')
            await player.set_pause(True)

    # Resumes playback of song
    @commands.command(name='Resume', aliases=['unpause'])
    async def Resume(self, ctx):
        player = self.client.music.player_manager.get(ctx.guild.id)

        # Check if bot is connected to a voice channel
        if not player:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)
        elif not player.is_connected:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)

        # Check if bot is playing audio
        if not player.is_playing:
            return await ctx.send('Bot is not playing anything!', delete_after=10)

        # Check if user calling skip is in the same voice channel as bot
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voice channel!', delete_after=10)
        else:
            await ctx.send('Song resumed!')
            await player.set_pause(False)

    # Skips current song
    @commands.command(name='Skip', aliases=['next'])
    async def Skip(self, ctx):
        player = self.client.music.player_manager.get(ctx.guild.id)

        # Check if bot is connected to a voice channel
        if not player:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)
        elif not player.is_connected:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)

        # Check if bot is playing audio
        if not player.is_playing:
            return await ctx.send('Bot is not playing anything!', delete_after=10)

        # Check if user calling skip is in the same voice channel as bot
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voice channel!', delete_after=10)
        else:
            await player.skip()
            await ctx.send('✅ Skipped current track.')

    # Shows songs in queue
    @commands.command(name='Queue')
    async def Queue(self, ctx):
        player = self.client.music.player_manager.get(ctx.guild.id)

        queue_list = ''
        for index, track in enumerate(player.queue):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        if len(player.queue) == 1:
            tracks = 'track'
        else:
            tracks = 'tracks'

        embed = discord.Embed(title='Music Queue',
                              description=f'{len(player.queue)} {tracks} in queue\n\n{queue_list}', color=embedColor)
        await ctx.send(embed=embed)

    # Leaves Voice Channel
    @commands.command(name='Disconnect', aliases=['leave', 'stop'])
    async def Disconnect(self, ctx):
        player = self.client.music.player_manager.get(ctx.guild.id)

        if not player:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)
        elif not player.is_connected:
            return await ctx.send('Bot is not in a voice channel!', delete_after=10)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voice channel!', delete_after=10)

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('Stopped music playback and left the voice channel.')

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
