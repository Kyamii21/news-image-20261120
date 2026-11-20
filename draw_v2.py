#!/usr/bin/env python3
"""Render entry.png for news-image-20261120 v2.

One 1024x1024 image summing up the world news of Friday 20 November 2026.
Drawn at 2x and downscaled for clean edges. Stories and sources: NOTES.md.
"""
from PIL import Image, ImageDraw, ImageFont
import math

S = 2  # supersampling factor
W = H = 1024

FONT_DIR = "/usr/share/fonts/truetype/noto/"
F_BLACK = FONT_DIR + "NotoSans-Black.ttf"
F_XBOLD = FONT_DIR + "NotoSans-ExtraBold.ttf"
F_BOLD = FONT_DIR + "NotoSans-Bold.ttf"
F_SEMI = FONT_DIR + "NotoSans-SemiBold.ttf"
F_MED = FONT_DIR + "NotoSans-Medium.ttf"

# palette
NAVY_DARK = (9, 26, 48)
NAVY = (16, 52, 102)
NAVY_MID = (24, 72, 138)
GOLD = (245, 184, 29)
PAPER = (244, 241, 234)
WHITE = (255, 255, 255)
INK = (20, 30, 44)
SUB = (52, 64, 82)
LIGHT_BLUE = (168, 200, 240)

img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


def tw(text, f):
    return d.textlength(text, font=f) / S


def fit(text, path, size, max_w):
    """Shrink font until text fits max_w (in 1024-space px)."""
    f = font(path, size)
    while tw(text, f) > max_w and size > 10:
        size -= 1
        f = font(path, size)
    return f


def text(x, y, s, f, fill, anchor="la"):
    d.text((x * S, y * S), s, font=f, fill=fill, anchor=anchor)


