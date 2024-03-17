import pygame
pygame.init()
import numpy as np
import sys, os
from dices import Constant, StandardDice, NonStandardDice


def roll(dices: list):
    total = 0
    for dice in dices:
        total += dice.roll()

    return total


def log(surface: pygame.Surface, field, title, log):
    pygame.draw.rect(surface, (0x2D2D2D), field)
    surface.blit(title, (field.x+5, field.y+5)) 
    for index, line in enumerate(log, 1):
        surface.blit(line, (field.x + 5, field.y + 20*index)) 


def check_valid_input(input, standard_dices):
    split_input = input.split("+")
    dices = []

    for dice in split_input:
        index = dice.find("d")
        if index == -1:
            try:
                dices.append(Constant(int(dice)))
            except:
                return False, []
            
        else:
            try:
                dice_sides = int(dice[index+1:])
                if dice[:index] == "":
                    dice_amount = 1
                else:
                    dice_amount = int(dice[:index])
                for i in range(dice_amount):
                    if dice_sides in standard_dices:
                        dices.append(StandardDice(dice_sides))
                    else:
                        dices.append(NonStandardDice(dice_sides))
            except:
                return False, []

    return True, dices


def sort_key(path):
    # Extract the dice number from the file name
    num_part = path.split('d')[-1].split('.')[0]
    return int(num_part)


