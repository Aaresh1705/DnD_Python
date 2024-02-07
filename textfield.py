import pygame


class Text:
    def __init__(self, font: pygame.font.Font, text, pos, color):
        self.text = text
        self.font = font
        self.color = color

        self.pos = pos

    def draw(self, surface):
        title_surface = self.font.render(self.text, True, self.color)
        surface.blit(title_surface, self.pos)


class TextField:
    def __init__(self, x, y, width, height, font: pygame.font.Font, title):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White
        self.title = title
        self.text = ''
        self.font = font
        self.title_surface = font.render(title, True, self.color)
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False

        self.backspace_initial_delay_passed = False
        self.initial_delay = 500
        self.repeat_rate = 50
        self.last_backspace_time = None
        self.key_pressed_time = 0
        self.backspace_pressed = False

        self.output = None

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
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
                    self.output = self.text.lower()

            if event.type == pygame.TEXTINPUT and self.active:
                # Add the character from the TEXTINPUT event to the text
                self.text += event.text
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))

            if event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
                self.backspace_pressed = False

    def delete_character(self):
        self.text = self.text[:-1]

        self.txt_surface = self.font.render(self.text, True, (255, 255, 255))
            
    def delete_repeat(self):
        current_time = pygame.time.get_ticks()
        if self.active and self.backspace_pressed:
            if (current_time - self.last_backspace_time) >= self.initial_delay:  # 1 second delay
                self.delete_character()
                self.last_backspace_time = current_time

                self.last_backspace_time -= current_time - 1000

    def deselect(self):
        self.output = None
        self.active = False
        self.color = 0xFFFFFF

    def draw(self, surface):
        self.delete_repeat()

        title_pos = (self.rect.x, self.rect.y - 20)  # Position the title above the text field
        surface.blit(self.title_surface, title_pos)
        
        # Blit the text.
        surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        
        # Blit the rect.
        pygame.draw.rect(surface, self.color, self.rect, 2)