def rrect(box, r, fill):
    d.rounded_rectangle([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
                        radius=r * S, fill=fill)


def rect(box, fill):
    d.rectangle([box[0] * S, box[1] * S, box[2] * S, box[3] * S], fill=fill)


def line(pts, fill, width):
    d.line([(x * S, y * S) for x, y in pts], fill=fill, width=int(width * S))


def ellipse(box, fill=None, outline=None, width=1):
    d.ellipse([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
              fill=fill, outline=outline, width=int(width * S))


def poly(pts, fill):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill)


# ---------------------------------------------------------------- pictograms
def icon_cyclone(cx, cy, r, color, bg):
    # spiral of shrinking arcs
    for i in range(3):
        rr = r - i * r * 0.28
        box = [cx - rr, cy - rr, cx + rr, cy + rr]
        d.arc([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
              start=20 + i * 55, end=300 + i * 55, fill=color, width=int(7 * S))
    ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)


def icon_scales(cx, cy, r, color, bg):
    top = cy - r
    line([(cx, top), (cx, cy + r * 0.55)], color, 6)
    line([(cx - r * 0.85, top + 6), (cx + r * 0.85, top + 6)], color, 6)
    for sx in (-1, 1):
        px = cx + sx * r * 0.85
        line([(px, top + 6), (px - 13, cy + 2)], color, 4)
        line([(px, top + 6), (px + 13, cy + 2)], color, 4)
        d.arc([(px - 16) * S, (cy - 6) * S, (px + 16) * S, (cy + 16) * S],
              start=15, end=165, fill=color, width=int(6 * S))
    line([(cx - 16, cy + r * 0.62), (cx + 16, cy + r * 0.62)], color, 7)


def icon_tower(cx, cy, r, color, bg):
    w = r * 0.86
    # stepped skyscraper silhouette
    rect([cx - w / 2, cy - r * 0.55, cx + w / 2, cy + r], color)
    rect([cx - w * 0.32, cy - r, cx + w * 0.32, cy - r * 0.5], color)
    # windows punched out in the block colour
    for row in range(4):
        for col in range(2):
            wx = cx - w / 2 + 6 + col * (w / 2)
            wy = cy - r * 0.42 + row * (r * 0.34)
            rect([wx, wy, wx + 7, wy + 7], bg)
    rect([cx - 3.5, cy - r + 8, cx + 3.5, cy - r + 15], bg)
    # burst at top-right corner
    bx, by = cx + w / 2 + 10, cy - r * 0.72
    for ang in range(0, 360, 45):
        x2 = bx + 14 * math.cos(math.radians(ang))
        y2 = by + 14 * math.sin(math.radians(ang))
        line([(bx, by), (x2, y2)], GOLD, 5)


def icon_chart_down(cx, cy, r, color, bg):
    pts = [(cx - r, cy - r * 0.55), (cx - r * 0.35, cy - r * 0.1),
           (cx + r * 0.1, cy - r * 0.35), (cx + r * 0.85, cy + r * 0.6)]
    line(pts, color, 7)
    ax, ay = pts[-1]
    poly([(ax, ay), (ax - 20, ay - 2), (ax - 4, ay - 18)], color)
    line([(cx - r, cy + r * 0.85), (cx + r, cy + r * 0.85)], color, 4)


def icon_leaf(cx, cy, r, color, bg):
    # leaf: slim vesica from two arcs, rotated 45 deg so the tip points up-right
    pts = []
    for t in range(0, 181, 6):
        a = math.radians(t)
        pts.append((cx + r * 1.05 * math.cos(a) - r * 0.38,
                    cy - r * 0.62 * math.sin(a) + r * 0.16))
    for t in range(180, -1, -6):
        a = math.radians(t)
        pts.append((cx + r * 1.05 * math.cos(a) + r * 0.38,
                    cy + r * 0.62 * math.sin(a) - r * 0.16))
    rot = []
    for x, y in pts:
        dx, dy = x - cx, y - cy
        rot.append((cx + (dx - dy) * 0.7071, cy + (dx + dy) * 0.7071))
    poly(rot, color)
    # vein + stem in the block colour
    line([(cx - r * 0.95, cy + r * 0.95), (cx + r * 0.62, cy - r * 0.62)], bg, 5)


def icon_bubbles(cx, cy, r, color, bg):
    rrect([cx - r, cy - r * 0.85, cx + r * 0.25, cy + r * 0.15], 9, color)
    poly([(cx - r * 0.55, cy + r * 0.1), (cx - r * 0.55, cy + r * 0.55),
          (cx - r * 0.05, cy + r * 0.12)], color)
    rrect([cx - r * 0.1, cy - r * 0.05, cx + r, cy + r * 0.75], 9, None)
    d.rounded_rectangle([(cx - r * 0.1) * S, (cy - r * 0.05) * S,
                         (cx + r) * S, (cy + r * 0.75) * S],
                        radius=9 * S, outline=color, width=int(6 * S))


def icon_ballot(cx, cy, r, color, bg):
    # ballot paper sticking out of the box
    rect([cx - r * 0.42, cy - r * 0.95, cx + r * 0.42, cy - r * 0.05], color)
    rrect([cx - r * 0.88, cy - r * 0.12, cx + r * 0.88, cy + r * 0.85], 6, color)
    line([(cx - r * 0.6, cy + r * 0.05), (cx + r * 0.6, cy + r * 0.05)], bg, 5)
    # big check in the block colour
    line([(cx - 14, cy + r * 0.42), (cx - 4, cy + r * 0.62)], bg, 8)
    line([(cx - 4, cy + r * 0.62), (cx + 16, cy + r * 0.24)], bg, 8)


def icon_gamepad(cx, cy, r, color, bg):
    rrect([cx - r, cy - r * 0.62, cx + r, cy + r * 0.62], 22, color)
    # d-pad in the block colour
    px, py = cx - r * 0.48, cy
    rect([px - 6, py - 17, px + 6, py + 17], bg)
    rect([px - 17, py - 6, px + 17, py + 6], bg)
    for dx, dy in ((0.42, -0.26), (0.68, 0.02), (0.42, 0.3), (0.16, 0.02)):
        ellipse([cx + r * dx - 7, cy + r * dy - 7, cx + r * dx + 7, cy + r * dy + 7],
                fill=bg)


ICONS = {
    "cyclone": icon_cyclone,
    "scales": icon_scales,
    "tower": icon_tower,
    "chart": icon_chart_down,
    "leaf": icon_leaf,
    "bubbles": icon_bubbles,
    "ballot": icon_ballot,
    "gamepad": icon_gamepad,
}

# ------------------------------------------------------------------- masthead
rect([0, 0, W, 122], NAVY_DARK)
text(26, 14, "THE WORLD TODAY", font(F_BLACK, 56), WHITE)
text(28, 78, "FRIDAY, 20 NOVEMBER 2026", font(F_BOLD, 27), GOLD)
# Children's Day chip
rrect([712, 18, 998, 104], 14, GOLD)
text(855, 30, "WORLD", font(F_XBOLD, 26), NAVY_DARK, anchor="ma")
text(855, 60, "CHILDREN'S DAY", font(F_XBOLD, 26), NAVY_DARK, anchor="ma")
rect([0, 122, W, 130], GOLD)

# ----------------------------------------------------------------- lead panel
rect([0, 130, W, 414], NAVY)
text(26, 146, "LEAD STORY · SHENZHEN SUMMIT", font(F_BOLD, 23), GOLD)
text(24, 176, "3 POWERS ISSUE 'PEACE'", font(F_BLACK, 57), WHITE)
text(24, 238, "DECLARATION", font(F_BLACK, 57), WHITE)
text(26, 320, "Trump · Xi · Putin — first-ever 3-way summit", font(F_SEMI, 26), WHITE)
text(26, 352, "\"Nuclear war must never be fought\"", font(F_BOLD, 29), GOLD)
text(26, 386, "No word on Ukraine or Iran wars · UN reform · oil · courts",
     fit("No word on Ukraine or Iran wars · UN reform · oil · courts",
         F_SEMI, 23, 640), LIGHT_BLUE)

# globe + flags on the right of the lead panel
gx, gy, gr = 888, 218, 64
ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(84, 166, 230))
for k in (-0.55, 0, 0.55):
    wdt = gr * math.sqrt(max(0.05, 1 - k * k))
    d.ellipse([(gx - wdt) * S, (gy - gr) * S, (gx + wdt) * S, (gy + gr) * S],
              outline=WHITE, width=int(3 * S))
