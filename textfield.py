import pygame
import math
from global_config import get_image


class Button:
    def __init__(self, x, y, radius):
        # The button's clickable area is still a rect for easy click detection
        # But it is sized based on the radius
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.bg_color = (255, 255, 255)  # Black
        self.fg_color = (0, 0, 0)  # Black
        self.radius = radius
        self.inner_radius = radius
        self.pressed = False

    def draw(self, surface):
        # Draw the outer circle
        pygame.draw.ellipse(surface, self.bg_color, self.rect)
        # Draw the inner circle slightly smaller
        inner_rect = self.rect.inflate(-4, -4)  # Adjust the border size as needed
        if self.pressed:
            pygame.draw.ellipse(surface, self.fg_color, inner_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is within the rect
            if self.rect.collidepoint(event.pos):
                # Additional check to see if click is within the circle's radius
                distance = math.sqrt((event.pos[0] - self.rect.centerx) ** 2 +
                                     (event.pos[1] - self.rect.centery) ** 2)
                if distance < self.radius:
                    self.pressed = not self.pressed

                    return True
                    # Button was clicked, perform an action
        return False

class Text:
    def __init__(self, font: pygame.font.Font, text, pos, color):
        self.text = text
        self.font = font
        self.color = color
        self.title_surface = self.font.render(self.text, True, self.color)
        self.rect = self.title_surface.get_rect()
        self.rect.topleft = pos

    def draw(self, surface):
        surface.blit(self.title_surface, self.rect)

    def change_text(self, text):
        if text != self.text:
            self.text = text
            self.title_surface = self.font.render(text, True, self.color)
            self.rect = self.title_surface.get_rect(topleft=(self.rect.x, self.rect.y))


class ImageWithText:
    def __init__(self, font: pygame.font.Font, text: str, pos: tuple, color: tuple, image_path='', description=""):
        self.font = font
        self.text = text
        self.pos = pos
        self.color = color
        self.description = description  # Additional attribute for the description

        self.image = get_image(image_path, (32, 32))

        self.text_offset_x = self.image.get_width() + 10  # Adjust as needed
        self.image_rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

    def draw(self, surface):
        # Draw the image
        surface.blit(self.image, self.pos)

        # Render and draw the text
        text_surface = self.font.render(self.text, True, self.color)
        text_pos = (self.pos[0] + self.text_offset_x, self.pos[1])
        surface.blit(text_surface, text_pos)

    def draw_description(self, surface, mouse_pos):
        max_width = max(self.font.size(line)[0] for line in self.description)
        box_height = len(self.description) * self.font.get_linesize() + 10
        desc_background = pygame.Surface((max_width + 20, box_height))
        desc_background.fill((0, 0, 0))
        desc_background.set_alpha(180)

        desc_pos = (mouse_pos[0] + 20, mouse_pos[1])
        surface.blit(desc_background, desc_pos)

        for i, line in enumerate(self.description):
            line_surface = self.font.render(line, True, self.color)
            surface.blit(line_surface, (desc_pos[0] + 10, desc_pos[1] + 5 + i * self.font.get_linesize()))


class TextField:
    def __init__(self, x, y, width, height, font: pygame.font.Font, title, box_width: int = 2, text_shift: tuple = (0, 0), text: str = ''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White
        self.title = title
        self.width = box_width
        self.text = text
        self.font = font
        self.title_surface = font.render(title, True, self.color)
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False
        self.text_shift = text_shift

        self.backspace_initial_delay_passed = False
        self.initial_delay = 500
        self.repeat_rate = 50
        self.last_backspace_time = None
        self.key_pressed_time = 0
        self.backspace_pressed = False

        self.output = None

    def draw(self, surface):
        self.delete_repeat()
        self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
        title_pos = (self.rect.x, self.rect.y - 20)  # Position the title above the text field
        surface.blit(self.title_surface, title_pos)

        # Blit the text.
        surface.blit(self.txt_surface, (self.rect.x + self.text_shift[0], self.rect.y + self.text_shift[1]))

        # Blit the rect.
        pygame.draw.rect(surface, self.color, self.rect, self.width)

    def delete_repeat(self):
        current_time = pygame.time.get_ticks()
        if self.active and self.backspace_pressed:
            if (current_time - self.last_backspace_time) >= self.initial_delay:  # 1 second delay
                self.delete_character()
                self.last_backspace_time = current_time

                self.last_backspace_time -= current_time - 1000

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = True
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = 0x669766 if self.active else 0xFFFFFF
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.active:
                    self.backspace_pressed = True  # Mark backspace as pressed
                    self.delete_character()  # Immediately delete character
                    self.last_backspace_time = pygame.time.get_ticks()

                if event.key == pygame.K_RETURN:
                    self.output = self.text

            if event.type == pygame.TEXTINPUT and self.active:
                # Add the character from the TEXTINPUT event to the text
                self.text += event.text

            if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                self.backspace_pressed = False

    def delete_character(self):
        self.text = self.text[:-1]

    def deselect(self):
        self.output = None
        self.active = False
        self.color = 0xFFFFFF


