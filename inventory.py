import numpy as np
import pygame
pygame.init()
from global_config import FONT, get_image
from dictionarys.items import Items


def to_grayscale_optimized(surface):
    # Use pygame.surfarray to get a pixel array of the surface
    original_array = pygame.surfarray.array3d(surface)
    # Calculate the weighted sum of the RGB values
    array = np.sum(original_array[..., :3], axis=2)/3
    # The result must be converted to an 8-bit integer array
    gray_array = array.astype(np.uint8)
    # Stack the grayscale values into an RGB representation
    del original_array

    gray_surface = pygame.surfarray.make_surface(np.dstack((gray_array, gray_array, gray_array)))
    return gray_surface


class Inventory:
    def __init__(self, surface, width, height, start_x, start_y):
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y

        self.slot_size = (64, 64)
        self.columns = width // 64
        self.rows = height // 64

        self.background_color = 0x353535
        self.font = pygame.font.Font(FONT, 16)

        self.search_query = ""

        # self.selected_item_index = None
        self.dragging_start_pos = None
        self.dragging = False

    def draw(self, surface, player):
        """Draw the inventory grid and items."""
        inv_background = pygame.Surface((self.width, self.height))
        inv_background.fill(self.background_color)
        surface.blit(inv_background, (self.start_x, self.start_y))

        line_color = (200, 200, 200)
        # Draw the items and highlight the selected item
        for row in range(self.rows):
            # Horizontal lines
            pygame.draw.line(
                surface,
                line_color,
                (self.start_x, self.start_y + row * self.slot_size[1]),
                (self.start_x + self.width, self.start_y + row * self.slot_size[1])
            )
            for col in range(self.columns):
                # Vertical lines
                pygame.draw.line(
                    surface,
                    line_color,
                    (self.start_x + col * self.slot_size[0], self.start_y),
                    (self.start_x + col * self.slot_size[0], self.start_y + self.height)
                )
                # Get the item at the current index
                item = player.inventory[row][col]
                if item:  # If there's an item at this slot, draw it
                    self.draw_item(surface, item, row, col)

        self.highlight_selected(surface)

        mouse_pos = pygame.mouse.get_pos()
        slot = self.get_slot_at_mouse(mouse_pos)
        if slot[0] is not None and player.inventory[slot[0]][slot[1]]:
            row, col = slot
            item = player.inventory[row][col]
            if not item.id == 0:
                self.draw_description(surface, item, (mouse_pos[0] + 20, mouse_pos[1] + 20))

    def draw_item(self, surface, item, row, col):
        """Draw a single item in the inventory."""
        item_x = self.start_x + col * self.slot_size[0]
        item_y = self.start_y + row * self.slot_size[1]

        image = get_image(item.image)

        surface.blit(image, (item_x, item_y))
        if item.quantity:
            self.draw_quantity(surface, item, item_x, item_y)

    def draw_quantity(self, surface, item, x, y):
        """Draw the quantity of the item."""
        count_surf = self.font.render(str(item.quantity), True, pygame.Color('white'))
        surface.blit(count_surf, (x + self.slot_size[0] - count_surf.get_width() - 3,
                                  y + self.slot_size[1] - count_surf.get_height() - 3))

    def highlight_selected(self, surface):
        """Highlight the selected item slot."""
        pos = pygame.mouse.get_pos()
        slot = self.get_slot_at_mouse(pos)

        if (slot[0] or slot[1]) is not None:
            highlight_rect = pygame.Rect(self.start_x + slot[1] * self.slot_size[0],
                                         self.start_y + slot[0] * self.slot_size[1],
                                         *self.slot_size)
            pygame.draw.rect(surface, (150, 150, 0), highlight_rect, 3)

    def draw_description(self, surface, item, position):
        """Draw the item description box."""
        # Determine box size based on content
        box_width = max(self.font.size(line)[0] for line in item.info) + 20
        box_height = len(item.info) * self.font.get_linesize() + 10

        # Adjust position to ensure the box doesn't go off-screen
        if position[0] + box_width > surface.get_width():
            position = (position[0] - box_width, position[1])
        if position[1] + box_height > surface.get_height():
            position = (position[0], position[1] - box_height)

        # Draw the background box
        description_surface = pygame.Surface((box_width, box_height)).convert_alpha()
        description_surface.fill((0, 0, 0, 128))

        # Draw the text
        for i, line in enumerate(item.info):
            text_surface = self.font.render(line, True, pygame.Color('white'))
            description_surface.blit(text_surface, (10, 5 + i * self.font.get_linesize()))

        # Blit the semi-transparent surface onto the main surface
        surface.blit(description_surface, position)

    def handle_event(self, event, player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.search_query = self.search_query[:-1]
            else:
                self.search_query += event.unicode  # Add the character to the search query
            #self.search_items()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Start dragging
            slot = self.get_slot_at_mouse(pygame.mouse.get_pos())
            if slot[0] is not None:
                self.start_dragging(player, *slot)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            row, col = self.get_slot_at_mouse(pygame.mouse.get_pos())
            if row is not None and self.dragging:
                player.swap_items(self.dragging_start_pos[0], self.dragging_start_pos[1], row, col)
            elif self.dragging:
                player.add_item_to_inventory(player.dragging_item, *self.dragging_start_pos)

            self.end_dragging(player)

    def get_slot_at_mouse(self, mouse_pos):
        # Calculate the column and row indices based on the mouse position
        column = (mouse_pos[0] - self.start_x) // self.slot_size[0]
        row = (mouse_pos[1] - self.start_y) // self.slot_size[1]
        # Check if the indices are within the bounds of the inventory
        if 0 <= column < 5 and 0 <= row < 8:
            return row, column
        return None, None

    def start_dragging(self, player, row, col):
        """Start dragging an item from a specific row and col."""
        player.dragging_item = player.remove_item_from_inventory(row, col)
        self.dragging_start_pos = (row, col)
        self.dragging = True

    def end_dragging(self, player):
        # Reset dragging state
        player.dragging_item = None
        self.dragging_start_pos = None
        self.dragging = False

    # def search_items(self):
    #     if self.search_query == "":
    #         self.display_items = self.items
    #     else:
    #         self.display_items = [item for item in self.items if self.search_query.lower() in item.item.name.lower()]
    #
    # def sort_items(self, key=None, reverse=False):
    #     self.items.sort(key=key, reverse=reverse)
    #     self.search_items()  # Reapply search filter after sorting


class EquipmentSlot:
    def __init__(self, slot_name, slot_type, image_path):
        self.slot_name = slot_name
        self.slot_type = slot_type
        self.slot_size = (64, 64)
        self.slot_image = get_image(image_path)
        self.slot_image_selected = get_image(image_path[:-4] + '_gray' + image_path[-4:])
        self.item = Items.Empty()  # No item equipped initially
        self.dragging = False
        self.locked = False

    def set_position(self, position):
        """Set the position of the slot and update the slot_rect."""
        self.position = position
        self.slot_rect = pygame.Rect(position, (64, 64))

    def is_hovered(self, mouse_pos):
        if self.slot_rect and self.slot_rect.collidepoint(mouse_pos):
            return True
        return False

    def is_two_handed_equipped(self):
        if self.item:
            if 'Versatile' in self.item.properties:
                return True if self.item.properties['Versatile'] == 'two-hand' else False

    def start_dragging(self, player):
        player.dragging_item = self.item
        player.equipment[self.slot_name] = Items.Empty()
        self.dragging = True

    def stop_dragging(self, player):
        player.equipment[self.slot_name] = player.dragging_item
        self.item = player.dragging_item
        player.dragging_item = False
        self.dragging = False

    def update(self, player):
        self.item = player.equipment[self.slot_name]

    def draw(self, surface, position, player, equipment_dict=None):
        self.item = player.equipment[self.slot_name]

        if 'staff' in self.slot_type:
            opposite = 'meleeOffHand' if self.slot_name == 'meleeMainHand' else 'meleeMainHand'
            if self.is_two_handed_equipped():
                equipment_dict[opposite].locked = True
                opposite_slot = player.equipment[opposite]

                if opposite_slot:
                    # Move offhand item to inventory
                    player.add_item_to_inventory(opposite_slot)
                    player.equipment[opposite] = Items.Empty()
            else:
                equipment_dict[opposite].locked = False

        if self.item:
            item_image = get_image(self.item.image)

        # Draw the slot
        self.set_position(position)

        if self.locked:
            surface.blit(self.slot_image_selected, position)

        elif self.item.id == 0:
            surface.blit(self.slot_image, position)
        else:
            surface.blit(self.slot_image_selected, position)
            surface.blit(item_image, position)

    def handle_event(self, event, player):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = event.pos
                if not self.item.id == 0 and self.is_hovered(pos):
                    self.start_dragging(player)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.stop_dragging(player)
                return event.pos
