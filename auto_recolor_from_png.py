import json
import random
from pathlib import Path

OUT_DIR = Path("assets/shared/data/recolors")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# BASE PART COLORS (FNF-ish)
# -------------------------
BASE_PARTS = {
    "skin": ["#ffd7c2", "#ffbfa3"],
    "clothes": ["#ff0000", "#cc0000"],
    "shoes": ["#ffffff", "#e6e6e6"],
    "hair": ["#00ffff", "#00aacc"]
}

# -------------------------
# OC STYLE PRESETS
# -------------------------
OC_STYLES = {
    "neon": {
        "clothes": ["#00ffff", "#ff00ff"],
        "hair": ["#00ffea"],
        "shoes": ["#ffffff"]
    },
    "void": {
        "clothes": ["#1a1a1a", "#000000"],
        "hair": ["#3a007a"],
        "shoes": ["#222222"]
    },
    "pastel": {
        "clothes": ["#ffc0cb", "#bde0fe"],
        "hair": ["#cdb4db"],
        "shoes": ["#ffffff"]
    },
    "gold": {
        "clothes": ["#ffcc00", "#ffaa00"],
        "hair": ["#ffdd55"],
        "shoes": ["#332200"]
    },
    "glitch": {
        "clothes": ["#ff0044", "#00ff88"],
        "hair": ["#00ffff"],
        "shoes": ["#111111"]
    },
    "midnight": {
        "clothes": ["#0a0a2a", "#1b1b5f"],
        "hair": ["#3f37c9"],
        "shoes": ["#0f0f1a"]
    }
}

# -------------------------
# GENERATOR
# -------------------------
def make_oc(character, style):
    data = {
        "meta": {
            "character": character,
            "type": "oc",
            "style": style
        },
        "parts": {}
    }

    style_data = OC_STYLES[style]

    for part, base_colors in BASE_PARTS.items():
        replacements = {}

        for base in base_colors:
            if part in style_data:
                replacements[base] = random.choice(style_data[part])
            else:
                replacements[base] = base  # unchanged

        data["parts"][part] = replacements

    return data

# -------------------------
# BATCH GENERATION
# -------------------------
CHARACTERS = [
    "bf",
    "bf-christmas",
    "bf-pixel",
    "bf-pixel-dead",
    "bf-pixel-opponent",
    "bf-dead",
    "bf-car",
    "bf-holding-gf",
    "bf-holding-gf-dead",
    "gf",
    "gf-christmas",
    "gf-pixel",
    "gf-tankmen",
    "dad",
    "mom",
    "mom-car",
    "parents-christmas",
    "monster",
    "monster-christmas",
    "nene",
    "pico",
    "pico-blazin",
    "pico-dead",
    "pico-playable",
    "pico-speaker",
    "senpai",
    "senpai-angry",
    "spirit",
    "tankman",
    "tankman-playable",
    "darnell",
    "darnell-blazin",
    
]

for char in CHARACTERS:
    for style in OC_STYLES.keys():
        name = f"{char}_{style}"
        path = OUT_DIR / f"{name}.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(make_oc(char, style), f, indent=2)

        print("Generated:", name)

print("✅ OC preset generation complete")
