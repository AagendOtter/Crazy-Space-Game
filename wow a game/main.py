#Public library imports
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
pg.init()

#Own library imports
import globals as g
import inputs
import objects
from scenes import open_trade
from player import show, summon_meteor

screen = g.screen
Bg = objects.Background(os.path.join(g.img_path,"back_space.jpeg"))

#temp meteors zum testen
summon_meteor(speed=1)
summon_meteor()

tradeplanet = objects.Planet("Trade Planet", [0, 0], pg.image.load(os.path.join(g.img_path,"trade_planet.png")).convert_alpha(), 250, open_trade)
g.planets.append(tradeplanet)

arrow = objects.Pointer(tradeplanet, pg.transform.scale(pg.transform.rotate(pg.image.load(os.path.join(g.img_path,"arrow.png")).convert_alpha(), 0), (50, 50))) # type: ignore

def start_screen():
    Bg.render()
    start = True

    font = pg.font.SysFont("Consolas", 92, bold=True)
    sec_font = pg.font.SysFont("Consolas", 40, bold=True)
    crazy = font.render("Crazy", True, (255, 255, 255))
    space= font.render("Space", True, (255, 255, 255))
    game = font.render("Game", True, (255, 255, 255))
    sec_text = sec_font.render("Press Enter to Start", True, (135, 206, 235))
    crazy_rect = crazy.get_rect(center=(g.middle_x, g.middle_y - 80))
    space_rect = space.get_rect(center=(g.middle_x, g.middle_y))
    game_rect = game.get_rect(center=(g.middle_x, g.middle_y + 80))
    sec_text_rect = sec_text.get_rect(center=(g.middle_x, g.middle_y + 160))

    screen.blit(crazy, crazy_rect)
    screen.blit(space, space_rect)
    screen.blit(game, game_rect)
    screen.blit(sec_text, sec_text_rect)

    pg.display.update()
    
    while start:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                start = False
                g.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    start = False

        g.clock.tick(60)

def pause_screen():
    font = pg.font.SysFont("Consolas", 72, bold=True)
    sec_font = pg.font.SysFont("Consolas", 40, bold=True)
    pause_text = font.render("Paused", True, (255, 255, 255))
    sec_text = sec_font.render("Press Esc to Resume", True, (135, 206, 235))
    pause_rect = pause_text.get_rect(center=(g.middle_x, g.middle_y - 30))
    sec_text_rect = sec_text.get_rect(center=(g.middle_x, g.middle_y + 30))

    screen.blit(pause_text, pause_rect)
    screen.blit(sec_text, sec_text_rect)
    pg.display.update()

    paused = True
    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                paused = False
                g.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = False
        g.clock.tick(60)

def play_game() -> None:
    while g.playing:
        inputs.input() #inputs werden in der inputs.py verarbeitet | move() wird auseführt

        #hintergrung zeichnen
        Bg.render()
        #Bg.border() #nur zum testen, zeigt die grenzen des hintergrunds an

        #meteoren & gegner & projektile bewegen und zeichnen
        blit_batch = []
        for obj in g.objects:
            obj.move()
            blit_batch.append(obj.draw_data())

        for planet in g.planets:
            blit_batch.append(planet.draw_data())

        screen.blits(blit_batch)
        
        if g.debug:
            debug_batch = [obj.debug_data() for obj in g.objects]
            screen.blits(debug_batch)
                
        
        show() #player
        # hitbox des spielers visual
        if g.debug:
            pg.draw.circle(screen, (0, 255, 0), (g.middle_x, g.middle_y), g.player_hitbox_radius, 1)

        bullet_batch = []
        for bullet in g.player_bullets:
            if not bullet.move():
                bullet_batch.append(bullet.draw_data())
        screen.blits(bullet_batch)

        # Bullet-Meteor Kollisionserkennung
        meteors_to_remove = []
        for bullet in g.player_bullets:  # Erstellt Kopie und geht durch alle Bullets
            if not bullet.alive:
                continue
            for meteor in g.objects:  # Erstellt Kopie und geht durch alle Meteore
                if bullet.collides_with(meteor):
                    if g.debug: # Zum Debuggen die Infos ausgeben
                        print(f"TREFFER! Bullet trifft {meteor.name}! Damage: {bullet.damage}, Meteor Health: {meteor.health - bullet.damage}")
                    meteor.health -= bullet.damage
                    bullet.alive = False
                    
                    # Wenn Meteorit tot, zum Entfernen markieren
                    if meteor.health <= 0:
                        meteors_to_remove.append(meteor)
                        if g.debug:
                            print(f"{meteor.name} ist zerstört!")
                    #stoppt witeres prüfen eines bullet auf collision
                    break
        
        # Entferne tote Meteoriten
        for meteor in meteors_to_remove:
            if meteor in g.objects:
                g.objects.remove(meteor)
        
        # Entferne tote Bullets
        g.player_bullets = [b for b in g.player_bullets if b.alive]

        #test pfeil
        if g.shoparrow:
            arrow.render()

        # collision detection
        to_remove = []
        for obj in g.objects:
            if obj.shoot():
                to_remove.append(obj)
        for obj in to_remove:
            g.objects.remove(obj)

    
        for planet in g.planets:
            planet.player_meet()
                
            

        pg.display.update()
        dt = g.clock.tick(60) #60 fps

        if g.debug:
            print(g.clock.get_rawtime(), "ms/tick & meteors:", len(g.objects), "player bullets:", len(g.player_bullets))
        
        
def main():
    start_screen()
    play_game()
    pg.quit()


if __name__ == "__main__":
    main()


