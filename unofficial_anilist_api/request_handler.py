"""
File Name: requests.py
Original Author: Fis-chl
Created On: 04/12/2022
File Description: Contains all objects related to the AniList API.
"""
import aiohttp

from unofficial_anilist_api.query.anime_query import anime_queries
from unofficial_anilist_api.query.manga_query import manga_queries
from unofficial_anilist_api.query.user_query import user_queries
from unofficial_anilist_api.query.medialist_query import medialist_queries


class AniListRequestHandler:
    """
    Class Name: AniListRequestHandler
    Description: Object that handles all calls to the AniList API through AIOHTTP.
    NOTE: create_session() must be called before requests can be made, and close_session() should be called when the
    bot is shutting down.
    """
    def __init__(self, user_list_handler):
        self.base_url = "https://graphql.anilist.co"
        self.session = None
        self.ready = False
        self.user_list_handler = user_list_handler

    async def create_session(self):
        self.session = aiohttp.ClientSession()
        self.ready = True

    async def close_session(self):
        await self.session.close()

    async def post_request(self, query, variables):
        if self.ready:
            async with self.session.post(self.base_url, json={'query': query, 'variables': variables}) as response:
                return await response.json()

    # Anime methods
    async def anime_by_id(self, anime_id=1):
        query = anime_queries['anime_by_id']['query']
        variables = anime_queries['anime_by_id']['variables']
        variables['id'] = anime_id

        json_data = await self.post_request(query=query, variables=variables)
        return json_data['data']['Media']

    async def anime_by_title(self, anime_title="Cowboy Bebop"):
        query = anime_queries['anime_by_title']['query']
        variables = anime_queries['anime_by_title']['variables']
        variables['search'] = anime_title

        json_data = await self.post_request(query=query, variables=variables)
        print(json_data)
        return json_data['data']['Media']

    # Manga methods
    async def manga_by_id(self, manga_id=1):
        query = manga_queries['manga_by_id']['query']
        variables = manga_queries['manga_by_id']['variables']
        variables['id'] = manga_id

        json_data = await self.post_request(query=query, variables=variables)
        return json_data['data']['Media']

    async def manga_by_title(self, manga_title="86 - Eighty Six"):
        query = manga_queries['manga_by_title']['query']
        variables = manga_queries['manga_by_title']['variables']
        variables['search'] = manga_title

        json_data = await self.post_request(query=query, variables=variables)
        return json_data['data']['Media']

    # User methods
    async def user_by_name(self, username=""):
        query = user_queries['user_by_name']['query']
        variables = user_queries['user_by_name']['variables']
        variables['search'] = username

        json_data = await self.post_request(query=query, variables=variables)
        return json_data['data']['User']

    async def medialist_collection_by_name(self, username="", mediatype="ANIME", listname="Completed"):
        query = medialist_queries['medialist_collection_by_name']['query']
        variables = medialist_queries['medialist_collection_by_name']['variables']
        variables['userName'] = username
        variables['type'] = mediatype

        json_data = await self.post_request(query=query, variables=variables)
        for _list in json_data['data']['MediaListCollection']['lists']:
            if _list['name'] == listname:
                return _list['entries']
        return json_data['data']['MediaListCollection']['lists'][0]['entries']
