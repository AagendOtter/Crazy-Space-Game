from fremd import blitRotate
import globals as g
from math import atan2, cos, sin, pi, atan
from abc import ABC, abstractmethod
from random import randint
import pygame

class Background():
    def __init__(self, image, scale_factor:float=3):
        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale_factor, self.image.get_height() * scale_factor))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        

    def render(self):
        ox = g.pos_x % self.width
        oy = g.pos_y % self.height
        g.screen.blits([
            (self.image, (ox, oy)),
            (self.image, (ox - self.width, oy)),
            (self.image, (ox, oy - self.height)),
            (self.image, (ox - self.width, oy - self.height)),
        ])

    def border(self):
        pass


class Pointer(ABC):
    def __new__(cls, target, image, angle_offset: float = 0, distance_from_player: float | None = None):
        if cls is Pointer:
            if isinstance(target, (list, tuple)):
                return PointerToPos(target, image, angle_offset, distance_from_player)
            return PointerToObject(target, image, angle_offset, distance_from_player)
        return super().__new__(cls)

    @abstractmethod
    def render(self):
        raise NotImplementedError("Pointer subclasses must implement render()")

class PointerToObject(Pointer):
    def __init__(self, target, image, angle_offset: float = 0, distance_from_player: float | None = None):
        self.target = target
        self.image = image
        self.angle_offset = angle_offset
        self.distance_from_player = distance_from_player

    def render(self):
        dx = self.target.position[0] + g.pos_x + self.target.size / 2 - g.middle_x
        dy = self.target.position[1] + g.pos_y + self.target.size / 2 - g.middle_y
        angle_radians = atan2(dy, dx)
        distance = self.distance_from_player if self.distance_from_player is not None else g.player_hitbox_radius + max(self.image.get_width(), self.image.get_height()) / 2 + 10
        draw_pos = (g.middle_x + cos(angle_radians) * distance, g.middle_y + sin(angle_radians) * distance)
        angle = (180 / pi) * angle_radians + self.angle_offset
        blitRotate(g.screen, self.image, draw_pos, (self.image.get_width() // 2, self.image.get_height() // 2), -angle)

class PointerToPos(Pointer):
    def __init__(self, target, image, angle_offset: float = 0, distance_from_player: float | None = None):
        self.target = target
        self.image = image
        self.angle_offset = angle_offset
        self.distance_from_player = distance_from_player

    def render(self):
        dx = self.target[0] + g.pos_x - g.middle_x
        dy = self.target[1] + g.pos_y - g.middle_y
        angle_radians = atan2(dy, dx)
        distance = self.distance_from_player if self.distance_from_player is not None else g.player_hitbox_radius + max(self.image.get_width(), self.image.get_height()) / 2 + 10
        draw_pos = (g.middle_x + cos(angle_radians) * distance, g.middle_y + sin(angle_radians) * distance)
        angle = (180 / pi) * angle_radians + self.angle_offset
        blitRotate(g.screen, self.image, draw_pos, (self.image.get_width() // 2, self.image.get_height() // 2), -angle)


class Opponent(ABC):
    def __init__(self, name:str, health:int, damage:int, speed:float|int, image):
        self.name = name
        self.health = health
        self.damage = damage
        self.speed = speed
        self.image = image

    @abstractmethod
    def move(self):
        pass

    def get_name(self):
        return self.name
    
    def get_health(self):
        return self.health
    
    def get_damage(self):   
        return self.damage

    @abstractmethod
    def shoot(self):
        pass

class Meteor(Opponent):

    _hitbox_cache = {}

    def __init__(self, name, health, damage, speed, image,hitbox_radius:int=None,size:int=None,position=None,direction=None): # type: ignore
        super().__init__(name, health, damage, speed, image)
        self.size = size if size is not None else randint(50, 100)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))


        if hitbox_radius is not None:
            self.hitbox_radius = hitbox_radius
        else:
            self.hitbox_radius = self.size / 2

        if position is not None and direction is not None:
            # geladener Meteor: Zustand exakt uebernehmen
            self.position = position
            self.direction = direction
        else:
            # neuer Meteor: Startposition am Rand wuerfeln, Richtung zur Mitte
            t = randint(0, 1)
            if t == 0:
                self.position = [randint(0,1)*g.scr_width-self.size/2-g.pos_x, randint(0, g.scr_height)-self.size/2-g.pos_y]
            else:
                self.position = [randint(0, g.scr_width)-self.size/2-g.pos_x, randint(0,1)*g.scr_height-self.size/2-g.pos_y]

            dx = g.middle_x - (self.position[0] + g.pos_x + self.size / 2)
            dy = g.middle_y - (self.position[1] + g.pos_y + self.size / 2)
            self.direction = atan2(dy, dx)

        self.x_movement = self.speed * cos(self.direction)
        self.y_movement = self.speed * sin(self.direction)
    

    def move(self):
        self.position[0] += self.x_movement
        self.position[1] += self.y_movement

    def draw_data(self):
        return (self.image, (self.position[0] + g.pos_x, self.position[1] + g.pos_y))
        
    def hitbox_surf(self, radius):
        r = int(radius)
        # nur beim ERSTEN Mal
        if r not in self._hitbox_cache:
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 0, 0), (r, r), r, 1)
            self._hitbox_cache[r] = s
        return self._hitbox_cache[r]
    
    def debug_data(self):
        r = int(self.hitbox_radius)
        ring = self.hitbox_surf(r)
        cx = self.position[0] + g.pos_x + self.size / 2
        cy = self.position[1] + g.pos_y + self.size / 2
        return (ring, (cx - r, cy - r))


    def shoot(self):
        dx = self.position[0] + g.pos_x + self.size / 2 - g.middle_x
        dy = self.position[1] + g.pos_y + self.size / 2 - g.middle_y
        if dx * dx + dy * dy <= (self.hitbox_radius + g.player_hitbox_radius) ** 2:
            if g.debug:
                print(self.name, "Meteor hit!")
            g.lives -= self.damage
            return self
        return None

