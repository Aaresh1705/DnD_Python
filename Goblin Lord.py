import pygame
pygame.init()
import numpy as np
import sys
from icecream import ic
from pages import MainPage, InvPage, TurnPage, ChangePage
from collections import defaultdict 
from player import Player


def main():
    print("---============================---")
    character_file = input(
        "Input the file where you have saved your character,"
        "\nif you have not saved character yet then just press enter:")

    save_file = character_file
    if not character_file:
        print("---======---")
        while not save_file:
            save_file = input("Input the file location where you want to save your character:")
            if save_file:
                break
            print("Invalid input")

    surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Goblin Lord")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    player = Player()
    if character_file:
        player = player.load(character_file)

    space = 150
    bars = defaultdict(lambda: [pygame.Rect(0, 0, 0, 0), None]) 

    bars['main_bar'] = [pygame.Rect(5, 5, 100, 30), MainPage(surface, player)]
    bars['inv_bar'] = [pygame.Rect(5+space, 5, 100, 30), InvPage(surface, player)]
    bars['turn_bar'] = [pygame.Rect(5+space*2, 5, 100, 30), TurnPage(surface, player)]
    bars['change_bar'] = [pygame.Rect(5+space*3, 5, 100, 30), ChangePage(surface, player)]

    active_bar = 'main_bar'
    page = bars['main_bar'][1]

    def draw_bars():
        top_bar = pygame.Rect(0, 0, surface.get_width(), 40)
        pygame.draw.rect(surface, 0x262626, top_bar)

        for bar_name, (rect, page_) in bars.items():
            bar_color = 0x669766 if bar_name == active_bar else 0x353535
            pygame.draw.rect(surface, bar_color, rect, border_radius=10)

            text_surf = font.render(bar_name[:-4], True, (255, 255, 255)) 

            text_rect = text_surf.get_rect(center=rect.center)

            surface.blit(text_surf, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_q:
                    player.save(save_file)

                """if event.key == pygame.K_q:
                    player.update()
                    player.level += 1"""

            if event.type == pygame.VIDEORESIZE:
                old_surface_saved = surface
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                surface.blit(old_surface_saved, (0, 0))
                del old_surface_saved
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for bar_name, (rect, page_) in bars.items():
                        if rect.collidepoint(event.pos):
                            active_bar = bar_name
                            page = page_
                            
                            break

            page.handle_event(event, player)
                            
        surface.fill(0x1F1F1F)

        page.draw(surface, player)

        player.update()

        draw_bars()
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