def main():
    surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Dice Goblin")

    clock = pygame.time.Clock()

    log_title_font = pygame.font.Font(None, 26)
    log_font = pygame.font.Font(None, 22)
    log_field = pygame.Rect(surface.get_width()-300, surface.get_height()-100, 400, 100)
    log_title = log_title_font.render("LOG:", True, (255, 255, 255)) 
    log_text_contens = []
    i = 0

    input_font = pygame.font.Font(None, 32)
    input_text = ""
    input_field = pygame.Rect(100, 25, surface.get_width()-150, 32)
    cursor_position = 0
    last_key_pressed = None
    key_pressed_time = None

    clear_button = pygame.Rect(200, 200, 10, 10)
    roll_button = pygame.Rect(200, 220, 10, 10)

    sprites = []
    for root, dirs, files in os.walk("dice_sprites/"):
        for file in files:
            if any(file.lower().endswith(ext) for ext in [".png"]):
                sprites.append(os.path.join(root, file))
    sprites = sorted(sprites, key=sort_key)
    sprites.reverse()

    last_dice_chosen = None

    dice_field = pygame.Rect(100, 75, surface.get_width()-150, surface.get_height()-250)
    sorted_dice_sides = [sort_key(path) for path in sprites]
    dice = []
    total = 0

    goblin_sound = pygame.mixer.Sound("misc_sprites/goblin.mp3")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    if cursor_position > 0:
                        input_text = input_text[:cursor_position - 1] + input_text[cursor_position:]
                        key_pressed_time = pygame.time.get_ticks()
                        last_key_pressed = event.key
                        cursor_position -= 1
                elif event.key == pygame.K_DELETE:
                    if cursor_position < len(input_text):
                        input_text = input_text[:cursor_position] + input_text[cursor_position + 1:]
                        key_pressed_time = pygame.time.get_ticks()
                        last_key_pressed = event.key
                elif event.key == pygame.K_LEFT:
                    cursor_position = max(0, cursor_position - 1)
                    key_pressed_time = pygame.time.get_ticks()
                    last_key_pressed = event.key
                elif event.key == pygame.K_RIGHT:
                    cursor_position = min(len(input_text), cursor_position + 1)
                    key_pressed_time = pygame.time.get_ticks()
                    last_key_pressed = event.key
                elif event.key == pygame.K_RETURN:
                    valid_input, dice = check_valid_input(input_text, sorted_dice_sides)
                    if valid_input:
                        total = roll(dice)
                        log_text_contens.insert(0, log_font.render(f"[{i}] You rolled a total of: {total}", True, (255, 255, 255)))
                        i += 1
                    else:
                        log_text_contens.insert(0, log_font.render(f"[{i}] Invalid Dice Input", True, (255, 255, 255)))
                        i += 1
                else:
                    input_text = input_text[:cursor_position] + event.unicode + input_text[cursor_position:]
                    key_pressed_time = pygame.time.get_ticks()
                    last_key_pressed = event.key
                    cursor_position += 1

            if event.type == pygame.KEYUP:
                last_key_pressed = None

            if event.type == pygame.VIDEORESIZE:
                old_surface_saved = surface
                surface = pygame.display.set_mode((event.w, event.h),
                                                pygame.RESIZABLE)
                surface.blit(old_surface_saved, (0,0))
                del old_surface_saved

                input_field = pygame.Rect(100, 25, surface.get_width()-150, 32)
                log_field = pygame.Rect(surface.get_width()-300, surface.get_height()-100, 400, 100)
                dice_field = pygame.Rect(100, 75, surface.get_width()-150, surface.get_height()-250)
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if clear_button.collidepoint(event.pos):
                    input_text = ""
                
                elif roll_button.collidepoint(event.pos):
                    valid_input, dice = check_valid_input(input_text, sorted_dice_sides)
                    if valid_input:
                        roll(dice)
                    else:
                        log_text_contens.insert(0, log_font.render(f"[{i}] Invalid Dice Input", True, (255, 255, 255)))
                        i += 1
                elif goblin_rect.collidepoint(event.pos):
                    pygame.mixer.Sound.play(goblin_sound)

                for (sprite, d) in zip(sprite_rects, sorted_dice_sides):
                    if sprite.collidepoint(event.pos):
                        new_die = StandardDice(d)
                        new_die.roll()
                        total += new_die.roll_value
                        if len(input_text) == 0:
                            add_input = f'd{d}'
                            cursor_position += len(add_input)
                            input_text += add_input
                        else:
                            index_last_plus = input_text.rfind("+")
                            index_last_d = input_text.rfind("d")
                            if d == last_dice_chosen and index_last_d > -1:
                                val = input_text[index_last_plus+1:index_last_d]
                                if val == "":
                                    val = 1
                                else:
                                    val = int(val)

                                if len(input_text) == cursor_position:
                                    input_text = input_text[:index_last_plus+1]
                                    add_input = f'{val+1}d{d}'
                                    
                                    cursor_position = len(input_text)+len(add_input)
                                else:
                                    input_text = input_text[:index_last_plus+1]
                                    add_input = f'{val+1}d{d}'

                            else:
                                add_input = f'+d{d}'
                                if len(input_text) == cursor_position:
                                    cursor_position += len(add_input)

                            input_text += add_input

                        log_text_contens.insert(0, log_font.render(f"[{i}] New total: {total}", True, (255, 255, 255)))
                        i += 1
                        dice.append(new_die)

                        last_dice_chosen = d

                try:
                    if event.button == 1:
                        for index, die in enumerate(dice):
                            if die.rect.collidepoint(event.pos):
                                dice.pop(index)
                                total -= die.roll_value
                                log_text_contens.insert(0, log_font.render(f"[{i}] New total: {total}", True, (255, 255, 255)))
                                i += 1 
                                del die
                    elif event.button == 3:
                        for index, die in enumerate(dice):
                            if die.rect.collidepoint(event.pos):
                                total -= die.roll_value
                                die.roll()
                                die.start_angle = np.random.uniform(10,20)
                                total += die.roll_value
                                log_text_contens.insert(0, log_font.render(f"[{i}] New total: {total}", True, (255, 255, 255)))
                                i += 1 
                except:
                    pass
        
        current_time = pygame.time.get_ticks()
        if last_key_pressed and current_time - key_pressed_time > 500:  # Initial delay before repeating
            key_pressed = pygame.key.name(last_key_pressed)
            if key_pressed == "backspace":
                if cursor_position > 0:
                    input_text = input_text[:cursor_position - 1] + input_text[cursor_position:]
                    cursor_position -= 1
            elif key_pressed == "delete":
                if cursor_position < len(input_text):
                    input_text = input_text[:cursor_position] + input_text[cursor_position + 1:]
            elif key_pressed == "left":
                cursor_position = max(0, cursor_position - 1)
            elif key_pressed == "right":
                cursor_position = min(len(input_text), cursor_position + 1)
            else:
                input_text += key_pressed  # Append the last key pressed
                cursor_position += 1

            key_pressed_time = current_time - 1000  # Subsequent characters quicker
        
        surface.fill((0x1F1F1F))

        goblin = pygame.image.load("misc_sprites/Goblin.png")
        goblin = pygame.transform.scale(goblin, (goblin.get_width()/5, goblin.get_height()/5))
        goblin_rect = goblin.get_rect(center=(150,surface.get_height()-70))
        surface.blit(goblin, goblin_rect)

        pygame.draw.rect(surface, (0x181818), (0, 0, 75, surface.get_height()))
        pygame.draw.rect(surface, (0x454545), (-10, -10, 75+10, surface.get_height()+20), 2)
        
        pygame.draw.rect(surface, (0x353535), (10, surface.get_height()-10, 75-2*10, - 360), border_radius=10)
        pygame.draw.rect(surface, (0x1F1F1F), (10, surface.get_height()-10, 75-2*10, - 360),2 , border_radius=10)

        sprite_rects = []
        for index, sprite in enumerate(sprites):
            img = pygame.image.load(sprite)
            img = pygame.transform.scale(img, (img.get_width()/3, img.get_height()/3))
            img_rect = img.get_rect(center=(75/2,surface.get_height()-50*index - 40))
            sprite_rects.append(img_rect)
            surface.blit(img, img_rect)

        pygame.draw.rect(surface, (0x353535), dice_field, border_radius=5)  

        #pygame.draw.rect(surface, (0xff0000), clear_button)
        #pygame.draw.rect(surface, (0x00ff00), roll_button)

        pygame.draw.rect(surface, (0x2D2D2D), input_field, border_radius=5)
        text_surface = input_font.render(input_text, True, (255, 255, 255)) 
        surface.blit(text_surface, (input_field.x+5, input_field.y+5)) 

        x, y = (0, 0)
        if dice:
            for die in dice:
                die.draw(surface, (x, y))
                if die.rect.right > surface.get_width()-140:
                    y += 1
                    x = 0
                else:
                    x += 1  

        cursor_x = input_field.x + 5 + input_font.size(input_text[:cursor_position])[0]
        pygame.draw.line(surface, (255, 255, 255), (cursor_x, input_field.y + 5), (cursor_x, input_field.y + 25))

        log(surface, log_field, log_title, log_text_contens)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
