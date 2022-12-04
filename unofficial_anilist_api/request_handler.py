"""
File Name: requests.py
Original Author: Fis-chl
Created On: 04/12/2022
File Description: Contains all objects related to the AniList API.
"""
import aiohttp as requests


class AniListRequestHandler():
    """
    """
    def __init__(self):
        self.base_uri = 'https://graphql.anilist.co'