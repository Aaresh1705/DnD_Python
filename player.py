from collections import defaultdict 
from races import RaceGeneric
from classes import ClassGeneric
from background import BackgroundGeneric


class Player:
    def __init__(self):
        self.name = ""
        self.race = RaceGeneric()
        self.char_class = ClassGeneric()
        self.background = BackgroundGeneric()

        self.max_health = 10
        self.current_health = 7
        self.level = 1

        self.abilityscores = {"str": 0, "dex": 0, "int": 0, 'wis': 0, 'cha': 0, 'con': 0}
    
    def unlocks(self):
        pass

    def save(self):
        pass  # TODO: Make character save code

    def update_class(self):
        self.char_class.update(self.level)
