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


# Load .env file
load_dotenv()

# Create a bot
intents = discord.Intents.default()
intents.messages = True
bot = dbot.Bot(command_prefix="-", intents=intents)


# Functions that are not tagged with @bot
async def anime_embed(data):
    emb = discord.embeds.Embed(
        title=data['title']['romaji'],
        description=f"**AKA:** {data['title']['english']}, {data['title']['native']}",
        colour=0xFFAA55
    )
    if data['averageScore'] is None:
        data['averageScore'] = "NA"
    emb.add_field(
        name="Scores and Popularity",
        value=f"On {data['popularity']} user's lists\nAverage Score of {data['averageScore']}/100",
        inline=False
    )
    if data['status'] == "RELEASING":
        release_value = f"Started airing in **{data['startDate']['month']}/{data['startDate']['year']}** and is ongoing.\n"
    elif data['status'] == "NOT_YET_RELEASED":
        release_value = f"Estimated to start airing in **{data['startDate']['month']}/{data['startDate']['year']}** ({data['season']} {data['startDate']['year']}).\n"
    else:
        release_value = f"Aired from **{data['startDate']['month']}/{data['startDate']['year']}** to **{data['endDate']['month']}/{data['endDate']['year']}** ({data['season']} {data['startDate']['year']}).\n"
    if not data['episodes'] is None and not data['duration'] is None:
        release_value += f"**{data['episodes']}** episodes, average of **{data['duration']}m** per episode."
    else:
        if not data['episodes'] is None and data['duration'] is None:
            release_value += f"**{data['episodes']}** episodes."
        elif not data['duration'] is None and data['episodes'] is None:
            release_value += f"Average of **{data['duration']}m** per episode."
    emb.add_field(
        name="Release and Runtime",
        value=f"{release_value}",
        inline=False
    )
    emb.set_image(url=data['coverImage']['large'])
    emb.set_footer(text="AniList Unofficial", icon_url=bot.user.avatar_url)
    return emb


async def manga_embed(data):
    emb = discord.embeds.Embed(
        title=data['title']['romaji'],
        description=f"**AKA:** {data['title']['english']}, {data['title']['native']}",
        colour=0xFFAA55
    )
    emb.add_field(
        name="Scores and Popularity",
        value=f"On {data['popularity']} user's lists\nAverage Score of {data['averageScore']}/100",
        inline=False
    )
    if data['status'] == "RELEASING":
        release_value = f"Started releasing in **{data['startDate']['month']}/{data['startDate']['year']}** and is ongoing.\n"
    elif data['status'] == "NOT_YET_RELEASED":
        release_value = f"Estimated to start in **{data['startDate']['month']}/{data['startDate']['year']}**.\n"
    else:
        release_value = f"Released from **{data['startDate']['month']}/{data['startDate']['year']}** to **{data['endDate']['month']}/{data['endDate']['year']}**.\n"
    if not data['volumes'] is None and not data['chapters'] is None:
        release_value += f"**{data['volumes']}** volumes, **{data['chapters']}** chapters."
    else:
        if not data['volumes'] is None and data['chapters'] is None:
            release_value += f"**{data['volumes']}** volumes."
        elif not data['chapters'] is None and data['volumes'] is None:
            release_value += f"**{data['chapters']}** chapters"
    emb.add_field(
        name="Release and Runtime",
        value=f"{release_value}",
        inline=False
    )
    emb.set_image(url=data['coverImage']['large'])
    emb.set_footer(text="AniList Unofficial", icon_url=bot.user.avatar_url)
    return emb


# Functions tagged with @bot
@bot.event
async def on_ready():
    await anilist.create_session()  # Initialise an aiohttp session for the AniList request handler
    print(f'Logged in as {bot.user}')


@bot.command()
async def get_anime(ctx, arg):
    data = await anilist.anime_by_id(anime_id=arg)
    embed = await anime_embed(data)
    await send_message(ctx.channel, embed=embed)


@bot.command()
async def get_manga(ctx, arg):
    data = await anilist.manga_by_id(manga_id=arg)
    embed = await manga_embed(data)
    await send_message(ctx.channel, embed=embed)


async def send_message(channel, **kwargs):
    embed, content = None, None
    if 'embed' in kwargs:
        embed = kwargs['embed']
    if 'content' in kwargs:
        content = kwargs['content']
    await channel.send(content=content, embed=embed)


# Instantiate request handler to do calls to AniList API
anilist = AniListRequestHandler()


# Run the bot
bot.run(os.getenv('BOT_TOKEN'))
