
import pygame
import globals
from player import move, shoot, summon_meteor
from scenes import pause_screen


def input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            globals.playing = False
        if  event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            globals.shoparrow = not globals.shoparrow
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pause_screen()
    globals.forward = 0
    globals.right = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        globals.forward += 1
    if keys[pygame.K_s]:
        globals.forward -= 1
    if keys[pygame.K_a]:
        globals.right += 1
    if keys[pygame.K_d]:
        globals.right -= 1
    if keys[pygame.K_e]:
        summon_meteor(speed=0.2)   
    if keys[pygame.K_SPACE]:
        if globals.cooldown > 600:
            globals.cooldown = 0
# später ult
        if globals.cooldown >= 20:
            globals.cooldown = 0 #cooldown von 20 ticks, damit nicht zu viele projektile auf einmal gespawnt werden
            shoot(10, 500, 10, 4, 1, 2, 2)
    
    globals.cooldown += 1
    move()
