import pygame as pg
import os
import sys
#base werte

debug = False

playing = True

clock = pg.time.Clock()


#screen setup
# Ensure the video subsystem is initialized before querying display info.
if not pg.get_init():
	pg.init()
if not pg.display.get_init():
	pg.display.init()

#scr_width , scr_height = 800, 600
try:
	display_w, display_h = pg.display.Info().current_w, pg.display.Info().current_h
except pg.error:
	display_w, display_h = 800, 600

# macOS often clamps oversized resizable windows because of title bar and system UI.
if sys.platform == "darwin":
	scr_width = max(800, display_w - 32)
	scr_height = max(600, display_h - 96)
else:
	scr_width, scr_height = display_w, display_h

screen = pg.display.set_mode((scr_width, scr_height))
scr_width, scr_height = screen.get_size()
pg.display.set_caption("Wow a game")


#Bilder
img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

player_base = pg.image.load(os.path.join(img_path,"spaceShip.png")).convert_alpha()
player_base = pg.transform.scale(player_base, (80, 80))
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
maxhealth = 100
cooldown = 0#cooldown für die schussfrequenz

#gegner

objects = [] #Liste aller Objekte
player_bullets = [] #Liste aller Projektile, die der Spieler abgeschossen hat
planets = [] #Liste aller Planeten, die es gibt

to_buy = []





    