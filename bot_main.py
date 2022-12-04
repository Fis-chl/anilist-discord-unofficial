import discord
import os

from discord.ext.commands import bot
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

client.run(os.getenv('BOT_TOKEN'))
