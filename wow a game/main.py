#Public library imports
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
pg.init()

#Own library imports
import globals as g
import inputs
import objects
from player import show, summon_meteor

screen = g.screen
Bg = objects.Background(os.path.join(g.img_path,"back_space.jpeg"))

def open_trade():
    tradeing = True
    while tradeing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                tradeing = False
                g.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tradeing = False

        pg.display.update()
        g.clock.tick(60)

#temp meteors zum testen
summon_meteor(speed=1)
summon_meteor()

tradeplanet = objects.Planet("Trade Planet", [0, 0], pg.image.load(os.path.join(g.img_path,"trade_planet.png")).convert_alpha(), 250, open_trade)
g.planets.append(tradeplanet)

arrow = objects.Pointer(tradeplanet, pg.transform.scale(pg.transform.rotate(pg.image.load(os.path.join(g.img_path,"arrow.png")).convert_alpha(), 0), (50, 50)))


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
    bullet_gestorben = False
    for bullet in g.player_bullets:
        if bullet.move():
            bullet_gestorben = True
        else:
            bullet_batch.append(bullet.draw_data())
    screen.blits(bullet_batch)
    if bullet_gestorben:
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
    
    