class Bullet():
    def __init__(self, position, direction, speed, damage, range, image):
        self.position = position
        self.direction = direction
        self.direction_deg = -direction * 180 / pi - 90
        self.speed = speed
        self.damage = damage
        self.range = range/speed #wie viele frames die kugel fliegen soll, bevor sie verschwindet
        self.image = pygame.transform.rotate(image, self.direction_deg)
        self.movement_x = self.speed * cos(direction)
        self.movement_y = self.speed * sin(direction)
        self.half_w = self.image.get_width() / 2
        self.half_h = self.image.get_height() / 2
        self.alive = True
        self.hitbox_radius = max(self.half_w, self.half_h)

    def move(self):
        self.position[0] += self.movement_x
        self.position[1] += self.movement_y
        self.range -= 1
        if self.range <= 0:
            self.alive = False
            return True
    
    def draw_data(self):
        return (self.image, (self.position[0] + g.pos_x - self.half_w, self.position[1] + g.pos_y - self.half_h))
    
    def collides_with(self, obj):
        # Berechne quadrierter Abstand zwischen Bullet und Meteor (schneller ohne Wurzel)
        dx = self.position[0] - (obj.position[0] + obj.size / 2)
        dy = self.position[1] - (obj.position[1] + obj.size / 2)
        return dx * dx + dy * dy <= (self.hitbox_radius + obj.hitbox_radius) ** 2
class Planet():
    def __init__(self, name, position, image, size, geg_fkt=None):
        self.name = name
        self.image = pygame.transform.scale(image, (size, size))
        self.size = size
        self.position = position
        self.geg_fkt = geg_fkt
        self.half = size / 2
        

    def draw_data(self):
        return (self.image, (self.position[0] + g.pos_x, self.position[1] + g.pos_y))
    
    def player_meet(self):
        dx = self.position[0] + g.pos_x + self.half - g.middle_x
        dy = self.position[1] + g.pos_y + self.half - g.middle_y
        if dx * dx + dy * dy <= (self.half + g.player_hitbox_radius) ** 2:
            if g.debug:
                print(self.name, "getroffen!")
            if self.geg_fkt is not None:
                self.geg_fkt()
            g.pos_x = g.middle_x - self.position[0] - self.half
            g.pos_y = g.middle_y - self.position[1] + g.player_hitbox_radius + 10
            g.acceleration = 0
            g.rotation_deg = 90

class Button():
    def __init__(self, x, y, scale, img, pressed_img) -> None: # type: ignore
        width = img.get_width() * scale
        height = img.get_height() * scale
        self.img = pygame.transform.scale(img, (width,height))
        self.hover_img = pygame.transform.scale(pressed_img, (width,height))
        self.rect = self.img.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw_and_isclicked(self):
        pos = pygame.mouse.get_pos()
        action = False
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.rect.collidepoint(pos):
            
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True    
            g.screen.blit(self.hover_img, self.rect.topleft)
        else:
            g.screen.blit(self.img, self.rect.topleft)

        return action
    
        