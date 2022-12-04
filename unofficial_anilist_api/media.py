class Media:
    def __init__(self, data):
        self.data = data


class Anime(Media):
    def __init__(self, data):
        super().__init__(data)


class Manga(Media):
    def __init__(self, data):
        super().__init__(data)
