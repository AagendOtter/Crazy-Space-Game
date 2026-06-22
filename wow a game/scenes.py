import pygame as pg
import globals as g
from world import Bg


def start_screen():
    Bg.render()
    start = True

    font = pg.font.SysFont("Consolas", 92, bold=True)
    sec_font = pg.font.SysFont("Consolas", 40, bold=True)
    crazy = font.render("Crazy", True, (255, 255, 255))
    space = font.render("Space", True, (255, 255, 255))
    game = font.render("Game", True, (255, 255, 255))
    sec_text = sec_font.render("Press Enter to Start", True, (135, 206, 235))
    crazy_rect = crazy.get_rect(center=(g.middle_x, g.middle_y - 80))
    space_rect = space.get_rect(center=(g.middle_x, g.middle_y))
    game_rect = game.get_rect(center=(g.middle_x, g.middle_y + 80))
    sec_text_rect = sec_text.get_rect(center=(g.middle_x, g.middle_y + 160))

    g.screen.blit(crazy, crazy_rect)
    g.screen.blit(space, space_rect)
    g.screen.blit(game, game_rect)
    g.screen.blit(sec_text, sec_text_rect)

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

    g.screen.blit(pause_text, pause_rect)
    g.screen.blit(sec_text, sec_text_rect)
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