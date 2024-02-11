from collections import defaultdict
from Spells import ArtificerSpellList

class ClassGeneric:
    def __init__(self):
        self.spell_slots = defaultdict(int)

        self.name = None

    def update(self, *args):
        pass

    @staticmethod
    def calculate_proficiency_bonus(level):
        pass


class Artificer:
    def __init__(self):
        self.infusions = 0
        self.max_infusions = 0
        
        self.spell_slots = defaultdict(int)

        self.artificer_spell_list = ArtificerSpellList()
        self.artificer_spell_list.load()

    def update(self, level):
        self.spell_slot_update(level)

    def spell_slot_update(self, level):
        self.spell_slots['0'] = 2
        self.spell_slots['1'] = 2

        if level >= 3:
            self.spell_slots['1'] = 3

        if level >= 5:
            self.spell_slots['1'] = 4
            self.spell_slots['2'] = 2

        if level >= 7:
            self.spell_slots['2'] = 3

        if level >= 9:
            self.spell_slots['3'] = 2

        if level >= 10:
            self.spell_slots['0'] = 3

        if level >= 11:
            self.spell_slots['3'] = 3

        if level >= 13:
            self.spell_slots['4'] = 1

        if level >= 14:
            self.spell_slots['0'] = 4

        if level >= 15:
            self.spell_slots['4'] = 2

        if level >= 17:
            self.spell_slots['4'] = 3
            self.spell_slots['5'] = 1

        if level >= 19:
            self.spell_slots['5'] = 2

    @staticmethod
    def calculate_proficiency_bonus(level):
        if level <= 4:
            return 2
        elif level <= 8:
            return 3
        elif level <= 12:
            return 4
        elif level <= 16:
            return 5
        else:
            return 6

    def known_spells(self):
        pass


class Alchemist(Artificer):
    def __init__(self):
        Artificer.__init__(self)


class Armorer(Artificer):
    def __init__(self):
        Artificer.__init__(self)


class Artillerist(Artificer):
    def __init__(self):
        Artificer.__init__(self)
        self.name = 'Artillerist Artificer'

    def update(self, level):
        Artificer.update(self, level)


class BattleSmith(Artificer):
    def __init__(self):
        Artificer.__init__(self)


CLASSES = {'alchemist artificer': Alchemist(), 'armorer artificer': Armorer(), 'artillerist artificer': Artillerist(),
           'battle smith artificer': BattleSmith()}
