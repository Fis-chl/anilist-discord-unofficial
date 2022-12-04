"""
File Name: anime_query.py
Original Author: Fis-chl
Creation Date: 04/12/2022
File Description: Contains a dictionary of generic query strings for anime to keep them out of request_handler.
This is a dictionary of dictionaries, because each query has a string and a set of variables
"""

anime_queries = {
    'anime_by_id':
        {
            'query': """
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
                    status
                }
            }
            """,
            'variables':
                {'id': -1}
        },
    'anime_by_title':
        {
            'query': """
            query ($search: String) {
                Media (search: $search, type: ANIME) {
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
                    status
                }
            }
            """,
            'variables':
                {'search': ""}
        }

}
