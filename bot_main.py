import discord
import os

from discord.ext.commands import bot as dbot
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True

bot = dbot.Bot(command_prefix="-", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run(os.getenv('BOT_TOKEN'))
