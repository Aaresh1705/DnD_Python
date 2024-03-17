from global_config import SKILL_MAPPING


class BackgroundGeneric:
    def __init__(self):
        self.name = None
        self.skill_proficiencies = {skill: 0 for skill in SKILL_MAPPING}


class GuildArtisan(BackgroundGeneric):
    def __init__(self):
        super().__init__()
        self.name = 'Guild Artisan'

        new_proficiencies = {
            'Insight': 1,
            'Persuasion': 1,
        }
        self.skill_proficiencies.update(new_proficiencies)


BACKGROUND_DICT = {'Guild Artisan': GuildArtisan(), 'None': BackgroundGeneric()}
