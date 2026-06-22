# world.py — die "lebende" Spielwelt: Instanzen + Per-Frame-Updates.
# Operiert über die globalen Listen g.objects / g.player_bullets / g.planets.
import os

import pygame as pg

import globals as g
import objects
from player import summon_meteor

# --- Welt-Instanzen (vorher oben in main.py) ---
Bg = objects.Background(os.path.join(g.img_path, "back_space.jpeg"))

# geg_fkt wird in main.py gesetzt (verhindert Import-Zyklus world <-> scenes)
tradeplanet = objects.Planet(
    "Trade Planet",
    [0, 0],
    pg.image.load(os.path.join(g.img_path, "trade_planet.png")).convert_alpha(),
    250,
)
g.planets.append(tradeplanet)

arrow = objects.Pointer(
    tradeplanet,
    pg.transform.scale(
        pg.transform.rotate(pg.image.load(os.path.join(g.img_path, "arrow.png")).convert_alpha(), 0),
        (50, 50),
    ),
)  # type: ignore


def spawn_test_meteors():
    """Temporär zum Testen — zwei Meteore beim Start."""
    summon_meteor(speed=1)
    summon_meteor()


# --- Logik-Phase: bewegen + Kollisionen (kein Zeichnen) ---

def move_objects():
    """Meteore/Gegner bewegen."""
    for obj in g.objects:
        obj.move()


def move_bullets():
    """Bullets bewegen (abgelaufene markieren sich selbst als tot)."""
    for bullet in g.player_bullets:
        bullet.move()


def handle_bullet_hits():
    """Bullet-Meteor-Kollision; tote Meteore und Bullets entfernen."""
    meteors_to_remove = []
    for bullet in g.player_bullets:
        if not bullet.alive:
            continue
        for meteor in g.objects:
            if bullet.collides_with(meteor):
                if g.debug:
                    print(f"TREFFER! Bullet trifft {meteor.name}! Damage: {bullet.damage}, Meteor Health: {meteor.health - bullet.damage}")
                meteor.health -= bullet.damage
                bullet.alive = False
                if meteor.health <= 0:
                    meteors_to_remove.append(meteor)
                    if g.debug:
                        print(f"{meteor.name} ist zerstört!")
                # stoppt weiteres Prüfen dieses Bullets auf Kollision
                break

    for meteor in meteors_to_remove:
        if meteor in g.objects:
            g.objects.remove(meteor)

    g.player_bullets = [b for b in g.player_bullets if b.alive]


def update_enemies():
    """Gegner schießen (Schaden am Spieler) + Planeten-Kontakt prüfen."""
    to_remove = []
    for obj in g.objects:
        if obj.shoot():
            to_remove.append(obj)
    for obj in to_remove:
        g.objects.remove(obj)

    for planet in g.planets:
        planet.player_meet()


# --- Zeichen-Phase: nur zeichnen (kein Zustand mehr ändern) ---

def draw_background():
    Bg.render()


def draw_objects():
    """Meteore/Gegner + Planeten zeichnen, optional Hitboxen im Debug."""
    blit_batch = [obj.draw_data() for obj in g.objects]
    blit_batch += [planet.draw_data() for planet in g.planets]
    g.screen.blits(blit_batch)

    if g.debug:
        g.screen.blits([obj.debug_data() for obj in g.objects])


def draw_bullets():
    """Lebende Bullets zeichnen."""
    g.screen.blits([bullet.draw_data() for bullet in g.player_bullets if bullet.alive])


def draw_arrow():
    """Shop-Pfeil zum Trade-Planeten (nur wenn aktiviert)."""
    if g.shoparrow:
        arrow.render()
