from collections import defaultdict
from dictionarys.Spells import *
from dictionarys.buffs import Buffs
from dictionarys.actions import Actions


class ClassGeneric:
    def __init__(self):
        self.spell_slots = defaultdict(int)
        self.name = None
        self.spell_list = GenericSpellList()

        self.buffs = defaultdict(object)
        self.actions = dict()

        self.proficiencies = {}

        self.max_prepared_leveled_spells = 0
        self.max_prepared_cantrips = 0

        self.tool_proficiencies = defaultdict(int)
        self.armor_proficiencies = defaultdict(int)
        self.weapon_proficiencies = defaultdict(int)
        self.saves_proficiency = defaultdict(int)

        self.prepared_spells = []
        self.prepared_spells_names = []
        self.prepared_cantrips = []
        self.prepared_cantrips_names = []

        self.class_spells = []

        self.total_prepared = [] + [None]*10

    def update(self, *args):
        pass

    @staticmethod
    def calculate_proficiency_bonus(level):
        return 0

    def reload_spells(self):
        # First, reload the spell objects in the spell list
        self.spell_list.reload_spell_objects()

        # Then, update the prepared spells and cantrips
        self.update_prepared_spells()
        self.update_prepared_cantrips()

        self.update_total_prepared()

    def update_prepared_spells(self):
        # Re-map prepared spells to the new objects based on name
        updated_spells = []
        for spell in self.prepared_spells:
            for level, spells in self.spell_list.spells.items():
                for new_spell in spells:
                    if new_spell.name == spell.name:
                        updated_spells.append(new_spell)
                        break
        self.prepared_spells = updated_spells

    def update_prepared_cantrips(self):
        # Re-map prepared cantrips to the new objects based on name
        updated_cantrips = []
        for cantrip in self.prepared_cantrips:
            for new_cantrip in self.spell_list.spells['0']:  # Assuming '0' is the key for cantrips
                if new_cantrip.name == cantrip.name:
                    updated_cantrips.append(new_cantrip)
                    break
        self.prepared_cantrips = updated_cantrips

    def update_total_prepared(self):
        # Clear the current total_prepared list
        updated_spells_total = {spell.name: spell for level in self.spell_list.spells.values() for spell in level}

        # Go through the existing total_prepared list and update each entry with the new spell object
        for i, old_spell in enumerate(self.total_prepared):
            if old_spell is not None and old_spell.name in updated_spells_total:
                # Replace with the new spell object while maintaining the position
                self.total_prepared[i] = updated_spells_total[old_spell.name]
            else:
                # If the old spell is no longer available, mark the slot as None
                self.total_prepared[i] = None

    def update_prepared(self, spell, list_: list):
        if spell not in list_:
            list_.append(spell)
            self.change_total_prepared(spell)
        else:
            list_.remove(spell)
            self.change_total_prepared(spell)

    def change_total_prepared(self, spell):
        if spell in self.total_prepared:
            empty_index = self.total_prepared.index(spell)
            self.total_prepared[empty_index] = None
            self.compress_prepared()

        else:
            try:
                empty_index = self.total_prepared.index(None)
                self.total_prepared[empty_index] = spell
            except ValueError:
                self.expand_prepared()
                empty_index = self.total_prepared.index(None)
                self.total_prepared[empty_index] = spell

    def compress_prepared(self):
        if self.total_prepared[-10:].count(None) == 10 and len(self.total_prepared) > 10:
            self.total_prepared = self.total_prepared[:-10]

    def expand_prepared(self):
        additional_slots = [None] * 10  # Create additional slots for the new row
        self.total_prepared.extend(additional_slots)

    def change_prepared_spells_and_cantrips(self, cantrips: list[str], leveled: list[str]):
        self.prepared_cantrips_names = cantrips
        self.prepared_cantrips = self.spell_list.spell_class_from_name(cantrips)
        self.prepared_spells_names = leveled
        self.prepared_spells = self.spell_list.spell_class_from_name(leveled)


