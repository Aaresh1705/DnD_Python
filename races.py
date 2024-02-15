from collections import defaultdict
from buffs import Buffs
from actions import Actions


class RaceGeneric:
    def __init__(self):
        self.age = 0
        self.weight = 0
        self.speed = 25

        self.buffs = defaultdict()
        self.actions = defaultdict()

        self.languages = defaultdict(bool)
        self.languages['Common'] = True

        self.bonus_ability_scores = defaultdict(int)
        self.skill_ability_scores = defaultdict(int)

        self.name = None


class Gnome:
    def __init__(self):

        self.age = 0 
        self.weight = 0
        self.speed = 25

        self.buffs = defaultdict(object)
        self.buffs['darkvision'] = Buffs.Darkvison()
        self.buffs['gnome cunning'] = Buffs.GnomeCunning()

        self.actions = defaultdict()

        self.languages = defaultdict(bool)
        self.languages['Common'] = True
        self.languages['Gnomish'] = True

        self.bonus_ability_scores = defaultdict(int)
        self.bonus_ability_scores['int'] += 2

        self.skill_ability_scores = defaultdict(int)


class ForestGnome(Gnome):
    def __init__(self):
        Gnome.__init__(self)
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


RACES = {'rock gnome': RockGnome(), 'forest gnome': ForestGnome()}
