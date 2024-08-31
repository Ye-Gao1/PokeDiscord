import discord
from discord import app_commands
import random
from PIL import Image, ImageDraw, ImageFont
import os

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await tree.sync()

def create_dice_image(value):
    size = 100
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)

    dot_positions = {
        1: [(50, 50)],
        2: [(25, 25), (75, 75)],
        3: [(25, 25), (50, 50), (75, 75)],
        4: [(25, 25), (25, 75), (75, 25), (75, 75)],
        5: [(25, 25), (25, 75), (75, 25), (75, 75), (50, 50)],
        6: [(25, 25), (25, 50), (25, 75), (75, 25), (75, 50), (75, 75)]
    }

    for pos in dot_positions[value]:
        draw.ellipse((pos[0] - 10, pos[1] - 10, pos[0] + 10, pos[1] + 10), fill='black')

    img_path = f'dice_{value}.png'
    img.save(img_path)
    return img_path

@tree.command(name="roll", description="Roll a specified number of dice with a specified number of sides")
async def roll(interaction: discord.Interaction, sides: int = 6, count: int = 1):
    if sides < 2:
        await interaction.response.send_message("The dice must have at least 2 sides!")
    elif count < 1:
        await interaction.response.send_message("You must roll at least one dice!")
    else:
        image_paths = []
        for _ in range(count):
            result = random.randint(1, sides)
            if sides == 6:
                img_path = create_dice_image(result)
                image_paths.append(img_path)
            else:
                await interaction.response.send_message(f'You rolled: {result} on a {sides}-sided dice!')

        files = [discord.File(img_path) for img_path in image_paths]
        await interaction.response.send_message(f'You rolled:', files=files)

bot.run(os.environ['Token'])
