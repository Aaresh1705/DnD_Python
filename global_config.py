import os

if os.getenv('GAME') == '1':
    pass
import pygame
from pygame import Surface


def intToRoman(num) -> str:
    # Storing roman values of digits from 0-9
    # when placed at different places
    m: list[str] = ["", "M", "MM", "MMM"]
    c: list[str] = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM "]
    x: list[str] = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    i: list[str] = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands: str = m[num // 1000]
    hundreds: str = c[(num % 1000) // 100]
    tens: str = x[(num % 100) // 10]
    ones: str = i[num % 10]

    ans: str = (thousands + hundreds + tens + ones)

    return ans


FONT: str = 'misc/JetBrainsMono-Light.ttf'

SKILL_MAPPING: dict[str, str] = {
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

ABILITY_MAPPING: dict[str, int] = {
    "str": 0,
    "dex": 0,
    "int": 0,
    'wis': 0,
    'cha': 0,
    'con': 0
}


IMAGE_CACHE: dict[Surface] = {}
def get_image(image_path, size=(64, 64)):
    """
    Returns a scaled pygame.Surface object for the image at image_path.
    If the image is in the cache, it uses the cached version.
    Otherwise, it loads the image, caches it, and returns it.
    """
    global IMAGE_CACHE

    # Check if the image is already loaded
    if image_path not in IMAGE_CACHE:
        # Load the image and add it to the cache
        try:
            loaded_image: Surface = pygame.image.load(image_path).convert_alpha()
            loaded_image: Surface = pygame.transform.scale(loaded_image, size)
            IMAGE_CACHE[image_path] = loaded_image
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            loaded_image: Surface = pygame.image.load('images/Unknown.png').convert_alpha()
            loaded_image: Surface = pygame.transform.scale(loaded_image, size)
            IMAGE_CACHE[image_path] = loaded_image

    # Get the image from the cache
    image: Surface = IMAGE_CACHE[image_path]

    return image
