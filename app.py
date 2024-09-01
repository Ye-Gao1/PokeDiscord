import discord
import requests
import random, os
import yaml
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

rarity_tiers = {"Common": 60, "Uncommon": 25, "Rare": 10, "Legendary": 5}

if os.path.exists('caught_pokemon.yaml'):
    with open('caught_pokemon.yaml', 'r') as file:
        caught_pokemon = yaml.safe_load(file) or {}
else:
    caught_pokemon = {}


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='catch')
async def catch_pokemon(ctx):
    pokemon_id = random.randint(1, 898)
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')

    if response.status_code == 200:
        pokemon_data = response.json()
        name = pokemon_data['name'].capitalize()
        sprite_url = pokemon_data['sprites']['front_default']
        types = [t['type']['name'].capitalize() for t in pokemon_data['types']]
        height = f"{pokemon_data['height']/10} m"
        weight = f"{pokemon_data['weight']/10} kg"
        rarity = random.choices(list(rarity_tiers.keys()),
                                weights=rarity_tiers.values(),
                                k=1)[0]

        user_id = str(ctx.author.id)
        if user_id not in caught_pokemon:
            caught_pokemon[user_id] = []
        caught_pokemon[user_id].append({
            'name': name,
            'types': types,
            'height': height,
            'weight': weight,
            'rarity': rarity
        })
        with open('caught_pokemon.yaml', 'w') as file:
            yaml.dump(caught_pokemon, file)

        embed = discord.Embed(title=f'A wild {name} appeared!', color=0x00ff00)
        embed.set_image(url=sprite_url)
        embed.add_field(name='Type', value=', '.join(types))
        embed.add_field(name='Height', value=height)
        embed.add_field(name='Weight', value=weight)
        embed.add_field(name='Rarity', value=rarity)

        await ctx.send(embed=embed)
        await ctx.send(f"Congratulations! You caught a {name}!")
    else:
        await ctx.send("Oops! Failed to catch a Pokémon. Try again later.")


@bot.command(name='pokedex')
async def view_pokedex(ctx):
    user_id = str(ctx.author.id)
    if user_id in caught_pokemon and caught_pokemon[user_id]:
        embed = discord.Embed(title=f"{ctx.author.name}'s Pokédex",
                              color=0x0000ff)
        for pokemon in caught_pokemon[user_id]:
            embed.add_field(
                name=pokemon['name'],
                value=
                f"Type: {', '.join(pokemon['types'])}\nRarity: {pokemon['rarity']}\nHeight: {pokemon['height']}\nWeight: {pokemon['weight']}",
                inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Your Pokédex is empty. Go catch some Pokémon!")


bot.run(os.environ['Token'])
