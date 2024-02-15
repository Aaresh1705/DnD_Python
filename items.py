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


class Items:
    class Quarterstaff:
        def __init__(self, magic: int = 0):
            self.type = ['simple', 'staff']
            self.damage_type = 'Bludgeoning'
            self.properties = {'Versatile': False}
            self.magic = magic
            self.image = 'images/weapons/quarterstaff.png'
            self.quantity = None

            self.rarity = calculate_rarity(self.magic)

            if self.magic:
                self.name = f'Quarterstaff +{self.magic}'
            else:
                self.name = 'Quarterstaff'

            self.info = self.get_info()

        def damage(self):
            sides = 8 if self.properties['Versatile'] else 6
            if self.magic:
                return f'1d{sides}+{self.magic}'
            return f'1d{sides}'

        def damage_description(self):
            if self.magic:
                return f'(1d6|1d8)+{self.magic} {self.damage_type}'
            else:
                return f'1d6|1d8 {self.damage_type}'

        def hit(self, player):
            pass  # TODO: calculate to hit

        def get_info(self):
            info = [
                self.name,
                self.rarity,
                self.damage_description(),
            ]
            properties_str = ""
            for property in self.properties.keys():
                properties_str += property + ", "

            info.append(properties_str[:-2])
            info.append("")
            info.extend(["A sturdy staff that can be used for", "walking or as a weapon."])
            info.append("")
            info.append(f"Type: {', '.join(self.type)}")

            return info
