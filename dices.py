import pygame
import numpy as np

dice_font = pygame.font.SysFont(None, 32)

class Constant:
    def __init__(self, val):
        self.constant = val

        self.roll_value = self.constant
    
    def roll(self):
        self.roll_value = self.constant
        
        self.value_surface = dice_font.render(f'{self.constant}', True, (0x000000))
        self.rect = self.value_surface.get_rect()

        return self.roll_value
    
    def draw(self, surface: pygame.Surface, pos: tuple):
        (x, y) = pos

        self.const_rect = self.value_surface.get_rect(center=(150 + 75 * x,75+50+ 75*y))
        surface.blit(self.value_surface, self.const_rect)

class Standard_dice:
    def __init__(self, sides: int):
        self.sides = sides

        self.sprite = f'dice_sprites/d{sides}.png'
        self.img = pygame.image.load(self.sprite)
        self.img = pygame.transform.scale(self.img, (self.img.get_width()/2, self.img.get_height()/2))
        self.rect = self.img.get_rect(center=(75+75,75+50))

        self.start_angle = np.random.uniform(10,20)

        self.roll_value = None

    def roll(self):
        self.roll_value = np.random.randint(self.sides) + 1

        self.value_surface = dice_font.render(f'{self.roll_value}', True, (0x000000))

        return self.roll_value
    
    def draw(self, surface: pygame.Surface, pos: tuple):
        (x, y) = pos
        self.rect = self.img.get_rect(center=(150 + 75 * x,75+50+ 75*y))
        self.value_rect = self.value_surface.get_rect(center=(self.img.get_width()//2, self.img.get_height()//2))

        combined_surface = pygame.Surface(self.img.get_size(), pygame.SRCALPHA)
        combined_surface.blit(self.img, (0, 0))
        combined_surface.blit(self.value_surface, self.value_rect.topleft)


        rotated_img = pygame.transform.rotate(combined_surface, self.function(self.start_angle))
        rotated_rect = rotated_img.get_rect(center=(150 + 75 * x, 75 + 50 + 75 * y))

        surface.blit(rotated_img, rotated_rect.topleft)

        if self.start_angle > 0:
            self.start_angle -= 0.15
        if self.start_angle < 0:
            self.start_angle = 0

    def function(self, x):
        y = 5*x**2
        return y


class Non_standard_dice:
    def __init__(self, sides):
        self.sides = sides

        self.roll_value = None

    def roll(self):
        self.roll_value = np.random.randint(self.sides) + 1

        self.denominator_surface = dice_font.render(f'{self.roll_value}', True, (0x000000))
        self.numerator_surface = dice_font.render(f'd{self.sides}', True, (0x000000))

        self.rect = self.denominator_surface.get_rect()

        self.line_width = max(self.denominator_surface.get_width(), self.numerator_surface.get_width())

        return self.roll_value
    
    def draw(self, surface: pygame.Surface, pos: tuple):
        (x, y) = pos

        self.num_pos = (150 - self.numerator_surface.get_width() // 2 + 75 * x, 130 + 75*y)
        self.rect.right = 150 - self.numerator_surface.get_width() // 2 + 75 * x
        self.den_pos = (150  - self.denominator_surface.get_width() // 2 + 75 * x, 100 + 75*y)
        self.line_pos = (150 - self.line_width // 2 + 75 * x, 125 + 75*y)

        surface.blit(self.numerator_surface, self.num_pos)
        surface.blit(self.denominator_surface, self.den_pos)

        # Draw the division line
        pygame.draw.line(surface, (0x000000), self.line_pos, (self.line_pos[0] + self.line_width, self.line_pos[1]), 2)