class Artificer(ClassGeneric):
    def __init__(self):
        super().__init__()
        self.infusions = 0
        self.max_infusions = 0

        new_tools = {
            "thieves' tools": 1,
            "tinker's tools": 1,
            "artisan's tools": 1
        }
        self.tool_proficiencies.update(new_tools)

        new_armor = {
            "thieves' tools": 1,
            "tinker's tools": 1,
            "artisan's tools": 1
        }
        self.armor_proficiencies.update(new_armor)

        new_weapons = {
            'simple': 1,
            'firearm': 1,
            'Shields': 1
        }
        self.weapon_proficiencies.update(new_weapons)

        new_saves = {
            'con': 1,
            'int': 1
        }
        self.saves_proficiency.update(new_saves)

        self.spell_list = ArtificerSpellList()

        self.actions['magical tinkering'] = Actions.MagicalTinkering()

    def update_buffs(self, level):
        if level >= 6:
            self.buffs['tool expertise'] = Buffs.ToolExpertise()
        elif self.buffs['tool expertise']:
            del self.buffs['tool expertise']

    def update_actions(self, level):
        if level >= 2:
            if 'infuse item' not in self.actions:
                self.actions['infuse item'] = Actions.InfuseItem()
        elif 'infuse item' in self.actions:
            del self.actions['infuse item']

        if level >= 3:
            if 'the right tool for the job' not in self.actions:
                self.actions['the right tool for the job'] = Actions.TheRightToolForTheJob()
        elif 'the right tool for the job' in self.actions:
            del self.actions['the right tool for the job']

        if level >= 7:
            if 'flash of genius' not in self.actions:
                self.actions['flash of genius'] = Actions.FlashOfGenius()
        elif 'flash of genius' in self.actions:
            del self.actions['flash of genius']


    def update(self, player):
        self.update_buffs(player.level)
        self.update_actions(player.level)
        self.spell_slot_update(player.level)
        self.prepared_spells_update(player.ability_scores_mod['int'], player.level)
        self.prepared_cantrip_update(player.level)

    def spell_slot_update(self, level):
        self.spell_slots.clear()
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

        if level >= 11:
            self.spell_slots['3'] = 3

        if level >= 13:
            self.spell_slots['4'] = 1

        if level >= 15:
            self.spell_slots['4'] = 2

        if level >= 17:
            self.spell_slots['4'] = 3
            self.spell_slots['5'] = 1

        if level >= 19:
            self.spell_slots['5'] = 2

    def prepared_cantrip_update(self, level):
        if level >= 14:
            self.max_prepared_cantrips = 4
        elif level >= 10:
            self.max_prepared_cantrips = 3
        else:
            self.max_prepared_cantrips = 2

    def prepared_spells_update(self, int_mod, level):
        self.max_prepared_leveled_spells = max(int_mod + level // 2, 1)

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
        self.name = 'Alchemist Artificer'


class Armorer(Artificer):
    def __init__(self):
        Artificer.__init__(self)
        self.name = 'Armorer Artificer'


class Artillerist(Artificer):  # TODO: Make Artillerist Spells
    def __init__(self):
        Artificer.__init__(self)
        self.name = 'Artillerist Artificer'
        self.actions['eldritch cannon'] = Actions.EldritchCannon()
        self.tool_proficiencies["woodcarver's tools"] += 1

    def update(self, level):
        Artificer.update(self, level)

    def update_actions(self, level):
        super().update_actions(level)

    def update_buffs(self, level):
        super().update_buffs(level)
        if level >= 5:
            self.buffs['arcane firearm'] = Buffs.ArcaneFirearm()
        elif self.buffs['arcane firearm']:
            del self.buffs['arcane firearm']

    def update_class_spells(self, level):
        pass#if level >=


class BattleSmith(Artificer):
    def __init__(self):
        Artificer.__init__(self)
        self.name = 'Battle Smith Artificer'


CHAR_CLASS_DICT = {'Alchemist Artificer': Alchemist(), 'Armorer Artificer': Armorer(), 'Artillerist Artificer': Artillerist(),
           'Battle Smith Artificer': BattleSmith(), 'None': ClassGeneric()}
