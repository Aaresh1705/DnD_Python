from collections import defaultdict 


class RaceGeneric:
    def __init__(self):
        self.age = 0
        self.weight = 0
        self.speed = 25

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
        self.darkvision = True
        self.gnome_cunning = True

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

        self.artificers_lore = True
        self.tinker = True


RACES = {'rock gnome': RockGnome(), 'forest gnome': ForestGnome()}
