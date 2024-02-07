import pygame
from races import *
from classes import *
from background import *
from textfield import *
from player import Player


class MainPage:
    def __init__(self, surface: pygame.Surface):
        a, b = surface.get_width(), surface.get_height()
        self.x = pygame.Rect(a-100, b-100, 100, 100)

    def draw(self, surface: pygame.Surface, *args):
        a, b = surface.get_width(), surface.get_height()
        self.x = pygame.Rect(a-100, b-100, 100, 100)

        pygame.draw.rect(surface, 0xFF0000, self.x)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x.collidepoint(event.pos):
                print(event.pos)


class InvPage:
    def __init__(self, surface: pygame.Surface):
        a, b = surface.get_width(), surface.get_height()
        self.x = pygame.Rect(a-100, b-100, 100, 100)

    def draw(self, surface: pygame.Surface, *args):
        a, b = surface.get_width(), surface.get_height()
        self.x = pygame.Rect(a-100, b-100, 100, 100)

        pygame.draw.rect(surface, 0x00FF00, self.x)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x.collidepoint(event.pos):
                print(event.pos)


class TurnPage:
    def __init__(self, surface: pygame.Surface):
        a, b = surface.get_width(), surface.get_height()
        self.x = pygame.Rect(a-100, b-100, 100, 100)

    def draw(self, surface: pygame.Surface, *args):
        a, b = surface.get_width(), surface.get_height()
        self.x = pygame.Rect(a-100, b-100, 100, 100)

        pygame.draw.rect(surface, 0x0000FF, self.x)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x.collidepoint(event.pos):
                print(event.pos)


class ChangePage:
    def __init__(self, surface: pygame.Surface):
        self.font = pygame.font.SysFont(None, 24)
        titles_1 = ["race & subrace", "class & subclass", "background"]
        self.output_var_1 = ["race", "char_class", "background"]
        self.class_list = [RACES, CLASSES, BACKGROUNDS]

        titles_2_1 = ["level", "health", "abilityscores"]
        self.output_var_2_1 = ["level", "max_health", "abilityscores"]

        titles_2_2 = ["str", "dex", "int", 'wis', 'cha', 'con']
        self.output_var_2_2 = titles_2_2

        titles_3 = ["Age", "Weight"]
        self.output_var_3 = ["age", "weight"]

        self.input_boxes_1 = [TextField(20, 100 + 60*i, 140, 32, self.font, titles_1[i])
                              for i in range(len(titles_1))]
        self.input_boxes_2_1 = [TextField(200, 100 + 60*i, 140, 32, self.font, titles_2_1[i])
                                for i in range(len(titles_2_1))]
        self.input_boxes_2_2 = [TextField(20 + 180*j, 320 + 60*i, 140, 32, self.font, titles_2_2[i+j*3])
                                for j in range(2) for i in range(int(len(titles_2_2)/2))]
        self.input_boxes_3 = [TextField(380, 100 + 60*i, 140, 32, self.font, titles_3[i])
                              for i in range(len(titles_3))]

        self.x = Text(self.font, "Abilityscores", (self.input_boxes_2_2[0].rect.topleft[0],
                                                   self.input_boxes_2_2[0].rect.topleft[1]-40), (255, 255, 255))

    def text_box_output(self, player: Player):
        for index, box in enumerate(self.input_boxes_1):
            if box.output:
                if any(box.output == c for c in self.class_list[index]):
                    attr_name = self.output_var_1[index]
                    print(f'player.{attr_name}')

                    setattr(player, attr_name, self.class_list[index][box.output])
                    box.deselect()
                    print(getattr(player, attr_name, None))

        for index, box in enumerate(self.input_boxes_2_1):
            if box.output:
                attr_name = self.output_var_2_1[index]
                # Use setattr to dynamically set the attribute on self.active_class
                setattr(player, attr_name, box.output)
                box.deselect()
                print(getattr(player, attr_name, None))

        for index, box in enumerate(self.input_boxes_2_2):
            if box.output:
                player.abilityscores[self.output_var_2_2[index]] = box.output
                # Use setattr to dynamically set the attribute on self.active_class
                box.deselect()

    def draw(self, surface: pygame.Surface, *args):
        player = args[0]
        self.text_box_output(player)

        for box in self.input_boxes_1:
            box.draw(surface)
        for box in self.input_boxes_2_1:
            box.draw(surface)
        for box in self.input_boxes_2_2:
            box.draw(surface)

        if player.race:
            for box in self.input_boxes_3:
                box.draw(surface)

        self.x.draw(surface)

    def handle_event(self, event):
        for box in self.input_boxes_1:
            box.handle_event(event)
        for box in self.input_boxes_2_1:
            box.handle_event(event)
        for box in self.input_boxes_2_2:
            box.handle_event(event)
