import pygame


class Items:
    class Quarterstaff:
        def __init__(self, plus: int = 0):
            self.type = ['simple', 'staff']
            self.damage_type = 'Bludgeoning'
            self.properties = {'Versatile': False}
            self.magic = plus
            self.image = 'images/quarterstaff.png'

            self.name = 'Quarterstaff + ' + self.magic if self.magic else 'Quarterstaff'

        def damage(self):
            sides = 8 if self.properties['Versatile'] else 6
            if self.magic:
                return f'1d{sides}+{self.magic}'
            return f'1d{sides}'

        def hit(self, player):
            pass  # TODO: calculate to hit


class InventoryItem:
    def __init__(self, item, quantity):
        self.item = item
        self.image = pygame.image.load(item.image).convert_alpha()
        self.quantity = quantity
