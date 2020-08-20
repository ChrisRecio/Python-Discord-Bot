import discord
from discord.ext import commands
from requests import get
from datetime import datetime

embedColor = 0xffff00  # (255, 255, 0)


class Weather(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Weather Cog Loaded')

    @commands.command(name='Weather')
    async def Weather(self, ctx,  *, city):
        data = get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID=fb9df86d9c484eba8a69269cfb0beac9").json()

        if data['cod'] == '404':
            return await ctx.send('City not found!')

        cleared_data = {
            'City': data['name'],
            'Time': datetime.utcfromtimestamp(data['dt']).strftime('%H:%M:%S'),
            'Weather': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
            'Temperature': f"{data['main']['temp']}°C",
            'Feels like': f"{data['main']['feels_like']}°C",
            'Min temperature': f"{data['main']['temp_min']}°C",
            'Max temperature': f"{data['main']['temp_max']}°C",
            'Humidity': f"{data['main']['humidity']}%",
            'Pressure': f"{data['main']['pressure']}Pa",
            'Clouds': f"{data['clouds']['all']}%",
            'Wind': f"{data['wind']['speed']} km/h",
            'Sunset': datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
            'Sunrise': datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
        }
        embed = discord.Embed(
            title=f":white_sun_small_cloud: Weather in {cleared_data['City']}", color=embedColor)
        for key, value in cleared_data.items():
            embed.add_field(name=key, value=value)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Weather(client))
