from collections import defaultdict 
from races import RaceGeneric
from classes import ClassGeneric
from background import BackgroundGeneric
import pickle
from items import Items, InventoryItem

skill_mapping = {
    'Acrobatics': 'dex',
    'Animal Handling': 'wis',
    'Arcana': 'int',
    'Athletics': 'str',
    'Deception': 'cha',
    'History': 'int',
    'Insight': 'wis',
    'Intimidation': 'cha',
    'Investigation': 'int',
    'Medicine': 'wis',
    'Nature': 'int',
    'Perception': 'wis',
    'Performance': 'cha',
    'Persuasion': 'cha',
    'Religion': 'int',
    'Sleight of Hand': 'dex',
    'Stealth': 'dex',
    'Survival': 'wis'
}


class Player:
    def __init__(self):
        self.name = ""
        self.race = RaceGeneric()
        self.char_class = ClassGeneric()
        self.background = BackgroundGeneric()

        self.max_health = 0
        self.current_health = 0
        self.level = 1

        self.abilityscores_nonmod = {"str": 10, "dex": 10, "int": 10, 'wis': 10, 'cha': 10, 'con': 10}
        self.abilityscores = {"str": 10, "dex": 10, "int": 10, 'wis': 10, 'cha': 10, 'con': 10}

        self.bonus_ability_scores = defaultdict(int)

        self.skills = {skill: 0 for skill in skill_mapping}
        self.skills_nomod = {skill: 0 for skill in skill_mapping}
        self.skill_proficiency = {skill: 0 for skill in skill_mapping}
        self.skill_misc_modifier = {skill: 0 for skill in skill_mapping}

        self.weapon_proficiency = defaultdict(bool)
        self.weapon_proficiency['simple'] = False

        self.items = []
        self.items.append(Items.Quarterstaff())
        """for item in self.items:
            if 'simple' in item.type:
                print(2)"""

    def calculate_skills(self):
        proficiency_bonus = self.calculate_proficiency_bonus()

        for skill, ability in skill_mapping.items():
            ability_modifier = self.calculate_ability_modifier(ability)
            prof_bonus = proficiency_bonus * self.skill_proficiency[skill]
            misc_modifier = self.skill_misc_modifier[skill]
            self.skills[skill] = ability_modifier + prof_bonus + misc_modifier
            self.skills_nomod[skill] = ability_modifier + prof_bonus + misc_modifier

    def unlocks(self):
        pass

    def load(self, filename):
        with open(filename, 'rb') as f:
            print("Loaded player class")
            return pickle.load(f)


    def save(self, filename):
        with open(filename, 'wb') as f:  # Overwrites any existing file.
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        print("Saved player class")

    def calculate_ability_modifier(self, ability):
        ability_score = self.abilityscores.get(ability, 0)
        return (ability_score - 10) // 2

    def calculate_proficiency_bonus(self):
        if self.level <= 4:
            return 2
        elif self.level <= 8:
            return 3
        elif self.level <= 12:
            return 4
        elif self.level <= 16:
            return 5
        else:
            return 6

    def apply_racial_bonuses(self):
        # Assumes the race has a dictionary of bonus_ability_scores
        for ability, bonus in self.race.bonus_ability_scores.items():
            self.abilityscores[ability] = self.abilityscores_nonmod[ability] + bonus

    def update_inventory(self, inventory):
        # Clear current inventory items
        inventory.display_items.clear()
        inventory.items.clear()

        # Add each item from the player's items list to the inventory
        for item in self.items:
            inventory_item = InventoryItem(
                item=item,
                quantity=1
            )
            inventory.add_item(inventory_item)


    def update(self):
        self.char_class.update(self.level)
        self.apply_racial_bonuses()
        self.calculate_skills()
