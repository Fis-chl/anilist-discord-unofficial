user_queries = {
    'user_by_name':
        {
            'query': """
            query ($search: String) {
                User (search: $search) {
                    id
                    name
                    about
                    avatar {
                        medium
                        large
                    }
                    bannerImage
                    statistics {
                        anime {
                            count
                            meanScore
                            minutesWatched
                            episodesWatched
                        }
                        manga {
                            count
                            meanScore
                            chaptersRead
                            volumesRead
                        }
                    }
                    favourites {
                        anime {
                            nodes {
                                id
                            }
                        }
                        manga {
                            nodes {
                                id
                            }
                        }
                        characters {
                            nodes {
                                id
                            }
                        }
                    }
                }
            }
            """,
            'variables':
                {'search': ""}
        },
    'user_by_name_profile_picture':
        {
            'query': """
        query ($search: String) {
            User (search: $search) {
                avatar {
                    medium
                    large
                }
            }
        }
        """,
            'variables':
                {'search': ""}
        },
}
