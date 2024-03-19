import numpy as np


from global_config import *
from inventory import Inventory, EquipmentSlot
from actionbar import ActionBar
from textfield import *

from playerscripts.races import *
from playerscripts.classes import *
from playerscripts.background import *
from playerscripts.player import Player

from dictionarys.items import Items
from dictionarys.actions import Actions


class MainPage:
    def __init__(self, surface: Surface, *args):
        player: Player = args[0]

        """Text init"""
        self.font = pygame.font.Font(FONT, 16)
        self.text_color = (255, 255, 255)
        self.text_elements_left = {
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

            'current_health': (Text(self.font, f"Current health: {player.current_health} + {player.temporary_health}",
                                    (20, 350), self.text_color), 'Current health')
        }

        self.text_elements_right = {
            'ability_scores': (Text(self.font, f"{player.ability_scores}",
                           (20, 50), self.text_color), 'Ability_scores'),
        }

        # Initialize Text objects for ability score labels
        self.ability_score_labels = {}
        center = (surface.get_width() - 110, 150)
        angle = 2 * np.pi / len(player.ability_scores)
        for i, score_name in enumerate(player.ability_scores.keys()):
            x = center[0] + np.cos(i * angle) * 75
            y = center[1] + np.sin(i * angle) * 75
            pos = (x, y)
            self.ability_score_labels[score_name] = Text(self.font, score_name, pos, self.text_color)


        """Skill init"""
        self.skill_font = pygame.font.Font(FONT, 14)
        self.prof_font = pygame.font.SysFont('timesnewroman', 16)
        self.skills = [
            {f'{skill}': f'{skill} ({mapping})', 'total': str(player.skills[skill]),
             'prof': '0', 'misc': '0'}
            for (skill, ability), mapping in zip(player.skills.items(), SKILL_MAPPING.values())
        ]
        # Draw column headers
        self.headers = ['Skill', 'Total', 'Prof.', 'Misc', 'Prof. buttons']
        # Define positions and column widths
        self.start_x = 20  # Starting X position
        self.start_y = 400
        self.column_widths = [180, 45, 45, 45, 40]  # Width of each column
        self.line_height = 30  # Height of each line

        misc_text_fields = [
            TextField(self.start_x + sum(self.column_widths[:-2]), self.start_y + 50 + (i * self.line_height),
                      self.column_widths[3], self.line_height, self.skill_font, '', 1, (5, 5),
                      str(player_skill) if player_skill != 0 else '')
            for i, player_skill in enumerate(player.skill_misc_modifier.values())
        ]

        for i, skill in enumerate(self.skills):
            skill['misc'] = misc_text_fields[i]

        self.buttons = []
        for j in range(2):
            for i, proficiency in enumerate(player.skill_proficiency_butt_mod.values()):
                button = Button(self.start_x + sum(self.column_widths[:-1]) + 5 + + 20 * j,
                                self.start_y + 50 + (i * self.line_height) + 5 + 5, 5)
                button.pressed = 1 if proficiency - j > 0 else 0

                self.buttons.append(button)

        """Page inits"""
        self.total_scroll = 0
        self.scroll_min = 0
        self.scroll_max = -400

    def draw(self, surface: Surface, *args):
        player = args[0]

        """Left Text"""
        self.draw_left_text(surface, player)

        """Right Text"""
        self.draw_right_text(surface, player)

        """Hexagon"""
        center = (surface.get_width() - 110, 150)
        self.draw_hexagon_with_labels(surface, center, 75, 2 * np.pi / len(player.ability_scores),
                                      player.ability_scores, 3 * np.pi / 2)

        """Table"""
        self.update_table(player)
        self.draw_table(surface, player)

    def draw_left_text(self, surface, player):
        for key, (text_element, text) in self.text_elements_left.items():
            if key == 'current_health':
                temp_hp = getattr(player, 'temporary_health', None)
                if temp_hp:  # if temporary_health is not 0
                    if temp_hp > 0:
                        updated_text = f"Current health: {player.current_health} + {player.temporary_health}"
                    else:
                        updated_text = f"Current health: {player.current_health} - {abs(player.temporary_health)}"
                else:
                    updated_text = f"Current health: {player.current_health}"

            else:
                attr_value = getattr(player, key, None)
                if hasattr(attr_value, 'name'):  # if its class, race or background
                    attr_value = attr_value.name
                updated_text = f"{key.replace('_', ' ').title()}: {attr_value}"
            text_element.change_text(updated_text)
            text_element.draw(surface)

    def draw_labels(self, surface, labels, starting_point, y_offset_step=30, x_offset=0):
        for index, (label, value) in enumerate(labels):
            text = f'{label}: {value}' if value is not None else label
            label_surface = self.font.render(text, True, pygame.Color('white'))
            label_rect = label_surface.get_rect(left=starting_point[0] + x_offset,
                                                top=starting_point[1] + y_offset_step * index)
            surface.blit(label_surface, label_rect)

    def draw_right_text(self, surface, player):
        base_x_offset = surface.get_width() - 200
        label_y_offset = 350

        # Draw "Score" section
        self.draw_labels(surface, [('Score', None)], (base_x_offset, label_y_offset - 40), x_offset=0)

        # Draw ability scores
        self.draw_labels(surface, player.ability_scores.items(), (base_x_offset, label_y_offset))

        # Move the x offset for the next section
        next_section_x_offset = 100

        # Draw "Save" section
        self.draw_labels(surface, [('Save', None)], (base_x_offset, label_y_offset - 40),
                         x_offset=next_section_x_offset)

        # Draw save scores
        self.draw_labels(surface, player.saves.items(), (base_x_offset, label_y_offset), x_offset=next_section_x_offset)

    def draw_hexagon_with_labels(self, surface, center, radius, angle, ability_scores_dict, angle_of_rotation):
        line_color = 0xB0B0B0
        attribute_color = (255, 0, 0)
        text_color = (255, 255, 255)

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
            text_surface = self.font.render(score_name, True, text_color)
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

    @staticmethod
    def rotate_point(x, y, theta, center):
        cos_theta, sin_theta = np.cos(theta), np.sin(theta)
        x -= center[0]
        y -= center[1]
        new_x = x * cos_theta - y * sin_theta + center[0]
        new_y = x * sin_theta + y * cos_theta + center[1]
        return new_x, new_y

    def update_table(self, player):
        for ability, prof, skill in zip(player.skills.values(), player.skill_proficiency.values(), self.skills):
            skill['total'] = ability
            skill['prof'] = intToRoman(prof)

    def draw_table(self, surface, player):
        # Show titles of table
        for i, header in enumerate(self.headers):
            header_surf = self.skill_font.render(header, True, (255, 255, 255))
            surface.blit(header_surf, (self.start_x + sum(self.column_widths[:i]) + 5, self.start_y + 20))

        # Draw table
        for i, skill in enumerate(self.skills):
            y_position = self.start_y + 50 + (i * self.line_height) + 5  # Calculate the Y position for each skill
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
                                 (cell_rect.left - 5, cell_rect.top-5, self.column_widths[j], self.line_height), 1)

        pygame.draw.line(surface, (255, 255, 255), (self.start_x, self.start_y + 45),
                         (sum(self.column_widths) + self.start_x, self.start_y + 45), 1)

        for j in range(2):
            for i, proficiency in enumerate(player.skill_proficiency_butt_mod.values()):
                self.buttons[i+j*18].pressed = True if proficiency - j > 0 else False

        for button in self.buttons:
            button.draw(surface)

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

            for text in self.text_elements_left.values():
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
                                                 self.buttons[len(self.buttons) // 2:], SKILL_MAPPING.keys()):

            change1 = button_col1.handle_event(event)
            change2 = button_col2.handle_event(event)
            if change1 or change2:
                player.skill_proficiency_butt_mod[key] = button_col1.pressed + button_col2.pressed

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
                except Exception as e:
                    print(f'Error: {e}')


class InvPage:  # TODO: Finish InvPage
    def __init__(self, surface: pygame.Surface, *args):
        self.font = pygame.font.Font(FONT, 16)
        self.small_font = pygame.font.Font(FONT, 14)

        weapon_types = ['staff', 'simple', 'firearm']
        self.equipment_slots = {
            'helmet': EquipmentSlot('helmet', ['helmet'], 'images/inventory/helmet.png'),
            'cloak': EquipmentSlot('cloak', ['cloak'], 'images/inventory/cloak.png'),
            'chestplate': EquipmentSlot('chestplate', ['chestplate'], 'images/inventory/armour.png'),
            'gloves': EquipmentSlot('gloves', ['gloves'], 'images/inventory/gloves.png'),
            'pants': EquipmentSlot('pants', ['pants'], 'images/inventory/pants.png'),
            'boots': EquipmentSlot('boots', ['boots'], 'images/inventory/boots.png'),
            'amulet': EquipmentSlot('amulet', ['amulet'], 'images/inventory/necklace.png'),
            'ring1': EquipmentSlot('ring1', ['ring'], 'images/inventory/ring1.png'),
            'ring2': EquipmentSlot('ring2', ['ring'], 'images/inventory/ring2.png'),
            'meleeMainHand': EquipmentSlot('meleeMainHand', weapon_types, 'images/inventory/meleeMainHand.png'),
            'meleeOffHand': EquipmentSlot('meleeOffHand', weapon_types, 'images/inventory/meleeOffHand.png'),
        }

        self.inventory = Inventory(surface, 64 * 5, 64 * 8, surface.get_width() - 64 * 5, surface.get_height() - 64 * 8)

        self.versatile_switches = {}

        self.titel_1 = 'Add Item'
        self.add_item_box = TextField(self.inventory.start_x, self.inventory.start_y-40, 250, 32, self.font, self.titel_1, text_shift=(5, 5))

    def draw(self, surface: pygame.Surface, *args):
        player = args[0]
        # Adjust inventory pos:
        self.inventory.start_y = surface.get_height() - 64 * 8
        self.add_item_box.rect.top = self.inventory.start_y - 40

        buff_text_fileds = self.draw_buffs(surface, player)

        self.add_item_box.draw(surface)

        self.draw_equipment_slots(surface, player)

        self.inventory.draw(surface, player)

        self.draw_dragging_item(surface, player)

        self.draw_buffs_description(surface, buff_text_fileds)

    def draw_buffs(self, surface, player):
        buff_text_fileds = []
        for index, buff in enumerate(player.grouped_buffs):
            text = ImageWithText(self.small_font, buff.name, (220, 70 + 45 * index), (255, 255, 255), buff.image,
                                 buff.description)
            text.draw(surface)
            buff_text_fileds.append(text)

        return buff_text_fileds
        return buff_text_fileds

    def draw_buffs_description(self, surface, text_fileds):
        for text in text_fileds:
            mouse_pos = pygame.mouse.get_pos()
            if text.image_rect.collidepoint(mouse_pos):
                text.draw_description(surface, mouse_pos)

    def draw_equipment_slots(self, surface, player):
        start_x = 10  # Adjust as needed
        start_y = 50  # Adjust as needed
        padding = 10  # Space between slots
        for index, slot in enumerate(list(self.equipment_slots.values())[:6]):
            position = (start_x, start_y + index * (64 + padding))  # Adjust as needed
            slot.draw(surface, position, player)

        for index, slot in enumerate(list(self.equipment_slots.values())[6:-2]):
            position = (start_x + 100, start_y + index * (64 + padding))  # Adjust as needed
            slot.draw(surface, position, player)

        for index, slot in enumerate(list(self.equipment_slots.values())[-2:]):
            position = (start_x + index * (64 + padding), surface.get_height() - 10 - 64)  # Adjust as needed
            slot.draw(surface, position, player, self.equipment_slots)

        for slot_name, slot in self.equipment_slots.items():
            slot.update(player)
            if not slot.item == 0 and 'Versatile' in slot.item.properties:
                self.draw_versatile_switch(surface, slot, player)

        mouse_pos = pygame.mouse.get_pos()
        for slot in self.equipment_slots.values():
            if not slot.item.id == 0 and slot.is_hovered(mouse_pos):
                self.draw_equipment_info(surface, slot.item, slot.position)

    def draw_versatile_switch(self, surface, slot, player):
        # Determine the switch state based on the versatile mode of the weapon
        switch_state = player.equipment[slot.slot_name].properties['Versatile']
        switch_position = (slot.position[0] + 12, slot.position[1] - 25)  # Adjust as needed
        self.draw_switch(surface, switch_state, switch_position)
        self.versatile_switches[slot.slot_name] = switch_position

    def draw_switch(self, surface, state, position):
        # Draw the switch background
        background_rect = pygame.Rect(position[0], position[1], 40, 20)
        pygame.draw.rect(surface, (10, 20, 30), background_rect)
        # Draw the switch button
        button_position = position[0] + 5 if state == 'one-hand' else position[0] + 35
        pygame.draw.circle(surface, (100, 90, 30), (button_position, position[1] + 10), 10)

    def toggle_versatile_mode(self, player, slot_name):
        if slot_name in player.equipment and 'Versatile' in player.equipment[slot_name].properties:
            current_mode = player.equipment[slot_name].properties['Versatile']
            new_mode = 'two-hand' if current_mode == 'one-hand' else 'one-hand'
            player.equipment[slot_name].versatile = new_mode

    def draw_equipment_info(self, surface, item, position):
        line_height = self.font.get_linesize()
        box_width = max(self.font.size(line)[0] for line in item.info) + 10
        box_height = line_height * len(item.info) + 10

        # Create a new surface for the text box with an alpha channel
        text_box_surface = pygame.Surface((box_width, box_height)).convert_alpha()
        text_box_surface.fill((0, 0, 0, 128))  # Semi-transparent background

        # Render each line of text
        for i, line in enumerate(item.info):
            text_surface = self.font.render(line, True, pygame.Color('white'))
            # Blit the text line onto the text box surface
            text_box_surface.blit(text_surface, (5, 5 + i * line_height))

        right_offset = 70  # You can adjust this value as needed
        position = (position[0] + right_offset, position[1] - box_height + 64)

        # Blit the text box onto the main surface
        surface.blit(text_box_surface, position)

    def draw_dragging_item(self, surface, player):
        if player.dragging_item:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            image = get_image(player.dragging_item.image)
            item_image = pygame.transform.scale(
                image,
                self.inventory.slot_size
            )
            surface.blit(item_image, (mouse_x - self.inventory.slot_size[0] // 2,
                                      mouse_y - self.inventory.slot_size[1] // 2))

    def handle_event(self, event, player):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any versatile button is clicked
            for slot_name, position in self.versatile_switches.items():
                if pygame.Rect(position[0], position[1], 40, 20).collidepoint(event.pos):
                    self.toggle_versatile_mode(player, slot_name)
                    break

        if event.type == pygame.MOUSEBUTTONUP:
            if self.inventory.dragging:
                for slot_name, slot in self.equipment_slots.items():
                    if slot.is_hovered(event.pos):
                        # Check if the types match
                        if set(slot.slot_type) & set(player.dragging_item.types) and not slot.locked:
                            player.equip_item(player.dragging_item, self.inventory.dragging_start_pos, slot_name)
                            player.dragging_item = Items.Empty()
                            break

        for eq_slot_name, eq_slot in self.equipment_slots.items():
            pos = eq_slot.handle_event(event, player)
            if pos:
                inv_slot = self.inventory.get_slot_at_mouse(pos)
                if inv_slot[0] is not None:
                    player.unequip_item(eq_slot_name, inv_slot, eq_slot.slot_type)

                for nested_eq_slot_name, nested_eq_slot in self.equipment_slots.items():
                    if nested_eq_slot.is_hovered(event.pos):
                        if nested_eq_slot.slot_type == eq_slot.slot_type:
                            player.swap_equip(eq_slot_name, nested_eq_slot_name)
                        break

                break

        self.add_item_box.handle_event(event)
        if self.add_item_box.output:
            self.add_item_by_name(player)
            self.add_item_box.output = None

        self.inventory.handle_event(event, player)

    def add_item_by_name(self, player):
        # Strip whitespace and split the input by spaces to separate name and magic bonus if any
        parts = self.add_item_box.output.strip().split('+')
        name = parts[0].strip()
        magic = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0

        # Use a try-except block to attempt to create an item
        try:
            # Assuming the item's class name is the same as the item's name in the text field
            item_class = getattr(Items, name)
            print(item_class)
            new_item = item_class(magic)
            print(new_item)
            # Add the new item to the player's inventory
            player.add_item_to_inventory(new_item)
            self.add_item_box.text = ""
            self.add_item_box.deselect()

        except AttributeError:
            print(f"No item found with the name '{name}'.")
        except Exception as e:
            print(f"An error occurred while creating the item: {e}")


class SpellPage:
    def __init__(self, surface: pygame.Surface, *args):
        self.font = pygame.font.Font(FONT, 16)  # Choose an appropriate font

        self.spacing = 20  # Vertical spacing between spells
        self.level_spacing = 30  # Additional spacing between spell levels
        self.start_y = 50  # Vertical start position for drawing
        self.start_x = 250
        self.current_x = self.start_x
        self.horizontal_spacing = 250

        self.scroll_min = 0  # Prevent scrolling above the top of the window
        self.scroll_max = -2000
        self.total_scroll = 0

    def draw(self, surface: pygame.Surface, player):
        self.draw_all_spells(surface, player)

        self.draw_sidebar(surface, player)

    def draw_all_spells(self, surface, player):
        for index, level in enumerate(sorted(player.char_class.spell_list.spells.keys())):
            y_offset = self.start_y
            # Draw the spell level header
            level_header = f"Level {level} Spells" if int(level) > 0 else "Cantrips"
            header_surface = self.font.render(level_header, True, (255, 255, 255))
            surface.blit(header_surface, (self.current_x + self.horizontal_spacing * index, self.start_y))
            y_offset += self.level_spacing  # Move down for the spells
            # Iterate over spells in the current level
            for spell in player.char_class.spell_list.spells[level]:
                is_selected = spell in player.char_class.prepared_spells or spell in player.char_class.prepared_cantrips
                self.draw_spell(surface, spell, self.current_x + self.horizontal_spacing * index, y_offset, is_selected)
                y_offset += self.spacing  # Move down for the next spell

    def draw_spell(self, surface, spell, x, y, is_selected):
        """Draw a single spell entry."""
        color = (0, 255, 0) if is_selected else (255, 255, 255)  # Green for selected, white otherwise
        text_surface = self.font.render(spell.name, True, color)
        surface.blit(text_surface, (x, y))  # Adjust positioning as needed

    def draw_sidebar(self, surface, player):
        """Draw the sidebar with the number of prepared spells."""
        sidebar_width = 220  # Set the width of the sidebar
        sidebar_rect = pygame.Rect(0, 40, sidebar_width, surface.get_height())
        pygame.draw.rect(surface, (50, 50, 50), sidebar_rect)  # Draw the sidebar background

        # Set up the initial vertical offset for text
        y_offset = 20+40
        # Draw the header for the sidebar
        header_surface = self.font.render("Prepared Spells", True, (255, 255, 255))
        surface.blit(header_surface, (10, y_offset))
        y_offset += header_surface.get_height() + 10

        # Display the number of prepared cantrips
        cantrips_text = f"Cantrips: {len(player.char_class.prepared_cantrips)}/{player.char_class.max_prepared_cantrips}"
        cantrips_surface = self.font.render(cantrips_text, True, (255, 255, 255))
        surface.blit(cantrips_surface, (10, y_offset))
        y_offset += cantrips_surface.get_height() + 5

        # Display the number of prepared leveled spells
        leveled_spells_text = f"Leveled Spells: {len(player.char_class.prepared_spells)}/{player.char_class.max_prepared_leveled_spells}"
        leveled_spells_surface = self.font.render(leveled_spells_text, True, (255, 255, 255))
        surface.blit(leveled_spells_surface, (10, y_offset))

        y_offset += leveled_spells_surface.get_height() + 30

        for level, slot in player.char_class.spell_slots.items():
            spell_slot_text = f"Level {level} Slots: {slot}"
            pell_slot_surface = self.font.render(spell_slot_text, True, (255, 255, 255))
            surface.blit(pell_slot_surface, (10, y_offset))
            y_offset += pell_slot_surface.get_height() + 5

    def handle_event(self, event, player):
        """Handle user input to toggle spells on and off."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Determine which spell, if any, was clicked
            click_pos = pygame.mouse.get_pos()
            click = self.get_clicked_spell(click_pos, player)
            if click:
                clicked_spell, level = click
                if level == '0':
                    self.handle_cantrip_selection(clicked_spell, player)
                else:
                    self.handle_leveled_spell_selection(clicked_spell, player)

        elif event.type == pygame.MOUSEWHEEL:
            # Calculate the scroll amount based on the mouse wheel event
            scroll_amount = event.y * 30
            # Update the total scroll amount
            self.total_scroll += scroll_amount

            self.current_x += scroll_amount
            if self.current_x > self.start_x:
                self.current_x = self.start_x
            elif self.current_x < self.scroll_max:
                self.current_x = self.scroll_max

    def get_clicked_spell(self, click_pos, player):
        """Determine which spell was clicked based on the mouse position."""
        y_offset = self.start_y
        for index, level in enumerate(sorted(player.char_class.spell_list.spells.keys())):
            # Account for the level header
            y_offset += self.level_spacing

            for spell in player.char_class.spell_list.spells[level]:
                # Calculate the bounding box for the current spell
                spell_height = self.font.get_linesize()  # Height of one line of text
                spell_rect = pygame.Rect(self.current_x + self.horizontal_spacing * index, y_offset, 100, spell_height)

                if spell_rect.collidepoint(click_pos):
                    return spell, level  # Return the clicked spell

                y_offset += self.spacing  # Move to the next spell position
            y_offset = self.start_y

        return None  # Return None if no spell was clicked

    @staticmethod
    def handle_cantrip_selection(spell, player):
        spell_list = player.char_class.prepared_cantrips
        """Handle selection of leveled spells."""
        if len(spell_list) < player.char_class.max_prepared_cantrips or spell in spell_list:
            player.char_class.update_prepared(spell, spell_list)

    @staticmethod
    def handle_leveled_spell_selection(spell, player):
        spell_list = player.char_class.prepared_spells
        """Handle selection of leveled spells."""
        if len(spell_list) < player.char_class.max_prepared_leveled_spells or spell in spell_list:
            player.char_class.update_prepared(spell, spell_list)


class TurnPage:
    def __init__(self, surface: pygame.Surface, *args):
        player = args[0]
        self.surface = surface

        self.spell_action_bar = ActionBar([], ((surface.get_width() - 10 * 64) / 2, surface.get_height() - 100),
                                          (64, 64))
        self.melee_action_bar = ActionBar([], ((surface.get_width() - 10 * 64) / 2,
                                               self.spell_action_bar.y - 100 + 64 * (
                                                           len(player.grouped_actions) / 10 - 1)), (64, 64))

    def draw(self, surface: pygame.Surface, player):
        # update the equiped items
        for equip in player.equipment.values():
            if not equip.id == 0:
                equip.update(player)

        # Draw spell action bar
        self.spell_action_bar.y_start = surface.get_height() - 100
        self.spell_action_bar.draw(surface, player.char_class.total_prepared)

        # Draw melee action bar
        self.melee_action_bar.y_start = self.spell_action_bar.y - 100
        self.melee_action_bar.draw(surface, player.grouped_actions)

        mouse_pos = pygame.mouse.get_pos()
        melee_item = self.melee_action_bar.get_item_at_pos(mouse_pos)
        if melee_item:
            self.melee_action_bar.draw_item_description(surface, melee_item, player, mouse_pos)

        spell_item = self.spell_action_bar.get_item_at_pos(mouse_pos)
        if spell_item:
            self.spell_action_bar.draw_item_description(surface, spell_item, player, mouse_pos)

    def handle_event(self, event, player):
        # self.melee_action_bar.handle_event(event, player)
        self.spell_action_bar.handle_event(event, player)
        self.melee_action_bar.handle_event(event, player)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                # Check for clicks on melee action bar
                melee_item = self.melee_action_bar.get_item_at_pos(event.pos)
                if melee_item:
                    self.handle_melee_action(melee_item, player)

                # Check for clicks on spell action bar
                spell_item = self.spell_action_bar.get_slot_at_pos(event.pos)
                if spell_item:
                    self.handle_spell_action(spell_item, player)
            elif self.melee_action_bar.enlarge_button.is_clicked(event.pos):
                if len(player.grouped_actions) <= 20:
                    player.grouped_actions.extend([Actions.Empty()]*10)
            elif self.melee_action_bar.shrink_button.is_clicked(event.pos):
                count = sum(1 for action in player.grouped_actions[-10:] if action.id == 0)
                if count == 10 and len(player.grouped_actions) > 10:
                    player.grouped_actions = player.grouped_actions[:-10]

            elif self.spell_action_bar.enlarge_button.is_clicked(event.pos):
                if len(player.char_class.total_prepared) <= 20:
                    player.char_class.expand_prepared()
            elif self.spell_action_bar.shrink_button.is_clicked(event.pos):
                player.char_class.compress_prepared()

    def handle_melee_action(self, melee_item, player):
        print(f"Melee action with {melee_item.name}")
        # TODO: Implement melee action logic

    def handle_spell_action(self, spell_item, player):
        pass  # print(f"Spell action with {spell_item.name} by {player.name}")
        # TODO: Implement spell action logic


class ChangePage:  # TODO: Finish ChangePage
    def __init__(self, surface: pygame.Surface, *args):
        player = args[0]

        self.font = pygame.font.Font(FONT, 16)

        titles_1 = ["Race & Subrace", "Class & Subclass", "Background"]
        self.output_var_1 = ["race", "char_class", "background"]
        self.class_list = [RACE_DICT, CHAR_CLASS_DICT, BACKGROUND_DICT]

        titles_2_1 = ["Level", "Max health", "Current health", "Temporary health"]
        self.output_var_2_1 = ["level", "max_health", "current_health", "temporary_health"]

        titles_2_2 = ["str", "dex", "int", 'wis', 'cha', 'con']
        self.output_var_2_2 = titles_2_2

        titles_4 = ['Armor', 'Weapons', 'Tools', 'Saving Throws']
        self.output_var_2_2 = titles_2_2

        self.input_boxes_1 = [
            TextField(20, 100 + 60 * i, 250, 32, self.font, title, text_shift=(5, 5), text=(str(text) if text else ''))
            for i, (title, text) in
            enumerate(zip(titles_1, [player.race.name, player.char_class.name, player.background.name]))]
        self.input_boxes_2_1 = [
            TextField(300, 100 + 60 * i, 100, 32, self.font, title, text_shift=(5, 5), text=str(text))
            for i, (title, text) in
            enumerate(
                zip(titles_2_1, [player.level, player.max_health, player.current_health, player.temporary_health]))]
        self.input_boxes_2_2 = [
            TextField(20 + 16 * 4 * j, 320 + 60 * i, 32, 32, self.font, titles_2_2[i + j * 3], text_shift=(5, 5),
                      text=str(list(player.ability_scores_none_mod.values())[i + 3 * j]))
            for j in range(2) for i in range(len(titles_2_2) // 2)]

        self.input_boxes_4 = [TextField(20, 550 + 60 * i, 700, 32, self.font, title, text_shift=(5, 5)) for i, title in
                              enumerate(titles_4)]

        self.ability_score_text = Text(self.font, "Abilityscores", (self.input_boxes_2_2[0].rect.topleft[0],
                                                   self.input_boxes_2_2[0].rect.topleft[1] - 40), (255, 255, 255))
        self.proficiency_text = Text(self.font, "Proficiencies",
                      (self.input_boxes_4[0].rect.topleft[0], self.input_boxes_4[0].rect.topleft[1] - 40),
                      (255, 255, 255))

        self.scroll_min = 0  # Prevent scrolling above the top of the window
        self.scroll_max = -270
        self.total_scroll = 0

    def text_box_output(self, player: Player):
        for index, box in enumerate(self.input_boxes_1):
            if box.output:
                output = box.output
                if any(output == c for c in self.class_list[index].keys()):
                    attr_name = self.output_var_1[index]
                    print(f'player.{attr_name}')

                    setattr(player, attr_name, self.class_list[index][output])
                    box.deselect()
                    print(getattr(player, attr_name, None))
                box.output = None

        for index, box in enumerate(self.input_boxes_2_1):
            if box.output:
                output = box.output.lower()
                attr_name = self.output_var_2_1[index]
                # Use setattr to dynamically set the attribute on self.active_class
                setattr(player, attr_name, int(output))
                box.deselect()
                print(getattr(player, attr_name, None))

        for index, box in enumerate(self.input_boxes_2_2):
            if box.output:
                output = box.output.lower()
                player.ability_scores_none_mod[self.output_var_2_2[index]] = int(output)
                player.ability_scores[self.output_var_2_2[index]] = int(output)
                # Use setattr to dynamically set the attribute on self.active_class
                box.deselect()

    def draw(self, surface: pygame.Surface, *args):
        player = args[0]

        for box in self.input_boxes_1:
            box.draw(surface)
        for box in self.input_boxes_2_1:
            box.draw(surface)

        self.ability_score_text.draw(surface)
        for box in self.input_boxes_2_2:
            box.draw(surface)

        self.proficiency_text.draw(surface)
        for box in self.input_boxes_4:
            box.rect.width = surface.get_width() - 50
            box.draw(surface)

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

            for text in [self.ability_score_text, self.proficiency_text]:
                text.rect.y += scroll_amount

        for box in self.input_boxes_1:
            box.handle_event(event)
        for box in self.input_boxes_2_1:
            box.handle_event(event)
        for box in self.input_boxes_2_2:
            box.handle_event(event)
        for box in self.input_boxes_4:
            box.handle_event(event)

        self.text_box_output(player)
