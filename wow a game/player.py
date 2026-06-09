from math import cos, sin, pi

import globals as g
from fremd import blitRotate
from objects import Bullet, Meteor

meteor_count = 0

def show():
    blitRotate(g.screen, g.player_base, (g.middle_x , g.middle_y), (g.player_base.get_width() // 2, g.player_base.get_height() // 2), g.rotation_deg-90)

def move():
    g.rotation_deg += g.right 
    rotation = g.rotation_deg* pi / 180

    g.acceleration += g.forward * 0.4

    if abs(g.acceleration) >= 0.2:
        #die bewegung wird immer langsamer, mit beachtung der richtung
        g.acceleration -= 0.2 * (g.acceleration / abs(g.acceleration))

        
        if g.acceleration > g.max_speed:
            g.acceleration = g.max_speed
        elif g.acceleration < -g.max_speed:
            g.acceleration = -g.max_speed


        g.pos_x += g.acceleration * -cos(rotation)  * g.speed
        g.pos_y += g.acceleration * sin(rotation) * g.speed
    else:
        g.acceleration = 0


    
    
def shoot(dmg, range, speed, angle_offset=0):
    # spawn bullet at player screen center translated to world-relative coordinates
    start_x = g.middle_x - g.pos_x
    start_y = g.middle_y - g.pos_y
    direction_rad = -(g.rotation_deg + angle_offset) * pi / 180
    g.player_bullets.append(Bullet([start_x, start_y], direction_rad, speed, dmg, range, g.bullet_img))

def summon_meteor(health=100, damage=10, speed=0):
    global meteor_count
    meteor_count += 1
    g.objects.append(Meteor(f"Meteor{meteor_count}", health, damage, speed, g.meteor1_img))


