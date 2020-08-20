# Python Discord Bot

A Discord bot written in Python using the Discord.py and Lavalink.py packages.

## Getting Started

### Prerequisities

In order to run this container you'll need docker installed.

- [Windows](https://docs.docker.com/windows/started)
- [OS X](https://docs.docker.com/mac/started/)
- [Linux](https://docs.docker.com/linux/started/)

In order for the music functions to work, you will need a Lavalink server.

-[Lavalink](https://github.com/Frederikam/Lavalink)

### Usage

#### Container Parameters

List the different parameters available to your container

```shell
docker pull pootie/discordbot
```

#### Environment Variables

- `DiscordBotToken` - Your Discord bot token
- `DiscordBotPrefix` - The prefix you would like the bot to react to
- `LavaLinkIP` - Ip of the LavaLink server
- `LavaLinkPort` - Port of the LavaLink server
- `LavaLinkPassword` - LavaLink server password

## Built With

- Python
- Discord.py Rewrite
- Lavalink.py
