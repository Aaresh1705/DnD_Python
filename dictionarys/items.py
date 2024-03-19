from dictionarys.actions import Actions


def calculate_rarity(magic):
    if magic == 0:
        return 'Common'
    if magic == 1:
        return 'Uncommon'
    if magic == 2:
        return 'Rare'
    if magic == 3:
        return 'Very Rare'
    if magic == 4:
        return 'Legendary'


class GenericItem:
    def __init__(self):
        self.id = 0

        self._init_args = {}
        self.name = ""
        self.properties = {}
        self.magic = 0
        self.rarity = calculate_rarity(self.magic)
        self.damage_type = ''
        self.scaling = []
        self.types = []
        self.quantity = None
        self.range = '5'
        self.image = ''
        self.actions = dict()

        self.info = []

    def damage(self, ability_mod):
        pass

    def hit(self, proficiency_bonus, ability_mod, proficiencies):
        # If weapon can scale with the higher of STR or DEX, use the higher modifier
        if 'dex' in self.scaling:
            mod = max(ability_mod.get('str', 0), ability_mod.get('dex', 0))
        else:
            mod = ability_mod.get('str', 0)

        if any(prof in proficiencies for prof in self.types):
            hit_bonus = self.magic + mod + proficiency_bonus
        else:
            hit_bonus = self.magic + mod  # No proficiency bonus added
        if hit_bonus >= 0:
            return f'+{hit_bonus}'
        else:
            return f'{hit_bonus}'

    def damage_description(self):
        return ""

    def get_info(self):
        self.info = [
            self.name,
            self.rarity,
            self.damage_description(),
        ]
        if self.properties:
            properties_str = ""
            for property in self.properties.keys():
                properties_str += property + ", "

            self.info.append(properties_str[:-2])


class Items:
    class Empty(GenericItem):
        def __init__(self):
            super().__init__()
            self.image = 'images/Transparent.png'

    class Quarterstaff(GenericItem):
        def __init__(self, magic: int = 0, versatile: str = 'one-hand'):
            super().__init__()
            self.id = 1
            self._versatile = versatile
            self._init_args = {'magic': magic, 'versatile': self._versatile}
            self.types = ['simple', 'staff']
            self.damage_type = 'Bludgeoning'
            self.properties = {'Versatile': self._versatile}
            self.magic = magic
            self.image = 'images/weapons/quarterstaff.png'
            self.scaling = ['str']

            self.rarity = calculate_rarity(self.magic)

            if self.magic:
                self.name = f'Quarterstaff+{self.magic}'
            else:
                self.name = 'Quarterstaff'

            self.info = self.get_info()

            hit_description = [
                "1 Action",
                f"Range: {self.range} feet",
                f"Hit bonus: ",
                f'Damage: 0'
            ]
            hit_image = 'images/standard actions/Large Sword.png'
            self.actions = {'hit': Actions.Hit(self.name, hit_description, hit_image, 7.1)}

        def update(self, player):
            self.actions['hit'].description = [
                "1 Action",
                f"Range: {self.range} feet",
                f"Hit bonus: {self.hit(player.proficiency_bonus, player.ability_scores_mod, player.weapon_proficiency)}",
                f'Damage: {self.damage(player.ability_scores_mod)}'
            ]

        def damage_description(self):
            if self.magic:
                return f'(1d6|1d8)+{self.magic} {self.damage_type}'
            else:
                return f'1d6|1d8 {self.damage_type}'

        def damage(self, ability_mod):
            sides = 8 if self.properties['Versatile'] == 'two-hand' else 6

            if 'dex' in self.scaling:
                mod = max(ability_mod.get('str', 0), ability_mod.get('dex', 0))
            else:
                mod = ability_mod.get('str', 0)
            mod += self.magic
            if mod > 0:
                return f'1d{sides}+{mod} {self.damage_type}'
            elif mod < 0:
                return f'1d{sides}{mod} {self.damage_type}'
            else:
                return f'1d{sides} {self.damage_type}'

        def get_info(self):
            super().get_info()
            self.info.append("")
            self.info.extend(["A sturdy staff that can be used for", "walking or as a weapon."])
            self.info.append("")
            self.info.append(f"Type: {', '.join(self.types)}")

            return self.info

        @property
        def versatile(self):
            return self._versatile

        @versatile.setter
        def versatile(self, value):
            self._versatile = value
            self._init_args['versatile'] = value
            self.properties['Versatile'] = value

    class GeniusSteamGun(GenericItem):
        def __init__(self, magic: int = 0):
            super().__init__()

            self.id = 2

            self._init_args = {'magic': magic}
            self.types = ['firearm']
            self.damage_type = 'piercing'
            self.magic = magic
            self.image = 'images/weapons/genius steam gun.png'
            self.scaling = ['dex']
            self.range = '30/90'

            self.rarity = calculate_rarity(self.magic)

            if self.magic:
                self.name = f'Genius Steam Gun+{self.magic}'
            else:
                self.name = 'Genius Steam Gun'

            self.info = self.get_info()
            hit_description = [
                "1 Action",
                f"Range: {self.range} feet",
                f"Hit bonus: ",
                f'Damage: 0'
            ]
            hit_image = 'images/standard actions/Large Sword.png'
            self.actions = {'hit': Actions.Hit(self.name, hit_description, hit_image, 7.2)}

        def update(self, player):
            self.actions['hit'].description = [
                "1 Action",
                f"Range: {self.range} feet",
                f"Hit bonus: {self.hit(player.proficiency_bonus, player.ability_scores_mod, player.weapon_proficiency)}",
                f'Damage: {self.damage(player.ability_scores_mod)}'
            ]

        def damage(self, ability_mod):
            sides = 10

            mod = ability_mod.get('dex', 0)

            mod += self.magic
            if mod > 0:
                return f'1d{sides}+{mod} {self.damage_type}'
            elif mod < 0:
                return f'1d{sides}-{abs(mod)} {self.damage_type}'
            else:
                return f'1d{sides} {self.damage_type}'

        def damage_description(self):
            if self.magic:
                return f'1d10+{self.magic} {self.damage_type}'
            else:
                return f'1d10 {self.damage_type}'

        def get_info(self) -> list[str]:
            super().get_info()
            self.info.append("")
            self.info.extend(["A sturdy staff that can be used for", "walking or as a weapon."])
            self.info.append("")
            self.info.append(f"Type: {', '.join(self.types)}")

            return self.info


ITEMS_ID_DICT = {0: Items.Empty, 1: Items.Quarterstaff, 2: Items.GeniusSteamGun}
