from collections import defaultdict


class Artificer:
    def __init__(self):

        self.level = 1
        self.infusions = 0
        self.max_infusions = 0
        
        self.spell_slots = defaultdict(lambda: 0)
        self.spell_slots['cantrip'] = 2
        
    
class Alchemist(Artificer):
    def __init__(self):
        Artificer.__init__(self)


class Armorer(Artificer):
    def __init__(self):
        Artificer.__init__(self)


class Artillerist(Artificer):
    def __init__(self):
        Artificer.__init__(self)
    
    def unlocks(self):
        if self.level >= 3:
            print(3)


class BattleSmith(Artificer):
    def __init__(self):
        Artificer.__init__(self)


CLASSES = {'alchemist artificer': Alchemist(), 'armorer artificer': Armorer(), 'artillerist artificer': Artillerist(),
           'battle smith artificer': BattleSmith()}
