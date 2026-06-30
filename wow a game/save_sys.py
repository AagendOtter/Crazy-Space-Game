# save_sys.py — Speichern/Laden des Spielstands als JSON.
#
# Grundidee: Wir speichern NICHT die Objekte selbst, sondern nur ihren Zustand
# (die einfachen Daten). Bilder (Surfaces) und Funktionen werden NICHT gespeichert
# - sie werden beim Laden wieder aus globals geholt bzw. neu erzeugt.
#
# Bewusst NICHT gespeichert:
#   - planets : werden von world.py bei jedem Start identisch neu erzeugt (statisch)
#   - to_buy  : wird im Code aktuell nirgends befuellt

import json
import os

import globals as g
from objects import Meteor, Bullet

# Standard-Speicherort: neben dieser Datei
save_pfad = os.path.join(os.path.dirname(os.path.realpath(__file__)), "savegame.json")

# Einfache Werte (Zahlen/Bool/Text), die direkt aus globals gespeichert werden.
# Hier bei Bedarf weitere Variablennamen ergaenzen.
GLOBALS_TO_SAVE = [
    "money", "lives", "maxhealth", "cooldown",
    "pos_x", "pos_y", "acceleration", "rotation_deg",
    "max_speed", "speed",
]


# --- Objekt -> Dict (nur speicherbare Felder, kein Bild) ---

def _meteor_to_dict(m):
    return {
        "name": m.name,
        "health": m.health,
        "damage": m.damage,
        "speed": m.speed,
        "size": m.size,
        "hitbox_radius": m.hitbox_radius,
        "position": list(m.position),
        "direction": m.direction,
    }


def _bullet_to_dict(b):
    return {
        "position": list(b.position),
        "direction": b.direction,
        "speed": b.speed,
        "damage": b.damage,
        "range_frames": b.range,   # b.range ist bereits in Frames (range/speed)
        "alive": b.alive,
    }


# --- Dict -> Objekt (Bild kommt aus globals) ---

def _meteor_from_dict(d):
    return Meteor(d["name"], d["health"], d["damage"], d["speed"], g.meteor1_img[3],
                  hitbox_radius=d["hitbox_radius"], size=d["size"],
                  position=list(d["position"]), direction=d["direction"])


def _bullet_from_dict(d):
    # Der Bullet-Konstruktor teilt das uebergebene range nochmal durch speed.
    # Wir geben darum 0 rein und setzen range/alive danach exakt zurueck.
    b = Bullet(list(d["position"]), d["direction"], d["speed"], d["damage"], 0, g.bullet_img)
    b.range = d["range_frames"]
    b.alive = d["alive"]
    return b


# --- Oeffentliche API ---

def speichern(pfad=save_pfad):
    """Aktuellen Spielzustand in eine JSON-Datei schreiben."""
    daten = {
        "globals": {name: getattr(g, name) for name in GLOBALS_TO_SAVE},
        "meteors": [_meteor_to_dict(m) for m in g.objects],
        "bullets": [_bullet_to_dict(b) for b in g.player_bullets],
    }
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2)
    if g.debug:
        print(f"Gespeichert: {len(daten['meteors'])} Meteore, "
              f"{len(daten['bullets'])} Bullets -> {pfad}")


def laden(pfad=save_pfad):
    """Spielzustand aus einer JSON-Datei laden. True bei Erfolg, sonst False."""
    if not os.path.exists(pfad):
        if g.debug:
            print("Kein Spielstand gefunden:", pfad)
        return False

    with open(pfad, "r", encoding="utf-8") as f:
        daten = json.load(f)

    # einfache Werte zurueckschreiben
    for name, wert in daten.get("globals", {}).items():
        setattr(g, name, wert)

    # Listen in-place ersetzen ([:]), damit bestehende Referenzen gueltig bleiben
    g.objects[:] = [_meteor_from_dict(d) for d in daten.get("meteors", [])]
    g.player_bullets[:] = [_bullet_from_dict(d) for d in daten.get("bullets", [])]

    if g.debug:
        print(f"Geladen: {len(g.objects)} Meteore, "
              f"{len(g.player_bullets)} Bullets <- {pfad}")
    return True
