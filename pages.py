import pygame
import numpy as np
from races import *
from classes import *
from background import *
from textfield import *
from player import Player, skill_mapping
from inventory import Inventory
from items import Items


def intToRoman(num):
    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D",
         "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L",
         "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V",
         "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    ans = (thousands + hundreds +
           tens + ones)

    return ans


class MainPage:  # TODO: Make saving throw things
    def __init__(self, surface: pygame.Surface, *args):
        player = args[0]
        self.font = pygame.font.Font('JetBrainsMono-Light.ttf', 16) #24
        self.text_color = (255, 255, 255)
        self.text_elements = {
            'level': (Text(self.font, f"Level: {player.level}",
                           (20, 50), self.text_color), 'Level'),

            'race': (Text(self.font, f"Race: {player.race.name}",
                          (20, 100), self.text_color), 'Race'),

            'char_class': (Text(self.font, f"Class: {player.char_class.name}",
                                (20, 150), self.text_color), 'Class'),

            'background': (Text(self.font, f"Background: {player.background.name}",
                                (20, 200), self.text_color), 'Background'),

            'max_health': (Text(self.font, f"Max health: {player.max_health}",
                                (20, 300), self.text_color), 'Max health'),

            'current_health': (Text(self.font, f"Current health: {player.current_health}",
                                    (20, 350), self.text_color), 'Current health')
        }

        self.skill_font = pygame.font.Font('JetBrainsMono-Light.ttf', 12)
        self.prof_font = pygame.font.SysFont('timesnewroman', 16)
        self.skills = [
            {f'{skill}': f'{skill} ({mapping})', 'total': str(player.skills[skill]),
             'prof': '0', 'misc': '0'}
            for (skill, ability), mapping in zip(player.skills.items(), skill_mapping.values())
        ]

        # Draw column headers
        self.headers = ['Skill', 'Total', 'Prof.', 'Misc', 'Prof. buttons']
        # Define positions and column widths
        self.start_x = 20  # Starting X position
        self.start_y = 400
        self.column_widths = [180, 45, 45, 45, 40]  # Width of each column
        self.line_height = 20  # Height of each line

        misc_text_fields = [
            TextField(self.start_x + sum(self.column_widths[:-2]), self.start_y + 50 + (i * self.line_height),
                      self.column_widths[3], self.line_height, self.skill_font, '', 1, (5, 0),
                      str(player_skill) if player_skill != 0 else '')
            for i, player_skill in enumerate(player.skill_misc_modifier.values())
        ]

        for i, skill in enumerate(self.skills):
            skill['misc'] = misc_text_fields[i]

        self.buttons = []
        for j in range(2):
            for i, proficiency in enumerate(player.skill_proficiency.values()):
                button = Button(self.start_x + sum(self.column_widths[:-1]) + 5 + + 20 * j,
                                self.start_y + 50 + (i * self.line_height) + 5, 5)
                button.pressed = 1 if proficiency - j > 0 else 0

                self.buttons.append(button)

        self.total_scroll = 0
        self.scroll_min = 0
        self.scroll_max = -400

        self.label_offset = 0
        self.value_offset = 0

    def draw(self, surface: pygame.Surface, *args):
        player = args[0]

        self.update_table(player)

        # Left Text
        for key, (text_element, text) in self.text_elements.items():
            attr_name = getattr(player, key, None)
            attr_name = getattr(attr_name, 'name', None) if hasattr(attr_name, 'name') else attr_name
            text_element.change_text(f'{text}:  {attr_name}')
            text_element.draw(surface)

        # Hexagon
        self.label_offset = surface.get_width() - 90
        self.value_offset = self.label_offset + 50
        for index, (stat, value) in enumerate(player.abilityscores.items()):
            # Render the stat name
            label_surface = self.font.render(f'{stat}: {value}', True, pygame.Color('white'))
            label_rect = label_surface.get_rect(left=self.label_offset, top=300 + 30 * index)

            # Blit both surfaces to the screen
            surface.blit(label_surface, label_rect)

        center = (surface.get_width() - 110, 150)
        self.draw_hexagon_with_labels(surface, center, 75, 2 * np.pi / len(player.abilityscores),
                                      player.abilityscores, 3 * np.pi / 2)

        # Show titles of table
        for i, header in enumerate(self.headers):
            header_surf = self.skill_font.render(header, True, (255, 255, 255))
            surface.blit(header_surf, (self.start_x + sum(self.column_widths[:i]) + 5, self.start_y + 20))

        # Draw table
        for i, skill in enumerate(self.skills):
            y_position = self.start_y + 50 + (i * self.line_height)  # Calculate the Y position for each skill
            for j, (key, value) in enumerate(skill.items()):
                if key not in ['misc', 'prof']:  # Handle non-TextField values as before
                    cell_surf = self.skill_font.render(str(value), True, (255, 255, 255))
                    cell_rect = cell_surf.get_rect(topleft=(self.start_x + sum(self.column_widths[:j]) + 5, y_position))
                    surface.blit(cell_surf, cell_rect)
                elif key == 'prof':
                    cell_surf = self.prof_font.render(str(value), True, (255, 255, 255))
                    cell_rect = cell_surf.get_rect(topleft=(self.start_x + sum(self.column_widths[:j]) + 5, y_position))
                    surface.blit(cell_surf, cell_rect)
                else:  # For 'misc' column, draw the TextField
                    value.draw(surface)  # 'value' is a TextField object

                # Draw cell borders (optional)
                pygame.draw.rect(surface, (255, 255, 255),
                                 (cell_rect.left - 5, cell_rect.top, self.column_widths[j], self.line_height), 1)

        pygame.draw.line(surface, (255, 255, 255), (self.start_x, self.start_y + 45),
                         (sum(self.column_widths) + self.start_x, self.start_y + 45), 1)

        for button in self.buttons:
            button.draw(surface)

    def misc_box_output(self, player):
        for skill_box_row, skill_player_row in zip(self.skills, player.skill_misc_modifier.items()):
            box = skill_box_row['misc']
            if box.output or box.output == "":
                try:
                    box.output = 0 if box.output == "" else box.output
                    box.output = int(box.output)
                    player.skill_misc_modifier[skill_player_row[0]] = box.output
                    box.deselect()
                    box.output = None
                except:
                    pass

    def update_table(self, player):
        for ability, prof, skill in zip(player.skills.values(), player.skill_proficiency.values(), self.skills):
            skill['total'] = ability
            skill['prof'] = intToRoman(prof)

    def handle_event(self, event, player):
        if event.type == pygame.MOUSEWHEEL:
            scroll_amount = event.y * 30
            self.total_scroll += scroll_amount
            if self.total_scroll > self.scroll_min:
                scroll_amount -= (self.total_scroll - self.scroll_min)
                self.total_scroll = self.scroll_min
                # Check for the lower bound
            elif self.total_scroll < self.scroll_max:
                scroll_amount += (self.scroll_max - self.total_scroll)
                self.total_scroll = self.scroll_max

            for text in self.text_elements.values():
                text[0].rect.y += scroll_amount

            self.start_y += scroll_amount

            for box in self.skills:
                box['misc'].rect.y += scroll_amount

            for button in self.buttons:
                button.rect.y += scroll_amount

        for skill in self.skills:
            skill['misc'].handle_event(event)

        self.misc_box_output(player)

        for button_col1, button_col2, key in zip(self.buttons[:len(self.buttons) // 2],
                                                 self.buttons[len(self.buttons) // 2:], skill_mapping.keys()):
            button_col1.handle_event(event)
            button_col2.handle_event(event)

            player.skill_proficiency[key] = button_col1.pressed + button_col2.pressed

    @staticmethod
    def rotate_point(x, y, theta, center):
        cos_theta, sin_theta = np.cos(theta), np.sin(theta)
        x -= center[0]
        y -= center[1]
        new_x = x * cos_theta - y * sin_theta + center[0]
        new_y = x * sin_theta + y * cos_theta + center[1]
        return new_x, new_y

    def draw_hexagon_with_labels(self, surface, center, radius, angle, ability_scores_dict, angle_of_rotation):
        line_color = 0xB0B0B0
        attribute_color = pygame.Color('red')
        text_color = pygame.Color('white')

        font = pygame.font.Font('JetBrainsMono-Light.ttf', 14)

        # Determine the maximum value for scaling
        max_value = max(ability_scores_dict.values()) if max(ability_scores_dict.values()) > 20 else 20

        # Calculate points for the hexagon and ability score values
        for i, (score_name, value) in enumerate(ability_scores_dict.items()):
            # Position for the hexagon point
            x = center[0] + np.cos(i * angle) * radius
            y = center[1] + np.sin(i * angle) * radius

            # Rotate the hexagon point
            hexagon_point = self.rotate_point(x, y, angle_of_rotation, center)

            # Position for the value point
            value_x = center[0] + np.cos(i * angle) * (value / max_value) * radius
            value_y = center[1] + np.sin(i * angle) * (value / max_value) * radius

            # Rotate the value point
            value_point = self.rotate_point(value_x, value_y, angle_of_rotation, center)

            # Render the ability score name
            text_surface = font.render(score_name, True, text_color)
            text_rect = text_surface.get_rect(center=hexagon_point)

            # Adjust text position to not overlap with the hexagon
            offset_x, offset_y = 20, 20  # Adjust as needed for text offset

            if i in [0, 3]:  # Top and bottom points
                text_rect.centery -= offset_y if i == 0 else -offset_y
            elif i in [1, 2]:  # right points
                text_rect.centerx += offset_x
            else:  # left points
                text_rect.centerx -= offset_x

            # Draw the text on the surface
            surface.blit(text_surface, text_rect)

        # Draw the hexagon and the value polygon
        hexagon_points = [self.rotate_point(center[0] + np.cos(i * angle) * radius,
                                            center[1] + np.sin(i * angle) * radius,
                                            angle_of_rotation, center) for i in range(6)]

        value_points = [self.rotate_point(center[0] + np.cos(i * angle) * (value / max_value) * radius,
                                          center[1] + np.sin(i * angle) * (value / max_value) * radius,
                                          angle_of_rotation, center) for i, value in
                        enumerate(list(ability_scores_dict.values()))]

        for value in [10, 20]:
            scale = value / max_value  # Scale factor based on maximum value of 20
            inner_hexagon_points = [self.rotate_point(center[0] + np.cos(i * angle) * radius * scale,
                                                      center[1] + np.sin(i * angle) * radius * scale,
                                                      angle_of_rotation, center) for i in range(6)]
            pygame.draw.polygon(surface, line_color, inner_hexagon_points, 1)

        pygame.draw.polygon(surface, line_color, hexagon_points, 3)
        pygame.draw.polygon(surface, attribute_color, value_points, 1)


class InvPage:  # TODO: Finish InvPage
    def __init__(self, surface: pygame.Surface, *args):
        player = args[0]


        self.Inventory_matrix = Inventory(surface, 64*5, 64*8, surface.get_width() - 64*5, surface.get_height()-64*8)
        player.update_inventory(self.Inventory_matrix)
        self.font = pygame.font.Font('VeraMono.ttf', 16)

    def draw(self, surface: pygame.Surface, *args):
        self.Inventory_matrix.draw(surface)
        mouse_pos = pygame.mouse.get_pos()
        hovered_item = self.Inventory_matrix.get_item_under_mouse(mouse_pos)
        if hovered_item:
            self.draw_item_description(surface, hovered_item, mouse_pos)

    def draw_item_description(self, surface, item, position):
        """Draw a multiline description box for the given item at the specified position."""
        lines = [
            item.item.name,  # Assuming 'item' already has the attribute 'name'
            f"Qty: {item.quantity}",
            f"Type: {', '.join(item.item.type)}"  # Assuming 'item' has an attribute 'type' which is a list
        ]

        # Calculate the size of the text box
        line_height = self.font.get_linesize()
        box_width = max(self.font.size(line)[0] for line in lines) + 10
        box_height = line_height * len(lines) + 10

        # Create a new surface for the text box with an alpha channel
        text_box_surface = pygame.Surface((box_width, box_height)).convert_alpha()
        text_box_surface.fill((0, 0, 0, 128))  # Semi-transparent background

        # Render each line of text
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, pygame.Color('white'))
            # Blit the text line onto the text box surface
            text_box_surface.blit(text_surface, (5, 5 + i * line_height))

        right_offset = 10  # You can adjust this value as needed
        position = (position[0] + right_offset, position[1])

        # Blit the text box onto the main surface
        surface.blit(text_box_surface, position)

    def handle_event(self, event, player):
        self.Inventory_matrix.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                player.items.append(Items.Quarterstaff())
                player.update_inventory(self.Inventory_matrix)


class TurnPage:  # TODO: Make TurnPage
    def __init__(self, surface: pygame.Surface, *args):
        a, b = surface.get_width(), surface.get_height()
        self.x = pygame.Rect(a - 100, b - 100, 100, 100)

    def draw(self, surface: pygame.Surface, *args):
        a, b = surface.get_width(), surface.get_height()
        self.x = pygame.Rect(a - 100, b - 100, 100, 100)

        pygame.draw.rect(surface, 0x0000FF, self.x)

    def handle_event(self, event, player):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x.collidepoint(event.pos):
                print(event.pos)


class ChangePage:  # TODO: Finish ChangePage
    def __init__(self, surface: pygame.Surface, *args):
        player = args[0]

        self.font = pygame.font.Font('JetBrainsMono-Light.ttf', 16)
        titles_1 = ["Race & Subrace", "Class & Subclass", "Background"]
        self.output_var_1 = ["race", "char_class", "background"]
        self.class_list = [RACES, CLASSES, BACKGROUNDS]

        titles_2_1 = ["Level", "Max health", "Current health"]
        self.output_var_2_1 = ["level", "max_health", "current_health"]

        titles_2_2 = ["str", "dex", "int", 'wis', 'cha', 'con']
        self.output_var_2_2 = titles_2_2

        titles_3 = ["Age", "Weight"]
        self.output_var_3 = ["age", "weight"]

        titles_4 = ['Armor', 'Weapons', 'Tools', 'Saving Throws', 'Skills']
        self.output_var_2_2 = titles_2_2

        self.input_boxes_1 = [
            TextField(20, 100 + 60 * i, 250, 32, self.font, title, text_shift=(5, 5), text=(str(text) if text else ''))
            for i, (title, text) in
            enumerate(zip(titles_1, [player.race.name, player.char_class.name, player.background.name]))]
        self.input_boxes_2_1 = [
            TextField(300, 100 + 60 * i, 100, 32, self.font, title, text_shift=(5, 5), text=str(text))
            for i, (title, text) in
            enumerate(zip(titles_2_1, [player.level, player.max_health, player.current_health]))]
        self.input_boxes_2_2 = [
            TextField(20 + 16*4 * j, 320 + 60 * i, 32, 32, self.font, titles_2_2[i + j * 3], text_shift=(5, 5),
                      text=str(list(player.abilityscores_nonmod.values())[i + 3 * j]))
            for j in range(2) for i in range(len(titles_2_2) // 2)]

        """self.input_boxes_3 = [TextField(380, 100 + 60*i, 140, 32, self.font, title, text_shift=(5, 5))
                              for i, title in enumerate(titles_3)]"""

        self.input_boxes_4 = [TextField(20, 550 + 60 * i, 700, 32, self.font, title, text_shift=(5, 5)) for i, title in
                              enumerate(titles_4)]

        self.x = Text(self.font, "Abilityscores", (self.input_boxes_2_2[0].rect.topleft[0],
                                                   self.input_boxes_2_2[0].rect.topleft[1] - 40), (255, 255, 255))
        self.y = Text(self.font, "Proficiencies",
                      (self.input_boxes_4[0].rect.topleft[0], self.input_boxes_4[0].rect.topleft[1] - 40),
                      (255, 255, 255))

        self.scroll_min = 0  # Prevent scrolling above the top of the window
        self.scroll_max = -400
        self.total_scroll = 0

    def text_box_output(self, player: Player):
        for index, box in enumerate(self.input_boxes_1):
            if box.output:
                if any(box.output == c for c in self.class_list[index]):
                    attr_name = self.output_var_1[index]
                    print(f'player.{attr_name}')

                    setattr(player, attr_name, self.class_list[index][box.output])
                    box.deselect()
                    print(getattr(player, attr_name, None))
                box.output = None

        for index, box in enumerate(self.input_boxes_2_1):
            if box.output:
                attr_name = self.output_var_2_1[index]
                # Use setattr to dynamically set the attribute on self.active_class
                setattr(player, attr_name, int(box.output))
                box.deselect()
                print(getattr(player, attr_name, None))

        for index, box in enumerate(self.input_boxes_2_2):
            if box.output:
                player.abilityscores_nonmod[self.output_var_2_2[index]] = int(box.output)
                player.abilityscores[self.output_var_2_2[index]] = int(box.output)
                # Use setattr to dynamically set the attribute on self.active_class
                box.deselect()

    def draw(self, surface: pygame.Surface, *args):
        player = args[0]

        for box in self.input_boxes_1:
            box.draw(surface)
        for box in self.input_boxes_2_1:
            box.draw(surface)
        for box in self.input_boxes_2_2:
            box.draw(surface)

        """if player.race.name:
            for box in self.input_boxes_3:
                box.draw(surface)"""

        self.x.draw(surface)

        for box in self.input_boxes_4:
            box.rect.width = surface.get_width() - 50
            box.draw(surface)

        self.y.draw(surface)

    def handle_event(self, event, player):
        if event.type == pygame.MOUSEWHEEL:
            scroll_amount = event.y * 30
            self.total_scroll += scroll_amount
            if self.total_scroll > self.scroll_min:
                scroll_amount -= (self.total_scroll - self.scroll_min)
                self.total_scroll = self.scroll_min
                # Check for the lower bound
            elif self.total_scroll < self.scroll_max:
                scroll_amount += (self.scroll_max - self.total_scroll)
                self.total_scroll = self.scroll_max

            for box_group in [self.input_boxes_1, self.input_boxes_2_1, self.input_boxes_2_2,  # self.input_boxes_3,
                              self.input_boxes_4]:
                for box in box_group:
                    # Update y position with scroll amount
                    box.rect.y += scroll_amount

            for text in [self.x, self.y]:
                text.rect.y += scroll_amount

        for box in self.input_boxes_1:
            box.handle_event(event)
        for box in self.input_boxes_2_1:
            box.handle_event(event)
        for box in self.input_boxes_2_2:
            box.handle_event(event)
        """for box in self.input_boxes_3:
            box.handle_event(event)"""
        for box in self.input_boxes_4:
            box.handle_event(event)

        self.text_box_output(player)
