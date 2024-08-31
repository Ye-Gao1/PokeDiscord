import discord
from discord import app_commands
import random, os

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await tree.sync()

dice_emojis = {
    1: "⚀",
    2: "⚁",
    3: "⚂",
    4: "⚃",
    5: "⚃",
    6: "⚅"
}

@tree.command(name="roll", description="Roll a specified number of dice with a specified number of sides")
async def roll(interaction: discord.Interaction, sides: int = 6, count: int = 1):
    if sides < 2:
        await interaction.response.send_message("The dice must have at least 2 sides!")
    elif count < 1:
        await interaction.response.send_message("You must roll at least one dice!")
    else:
        results = []
        for _ in range(count):
            result = random.randint(1, sides)
            if result in dice_emojis and sides <= 6:
                results.append(f'{dice_emojis[result]} {result}')
            else:
                results.append(str(result))

        await interaction.response.send_message(f'You rolled: {" ".join(results)} on a {sides}-sided dice!')

bot.run(os.environ['Token'])
