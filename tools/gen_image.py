#!/usr/bin/env python3
"""Hand-drawn flat-vector world news page for 25 Nov 2026 (36 stories).

Renders entry.png at 1024x1024 with PIL only. Run: python3 tools/gen_image.py
Layout mirrors the 24 Nov page: header, 3 big headlines, 10 small cards,
world map with 13 numbered pins, region bars, 23 one-line briefs.
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "entry.png")
FONTDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTDIR, name), size)


def bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def regular(size):
    return font("DejaVuSans.ttf", size)


W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
MUTED = (90, 88, 80)
RED = (192, 57, 43)
NAVY = (26, 32, 44)
BLUE = (31, 78, 121)
TEAL = (18, 120, 110)
OCEAN = (168, 200, 220)
LAND = (232, 217, 168)
GOLD = (212, 160, 40)
GREEN = (46, 125, 60)
ORANGE = (230, 110, 30)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap_text(text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(text, fnt, maxw, maxlines):
    lines = wrap_text(text, fnt, maxw)
    while len(lines) > maxlines and len(lines) > 1:
        words = text.split()
        if len(words) <= 4:
            break
        text = " ".join(words[:-3]) + "."
        lines = wrap_text(text, fnt, maxw)
    return lines


# ---------------------------------------------------------------- map data
# Natural Earth 50m coastline + borders, pre-projected to MAP pixel space.
# land / lakes / borders are lists of polygons in pixel coordinates.
MAPBOX = (8, 438, 684, 576)  # x0, y0, x1, y1


def project(lon, lat):
    x0, y0, x1, y1 = MAPBOX
    px = x0 + (lon + 180) / 360.0 * (x1 - x0)
    py = y0 + (75 - lat) / 130.0 * (y1 - y0)
    return (px, py)


with open(os.path.join(HERE, "mapdata.json")) as fh:
    _data = json.load(fh)
LAND_POLYS = [[tuple(p) for p in poly] for poly in _data["land"]]
LAKE_POLYS = [[tuple(p) for p in poly] for poly in _data["lakes"]]
BORDER_RINGS = [[tuple(p) for p in poly] for poly in _data["borders"]]

# (lon, lat, story number). Number IS the story number.
# Pins 1 and 27 are distinct places in the Gulf that round to the same
# whole degree (26N 56E), so they now carry one-decimal coordinates and
# their markers are offset from the true spot with a thin leader line
# back to it, so the two never read as one pin.
PINS = [
    (56.3, 26.6, 1), (100, 41, 2), (-76, 10, 3), (50, 26, 4),
    (34, 31, 6), (34, 12, 8), (149, -35, 9), (-74, 41, 10),
    (107, -7, 12), (31, 46, 14), (-91, 41, 22), (55.9, 25.8, 27),
    (-58, -35, 33),
]
# Marker offset (dx, dy) in px from the true projected point, for pins
# whose true spots are too close to draw on top of each other.
MARKER_OFF = {
    1: (-20, -20),   # Hormuz: marker up-left of the true spot
    27: (18, 14),    # Ras Al Khaimah: marker down-right of the true spot
}

# ---------------------------------------------------------------- header
d.rectangle([0, 0, W, 62], fill=NAVY)
d.rectangle([0, 62, W, 66], fill=RED)
d.text((16, 8), "THE WORLD IN ONE DAY", font=bold(30), fill=PAPER)
d.text((16, 42), "WEDNESDAY, 25 NOVEMBER 2026  \u00b7  36 STORIES, ONE DAY",
       font=regular(12), fill=(200, 205, 215))
d.text((W - 16, 12), "No. 25", font=bold(14), fill=GOLD, anchor="ra")
d.text((W - 16, 34), "ALL HAND-DRAWN", font=regular(11),
       fill=(200, 205, 215), anchor="ra")

# ---------------------------------------------------------------- big headlines
HEADLINES = [
    ("1  IRAN SAYS TWO TANKERS HIT MINES IN STRAIT OF HORMUZ",
     "Iran's Guard Navy said two tankers struck mines and caught fire in the "
     "Strait of Hormuz on Wednesday. The mine claims were unconfirmed.",
     "REUTERS / AL JAZEERA"),
    ("2  SHENZHOU-24 DOCKS WITH FIRST FOREIGN ASTRONAUT ABOARD",
     "Shenzhou-24 launched from Jiuquan on Wednesday and docked with Tiangong "
     "hours later. Pakistan's Muhammad Zeeshan Ali, 40, is the first foreigner aboard.",
     "REUTERS / XINHUA"),
    ("3  COLOMBIA FREES ALL CARTAGENA HOSTAGES",
     "Security forces stormed an Exito supermarket in Cartagena early on "
     "Wednesday and freed about 20 hostages after a 17-hour siege, killing one captor.",
     "BBC / AP"),
]


def illu_strait(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(178, 208, 228))
    d.rectangle(box, outline=INK, width=2)
    # cliffs left and right, sea channel between them
    d.polygon([(x0, y0), (x0 + 62, y0), (x0 + 38, y0 + 34), (x0, y0 + 34)],
              fill=(146, 122, 88))
    d.polygon([(x1, y0), (x1 - 62, y0), (x1 - 38, y0 + 34), (x1, y0 + 34)],
              fill=(146, 122, 88))
    d.rectangle([x0, y0 + 40, x1, y1], fill=(52, 110, 150))
    # two burning tankers
    for cx in (x0 + 108, x0 + 208):
        d.rectangle([cx - 34, y0 + 42, cx + 34, y0 + 53], fill=(48, 48, 48))
        d.rectangle([cx - 12, y0 + 34, cx + 12, y0 + 42], fill=(120, 120, 120))
        d.polygon([(cx - 10, y0 + 34), (cx + 10, y0 + 34), (cx, y0 + 18)],
                  fill=ORANGE)
        d.ellipse([cx - 5, y0 + 4, cx + 5, y0 + 18], fill=(70, 70, 70))
        d.ellipse([cx - 9, y0 + 1, cx + 3, y0 + 9], fill=(90, 90, 90))
    # a mine bobbing in the water
    mx, my = x0 + 158, y0 + 56
    d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(20, 20, 20))
    for dx, dy in ((-7, 0), (7, 0), (0, -7), (-5, -5), (5, -5)):
        d.line([mx, my, mx + dx, my + dy], fill=(20, 20, 20), width=2)


def illu_shenzhou(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(16, 24, 48))
    d.rectangle(box, outline=INK, width=2)
    # stars
    for sx, sy in ((x0 + 20, y0 + 8), (x0 + 60, y0 + 16), (x0 + 290, y0 + 10),
                   (x0 + 250, y0 + 20), (x0 + 120, y0 + 6), (x0 + 200, y0 + 26)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # Earth arc along the bottom (kept inside the box; spill erased below)
    d.ellipse([x0, y0 + 40, x1, y0 + 96], fill=(52, 110, 170))
    d.ellipse([x0 + 30, y0 + 46, x0 + 110, y0 + 74], fill=(70, 150, 90))
    d.rectangle([x0, y1, x1, y1 + 40], fill=(255, 255, 255))
    d.rectangle(box, outline=INK, width=2)
    # space station: central module + solar panels
    d.rectangle([x0 + 118, y0 + 22, x0 + 198, y0 + 36], fill=(200, 205, 210),
                outline=INK, width=1)
    d.rectangle([x0 + 78, y0 + 26, x0 + 118, y0 + 32], fill=(40, 90, 160))
    d.rectangle([x0 + 198, y0 + 26, x0 + 238, y0 + 32], fill=(40, 90, 160))
    d.rectangle([x0 + 150, y0 + 12, x0 + 166, y0 + 22], fill=(180, 185, 190),
                outline=INK, width=1)
    # capsule docking from the left, flags on its side
    d.rounded_rectangle([x0 + 238, y0 + 20, x0 + 296, y0 + 38], 6,
                        fill=(245, 245, 245), outline=INK, width=1)
    d.rectangle([x0 + 246, y0 + 24, x0 + 258, y0 + 30], fill=(20, 90, 50))
    d.rectangle([x0 + 262, y0 + 24, x0 + 274, y0 + 30], fill=RED)
    d.text((x0 + 264, y0 + 24), "*", font=bold(7), fill=(255, 220, 0))
    d.line([x0 + 238, y0 + 29, x0 + 230, y0 + 29], fill=INK, width=2)


def illu_cartagena(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 232, 238))
    d.rectangle(box, outline=INK, width=2)
    # supermarket front
    d.rectangle([x0 + 18, y0 + 16, x0 + 210, y0 + 58], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([x0 + 18, y0 + 16, x0 + 210, y0 + 28], fill=(20, 110, 60))
    d.text((x0 + 26, y0 + 18), "SUPERMARKET", font=bold(9), fill=(255, 255, 255))
    d.rectangle([x0 + 100, y0 + 36, x0 + 128, y0 + 58], fill=(120, 170, 200),
                outline=INK, width=1)
    # police cordon tape
    d.line([x0 + 6, y0 + 52, x1 - 6, y0 + 52], fill=(240, 200, 40), width=4)
    d.line([x0 + 6, y0 + 52, x1 - 6, y0 + 52], fill=INK, width=1)
    # helicopter overhead
    hx, hy = x0 + 262, y0 + 14
    d.ellipse([hx - 16, hy - 4, hx + 16, hy + 6], fill=(90, 90, 90))
    d.line([hx - 26, hy - 6, hx + 26, hy - 6], fill=INK, width=2)
    d.line([hx + 16, hy, hx + 28, hy - 6], fill=INK, width=2)
    # officers leading two freed hostages out
    for px, col in ((x0 + 52, NAVY), (x0 + 70, (120, 90, 60)),
                    (x0 + 88, NAVY), (x0 + 106, (120, 90, 60))):
        d.ellipse([px - 3, y0 + 44, px + 3, y0 + 50], fill=(220, 180, 140))
        d.rectangle([px - 3, y0 + 50, px + 3, y0 + 58], fill=col)


BIG_ILLUS = [illu_strait, illu_shenzhou, illu_cartagena]
for i, (title, body, src) in enumerate(HEADLINES):
    x = 8 + i * 340
    w = 332
    d.rectangle([x, 72, x + w, 250], fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([x, 72, x + w, 92], fill=NAVY)
    d.text((x + 8, 76), "TOP STORY %d  \u00b7  %s" % (i + 1, src),
           font=bold(11), fill=PAPER)
    BIG_ILLUS[i]((x + 8, 98, x + w - 8, 98 + 62))
    yy = 166
    for ln in fit_text(title, bold(13), w - 16, 2):
        d.text((x + 8, yy), ln, font=bold(13), fill=INK)
        yy += 16
    yy += 2
    for ln in fit_text(body, regular(11), w - 16, 3):
        d.text((x + 8, yy), ln, font=regular(11), fill=INK)
        yy += 14

# ---------------------------------------------------------------- small stories
SMALL = [
    ("4  HOUTHIS SAY THEY HIT RAS TANURA",
     "Houthis claim a strike; coalition denies.",
     "refinery"),
    ("5  UKRAINE SAYS DRONES HIT REFINERIES",
     "Drones reportedly hit two refineries.",
     "refinery2"),
    ("6  ISRAEL KILLS HAMAS CHIEF",
     "Israel killed a Hamas security chief, his wife and two children in Gaza.",
     "gaza"),
    ("7  ASIAN TECH STOCKS TUMBLE",
     "KOSPI fell 6.16% and the Nikkei 2.78% as investors fretted over AI and debt.",
     "chart"),
    ("8  SUDAN STRIKES KILL 19",
     "RSF drones killed 19 civilians and wounded 20 in two Blue Nile cities.",
     "sudan"),
    ("9  SOLOMONS TREATY",
     "Solomons named Australia its top security partner; no foreign bases.",
     "treaty"),
    ("10  TUESDAY: HUAWEI GUILTY",
     "Guilty of bank fraud; Huawei will appeal, Beijing accused Washington.",
     "gavel"),
    ("11  TUESDAY: SENEGAL WINS",
     "CAS reinstated Senegal as 2025 AFCON winners; Morocco vowed legal action.",
     "trophy"),
    ("12  INDONESIA MINE TOLL RISES",
     "Three more bodies were found in Bogor; the toll is six, about 20 still trapped.",
     "mine"),
    ("13  TRUMP PLANS NEW TARIFFS",
     "The US is preparing new tariffs on 16 economies, including China and the EU.",
     "tariff"),
]


def illu_small(kind, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle(box, fill=(235, 238, 240))
    d.rectangle(box, outline=INK, width=1)
    if kind == "refinery":
        d.rectangle(box, fill=(24, 28, 44))
        for tx in (x0 + 30, x0 + 70, x0 + 110):
            d.rectangle([tx - 8, y0 + 12, tx + 8, y1 - 4], fill=(90, 90, 100))
        d.ellipse([cx - 12, y0 + 2, cx + 12, y0 + 18], fill=ORANGE)
        d.ellipse([cx - 6, y0 + 6, cx + 6, y0 + 14], fill=(240, 200, 40))
        d.ellipse([x1 - 24, y0 + 3, x1 - 16, y0 + 9], fill=(200, 200, 200))
        d.line([x1 - 28, y0 + 6, x1 - 12, y0 + 6], fill=(200, 200, 200), width=1)
    elif kind == "refinery2":
        d.rectangle(box, fill=(24, 28, 44))
        for tx in (x0 + 55, x0 + 130):
            d.rectangle([tx - 12, y0 + 12, tx + 12, y1 - 4], fill=(90, 90, 100))
            d.polygon([(tx - 8, y0 + 12), (tx + 8, y0 + 12), (tx, y0 + 2)],
                      fill=ORANGE)
        d.ellipse([cx - 4, y0 + 2, cx + 4, y0 + 8], fill=(60, 60, 60))
        d.line([cx - 10, y0 + 5, cx + 10, y0 + 5], fill=(60, 60, 60), width=1)
    elif kind == "gaza":
        d.rectangle([x0 + 14, y0 + 8, x0 + 90, y1 - 4], fill=(170, 165, 150),
                    outline=INK, width=1)
        d.line([x0 + 40, y0 + 8, x0 + 52, y1 - 4], fill=INK, width=1)
        d.line([x0 + 66, y0 + 8, x0 + 58, y1 - 4], fill=INK, width=1)
        d.ellipse([x0 + 110, y0 + 2, x0 + 122, y0 + 12], fill=(120, 120, 120))
        d.ellipse([x0 + 118, y0 + 8, x0 + 132, y0 + 20], fill=(140, 140, 140))
        # stretcher carried by a rescue worker
        d.line([x1 - 58, y1 - 8, x1 - 18, y1 - 8], fill=RED, width=3)
        d.ellipse([x1 - 62, y1 - 16, x1 - 56, y1 - 10], fill=(220, 180, 140))
        d.rectangle([x1 - 62, y1 - 10, x1 - 56, y1 - 4], fill=(200, 60, 50))
        d.ellipse([x1 - 14, y1 - 16, x1 - 8, y1 - 10], fill=(220, 180, 140))
        d.rectangle([x1 - 14, y1 - 10, x1 - 8, y1 - 4], fill=(200, 60, 50))
    elif kind == "chart":
        d.line([x0 + 8, y0 + 6, x0 + 60, y0 + 10, x0 + 110, y0 + 6, x1 - 10, y1 - 6],
               fill=RED, width=3)
        d.rectangle([x1 - 34, y0 + 4, x1 - 14, y0 + 16], fill=GREEN,
                    outline=INK, width=1)
        d.line([x1 - 30, y0 + 8, x1 - 18, y0 + 8], fill=(255, 255, 255), width=1)
        d.line([x1 - 30, y0 + 12, x1 - 18, y0 + 12], fill=(255, 255, 255), width=1)
        d.ellipse([x0 + 10, y0 + 12, x0 + 16, y0 + 18], fill=(220, 180, 140))
        d.rectangle([x0 + 9, y0 + 18, x0 + 17, y1 - 4], fill=NAVY)
    elif kind == "sudan":
        d.rectangle([x0, y1 - 8, x1, y1], fill=(200, 175, 130))
        d.polygon([(x0 + 16, y1 - 8), (x0 + 52, y1 - 8), (x0 + 46, y0 + 10),
                   (x0 + 22, y0 + 10)], fill=(170, 140, 100), outline=INK)
        d.polygon([(x0 + 62, y1 - 8), (x0 + 96, y1 - 8), (x0 + 90, y0 + 14),
                   (x0 + 68, y0 + 14)], fill=(150, 120, 85), outline=INK)
        d.ellipse([x1 - 30, y0 + 3, x1 - 22, y0 + 9], fill=(60, 60, 60))
        d.line([x1 - 34, y0 + 6, x1 - 18, y0 + 6], fill=(60, 60, 60), width=1)
        # Red Crescent worker
        d.ellipse([cx - 2, y0 + 12, cx + 4, y0 + 18], fill=(220, 180, 140))
        d.rectangle([cx - 3, y0 + 18, cx + 5, y1 - 8], fill=(255, 255, 255),
                    outline=RED, width=1)
        d.ellipse([cx - 1, y0 + 20, cx + 3, y0 + 24], fill=RED)
    elif kind == "treaty":
        d.rectangle([x0 + 20, y0 + 8, x0 + 120, y1 - 6], fill=(255, 255, 255),
                    outline=INK, width=1)
        for yy in range(y0 + 12, y1 - 8, 4):
            d.line([x0 + 26, yy, x0 + 114, yy], fill=(150, 150, 150), width=1)
        # two hands shaking over the document
        d.rounded_rectangle([x0 + 46, y0 + 14, x0 + 76, y0 + 22], 3,
                            fill=(220, 180, 140), outline=INK, width=1)
        d.rounded_rectangle([x0 + 62, y0 + 12, x0 + 92, y0 + 20], 3,
                            fill=(200, 160, 120), outline=INK, width=1)
        # small flags behind: Australia blue, Solomons green-yellow-blue
        d.rectangle([x1 - 52, y0 + 4, x1 - 32, y0 + 14], fill=(20, 60, 140))
        d.rectangle([x1 - 26, y0 + 4, x1 - 6, y0 + 14], fill=(20, 120, 60))
        d.rectangle([x1 - 26, y0 + 8, x1 - 6, y0 + 10], fill=(240, 200, 40))
    elif kind == "gavel":
        d.polygon([(x0 + 24, y0 + 6), (x0 + 66, y0 + 2), (x0 + 70, y0 + 14),
                   (x0 + 28, y0 + 18)], fill=(120, 72, 30))
        d.line([x0 + 46, y0 + 12, x0 + 84, y0 + 24], fill=(120, 72, 30), width=5)
        d.rounded_rectangle([x0 + 108, y0 + 6, x0 + 138, y0 + 24], 3,
                            fill=(40, 44, 54), outline=(200, 200, 200), width=1)
        d.line([x0 + 118, y0 + 8, x0 + 128, y0 + 22], fill=(255, 255, 255), width=1)
        d.rectangle([x1 - 56, y1 - 12, x1 - 6, y1 - 3], outline=RED, width=2)
        d.text((x1 - 52, y1 - 12), "GUILTY", font=bold(7), fill=RED)
    elif kind == "trophy":
        d.polygon([(cx - 14, y0 + 2), (cx + 14, y0 + 2), (cx + 10, y0 + 14),
                   (cx - 10, y0 + 14)], fill=GOLD)
        d.rectangle([cx - 16, y0 + 14, cx + 16, y0 + 18], fill=GOLD)
        d.rectangle([cx - 4, y0 + 18, cx + 4, y0 + 22], fill=GOLD)
        d.polygon([(x1 - 44, y0 + 4), (x1 - 22, y0 + 2), (x1 - 20, y0 + 10),
                   (x1 - 42, y0 + 12)], fill=(120, 72, 30))
        for px, pc in ((x0 + 8, RED), (x0 + 22, GOLD), (x0 + 36, GREEN),
                       (x1 - 14, RED), (x1 - 28, GOLD)):
            d.rectangle([px, y0 + 2, px + 4, y0 + 6], fill=pc)
    elif kind == "mine":
        d.rectangle(box, fill=(90, 80, 60))
        d.polygon([(cx - 34, y1 - 4), (cx - 24, y0 + 6), (cx + 24, y0 + 6),
                   (cx + 34, y1 - 4)], fill=(30, 30, 30))
        d.rectangle([x0 + 8, y1 - 10, x0 + 44, y1 - 4], fill=(60, 90, 140))
        d.ellipse([x0 + 12, y1 - 16, x0 + 18, y1 - 10], fill=(240, 200, 40))
        d.line([x1 - 48, y1 - 8, x1 - 14, y1 - 8], fill=(200, 200, 200), width=3)
        d.ellipse([x1 - 52, y1 - 16, x1 - 46, y1 - 10], fill=(220, 180, 140))
        d.ellipse([x1 - 12, y1 - 16, x1 - 6, y1 - 10], fill=(220, 180, 140))
    elif kind == "tariff":
        d.rectangle([x0 + 12, y0 + 12, x0 + 62, y0 + 20], fill=RED)
        d.rectangle([x0 + 66, y0 + 12, x0 + 116, y0 + 20], fill=BLUE)
        d.rectangle([x0 + 38, y0 + 4, x0 + 88, y0 + 12], fill=GOLD)
        d.text((x0 + 44, y0 + 4), "TARIFF", font=bold(6), fill=INK)
        d.polygon([(x0 + 120, y1 - 6), (x1 - 8, y1 - 6), (x1 - 16, y1 - 14),
                   (x0 + 128, y1 - 14)], fill=(60, 60, 60))
        d.rectangle([x1 - 52, y0 + 2, x1 - 8, y0 + 12], fill=(255, 255, 255),
                    outline=RED, width=1)
        d.text((x1 - 48, y0 + 3), "TARIFF", font=bold(7), fill=RED)


for i, (title, body, kind) in enumerate(SMALL):
    col, row = i % 5, i // 5
    x = 8 + col * 204
    y = 258 + row * 78
    w, h = 196, 74
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    illu_small(kind, (x + 4, y + 4, x + w - 4, y + 30))
    tlines = fit_text(title, bold(10), w - 10, 2)
    yy = y + 33
    for ln in tlines:
        d.text((x + 5, yy), ln, font=bold(10), fill=INK)
        yy += 12
    max_body = 2 if len(tlines) == 1 else 1
    for ln in fit_text(body, regular(9), w - 10, max_body):
        d.text((x + 5, yy), ln, font=regular(9), fill=INK)
        yy += 11

# ---------------------------------------------------------------- map + regions
d.text((8, 416), "WHERE IT HAPPENED  \u00b7  13 PLACES PINNED", font=bold(14), fill=INK)
d.rectangle(MAPBOX, fill=OCEAN, outline=INK, width=2)
GRID = (145, 180, 205)
for lon in range(-180, 181, 30):
    gx = MAPBOX[0] + (lon + 180) / 360.0 * (MAPBOX[2] - MAPBOX[0])
    d.line([gx, MAPBOX[1], gx, MAPBOX[3]], fill=GRID, width=1)
for lat in (60, 30, 0, -30):
    gy = project(0, lat)[1]
    d.line([MAPBOX[0], gy, MAPBOX[2], gy], fill=GRID, width=1)
for poly in LAND_POLYS:
    d.polygon(poly, fill=LAND, outline=(150, 140, 100))
for poly in LAKE_POLYS:
    d.polygon(poly, fill=OCEAN, outline=(150, 140, 100))
for ring in BORDER_RINGS:
    d.line(ring, fill=(120, 110, 70), width=1)
# tidy the frame: land polygons can poke a few px above the box top
d.rectangle(MAPBOX, outline=INK, width=2)

# pin check: every pin needs land or coastline pixels within a 16px radius.
# Sea pins (Hormuz / Ras Al Khaimah) sit in water next to a coast, so they
# pass on nearby land; no pin is ever moved to pass the check.
_px = img.load()
_coast = {(150, 140, 100), (120, 110, 70)}
_disc = {}
for (lon, lat, n) in PINS:
    px, py = project(lon, lat)
    xi, yi = int(px), int(py)
    hits = 0
    for dx in range(-16, 17):
        for dy in range(-16, 17):
            if math.hypot(dx, dy) <= 16:
                xx, yy = xi + dx, yi + dy
                if 0 <= xx < W and 0 <= yy < H and (
                        _px[xx, yy] == LAND or _px[xx, yy] in _coast):
                    hits += 1
    _disc[n] = hits
    if hits == 0:
        print("PIN %d has no land/coastline pixels within 16px" % n)
        sys.exit(1)
print("pin disc check: 13/13 have land/coastline within 16px:", _disc)

# markers first, labels last, so no label is ever covered by a marker.
# A pin with a MARKER_OFF draws its marker at the offset spot and a thin
# leader line back to the true point, so two close pins never share a dot.
for (lon, lat, n) in PINS:
    px, py = project(lon, lat)
    mx, my = px, py
    ox, oy = MARKER_OFF.get(n, (0, 0))
    if ox or oy:
        mx, my = px + ox, py + oy
        d.line([px, py, mx, my + 4], fill=RED, width=1)
    d.ellipse([mx - 7, my - 16, mx + 7, my - 2], fill=RED,
              outline=(255, 255, 255), width=1)
    d.polygon([(mx - 6, my - 4), (mx + 6, my - 4), (mx, my + 4)], fill=RED)
    d.ellipse([mx - 2, my - 13, mx + 2, my - 9], fill=(255, 255, 255))
LABEL_OFF = {
    1: (0, -32),     # Hormuz: label directly above its offset marker
    27: (10, 0),     # Ras Al Khaimah: label right of its offset marker
    4: (10, -28),    # Ras Tanura: label above, clear of the Hormuz cluster
    8: (-26, -4),    # Damazin: label to the left, clear of Gaza's marker
    14: (10, -28),   # Odesa: label above
    2: (10, 6),      # Jiuquan: label below-right
    3: (10, -28),    # Cartagena: label above
}
for (lon, lat, n) in PINS:
    px, py = project(lon, lat)
    ox, oy = MARKER_OFF.get(n, (0, 0))
    lx, ly = px + ox, py + oy
    dx, dy = LABEL_OFF.get(n, (8, -18))
    d.text((lx + dx, ly + dy), str(n), font=bold(10), fill=RED,
           stroke_width=2, stroke_fill=(255, 255, 255))

# region panel
RX0, RY0 = 700, 438
d.rectangle([RX0, RY0, 1016, 576], fill=(255, 255, 255), outline=INK, width=2)
d.text((RX0 + 10, RY0 + 6), "STORIES BY REGION", font=bold(12), fill=INK)
REGIONS = [("Europe", 5, BLUE), ("North America", 7, RED),
           ("Asia", 7, TEAL), ("Middle East", 6, GOLD),
           ("Africa", 5, GREEN), ("South America", 3, (120, 72, 30)),
           ("Global", 3, MUTED)]
yy = RY0 + 24
for name, cnt, col in REGIONS:
    d.text((RX0 + 10, yy), name, font=regular(11), fill=INK)
    bw = int(cnt / 7.0 * 150)
    d.rectangle([RX0 + 120, yy + 2, RX0 + 120 + bw, yy + 12], fill=col)
    d.text((RX0 + 278, yy), str(cnt), font=bold(12), fill=INK)
    yy += 13
d.text((RX0 + 10, yy + 2), "TOTAL  36 STORIES", font=bold(12), fill=RED)

# ---------------------------------------------------------------- briefs 14-36
BRIEFS = [
    (14, "RUSSIAN STRIKE KILLS 2 IN ODESA",
     "A Russian strike killed two and injured three, including a child, in Odesa overnight; an attack on Kyiv set fire to a block and injured two."),
    (15, "LIBYA VOWS RETALIATION AFTER TWO OFFICERS DIE",
     "Libya's army vowed retaliation after two naval officers died of wounds from Sunday's Ukrainian drone attack on the corvette Merkury at Benghazi."),
    (16, "MERZ WARNS RUSSIA WANTS MORE THAN UKRAINE",
     "Chancellor Merz told the Bundestag Russia is escalating threats to European security and \u201cwants more than Ukraine\u201d."),
    (17, "BBC: 490,334 RUSSIAN WAR DEAD",
     "At least 490,334 Russian soldiers have died since 2022, the BBC found in leaked government statistics drawn from over 11 million death records."),
    (18, "RUSSIAN DRONE ENTERS POLISH AIRSPACE",
     "A Russian drone entered Polish airspace overnight, days after three Russian missiles crossed into Poland on 20 November."),
    (19, "TUESDAY: ABREGO GARCIA LEAVES US FOR SPAIN",
     "Kilmar Abrego Garcia left the US for Spain on Tuesday night; Homeland Security said he self-deported, ending a nearly two-year legal fight."),
    (20, "TUESDAY: SULLIVAN CONCEDES ALASKA RACE TO PELTOLA",
     "Senator Dan Sullivan conceded to Mary Peltola on Tuesday; the Justice Department had abandoned its lawsuit over the Alaska race."),
    (21, "UNCLASSIFIED CIA SYSTEM BREACHED",
     "Hackers breached an unclassified CIA analysis system, an AP source said, and the Office of the Director of National Intelligence was also affected."),
    (22, "IOWA ARMY TO DETONATE FIVE TONS OF LEAD AZIDE",
     "The US Army will detonate 68 drums of lead azide, about five tons, at the Iowa Army Ammunition Plant at 9 a.m. on Wednesday."),
    (23, "TUESDAY: DOW CLOSES ABOVE 50,000 FOR FIRST TIME",
     "The Dow closed above 50,000 for the first time on Tuesday, up 0.9% to 50,018.70, while the Nasdaq fell 1.5% and the S&P 500 fell 0.5%."),
    (24, "TUESDAY: CHINA PROBES POLITBURO MEMBER CHEN JINING",
     "Shanghai party chief Chen Jining is under investigation, Xinhua said Tuesday; the fourth top leader probed since 2025."),
    (25, "BANGLADESH GARMENT WORKERS WIN 36% PAY RISE",
     "Bangladesh's wage board raised the garment minimum wage from 12,500 to 17,000 taka a month, a 36% rise, after weeks of protests."),
    (26, "HANOI RESTAURANT BLAST TOLL RISES TO SEVEN",
     "The toll from Tuesday's gas explosion at a Hanoi hotpot restaurant rose to seven dead and nine injured on Wednesday."),
    (27, "BUS CRASH KILLS 13 IN RAS AL KHAIMAH",
     "A bus hit a stationary truck in Ras Al Khaimah on Wednesday, killing 13 people and injuring 14."),
    (28, "IRAN FLOGS SINGER 74 TIMES OVER UNVEILED CONCERT",
     "Singer Parastoo Ahmadi and four team members were each given 74 lashes in Qom over an unveiled concert, reports said Wednesday."),
    (29, "POPE LAMENTS FAILURE OF COP31 CLIMATE TALKS",
     "Pope Leo XIV expressed concern over the failure of the UN COP31 climate talks to reach an agreement."),
    (30, "UN WARNS HIV GAINS COULD UNRAVEL",
     "The UN warned decades of progress against AIDS could reverse as international funding is cut."),
    (31, "ZAMBIA INDICTS OPPOSITION LEADER FOR TREASON",
     "Prosecutors indicted Zambia's main opposition leader and 12 others on treason charges over an alleged plot to overthrow the government."),
    (32, "DR CONGO HALTS COBALT EXPORTS AGAIN",
     "DR Congo will suspend cobalt exports from the end of the month to lift falling prices, its second such pause."),
    (33, "ARGENTINA ENTERS TECHNICAL RECESSION",
     "Argentina entered a technical recession after two straight quarters of contraction; activity fell 1.2% year on year in September."),
    (34, "TUESDAY: VENEZUELA REVEALS $237.5BN PUBLIC DEBT",
     "Venezuela put public debt at $237.5 billion in a framework published Tuesday, ahead of restructuring talks; police clashed with wage protesters."),
    (35, "BEPICOLOMBO REACHES MERCURY ORBIT",
     "The European-Japanese BepiColombo probe reached Mercury orbit on Wednesday after an eight-year journey since its 2018 launch."),
    (36, "SOORYAVANSHI, 15, SMASHES RECORD 204 OFF 53 BALLS",
     "Fifteen-year-old Vaibhav Sooryavanshi scored 204 off 53 balls for India A against the UAE in Doha, the fastest double century in List A cricket."),
]
d.text((8, 586), "THE DAY IN BRIEF  \u00b7  14\u201336", font=bold(14), fill=INK)
# red DATE CHECK box on the same row, right side
d.rectangle([700, 584, 1016, 604], outline=RED, width=2)
d.text((858, 588), "DATE CHECK \u00b7 25 NOV NEWS & FOLLOW-UPS",
       font=bold(9), fill=RED, anchor="ma")
d.line([8, 606, 1016, 606], fill=INK, width=1)
yy = 610
for num, title, body in BRIEFS:
    size = 11
    while size >= 9:
        fb, fr = bold(size), regular(size)
        head = "%d. %s  " % (num, title)
        if fb.getlength(head) + fr.getlength(body) <= 1000:
            break
        size -= 1
    else:
        fb, fr = bold(9), regular(9)
        head = "%d. %s  " % (num, title)
        words = body.split()
        while fb.getlength(head) + fr.getlength(body) > 1000 and len(words) > 8:
            words = words[:-2]
            body = " ".join(words) + "."
    d.text((8, yy), head, font=fb, fill=INK)
    d.text((8 + fb.getlength(head), yy), body, font=fr, fill=INK)
    yy += 16
assert yy <= 985, "briefs overflow: end y=%d" % yy

# ---------------------------------------------------------------- footer
d.line([8, 982, 1016, 982], fill=INK, width=1)
d.text((8, 988),
       "Map drawn from public coastline data; all other illustrations are hand-drawn flat-vector art made for this page. No photographs and no wire-service images are used.",
       font=regular(9), fill=MUTED)
d.text((8, 1001),
       "Sources: Reuters, AP, BBC, Al Jazeera, AFP, NYT, NPR, Xinhua, SCMP, VnExpress, Gulf News, France 24, Fox News, UPI, UN News, RFI, Africanews, Le Monde, MercoPress, ESA, BBC Sport, CNBC, The Hindu.",
       font=regular(9), fill=MUTED)
d.text((8, 1013),
       "Follow-ups are labelled in the item itself: Tuesday (10, 11, 19, 20, 23, 24, 34). All figures are as reported on 25 Nov 2026.",
       font=regular(9), fill=MUTED)

# ---------------------------------------------------------------- checks before save
img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
print("counts: headlines 3, small 10, briefs", len(BRIEFS),
      "total", 3 + 10 + len(BRIEFS),
      "regions total", sum(c for _, c, _ in REGIONS))
