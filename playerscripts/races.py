from dictionarys.buffs import Buffs
from dictionarys.actions import Actions
from global_config import ABILITY_MAPPING, SKILL_MAPPING


class RaceGeneric:
    def __init__(self):
        self.age = 0
        self.weight = 0
        self.speed = 30

        self.buffs = dict()
        self.actions = dict()

        self.languages = dict()
        self.languages['Common'] = True

        self.bonus_ability_scores = {skill: 0 for skill in ABILITY_MAPPING}
        self.skill_ability_scores = {skill: 0 for skill in SKILL_MAPPING}

        self.name = None

        self.proficiencies = {}


class Gnome(RaceGeneric):
    def __init__(self):
        super().__init__()

        self.speed = 25

        self.buffs['darkvision'] = Buffs.Darkvison()
        self.buffs['gnome cunning'] = Buffs.GnomeCunning()

        self.languages['Gnomish'] = True

        self.bonus_ability_scores['int'] += 2


class ForestGnome(Gnome):
    def __init__(self):
        Gnome.__init__(self)
        self.name = 'Forest Gnome'
        
        self.bonus_ability_scores['dex'] += 1

        self.speak_with_small_beasts = True
        self.natural_illusionist = True


class RockGnome(Gnome):
    def __init__(self):
        Gnome.__init__(self)
        self.name = 'Rock Gnome'

        self.bonus_ability_scores['con'] += 1

        self.buffs['artificers lore'] = Buffs.ArtificersLore()

        self.actions['tinker'] = Actions.Tinker()

        self.proficiencies["tinker's tools"] = True


RACE_DICT = {'Rock Gnome': RockGnome(), 'Forest Gnome': ForestGnome(), 'None': RaceGeneric()}
