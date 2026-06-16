import pygame as pg
import globals as g


def open_trade():
    tradeing = True
    in_shop = g.to_buy[:3]
    while tradeing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                tradeing = False
                g.playing = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tradeing = False
            pressed = False
            mouse_pos = pg.mouse.get_pos()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pressed = True

        g.screen.fill((0, 0, 0))
        pg.display.update()
        g.clock.tick(60)