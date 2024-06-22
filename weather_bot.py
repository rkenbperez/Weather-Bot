import discord
from discord.ext import commands
import aiohttp

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot client
client = commands.Bot(command_prefix='!', intents=intents)

# Replace this with your actual API key
API_KEY = ''
TOKEN = ''

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def weather(ctx, city: str):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            if data['cod'] != 200:
                await ctx.send(f'Error: {data["message"]}')
                return

            weather_data = data['weather'][0]
            main_data = data['main']
            wind_data = data['wind']

            description = weather_data['description'].capitalize()
            current_temperature = f'{main_data["temp"]}°C'
            min_temperature = f'{main_data["temp_min"]}°C'
            max_temperature = f'{main_data["temp_max"]}°C'
            humidity = f'{main_data["humidity"]}%'
            wind_speed = f'{wind_data["speed"]} m/s'

            embed = discord.Embed(title=f'{city} Weather', description=description, color=discord.Color.blue())
            embed.add_field(name='Current Temperature', value=current_temperature, inline=True)
            embed.add_field(name='Minimum Temperature', value=min_temperature, inline=True)
            embed.add_field(name='Maximum Temperature', value=max_temperature, inline=True)
            embed.add_field(name='Humidity', value=humidity, inline=True)
            embed.add_field(name='Wind Speed', value=wind_speed, inline=True)

            await ctx.send(embed=embed)


client.run(TOKEN)