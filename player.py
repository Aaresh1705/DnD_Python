from collections import defaultdict 


class Player:
    def __init__(self):
        self.name = ""
        self.race = None
        self.char_class = None
        self.background = None

        self.max_health = 0
        self.level = 1

        self.abilityscores = {"str": 0, "dex": 0, "int": 0, 'wis': 0, 'cha': 0, 'con': 0}
    
    def unlocks(self):
        pass

    def save(self):
        pass  # TODO: Make character save code
