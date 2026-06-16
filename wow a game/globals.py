import pygame as pg
import os
#base werte

debug = True

playing = True

clock = pg.time.Clock()


#screen setup
#scr_width , scr_height = 800, 600
scr_width , scr_height = pg.display.Info().current_w, pg.display.Info().current_h
screen = pg.display.set_mode((scr_width, scr_height),pg.RESIZABLE)
pg.display.set_caption("Wow a game")


#Bilder
img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

player_base = pg.image.load(os.path.join(img_path,"SpaceShipSmall.png")).convert_alpha()
player_hitbox_radius = 40#max(player_base.get_width(), player_base.get_height()) // 2

bullet_img = pg.image.load(os.path.join(img_path,"Bullet.png")).convert_alpha()
#bullet_img = pg.transform.scale(bullet_img, (bullet_img.get_width()*5, bullet_img.get_height()*5))

meteor1_img = pg.image.load(os.path.join(img_path,"Meteor.jpg")).convert_alpha()

middle_x = scr_width // 2 
middle_y = scr_height // 2

#ka was das ist
shoparrow = False


#bewegung

forward = 0 # für die Bewegung nach vorne und hinten, wird in inputs.py gesetzt
right = 0 # für die Rotation, wird in inputs.py gesetzt

rotation_deg = 0 #rotation in grad, wird in movement.py gesetzt, da die Rotation von der Bewegung abhängt

pos_x = 0
pos_y = 0
acceleration = 0
max_speed = 30
speed = 0.1

#player

lives = 100
cooldown = 0#cooldown für die schussfrequenz

#gegner

objects = [] #Liste aller Objekte
player_bullets = [] #Liste aller Projektile, die der Spieler abgeschossen hat
planets = [] #Liste aller Planeten, die es gibt

to_buy = []





    