import pygame
import sys
import asyncio

pygame.init()

from global_config import *
from pages import MainPage, InvPage, SpellPage, TurnPage, ChangePage
from playerscripts.player import Player


from js import window
from js import window
from js import eval as js_eval
import json


async def main():
    browser_width = window.innerWidth
    browser_height = window.innerHeight
    screen = pygame.display.set_mode((browser_width, browser_height), 0)

    pygame.display.set_caption("Goblin Lord")

    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT, 16)

    player = Player()

    space = 150
    bars = {
        'main_bar': [pygame.Rect(5, 5, 100, 30), MainPage(screen, player)],
        'inv_bar': [pygame.Rect(5 + space, 5, 100, 30), InvPage(screen, player)],
        'spell_bar': [pygame.Rect(5 + space * 2, 5, 100, 30), SpellPage(screen, player)],
        'turn_bar': [pygame.Rect(5 + space * 3, 5, 100, 30), TurnPage(screen, player)],
        'change_bar': [pygame.Rect(5 + space * 4, 5, 100, 30), ChangePage(screen, player)]
    }

    active_bar = 'main_bar'
    page = bars[active_bar][1]

    def draw_bars():
        top_bar = pygame.Rect(0, 0, screen.get_width(), 40)
        pygame.draw.rect(screen, 0x262626, top_bar)

        for bar_name, (rect, page_) in bars.items():
            bar_color = 0x669766 if bar_name == active_bar else 0x353535
            pygame.draw.rect(screen, bar_color, rect, border_radius=10)

            text_surf = font.render(bar_name[:-4], True, (255, 255, 255))

            text_rect = text_surf.get_rect(center=rect.center)

            screen.blit(text_surf, text_rect)

    def handle_uploaded_file(file_content):
        window.console.log(player.level)
        player.load(file_content)
        window.console.log(file_content)
        window.console.log(player.level)

    window.console.log("This is a log message from Python!")

    window.handle_uploaded_file = handle_uploaded_file

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_1:
                    js_eval(f'saveTextAsFile({json.dumps(player.save())}, {json.dumps(f"{player.name}.txt")})')

                if event.key == pygame.K_2:
                    window.promptFileUpload()

            if event.type == pygame.VIDEORESIZE:
                old_surface_saved = screen
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                screen.blit(old_surface_saved, (0, 0))
                del old_surface_saved

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for bar_name, (rect, page_) in bars.items():
                        if rect.collidepoint(event.pos):
                            active_bar = bar_name
                            page = page_

                            break

            page.handle_event(event, player)

        screen.fill(0x1F1F1F)

        player.update()

        page.draw(screen, player)

        draw_bars()

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
