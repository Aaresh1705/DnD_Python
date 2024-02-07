from collections import defaultdict 


class BackgroundGeneric:
    def __init__(self):
        self.name = None

class GuildArtisan:
    def __init__(self):
        self.name = 'Guild Artisan'


BACKGROUNDS = {'guild artisan': GuildArtisan()}
