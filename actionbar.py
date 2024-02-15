import pygame
from global_config import FONT


class ArrowButton:
    def __init__(self, x, y, width, height, direction, color):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = direction
        self.color = color  # Button color

        # Define the triangle for the arrow based on direction
        if self.direction == 'up':
            self.triangle = [
                (self.rect.centerx, self.rect.top + 10),
                (self.rect.left + 10, self.rect.bottom - 10),
                (self.rect.right - 10, self.rect.bottom - 10),
            ]
        elif self.direction == 'down':
            self.triangle = [
                (self.rect.centerx, self.rect.bottom - 10),
                (self.rect.left + 10, self.rect.top + 10),
                (self.rect.right - 10, self.rect.top + 10),
            ]

    def draw(self, surface):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.direction == 'up':
            self.triangle = [
                (self.rect.centerx, self.rect.top + 10),
                (self.rect.left + 10, self.rect.bottom - 10),
                (self.rect.right - 10, self.rect.bottom - 10),
            ]
        elif self.direction == 'down':
            self.triangle = [
                (self.rect.centerx, self.rect.bottom - 10),
                (self.rect.left + 10, self.rect.top + 10),
                (self.rect.right - 10, self.rect.top + 10),
            ]
        # Draw the arrow using the triangle points
        pygame.draw.polygon(surface, self.color, self.triangle)

    def is_clicked(self, mouse_pos):
        # Use the point_inside_triangle function to check if the click is within the arrow's triangle
        return self.point_inside_triangle(mouse_pos, self.triangle)

    def point_inside_triangle(self, pt, tri):
        """Check if a point (x, y) is inside a triangle represented by 3 points (x, y)."""

        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(pt, tri[0], tri[1]) < 0.0
        b2 = sign(pt, tri[1], tri[2]) < 0.0
        b3 = sign(pt, tri[2], tri[0]) < 0.0

        return (b1 == b2) and (b2 == b3)


class ActionBar:
    def __init__(self, items, pos, size):
        self.x, self.y = pos  # Tuple (x, y) position of the action bar
        self.y_start = self.y
        self.size = size  # Tuple (width, height) of the action bar slots

        self.items = items
        self.columns = 10
        self.rows = len(items)//10

        self.dragged_item = None
        self.dragged_index = None
        x = self.x + self.size[0]*10 + self.x/4  # 0x04AA6D
        self.enlarge_button = ArrowButton(x, self.y, 40, 40, 'up', 0x008CBA)
        self.shrink_button = ArrowButton(x, self.y+30, 40, 40, 'down', 0x008CBA)

    def draw(self, surface, items):
        self.items = items

        self.rows = len(items) // 10
        self.y = self.y_start - self.size[1] * (self.rows-1)

        self.enlarge_button.y = self.y + 64 * (len(items) // 10 - 1)
        self.shrink_button.y = self.y+30 + 64 * (len(items) // 10 - 1)
        self.enlarge_button.draw(surface)
        self.shrink_button.draw(surface)

        for index, item in enumerate(self.items):
            column = index % self.columns
            row = index // self.columns

            slot_x = self.x + column * self.size[0]
            slot_y = self.y + row * self.size[1]
            slot_rect = pygame.Rect(slot_x, slot_y, *self.size)

            pygame.draw.rect(surface, 0x353535, slot_rect)  # Draw slot background

            if item:  # If the item has an image, display it
                try:
                    if item.image:
                        image_surface = pygame.transform.scale(pygame.image.load(item.image).convert_alpha(), self.size)
                        surface.blit(image_surface, slot_rect.topleft)
                    else:
                        image = 'images/Unknown.png'
                        image_surface = pygame.transform.scale(pygame.image.load(image).convert_alpha(), self.size)
                        surface.blit(image_surface, slot_rect.topleft)
                except:
                    image = 'images/Unknown.png'
                    image_surface = pygame.transform.scale(pygame.image.load(image).convert_alpha(), self.size)
                    surface.blit(image_surface, slot_rect.topleft)

        self.draw_grid(surface)

    def draw_grid(self, surface):
        # Vertical lines
        for col in range(self.columns + 1):
            start_pos = (self.x + col * self.size[0], self.y)
            end_pos = (start_pos[0], self.y + self.rows * self.size[1])
            pygame.draw.line(surface, (200, 200, 200), start_pos, end_pos, 1)

        # Horizontal lines
        for row in range(self.rows + 1):
            start_pos = (self.x, self.y + row * self.size[1])
            end_pos = (self.x + self.columns * self.size[0], start_pos[1])
            pygame.draw.line(surface, (200, 200, 200), start_pos, end_pos, 1)

    def get_slot_at_pos(self, pos):
        for index, item in enumerate(self.items):
            column = index % self.columns
            row = index // self.columns
            if row >= self.rows:  # Ignore slots that exceed the specified rows
                continue
            item_rect = pygame.Rect(
                (self.x + column * self.size[0], self.y + row * self.size[1]),
                self.size
            )
            if item_rect.collidepoint(pos):
                return index
        return None

    def get_item_at_pos(self, pos):
        index = self.get_slot_at_pos(pos)
        if index is not None:
            return self.items[index]
        return None

    def draw_item_description(self, surface, item, player, position):
        """Draw a description box for the given item at the specified position."""
        if item:
            lines = [
                item.name,
            ]
            if hasattr(item, 'action_description'):
                for line in item.action_description(player.level):
                    lines.append(line)
            else:
                lines.append('No description available.')

            font = pygame.font.Font(FONT, 12)
            line_height = font.get_linesize()
            tooltip_width = max(font.size(line)[0] for line in lines)+10
            tooltip_height = line_height * len(lines)

            # Create a background for the tooltip
            tooltip_background = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
            tooltip_background.fill((0, 0, 0, 220))  # Semi-transparent background

            # Render each line of text and blit onto the tooltip background
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, pygame.Color('white'))
                tooltip_background.blit(text_surface, (5, i * line_height))

                # Initially position the tooltip to the right of the mouse
            tooltip_x = position[0] + 20
            tooltip_y = position[1]

            # Check if the tooltip goes beyond the right edge of the surface
            if tooltip_x + tooltip_width > surface.get_width():
                # Reposition tooltip to the left of the mouse if it overflows
                tooltip_x = position[0] - tooltip_width - 10

            # Ensure the tooltip does not go off the top or bottom of the screen
            if tooltip_y < 0:
                tooltip_y = 0
            elif tooltip_y + tooltip_height > surface.get_height():
                tooltip_y = surface.get_height() - tooltip_height

            # Blit the tooltip background onto the main surface at the adjusted position
            surface.blit(tooltip_background, (tooltip_x, tooltip_y))

    def handle_event(self, event, player):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_index = self.get_slot_at_pos(pygame.mouse.get_pos())
            if clicked_index is not None:
                self.dragged_item = self.items[clicked_index]
                self.dragged_index = clicked_index

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragged_item:
                dropped_index = self.get_slot_at_pos(pygame.mouse.get_pos())
                if dropped_index is not None and dropped_index != self.dragged_index:
                    # Swap items within the grid
                    self.items[self.dragged_index], self.items[dropped_index] = self.items[
                        dropped_index], self.dragged_item
                self.dragged_item = None
                self.dragged_index = None
