medialist_queries = {
    'medialist_collection_by_name':
        {
            'query': """
            query ($userName: String, $type: MediaType) {
                MediaListCollection (userName: $userName, type: $type) {
                    lists {
                        entries {
                            media {
                                title {
                                    romaji
                                    english
                                    native
                                }
                                episodes
                            }
                            score
                            status
                            progress
                        }
                        name
                    }
                }
            }
            """,
            'variables':
                {
                    'userName': "",
                    'type': "ANIME"
                }
        },
}
