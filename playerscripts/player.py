import ast

from global_config import SKILL_MAPPING, ABILITY_MAPPING

from playerscripts.races import RaceGeneric, RACE_DICT
from playerscripts.classes import ClassGeneric, CHAR_CLASS_DICT
from playerscripts.background import BackgroundGeneric, BACKGROUND_DICT
from dictionarys.actions import Actions, ACTIONS_ID_DICT
from dictionarys.items import Items, GenericItem, ITEMS_ID_DICT
from dictionarys.buffs import Buffs, BUFFS_ID_DICT


class Player:
    def __init__(self):
        self.race = RaceGeneric()
        self.char_class = ClassGeneric()
        self.background = BackgroundGeneric()

        self.name = 'Bob'

        self.level = 1
        self.max_health = 0
        self.current_health = 0
        self.temporary_health = 0

        self.proficiency_bonus = 0
        self.tool_proficiencies = dict()
        self.armor_proficiencies = dict()
        self.weapon_proficiency = dict()

        self.ability_scores             = {skill: 10 for skill in ABILITY_MAPPING}
        self.ability_scores_none_mod    = {skill: 10 for skill in ABILITY_MAPPING}
        self.ability_scores_mod         = {skill: 0 for skill in ABILITY_MAPPING}

        self.saves                      = {skill: 0 for skill in ABILITY_MAPPING}
        self.saves_none_mod             = {skill: 0 for skill in ABILITY_MAPPING}
        self.saves_proficiency          = {skill: 0 for skill in ABILITY_MAPPING}

        self.skills                     = {skill: 0 for skill in SKILL_MAPPING}
        self.skill_proficiency          = {skill: 0 for skill in SKILL_MAPPING}
        self.skill_proficiency_butt_mod = {skill: 0 for skill in SKILL_MAPPING}
        self.skill_misc_modifier        = {skill: 0 for skill in SKILL_MAPPING}

        self.inventory: list[list[GenericItem]] = [[Items.Empty() for _ in range(5)] for _ in range(8)]  # 8 rows and 5 columns

        self.equipment: dict[str, Items] = {  # This dictionary represents the equipped items
            'helmet': Items.Empty(),
            'cloak': Items.Empty(),
            'chestplate': Items.Empty(),
            'gloves': Items.Empty(),
            'pants': Items.Empty(),
            'boots': Items.Empty(),
            'amulet': Items.Empty(),
            'ring1': Items.Empty(),
            'ring2': Items.Empty(),
            'meleeMainHand': Items.Empty(),
            'meleeOffHand': Items.Empty(),
        }

        self.dragging_item: Items | None = None

        self.grouped_actions: list = [Actions.Empty()] * 10
        self.grouped_buffs: list = []

    @staticmethod
    def matrix_to_id_matrix(matrix: list[list[object] | object]) -> list[list[int] | int]:
        if not matrix:
            return []
        elif isinstance(matrix[0], list):
            id_matrix = [[element.id for element in row] for row in matrix]
        else:
            id_matrix = [element.id for element in matrix]

        return id_matrix

    @staticmethod
    def id_matrix_to_matrix(id_matrix: list[list[int] | int], DICT: dict[object], attributes=None) -> list[list]:
        if not id_matrix:
            return []

        def create_item(item_id, attr=None):
            item_class = DICT.get(int(item_id))
            if item_class is None:
                return None  # or raise an error
            if attr:
                return item_class(**attr)
            return item_class()

        if isinstance(id_matrix[0], list):
            # Handling a 2D matrix
            if attributes and isinstance(attributes[0], list):
                matrix = [
                    [create_item(item_id, attr) for item_id, attr in zip(row, attr_row)]
                    for row, attr_row in zip(id_matrix, attributes)
                ]
            else:
                matrix = [[create_item(item_id) for item_id in row] for row in id_matrix]
        else:
            # Handling a 1D list
            if attributes:
                matrix = [create_item(item_id, attr) for item_id, attr in zip(id_matrix, attributes)]
            else:
                matrix = [create_item(item_id) for item_id in id_matrix]

        return matrix

    @staticmethod
    def dict_to_id_dict(dictionary: dict[str, object]) -> dict[str, int]:
        id_dict = {key: element.id for key, element in dictionary.items()}
        return id_dict

    @staticmethod
    def id_dict_to_dict(id_dictionary: dict[str, int], DICT: dict[object], attributes=None) -> dict[str, object]:
        if attributes is None:
            attributes = {}
        dictionary = {key: DICT[id](**attributes.get(key, {})) for key, id in id_dictionary.items() if id in DICT}
        return dictionary

    @staticmethod
    def get_args_from_matrix(matrix: list[list[object] | object]):
        if not matrix:
            return []
        elif isinstance(matrix[0], list):
            id_matrix = [[element._init_args for element in row] for row in matrix]
        else:
            id_matrix = [element._init_args for element in matrix]

        return id_matrix

    @staticmethod
    def get_args_from_dict(dictionary: dict[str, Items]):
        id_dict = {key: element._init_args for key, element in dictionary.items()}
        return id_dict

    def load(self, content: str) -> None:
        contents: list[str] = content.split('  ')

        easy_attributes: dict[str, int | str] = ast.literal_eval(contents[0])

        self.name = easy_attributes.pop('name')
        for key, val in easy_attributes.items():
            setattr(self, key, val)

        hard_attributes: dict[str, any] = ast.literal_eval(contents[1])

        self.race = RACE_DICT[hard_attributes['race']]
        self.char_class = CHAR_CLASS_DICT[hard_attributes['char_class']]
        self.background = BACKGROUND_DICT[hard_attributes['background']]

        inv = hard_attributes['inventory']
        self.inventory = self.id_matrix_to_matrix(inv['id'], ITEMS_ID_DICT, attributes=inv['attributes'])

        grouped_actions = hard_attributes['grouped_actions']
        self.grouped_actions = self.id_matrix_to_matrix(grouped_actions['id'], ACTIONS_ID_DICT, attributes=grouped_actions['attributes'])

        self.grouped_buffs = self.id_matrix_to_matrix(hard_attributes['grouped_buffs'], BUFFS_ID_DICT)

        equipment = hard_attributes['equipment']
        self.equipment = self.id_dict_to_dict(equipment['id'], ITEMS_ID_DICT, attributes=equipment['attributes'])

        self.update()

    def save(self) -> str:
        inv = {"id": self.matrix_to_id_matrix(self.inventory), "attributes": self.get_args_from_matrix(self.inventory)}
        grouped_actions = {"id": self.matrix_to_id_matrix(self.grouped_actions), "attributes": self.get_args_from_matrix(self.grouped_actions)}
        equipment = {"id": self.dict_to_id_dict(self.equipment), "attributes": self.get_args_from_dict(self.equipment)}

        contents = (
            '{'
            f'"name": "{self.name}", '

            f'"level": {self.level}, '
            f'"max_health": {self.max_health}, '
            f'"current_health": {self.current_health}, '
            f'"temporary_health": {self.temporary_health}, '

            f'"tool_proficiencies": {self.tool_proficiencies}, '
            f'"armor_proficiencies": {self.armor_proficiencies}, '
            f'"weapon_proficiency": {self.weapon_proficiency}, '

            f'"ability_scores": {self.ability_scores}, '
            f'"ability_scores_none_mod": {self.ability_scores_none_mod}, '
            f'"ability_scores_mod": {self.ability_scores_mod}, '

            f'"saves_none_mod": {self.saves_none_mod}, '
            f'"saves_proficiency": {self.saves_proficiency}, '

            f'"skill_proficiency": {self.skill_proficiency}, '
            f'"skill_proficiency_butt_mod": {self.skill_proficiency_butt_mod}, '
            f'"skill_misc_modifier": {self.skill_misc_modifier}'
            '}  '
            '{'
            f'"race": "{self.race.name}", '
            f'"char_class": "{self.char_class.name}", '
            f'"background": "{self.background.name}", '

            f'"inventory": {inv}, '
            f'"equipment": {equipment}, '
            f'"grouped_actions": {grouped_actions}, '
            f'"grouped_buffs": {self.matrix_to_id_matrix(self.grouped_buffs)}'
            '}'
        )

        return contents

    def update_grouped_actions(self) -> None:
        all_actions = []
        for action in self.race.actions.values():
            all_actions.append(action)
        for action in self.char_class.actions.values():
            all_actions.append(action)
        for slot in self.equipment.values():
            if slot:
                for action in slot.actions.values():
                    all_actions.append(action)

        all_actions_id = [action.id for action in all_actions]
        # Remove actions from grouped_actions if they are not in all_actions
        for index, action in enumerate(self.grouped_actions):
            # If the current action is not in all_actions, set the corresponding index to None
            if action.id not in all_actions_id:
                self.grouped_actions[index] = Actions.Empty()

        # Find new actions that are not yet in grouped_actions
        grouped_action_ids = [action.id for action in self.grouped_actions]
        new_actions = [action for action in all_actions if action.id not in grouped_action_ids]

        # Fill in the first None slots in grouped_actions with new actions
        for new_action in new_actions:
            for index, slot in enumerate(self.grouped_actions):
                if slot.id == 0:
                    self.grouped_actions[index] = new_action
                    break  # Stop after placing each new action to avoid duplicates

    def update_grouped_buffs(self) -> None:
        self.grouped_buffs = []
        for val in self.race.buffs.values():
            self.grouped_buffs.append(val)
        for val in self.char_class.buffs.values():
            self.grouped_buffs.append(val)

    def update_proficiencies(self) -> None:
        self.proficiency_bonus = self.char_class.calculate_proficiency_bonus(self.level)
        self.tool_proficiencies = dict(self.char_class.tool_proficiencies)
        self.armor_proficiencies = dict(self.char_class.armor_proficiencies)
        self.weapon_proficiency = dict(self.char_class.weapon_proficiencies)

    def calculate_skills(self) -> None:
        self.skill_proficiency = self.skill_proficiency_butt_mod.copy()

        for skill, skill_proficiency in self.background.skill_proficiencies.items():
            self.skill_proficiency[skill] += skill_proficiency

        for skill, ability in SKILL_MAPPING.items():
            ability_modifier = self.ability_scores_mod[ability]
            prof_bonus = self.proficiency_bonus * self.skill_proficiency[skill]
            misc_modifier = self.skill_misc_modifier[skill]
            self.skills[skill] = ability_modifier + prof_bonus + misc_modifier

    def calculate_save(self) -> None:
        self.saves = self.ability_scores_mod.copy()
        for key, val in self.char_class.saves_proficiency.items():
            self.saves[key] += self.proficiency_bonus * val

        for skill in self.saves.keys():
            prof_bonus = self.proficiency_bonus * self.saves_proficiency[skill]
            self.saves[skill] += prof_bonus

    def calculate_ability_modifier(self) -> None:
        for key in self.ability_scores_mod.keys():
            self.ability_scores_mod[key] = (self.ability_scores[key] - 10) // 2

    def calculate_ability_scores(self) -> None:
        # Assumes the race has a dictionary of bonus_ability_scores
        for ability in self.ability_scores.keys():
            self.ability_scores[ability] = self.ability_scores_none_mod[ability] + self.race.bonus_ability_scores[ability]

    def add_item_to_inventory(self, item, row=None, column=None) -> None:
        if (row and column) is not None:
            print(self.inventory[row][column])
            """Add an item to the inventory at a specific row and column."""
            if 0 <= row < 8 and 0 <= column < 5:  # Ensure the row and column are within bounds
                if self.inventory[row][column].id == 0:  # Check if the slot is empty
                    self.inventory[row][column] = item

        else:
            break_ = False
            for _row in range(8):
                for _col in range(5):
                    if self.inventory[_row][_col].id == 0:
                        self.inventory[_row][_col] = item
                        break_ = True
                        break
                if break_:
                    break

    def remove_item_from_inventory(self, row, column) -> Items | None:
        """Remove an item from the inventory at a specific row and column."""
        if 0 <= row < 8 and 0 <= column < 5:  # Ensure the row and column are within bounds
            item: Items = self.inventory[row][column]
            self.inventory[row][column] = Items.Empty()
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
                self.inventory[end_row][end_col], self.dragging_item
            self.dragging_item = None
        else:
            print("Invalid inventory slot indices!")

    def swap_equip(self, slot_1, slot_2):
        item_1 = self.equipment[slot_1]
        item_2 = self.equipment[slot_2]
        self.equipment[slot_1], self.equipment[slot_2] = item_2, item_1

    def equip_item(self, item, item_pos, slot):
        """Equip an item to a specific slot, and remove it from the inventory."""
        replace = None
        if slot in self.equipment:
            # Unequip the current item in the slot and add it back to the inventory
            if self.equipment[slot] is not None:
                replace = self.equipment[slot]

            # Equip the new item and remove it from the inventory
            self.equipment[slot] = item
            row, col = item_pos
            self.inventory[row][col] = replace

    def unequip_item(self, slot, pos, slot_type):
        """Unequip an item from a specific slot and add it back to the inventory."""
        if not self.equipment[slot].id == 0:
            row, col = pos
            inventory_item = self.inventory[row][col]
            equipment_item = self.equipment[slot]

            if self.inventory[row][col] is None:
                self.inventory[row][col] = equipment_item
                self.equipment[slot] = None

            elif set(inventory_item.types) & set(slot_type) or inventory_item.id == 0:
                self.inventory[row][col], self.equipment[slot] = equipment_item, inventory_item

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
        self.update_proficiencies()
        self.calculate_ability_scores()
        self.calculate_ability_modifier()

        self.calculate_skills()
        self.calculate_save()

        self.update_grouped_buffs()
        self.update_grouped_actions()
