# hud.py — Anzeige von Leben und Schuss-Cooldown am unteren Bildrand.
import pygame as pg

import globals as g

# --- Layout-Konstanten (vorher "magische Zahlen" in main.py) ---
BAR_X = 50            # linker Rand der Balken
BORDER = 5           # innerer Rand zwischen Rahmen und Füllung
BAR_HEIGHT = 40      # Höhe des äußeren Rahmens
PX_PER_LIFE = 4      # Balkenbreite (px) pro Lebenspunkt

HEALTH_BAR_Y = g.scr_height - 50    # y-Position Lebensbalken (von unten)
COOLDOWN_BAR_Y = g.scr_height - 100  # y-Position Cooldown-Balken
COOLDOWN_MAX = 600   # ab diesem Cooldown ist der Schuss bereit
COOLDOWN_WIDTH = 300  # max. Füllbreite des Cooldown-Balkens


def draw_hud():
    _draw_health()
    _draw_cooldown()


def _draw_health():
    # weißer Rahmen + rote Füllung (aktuelle Leben)
    pg.draw.rect(g.screen, "white", (BAR_X, HEALTH_BAR_Y, g.maxhealth * PX_PER_LIFE + 10, BAR_HEIGHT))
    pg.draw.rect(g.screen, "red", (BAR_X + BORDER, HEALTH_BAR_Y + BORDER, g.lives * PX_PER_LIFE, BAR_HEIGHT - 2 * BORDER))


def _draw_cooldown():
    # Cooldown 0..600 -> Füllbreite 0..300
    fill = min(g.cooldown, COOLDOWN_MAX) / 2
    pg.draw.rect(g.screen, "white", (BAR_X, COOLDOWN_BAR_Y, COOLDOWN_WIDTH + 10, BAR_HEIGHT))
    pg.draw.rect(g.screen, "blue", (BAR_X + BORDER, COOLDOWN_BAR_Y + BORDER, fill, BAR_HEIGHT - 2 * BORDER))
