import globals as g
import pygame as pg
from os import path
from objects import Button

button_img = player_base = pg.image.load(path.join(g.img_path,"card_trade.png")).convert_alpha()
button_img_hover = player_base = pg.image.load(path.join(g.img_path,"card_trade_hover.png")).convert_alpha()



class Trade():
    def __init__(self, name, price:list, stat, amount) -> None:
        self.name = name
        self.price = price
        self.iteration = 0
        self.stat = stat
        self.amount = amount
        button_scale = g.scr_width/200
        self.button = Button(0,0,button_scale,button_img,button_img_hover)

    def buy(self):
        if g.money < self.price[self.iteration]:
            return False
        g.money -= self.price[self.iteration]
        setattr(g, self.stat, getattr(g, self.stat) + self.amount)  #bsp: g.maxhealth += amount
        return True
    
    def render(self, pos):
        self.button.rect.topleft = (pos)
        font = pg.font.SysFont("Consolas", 40)
        name = font.render(self.name, True, (255, 255, 255))
        price = font.render(str(self.price[self.iteration]), True, (255, 255, 255))
        if self.amount < 0:
            description = font.render(f"{self.stat} verringert um {self.amount}", True, (255, 255, 255))
        else:
            description = font.render(f"{self.stat} erhöht um {self.amount}", True, (255, 255, 255))

# rendern für wann anders
        if self.button.draw_and_isclicked():
            self.buy()
        