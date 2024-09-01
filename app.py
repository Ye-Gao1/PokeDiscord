import discord
import requests
import os
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

COMMAND_PREFIX = '!'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f'{COMMAND_PREFIX}kanye quote'):
        try:
            response = requests.get('https://api.kanye.rest/')
            quote = response.json().get('quote')
            await message.channel.send(f'Kanye says: "{quote}"')
        except Exception as e:
            await message.channel.send('Oops! Something went wrong.')

    elif message.content.startswith(f'{COMMAND_PREFIX}advice'):
        try:
            response = requests.get('https://api.adviceslip.com/advice')
            advice = response.json()['slip']['advice']
            await message.channel.send(f'Here\'s some advice: {advice}')
        except Exception as e:
            await message.channel.send('Oops! Something went wrong.')

    elif message.content.startswith(f'{COMMAND_PREFIX}cat'):
        try:
            response = requests.get('https://api.thecatapi.com/v1/images/search')
            cat_url = response.json()[0]['url']
            await message.channel.send(f'Here\'s a cat picture: {cat_url}')
        except Exception as e:
            await message.channel.send('Oops! Something went wrong.')

    elif message.content.startswith(f'{COMMAND_PREFIX}joke'):
        try:
            response = requests.get('https://official-joke-api.appspot.com/random_joke')
            joke_data = response.json()
            setup = joke_data['setup']
            punchline = joke_data['punchline']
            await message.channel.send(f'Here\'s a joke:\n{setup}\n{punchline}')
        except Exception as e:
            await message.channel.send('Oops! Something went wrong.')

    elif message.content.startswith(f'{COMMAND_PREFIX}fact'):
        try:
            response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
            fact = response.json()['text']
            await message.channel.send(f'Here\'s a random fact: {fact}')
        except Exception as e:
            await message.channel.send('Oops! Something went wrong.')

    elif message.content.startswith(f'{COMMAND_PREFIX}weather'):
        try:
            city = message.content.split(f'{COMMAND_PREFIX}weather ', 1)[1]
            api_key = os.environ['OPENWEATHER_API_KEY']
            response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            await message.channel.send(f'The weather in {city} is {description} with a temperature of {temperature}°C')
        except Exception as e:
            await message.channel.send('Oops! Something went wrong. Make sure to provide a valid city name.')

    elif message.content.startswith(f'{COMMAND_PREFIX}help'):
        help_message = (
            "Here are the available commands:\n"
            f"!kanye quote - Get a random Kanye West quote.\n"
            f"!advice - Get a piece of advice.\n"
            f"!cat - Get a random cat picture.\n"
            f"!joke - Get a random joke.\n"
            f"!fact - Get a random fact.\n"
            f"!weather <city> - Get the current weather for a specified city."
        )
        await message.channel.send(help_message)

client.run(os.environ['Token'])
