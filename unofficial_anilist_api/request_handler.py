"""
File Name: requests.py
Original Author: Fis-chl
Created On: 04/12/2022
File Description: Contains all objects related to the AniList API.
"""
import aiohttp


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

    async def anime_by_id_query(self, anime_id):
        query = """
        query ($id: Int) {
            Media (id: $id, type: ANIME) {
                id
                title {
                    romaji
                    english
                    native
                }
                coverImage {
                    large
                }
                averageScore
                popularity
                startDate {
                    year
                    month
                }
                endDate {
                    year
                    month
                }
                season
                seasonYear
                episodes
                duration
            }
        }
        """

        variables = {
            'id': anime_id
        }

        json_data = await self.post_request(query=query, variables=variables)
        return json_data['data']['Media']
