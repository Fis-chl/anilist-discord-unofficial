"""
File Name: manga_query.py
Original Author: Fis-chl
Creation Date: 04/12/2022
File Description: Contains a dictionary of generic query strings for manga to keep them out of request_handler.
This is a dictionary of dictionaries, because each query has a string and a set of variables
"""

manga_queries = {
    'manga_by_id':
        {
            'query': """
            query ($id: Int) {
                Media (id: $id, type: MANGA) {
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
                    volumes
                    chapters
                    status
                }
            }
            """,
            'variables':
                {'id': -1}
        }
}
