import random
import time
import discord
from discord.ext import commands
from discord.ext.commands import command, cooldown
from Utils import Responses

embedColor = 0x42b0ff  # (66, 176, 255)


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun Cog Loaded')

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
    @commands.command(name='8Ball')
    async def EightBall(self, ctx, *, question: commands.clean_content):
        answer = random.choice(Responses.eightballAnswers)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    # Text To Morse Code
    @commands.command(name='Morse')
    async def Morse(self, ctx, *, text: commands.clean_content):
        morseText = ''
        for letter in text.upper():
            if letter != ' ':
                morseText = morseText + Responses.MorseCodeDict[letter] + ' '
            else:
                morseText = morseText + ' / '

        await ctx.send('```' + morseText + '```')

    # Coin Flip

    @commands.command(name='Coin Flip', aliases=['flip', 'coin'])
    async def CoinFlip(self, ctx):
        coinsides = ['Heads', 'Tails']
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    # Creates let me google this for you link
    @commands.command(pass_context=True, name="Lmgtfy", aliases=['google'])
    async def Lmgtfy(self, ctx, *, msg: str):
        lmgtfy = 'http://lmgtfy.com/?q='
        await ctx.send(lmgtfy + urllib.parse.quote_plus(msg.lower().strip()))


def setup(client):
    client.add_cog(Fun(client))
