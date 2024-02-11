import pygame
from items import InventoryItem


class Inventory:
    def __init__(self, surface, width, height, start_x=0, start_y=0):
        self.items = []
        self.display_items = []  # Items to display after sorting/searching
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.slot_size = (64, 64)
        self.columns = width // 64
        self.rows = height // 64
        self.background_color = 0x353535
        self.font = pygame.font.Font(None, 24)
        self.search_query = ""

    def add_item(self, item):
        self.items.append(item)
        self.display_items.append(item)  # Add the item to the display list as well

    def draw(self, surface: pygame.surface.Surface):
        # Draw the inventory background with an offset
        inv_background = pygame.Surface((self.width, self.height))
        inv_background.fill(self.background_color)
        surface.blit(inv_background, (self.start_x, self.start_y))

        # Draw the items with an offset
        padding = 0  # Padding between items
        for index, item in enumerate(self.display_items):
            column = index % self.columns
            row = index // self.columns

            item_x = self.start_x + padding + column * (self.slot_size[0] + padding)
            item_y = self.start_y + padding + row * (self.slot_size[1] + padding)

            # Scale the image down to fit the slot size
            scaled_image = pygame.transform.scale(item.image, self.slot_size)

            surface.blit(scaled_image, (item_x, item_y))
            count_surf = self.font.render(str(item.quantity), True, pygame.Color('white'))
            surface.blit(count_surf, (item_x + self.slot_size[0] - count_surf.get_width() - 3,
                                      item_y + self.slot_size[1] - count_surf.get_height() - 3))

        for i in range(self.columns + 1):
            pygame.draw.line(surface, 0x000000, (self.start_x + 64 * i, self.start_y),
                             (self.start_x + 64 * i, self.height + self.start_y))
        for i in range(self.rows + 1):
            pygame.draw.line(surface, 0x000000, (self.start_x, self.start_y + 64*i),
                             (self.width + self.start_x, self.start_y + 64*i))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.search_query = self.search_query[:-1]
            else:
                self.search_query += event.unicode  # Add the character to the search query
            self.search_items()

    def get_item_under_mouse(self, mouse_pos):
        """Return the item under the mouse cursor, if any."""
        padding = 0  # Assuming padding is defined here
        for index, item in enumerate(self.display_items):
            column = index % self.columns
            row = index // self.columns
            item_x = self.start_x + padding + column * (self.slot_size[0] + padding)
            item_y = self.start_y + padding + row * (self.slot_size[1] + padding)
            item_rect = pygame.Rect(item_x, item_y, *self.slot_size)
            if item_rect.collidepoint(mouse_pos):
                return item
        return None

    def search_items(self):
        if self.search_query == "":
            self.display_items = self.items
        else:
            self.display_items = [item for item in self.items if self.search_query.lower() in item.item.name.lower()]

    def sort_items(self, key=None, reverse=False):
        self.items.sort(key=key, reverse=reverse)
        self.search_items()  # Reapply search filter after sorting
