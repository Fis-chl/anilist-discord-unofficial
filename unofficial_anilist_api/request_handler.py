"""
File Name: requests.py
Original Author: Fis-chl
Created On: 04/12/2022
File Description: Contains all objects related to the AniList API.
"""
import aiohttp

from unofficial_anilist_api.query.anime_query import anime_queries
from unofficial_anilist_api.query.manga_query import manga_queries


class AniListRequestHandler:
    """
    Class Name: AniListRequestHandler
    Description: Object that handles all calls to the AniList API through AIOHTTP.
    NOTE: create_session() must be called before requests can be made, and close_session() should be called when the
    bot is shutting down.
    """
    def __init__(self):
        self.base_url = "https://graphql.anilist.co"
        self.session = None
        self.ready = False

    async def create_session(self):
        self.session = aiohttp.ClientSession()
        self.ready = True

    async def close_session(self):
        await self.session.close()

    async def post_request(self, query, variables):
        if self.ready:
            async with self.session.post(self.base_url, json={'query': query, 'variables': variables}) as response:
                return await response.json()

    async def anime_by_id(self, anime_id=1):
        query = anime_queries['anime_by_id']['query']
        variables = anime_queries['anime_by_id']['variables']
        variables['id'] = anime_id

        json_data = await self.post_request(query=query, variables=variables)
        return json_data['data']['Media']

    async def manga_by_id(self, manga_id=1):
        query = manga_queries['manga_by_id']['query']
        variables = manga_queries['manga_by_id']['variables']
        variables['id'] = manga_id

        json_data = await self.post_request(query=query, variables=variables)
        return json_data['data']['Media']
