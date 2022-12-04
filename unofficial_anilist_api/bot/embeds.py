"""
File Name: embeds.py
Original Author: Fis-chl
Creation Date: 04/12/2022
File Description: Contains EmbedHandler which is instantiated to handle all embeds. This keeps it out of the main
bot script.
"""

import discord


class EmbedHandler:
    def __init__(self, avatar_url):
        self.avatar_url = avatar_url

    async def anime_embed(self, data):
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
        emb.set_footer(text="AniList Unofficial", icon_url=self.avatar_url)
        return emb

    async def manga_embed(self, data):
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
        emb.set_footer(text="AniList Unofficial", icon_url=self.avatar_url)
        return emb