for k in (-0.5, 0, 0.5):
    yy = gy + k * gr
    wdt = gr * math.sqrt(max(0.05, 1 - k * k))
    line([(gx - wdt, yy), (gx + wdt, yy)], WHITE, 3)
ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=WHITE, width=4)


def flag_us(x, y, w, h):
    rect([x, y, x + w, y + h], (200, 40, 50))
    for i in range(3):
        rect([x, y + h * (0.18 + i * 0.3), x + w, y + h * (0.34 + i * 0.3)], WHITE)
    rect([x, y, x + w * 0.45, y + h * 0.55], (30, 50, 130))
    for r in range(3):
        for c in range(4):
            ellipse([x + 5 + c * 9, y + 4 + r * 8, x + 9 + c * 9, y + 8 + r * 8], fill=WHITE)


def flag_cn(x, y, w, h):
    rect([x, y, x + w, y + h], (205, 35, 40))
    ellipse([x + 8, y + 7, x + 24, y + 23], fill=GOLD)
    for dx, dy in ((30, 6), (34, 14), (34, 24), (30, 32)):
        ellipse([x + dx, y + dy, x + dx + 7, y + dy + 7], fill=GOLD)


def flag_ru(x, y, w, h):
    rect([x, y, x + w, y + h / 3], WHITE)
    rect([x, y + h / 3, x + w, y + 2 * h / 3], (40, 80, 180))
    rect([x, y + 2 * h / 3, x + w, y + h], (200, 40, 50))


flag_us(716, 312, 92, 50)
flag_cn(820, 312, 92, 50)
flag_ru(768, 368, 92, 40)

# ---------------------------------------------------------------------- cards
CARD_W, CARD_H = 494, 138
MARGIN, GAP = 14, 12
X0 = MARGIN
X1 = MARGIN + CARD_W + GAP


def card(x, y, color, icon, kicker, headline_lines, subline, w=CARD_W, h=CARD_H):
    rrect([x, y, x + w, y + h], 14, WHITE)
    # colour block (left), squared off on the right side
    d.rounded_rectangle([x * S, y * S, (x + 100) * S, (y + h) * S],
                        radius=14 * S, fill=color)
    rect([x + 86, y, x + 100, y + h], color)
    ICONS[icon](x + 50, y + h / 2, 34, WHITE, color)
    tx = x + 116
    max_w = w - 130
    text(tx, y + 13, kicker, fit(kicker, F_BOLD, 20, max_w), color)
    yy = y + 39
    for hl in headline_lines:
        text(tx, yy, hl, fit(hl, F_XBOLD, 31, max_w), INK)
        yy += 36
    text(tx, y + h - 34, subline, fit(subline, F_SEMI, 23, max_w), SUB)


RED = (208, 48, 38)
PURPLE = (118, 60, 180)
TEAL = (8, 122, 130)
CRIMSON = (178, 30, 55)
GREEN = (28, 138, 66)
BLUE = (30, 96, 196)
ORANGE = (222, 120, 20)
VIOLET = (96, 52, 190)

row_y = [422, 568, 714]
card(X0, row_y[0], RED, "cyclone", "INDIA · CYCLONE AKVAN",
     ["CYCLONE HITS ODISHA"], "300,000 evacuated · winds 100 km/h")
card(X1, row_y[0], PURPLE, "scales", "WORLD COURT · ICJ",
     ["MYANMAR GUILTY", "OF GENOCIDE"], "First such ruling · Rohingya case")
card(X0, row_y[1], TEAL, "tower", "MIDDLE EAST · RIYADH",
     ["MISSILE HITS", "TALLEST TOWER"], "Houthi strike on PIF Tower · no injuries")
card(X1, row_y[1], CRIMSON, "chart", "MARKETS · WALL STREET",
     ["DOW FALLS 1,101 PTS"], "Anthropic debut +17% fails to lift AI trade")
card(X0, row_y[2], GREEN, "leaf", "CLIMATE · COP31 ANTALYA",
     ["DEAL DROPS", "FOSSIL FUELS"], "Draft cut 144 to 80 points · final day")
card(X1, row_y[2], BLUE, "bubbles", "UKRAINE · BERLIN TALKS",
     ["EUROPE READY", "TO TALK"], "Leaders back talks with Russia on Ukraine")

# --------------------------------------------------------------- bottom split
by = 860
card(X0, by, ORANGE, "ballot", "EL SALVADOR · ELECTION 2027",
     ["BUKELE SEEKS 3RD TERM"], "Registers candidacy · polls 55–70%",
     w=CARD_W, h=150)
card(X1, by, VIOLET, "gamepad", "GAMING · GTA 6 LAUNCH",
     ["EST. $1.84 BILLION", "IN ONE DAY"], "19M copies · Sensor Tower estimate",
     w=CARD_W, h=150)

# ---------------------------------------------------------------------- output
out = img.resize((W, H), Image.LANCZOS)
out.save("entry.png", optimize=True)
out.resize((300, 300), Image.LANCZOS).save("preview-300.png")
print("entry.png + preview-300.png written")
