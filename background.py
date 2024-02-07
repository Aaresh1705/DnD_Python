from collections import defaultdict 


class GuildArtisan:
    def __init__(self):

        self.level = 1
        self.infusions = 0
        self.max_infusions = 0
        
        self.spell_slots = defaultdict(lambda: 0)
        self.spell_slots['can'] = 2


BACKGROUNDS = {'guild artisan': GuildArtisan()}
