# Initial setup: Import dependencies
# - Standard library imports for basic functionality and compatibility checks.
# - Local application/library specific imports for game configuration and pages.
import asyncio
import json
import sys

from global_config import *
from pages import MainPage, InvPage, SpellPage, TurnPage, ChangePage
from playerscripts.player import Player

# Environment check and configuration
# - Determine the execution environment (web or local) to adapt game settings accordingly.
# - If running in a web environment, import JavaScript interop modules for file handling.
web = False
if sys.platform == "emscripten":
    web = True
    from js import window, eval as js_eval
    window.console.log(2)


# Main game function
# - Handles the setup and main loop of the game, adjusting display settings based on environment.
# - Initializes game window, clock, font, player, and navigation bars.
# - Defines function for drawing navigation bars and handling file uploads (web only).
async def main():
    # Screen setup: Adjust window size for web or default settings.
    # Game initialization: Set window title, initialize clock for frame timing, and create font object for text rendering.
    # Player and UI setup: Instantiate the player and setup UI elements like navigation bars.
    scale = 1.5
    if web:
        web_width = window.innerWidth
        web_height = window.innerHeight
        screen = pygame.display.set_mode((web_width, web_height), 0)
    else:
        width = 1280
        height = 720
        screen = pygame.display.set_mode((width, height), pygame.SCALED)

    pygame.display.set_caption("Goblin Lord")

    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT, 16)

    player = Player()

    space = 150
    bars = {                   # x, y,   w,  h
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
        # window.console.log(player.level)
        player.load(file_content)

    if web:
        window.handle_uploaded_file = handle_uploaded_file

    # Main loop: Handles game events, updates, and rendering.
    # - Event handling: Quit, keyboard inputs, and mouse interactions.
    # - Game state updates: Player and current page updates.
    # - Rendering: Clear screen, draw current page and navigation bars, update display.
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
                    if web:
                        js_eval(f'saveTextAsFile({json.dumps(player.save())}, {json.dumps(f"{player.name}.txt")})')

                if event.key == pygame.K_2:
                    if web:
                        window.promptFileUpload()

            # if event.type == pygame.VIDEORESIZE:
            #     old_surface_saved = screen
            #     screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            #     screen.blit(old_surface_saved, (0, 0))
            #     del old_surface_saved

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

        pygame.display.update()
        clock.tick(60)

        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
