from collections import defaultdict
from Spells import *
from buffs import Buffs
from actions import Actions


class ClassGeneric:
    def __init__(self):
        self.spell_slots = defaultdict(int)
        self.name = None
        self.spell_list = GenericSpellList()

        self.buffs = defaultdict(object)
        self.actions = defaultdict(object)

        self.max_prepared_leveled_spells = 0
        self.max_prepared_cantrips = 0

        self.prepared_spells = []
        self.prepared_cantrips = []

        self.total_prepared = [] + [None]*10

    def update(self, *args):
        pass

    @staticmethod
    def calculate_proficiency_bonus(level):
        pass

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


class Artificer(ClassGeneric):
    def __init__(self):
        super().__init__()
        self.infusions = 0
        self.max_infusions = 0

        self.spell_list = ArtificerSpellList()

    def update_buffs(self, level):
        if level >= 6:
            self.buffs['tool expertise'] = Buffs.ToolExpertise()
        elif self.buffs['tool expertise']:
            del self.buffs['tool expertise']

    def update_actions(self, level):
        self.actions['magical tinkering'] = Actions.MagicalTinkering()

        if level >= 2:
            self.actions['infuse item'] = Actions.InfuseItem()
        elif self.actions['infuse item']:
            del self.actions['infuse item']

        if level >= 3:
            self.actions['the right tool for the job'] = Actions.TheRightToolForTheJob()
        elif self.actions['the right tool for the job']:
            del self.actions['the right tool for the job']

    def update(self, player):
        self.update_buffs(player.level)
        self.update_actions(player.level)
        self.spell_slot_update(player.level)
        self.prepared_spells_update(player.calculate_ability_modifier('int'), player.level)
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

    def calculate_proficiency_bonus(self, level):
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


class Artillerist(Artificer):  # TODO: Make Artillerist Spells
    def __init__(self):
        Artificer.__init__(self)
        self.name = 'Artillerist Artificer'
        self.actions['eldritch cannon'] = Actions.EldritchCannon()

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


class BattleSmith(Artificer):
    def __init__(self):
        Artificer.__init__(self)


CLASSES = {'alchemist artificer': Alchemist(), 'armorer artificer': Armorer(), 'artillerist artificer': Artillerist(),
           'battle smith artificer': BattleSmith()}
