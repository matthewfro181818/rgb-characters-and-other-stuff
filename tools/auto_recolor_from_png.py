import os, json, random
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

# ==================================================
# CONFIG
# ==================================================
CHAR_JSON_DIR = "CHAR_JSON_DIR" = "assets\base_game\shared\characters"
CHAR_IMG_DIR  = "assets\base_game\shared\images\characters"
OUT_DIR       = "assets/shared/data/recolors"

CLUSTERS      = 8
MIN_PIXELS    = 60
VARIANTS      = 0     # set to 100+ for mass recolors

# ==================================================
# UTILS
# ==================================================
def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def hex_to_rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (1,3,5))

def brightness(c):
    return c[0]*0.299 + c[1]*0.587 + c[2]*0.114

# ==================================================
# COLOR CLASSIFIER (FNF TUNED)
# ==================================================
def classify(rgb):
    r,g,b = rgb
    if r < 40 and g < 40 and b < 40:
        return "outline"
    if r > 200 and g > 170 and b > 140:
        return "skin"
    if b > r + 40 and b > g + 40:
        return "pants"
    if r > g + 40 and r > b + 40:
        return "shirt"
    if brightness(rgb) > 220:
        return "shoes"
    return "accessory"

# ==================================================
# CORE
# ==================================================
def extract_palette(png_path):
    img = Image.open(png_path).convert("RGBA")
    px  = np.array(img)

    mask = px[:,:,3] > 0
    colors = px[:,:,:3][mask]

    if len(colors) < 100:
        return None

    kmeans = KMeans(n_clusters=CLUSTERS, n_init=10)
    labels = kmeans.fit_predict(colors)
    centers = kmeans.cluster_centers_.astype(int)

    recolor = {}
    for i, c in enumerate(centers):
        if np.sum(labels == i) < MIN_PIXELS:
            continue
        layer = classify(tuple(c))
        recolor.setdefault(layer, {})
        recolor[layer][rgb_to_hex(c)] = rgb_to_hex(c)

    return recolor

# ==================================================
# VARIANT GENERATOR
# ==================================================
def random_shift(hex_color):
    r,g,b = hex_to_rgb(hex_color)
    return rgb_to_hex((
        min(255, max(0, r + random.randint(-60, 60))),
        min(255, max(0, g + random.randint(-60, 60))),
        min(255, max(0, b + random.randint(-60, 60))),
    ))

def generate_variants(base, count):
    variants = []
    for i in range(count):
        v = {}
        for layer, colors in base.items():
            v[layer] = {k: random_shift(k) for k in colors}
        variants.append(v)
    return variants

# ==================================================
# BATCH RUNNER
# ==================================================
def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    for file in os.listdir(CHAR_JSON_DIR):
        if not file.endswith(".json"):
            continue

        name = file.replace(".json", "")
        png  = os.path.join(CHAR_IMG_DIR, name + ".png")

        if not os.path.exists(png):
            print("⚠ Missing PNG:", name)
            continue

        print("Processing:", name)
        base = extract_palette(png)
        if not base:
            continue

        out = { "base": base }

        if VARIANTS > 0:
            out["variants"] = generate_variants(base, VARIANTS)

        with open(os.path.join(OUT_DIR, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)

    print("✔ Batch complete")

# ==================================================
if __name__ == "__main__":
    main()
