"""
File Name: bot_main.py
Original Author: Fis-chl
Created On: 04/12/2022
File Description: Python script that is responsible for starting the AniList bot.
"""

import discord
import os

from discord.ext.commands import bot as dbot
from dotenv import load_dotenv
from unofficial_anilist_api.request_handler import AniListRequestHandler
from unofficial_anilist_api.bot.embeds import EmbedHandler

# Load .env file
load_dotenv()

# Create a bot
intents = discord.Intents.default()
intents.messages = True
bot = dbot.Bot(command_prefix="-", intents=intents)


# Functions not tagged with @bot
async def valid_data(data):
    return 'errors' not in data


# Functions tagged with @bot
@bot.event
async def on_ready():
    await anilist.create_session()  # Initialise an aiohttp session for the AniList request handler
    embeds.avatar_url = bot.user.avatar_url
    print(f'Logged in as {bot.user}')


# Commands
# Anime-related commands
@bot.command()
async def get_anime(ctx, arg):
    data = await anilist.anime_by_id(anime_id=arg)
    if await valid_data(data):
        embed = await embeds.anime_embed(data)
        await send_message(ctx.channel, embed=embed)


@bot.command()
async def search_anime(ctx, arg):
    data = await anilist.anime_by_title(anime_title=arg)
    if await valid_data(data):
        embed = await embeds.anime_embed(data)
        await send_message(ctx.channel, embed=embed)


# Manga-related commands
@bot.command()
async def get_manga(ctx, arg):
    data = await anilist.manga_by_id(manga_id=arg)
    if await valid_data(data):
        embed = await embeds.manga_embed(data)
        await send_message(ctx.channel, embed=embed)


@bot.command()
async def search_manga(ctx, arg):
    data = await anilist.manga_by_title(manga_title=arg)
    if await valid_data(data):
        embed = await embeds.manga_embed(data)
        await send_message(ctx.channel, embed=embed)

# End Commands


async def send_message(channel, **kwargs):
    embed, content = None, None
    if 'embed' in kwargs:
        embed = kwargs['embed']
    if 'content' in kwargs:
        content = kwargs['content']
    await channel.send(content=content, embed=embed)


# Instantiate request handler to do calls to AniList API
anilist = AniListRequestHandler()

# Instantiate an embed handler to create embeds
embeds = EmbedHandler(None)

# Run the bot
bot.run(os.getenv('BOT_TOKEN'))
# Update the avatar_url
