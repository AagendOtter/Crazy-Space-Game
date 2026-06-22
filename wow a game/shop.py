import globals as g
import pygame as pg


class Trade():
    def __init__(self, name, price:list, stat, amount, bg) -> None:
        self.name = name
        self.price = price
        self.iteration = 0
        self.stat = stat
        self.amount = amount
        self.background = bg

    def buy(self):
        if g.money < self.price[self.iteration]:
            return False
        g.money -= self.price[self.iteration]
        setattr(g, self.stat, getattr(g, self.stat) + self.amount)  #bsp: g.maxhealth += amount
        return True
    
    def render(self, pos):
        g.screen.blit(self.background,pos)
        font = pg.font.SysFont("Consolas", 40)
        name = font.render(self.name, True, (255, 255, 255))
        price = font.render(self.price[self.iteration], True, (255, 255, 255))
        if self.amount < 0:
            description = font.render(f"{self.stat} verringert um {self.amount}", True, (255, 255, 255))
        else:
            description = font.render(f"{self.stat} erhöht um {self.amount}", True, (255, 255, 255))

# rendern für wann anders