#Public library imports
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
pg.init()

#Own library imports
import globals as g
import inputs
import world
import hud
from player import show
from scenes import open_trade, start_screen

# Trade-Callback verdrahten (verhindert Import-Zyklus world <-> scenes)
world.tradeplanet.geg_fkt = open_trade

# temp meteors zum testen
world.spawn_test_meteors()


def play_game() -> None:
    while g.playing:
    #Logik: alles bewegen + Kollisionen ---
        inputs.input()                # inputs verarbeiten | move()/shoot()
        world.move_objects()          # meteore/gegner bewegen
        world.move_bullets()          # bullets bewegen
        world.handle_bullet_hits()    # bullet-meteor treffer + aufräumen
        world.update_enemies()        # gegner-schüsse + planeten-kontakt

    #Zeichnen: konsistenter Snapshot des Weltzustands ---
        world.draw_background()
        world.draw_objects() 
        world.draw_bullets()          # meteore/gegner + planeten
        show()                        # spieler
        world.draw_arrow()            # shop-pfeil (falls aktiv)
        hud.draw_hud()                # leben- + cooldown-balken

        pg.display.update()
        g.clock.tick(60)              # 60 fps

        if g.debug:
            print(g.clock.get_rawtime(), "ms/tick & meteors:", len(g.objects), "player bullets:", len(g.player_bullets))


def main():
    start_screen()
    play_game()
    pg.quit()


if __name__ == "__main__":
    main()
