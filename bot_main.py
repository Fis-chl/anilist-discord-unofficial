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
async def media_embed(data):
    emb = discord.embeds.Embed(
        title=data['title']['romaji'],
        description=f"**AKA:** {data['title']['english']}, {data['title']['native']}",
        colour=0xFFAA55
    )
    emb.add_field(
        name="Scores and Popularity",
        value=f"Popularity: {data['popularity']}\nAverage Score: {data['averageScore']}/100",
        inline=False
    )
    emb.add_field(
        name="Release and Runtime",
        value=f"Aired from **{data['startDate']['month']}/{data['startDate']['year']}** to **{data['endDate']['month']}/{data['endDate']['year']}** ({data['season']} {data['startDate']['year']}).\n"
              f"**{data['episodes']}** episodes, average of **{data['duration']}m** per episode.",
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
    data = await anilist.anime_by_id_query(arg)
    embed = await media_embed(data)
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
