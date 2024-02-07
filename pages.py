import pygame
from races import *
from classes import *
from background import *
from textfield import *
from player import Player


class MainPage:
    def __init__(self, surface: pygame.Surface, *args):
        self.font = pygame.font.SysFont(None, 24)
        self.level_text = Text(self.font, "level: 0", (20, 50), (255, 255, 255))
        self.race_text = Text(self.font, "None", (20, 100), (255, 255, 255))
        self.class_text = Text(self.font, "None", (20, 150), (255, 255, 255))
        self.background_text = Text(self.font, "None", (20, 200), (255, 255, 255))
        self.max_health = Text(self.font, "None", (20, 400), (255, 255, 255))
        self.cur_health = Text(self.font, "None", (20, 450), (255, 255, 255))

        self.score = [Text(self.font, "?", (400, 150+50*index), (255, 255, 255))
                      for index in range(len(args[0].abilityscores))]

    def draw(self, surface: pygame.Surface, *args):
        self.level_text.text = 'Level: ' + str(args[0].level)
        self.level_text.draw(surface)
        self.race_text.text = 'Race: ' + str(args[0].race.name)
        self.race_text.draw(surface)
        self.class_text.text = 'Class: ' + str(args[0].char_class.name)
        self.class_text.draw(surface)
        self.background_text.text = 'Background: ' + str(args[0].background.name)
        self.background_text.draw(surface)
        self.max_health.text = 'Max health: ' + str(args[0].max_health)
        self.max_health.draw(surface)
        self.cur_health.text = 'Current health: ' + str(args[0].current_health)
        self.cur_health.draw(surface)

        for index, (score_name, val) in enumerate(args[0].abilityscores.items()):
            self.score[index].text = f"{score_name}: {val}"

        for i in self.score:
            i.draw(surface)

    def handle_event(self, event):
        pass


class InvPage:
    def __init__(self, surface: pygame.Surface, *args):
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
    def __init__(self, surface: pygame.Surface, *args):
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
    def __init__(self, surface: pygame.Surface, *args):
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
                box.output = None

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
