"""
Turing's Dungeon  —  CS 305 Theory of Computation Study Game
=====================================================================
A dungeon-crawler-style quiz game covering:
  DFA · NFA · ε-NFA · Regular Expressions · Pumping Theorem
  CFGs · Pushdown Automata · Turing Machines · UTM · P vs NP

HOW TO RUN LOCALLY (first time):
  1.  pip install pygame
  2.  python main.py

HOW TO SHARE WITH OTHERS (desktop):
  Give them the entire TuringsDungeon/ folder.
  They need Python 3.8+ and to run:
      pip install pygame
      python main.py

HOW TO BUILD FOR THE WEB (browser play, shareable link):
  1.  pip install pygbag
  2.  pygbag .
  3.  Open http://localhost:8000 in your browser to test
  4.  Upload the build/ folder to GitHub Pages, itch.io, or any web host
      (itch.io is easiest: drag-and-drop the build/web folder as a zip)

CONTROLS:
  Mouse       — click buttons and answer choices
  1 / A       — choose answer A
  2 / B       — choose answer B
  3 / C       — choose answer C
  4 / D       — choose answer D
  H           — use a hint (eliminates 2 wrong choices)
  S           — skip current question
  D           — toggle deep-dive explanation on feedback screen
  ESC         — pause game (not during active question)
"""

import sys
import asyncio
import pygame
from game import Game


SCREEN_W = 1200
SCREEN_H = 800
FPS      = 60
TITLE    = "Turing's Dungeon  —  CS 305 Study Game"


async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.SCALED)
    pygame.display.set_caption(TITLE)

    # Simple drawn icon
    icon = pygame.Surface((32, 32))
    icon.fill((10, 10, 22))
    pygame.draw.circle(icon, (220, 50, 50), (16, 12), 10)
    pygame.draw.line(icon, (220, 50, 50), (10, 22), (22, 28), 3)
    pygame.display.set_icon(icon)

    clock      = pygame.time.Clock()
    game       = Game(screen)
    fullscreen = False

    running = True
    while running:
        dt     = clock.tick(FPS)
        events = pygame.event.get()

        for ev in events:
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    from game import State
                    if game.state == State.TITLE:
                        running = False
                # F11 or Alt+Enter toggles fullscreen
                if ev.key == pygame.K_F11 or (
                        ev.key == pygame.K_RETURN and (ev.mod & pygame.KMOD_ALT)):
                    fullscreen = not fullscreen
                    flags = pygame.FULLSCREEN | pygame.SCALED if fullscreen else pygame.SCALED
                    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)
                    game.screen = screen
                    game.renderer.screen = screen
                    game.renderer._surf  = pygame.Surface((SCREEN_W, SCREEN_H))

        game.update(events, dt)
        game.render()
        pygame.display.flip()

        # Required by pygbag so the browser event loop can run
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
