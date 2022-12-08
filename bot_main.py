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
from unofficial_anilist_api.user_list_data import UserListHandler
from bot.embeds import EmbedHandler

# Load .env file
load_dotenv()

# Create a bot
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
bot = dbot.Bot(command_prefix="-", intents=intents)


# Functions not tagged with @bot
async def valid_data(data):
    return 'errors' not in data


# Events
@bot.event
async def on_ready():
    await anilist.create_session()  # Initialise an aiohttp session for the AniList request handler
    embeds.avatar_url = bot.user.avatar_url
    print(f'Logged in as {bot.user}')


@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user:
        embed = reaction.message.embeds[0]
        emote = reaction.emoji
        direction = "f"
        if emote == '◀':
            # Go back in the list
            direction = "b"
        elif emote == '▶':
            # Go forward in the list
            direction = "f"
        else:
            return
        await reaction.message.remove_reaction(emote, user)
        user_list_id, page = await user_list_handler.get_new_page(embed, direction)
        if user_list_id is not None and page is not None:
            embed = await embeds.user_medialist_embed(user_list_id, list_page=page)
            await reaction.message.edit(embed=embed)


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


# User-related commands
@bot.command()
async def search_user(ctx, arg):
    data = await anilist.user_by_name(username=arg)
    if await valid_data(data):
        embed = await embeds.user_embed(data)
        await send_message(ctx.channel, embed=embed)


@bot.command()
async def user_list(ctx, username, listname="Completed", mediatype="ANIME"):
    if not (mediatype == "ANIME" or mediatype == "MANGA"):
        mediatype = "ANIME"
    data = await anilist.medialist_collection_by_name(username=username, listname=listname, mediatype=mediatype)
    if await valid_data(data):
        user_list_id = await user_list_handler.create_list(data, username, mediatype, listname)
        embed = await embeds.user_medialist_embed(user_list_id)
        message = await send_message(ctx.channel, embed=embed)
        # Check that the list has enough entries for multiple pages
        ul = await user_list_handler.get_list(user_list_id)
        if len(ul.entries) > 10:
            react_with = ['◀', '▶']
            for reaction in react_with:
                await message.add_reaction(reaction)

# End Commands


async def send_message(channel, **kwargs):
    embed, content = None, None
    if 'embed' in kwargs:
        embed = kwargs['embed']
    if 'content' in kwargs:
        content = kwargs['content']
    return await channel.send(content=content, embed=embed)


user_list_handler = UserListHandler()

# Instantiate request handler to do calls to AniList API
anilist = AniListRequestHandler(user_list_handler)

# Instantiate an embed handler to create embeds
embeds = EmbedHandler(None, user_list_handler)

# Run the bot
bot.run(os.getenv('BOT_TOKEN'))
# Update the avatar_url
