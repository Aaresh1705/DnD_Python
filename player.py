from collections import defaultdict 
from races import RaceGeneric
from classes import ClassGeneric
from background import BackgroundGeneric
import pickle
from items import Items

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
        self.temporary_health = 0
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

        self.inventory = [[None for _ in range(5)] for _ in range(8)]  # 8 rows and 5 columns
        self.add_item_to_inventory(Items.Quarterstaff(1), 1, 1)
        self.add_item_to_inventory(Items.Quarterstaff(), 0, 1)

        self.equipment = {  # This dictionary represents the equipped items
            'helmet': None,
            'cloak': None,
            'chestplate': None,
            'gloves': None,
            'pants': None,
            'boots': None,
            'amulet': None,
            'ring1': None,
            'ring2': None,
            'meleeMainHand': None,
            'meleeOffHand': None,
        }

        self.grouped_actions = [] + [None]*10
        self.all_actions = []
        self.grouped_buffs = []

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
            player = pickle.load(f)
            player.reload_inventory_items()
            player.char_class.reload_spells()
            return player

    def save(self, filename):
        with open(filename, 'wb') as f:  # Overwrites any existing file.
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        print("Saved player class")

    def update_grouped_actions(self):
        self.all_actions = []
        for val in self.race.actions.values():
            self.all_actions.append(val)
        for val in self.char_class.actions.values():
            self.all_actions.append(val)

        # Remove actions from grouped_actions if they are not in all_actions
        for index, action in enumerate(self.grouped_actions):
            # If the current action is not in all_actions, set the corresponding index to None
            if action not in self.all_actions:
                self.grouped_actions[index] = None

        # Find new actions that are not yet in grouped_actions
        new_actions = [action for action in self.all_actions if action not in self.grouped_actions]

        # Fill in the first None slots in grouped_actions with new actions
        for new_action in new_actions:
            for index, slot in enumerate(self.grouped_actions):
                if slot is None:
                    self.grouped_actions[index] = new_action
                    break  # Stop after placing each new action to avoid duplicates


    def update_grouped_buffs(self):
        self.grouped_buffs = defaultdict(object)
        for key, val in self.race.buffs.items():
            self.grouped_buffs[key] = val
        for key, val in self.char_class.buffs.items():
            self.grouped_buffs[key] = val

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

    def add_item_to_inventory(self, item, row, column):
        """Add an item to the inventory at a specific row and column."""
        if 0 <= row < 8 and 0 <= column < 5:  # Ensure the row and column are within bounds
            if self.inventory[row][column] is None:  # Check if the slot is empty
                self.inventory[row][column] = item
            else:
                print("The slot is already occupied!")
        else:
            print("Invalid inventory slot!")

    def remove_item_from_inventory(self, row, column):
        """Remove an item from the inventory at a specific row and column."""
        if 0 <= row < 8 and 0 <= column < 5:  # Ensure the row and column are within bounds
            item = self.inventory[row][column]
            self.inventory[row][column] = None
            return item
        else:
            print("Invalid inventory slot!")
            return None

    def swap_items(self, start_row, start_col, end_row, end_col):
        """Swap items between two inventory slots."""
        # Ensure all indices are within bounds
        if all(0 <= idx < 8 for idx in [start_row, end_row]) and all(0 <= idx < 5 for idx in [start_col, end_col]):
            # Swap the items in the grid
            self.inventory[start_row][start_col], self.inventory[end_row][end_col] = \
                self.inventory[end_row][end_col], self.inventory[start_row][start_col]
        else:
            print("Invalid inventory slot indices!")

    def equip_item(self, item, slot):
        """Equip an item to a specific slot, and remove it from the inventory."""
        replace = None
        if slot in self.equipment:
            # Unequip the current item in the slot and add it back to the inventory
            if self.equipment[slot] is not None:
                replace = self.equipment[slot]

            # Equip the new item and remove it from the inventory
            self.equipment[slot] = item
            for row in self.inventory:
                if item in row:
                    index = row.index(item)
                    row[index] = replace
                    break

    def unequip_item(self, slot):
        """Unequip an item from a specific slot and add it back to the inventory."""
        if self.equipment[slot] is not None:
            for row in range(8):
                for col in range(5):
                    if self.inventory[row][col] is None:
                        self.inventory[row][col] = self.equipment[slot]
                        self.equipment[slot] = None
                        break

    def reload_inventory_items(self):
        for row_index, row in enumerate(self.inventory):
            for col_index, item in enumerate(row):
                if item:  # Check if there is an item to update
                    # Re-instantiate the item based on its class name
                    # For this to work, class names must match the item identifiers
                    class_name = item.__class__.__name__
                    if hasattr(Items, class_name):
                        # Get the new class from the Items module
                        new_class = getattr(Items, class_name)
                        # Prepare the keyword arguments for the new instance
                        # Only include attributes that match the __init__ parameters
                        init_params = new_class.__init__.__code__.co_varnames
                        item_attributes = {k: v for k, v in item.__dict__.items() if k in init_params}
                        # Create a new instance of the item with the filtered attributes
                        new_item = new_class(**item_attributes)
                        # Replace the old item instance with the new one
                        self.inventory[row_index][col_index] = new_item

    def update(self):
        self.char_class.update(self)
        self.apply_racial_bonuses()
        self.calculate_skills()

        self.update_grouped_buffs()
        self.update_grouped_actions()
