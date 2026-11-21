#!/usr/bin/env python3
"""Render entry.png for news-image-20261120 (v3).

One 1024x1024 front page summing up world news of Friday 20 November 2026.
Drawn fresh with Pillow; main.py (stdlib) copies the result byte-for-byte.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# --- palette -------------------------------------------------------------
BG        = (10, 17, 32)      # deep navy
PANEL     = (17, 28, 51)      # card fill
PANEL_ALT = (21, 34, 61)
INK       = (245, 247, 250)   # near white
MUTED     = (168, 182, 205)   # secondary text
FAINT     = (110, 128, 160)
RULE      = (58, 76, 112)

RED    = (255, 84, 84)
ORANGE = (255, 150, 66)
AMBER  = (255, 196, 66)
GREEN  = (92, 214, 140)
TEAL   = (64, 210, 196)
BLUE   = (96, 165, 255)
VIOLET = (188, 140, 255)
SLATE  = (150, 175, 220)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
F_XBOLD = "/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf"
F_BOLD  = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
F_COND  = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"
F_REG   = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, f, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def chip(draw, x, y, label, color, f):
    """Small category tag: colored bar + uppercase label."""
    draw.rectangle([x, y + 2, x + 10, y + 22], fill=color)
    draw.text((x + 18, y), label, font=f, fill=color)
    return y + 30


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

MARGIN = 36
CONTENT_W = W - 2 * MARGIN

# --- masthead ------------------------------------------------------------
d.rectangle([0, 0, W, 108], fill=(13, 22, 42))
d.rectangle([0, 108, W, 112], fill=AMBER)

f_mast = font(F_SERIF, 56)
d.text((MARGIN, 14), "THE WORLD TODAY", font=f_mast, fill=INK)

f_date = font(F_BOLD, 24)
date_s = "FRIDAY  ·  20 NOVEMBER 2026"
d.text((MARGIN, 76), date_s, font=f_date, fill=AMBER)

f_tag = font(F_COND, 23)
tag_s = "ONE DAY OF WORLD NEWS"
tw = text_w(d, tag_s, f_tag)
d.text((W - MARGIN - tw, 77), tag_s, font=f_tag, fill=MUTED)

# --- lead story ----------------------------------------------------------
lead_y = 128
lead_h = 222
d.rounded_rectangle([MARGIN, lead_y, W - MARGIN, lead_y + lead_h],
                    radius=14, fill=PANEL)
d.rectangle([MARGIN, lead_y, MARGIN + 10, lead_y + lead_h], fill=RED)

lx = MARGIN + 28
ly = lead_y + 16
ly = chip(d, lx, ly, "LEAD STORY · WAR IN EUROPE", RED, font(F_COND, 22))

f_lead = font(F_BLACK, 40)
lead_lines = wrap(d, "Russian Missiles Land in NATO Poland", f_lead, 640)
ly = draw_lines(d, lx, ly + 2, lead_lines, f_lead, INK, 46)

f_fact = font(F_REG, 20)
lead_fact = ("Two missiles and a jet drone came down in south-east Poland "
             "during Russia's biggest November strike on Ukraine. NATO "
             "called it a “grave violation”. No injuries in Poland.")
ly = draw_lines(d, lx, ly + 4, wrap(d, lead_fact, f_fact, 620),
                f_fact, MUTED, 27)

# stat chips on the right of the lead panel
stats = [("404", "drones fired\nat Ukraine"),
         ("111", "missiles in\nthe barrage"),
         ("3", "objects down\nin Poland")]
sx = W - MARGIN - 232
sy = lead_y + 20
for num, lab in stats:
    d.rounded_rectangle([sx, sy, sx + 208, sy + 56], radius=10,
                        fill=PANEL_ALT)
    d.text((sx + 14, sy + 4), num, font=font(F_BLACK, 36), fill=RED)
    nw = text_w(d, num, font(F_BLACK, 36))
    d.multiline_text((sx + 24 + nw, sy + 8), lab, font=font(F_REG, 17),
                     fill=MUTED, spacing=2)
    sy += 66

# --- story grid ----------------------------------------------------------
stories = [
    dict(cat="DIPLOMACY", color=TEAL,
         head="Trump Sells Shenzhen Summit",
         fact="First-ever US–China–Russia summit; 4-point peace deal.",
         big="80 min", biglab="of trilateral talks"),
    dict(cat="JUSTICE", color=VIOLET,
         head="Myanmar Guilty of Genocide",
         fact="9–6 vote; junta calls verdict “unfair”.",
         big="~10,000", biglab="Rohingya killed, 2017"),
    dict(cat="MARKETS", color=AMBER,
         head="AI Sell-Off: Stocks in Correction",
         fact="S&P -3.7%, Nasdaq -5.3%, Nikkei -5.1%.",
         big="-14%", biglab="Nvidia on Friday"),
    dict(cat="EUROPE", color=BLUE,
         head="UK and EU Seal “Reset” Deals",
         fact="Food trade, carbon link, 100k youth places/yr.",
         big="£5.1bn", biglab="a year, food deal"),
    dict(cat="MIDDLE EAST", color=ORANGE,
         head="Israeli Strikes Kill 6 in Gaza",
         fact="Hit despite ceasefire; 1,600+ dead since truce.",
         big="6 killed", biglab="in central Gaza"),
    dict(cat="CLIMATE", color=GREEN,
         head="COP31 Talks Run Into Overtime",
         fact="Draft drops fossil-fuel wording, $120bn target.",
         big="~200", biglab="nations deadlocked"),
    dict(cat="DISASTER", color=ORANGE,
         head="M6.7 Quake Shakes Peru",
         fact="19:09 near Cerro de Pasco; felt in Lima.",
         big="108 km", biglab="deep; no casualties"),
    dict(cat="US JUSTICE", color=VIOLET,
         head="Palisades Arsonist Found Guilty",
         fact="Retrial convicts Rinderknecht; ~6,800 buildings lost.",
         big="12", biglab="killed in the fire"),
    dict(cat="US POLITICS", color=SLATE,
         head="Judge Blocks Trump's $1bn Arch",
         fact="Second court halts 250-ft arch: “rushed job”.",
         big="$1bn", biglab="monument halted"),
]

grid_y = lead_y + lead_h + 12
cols, rows = 3, 3
gap = 14
card_w = (CONTENT_W - (cols - 1) * gap) // cols
card_h = 192

f_cat = font(F_COND, 20)
f_head = font(F_XBOLD, 25)
f_fact_c = font(F_REG, 18)
f_big = font(F_BLACK, 28)
f_biglab = font(F_REG, 15)

for i, s in enumerate(stories):
    cx = MARGIN + (i % cols) * (card_w + gap)
    cy = grid_y + (i // cols) * (card_h + gap)
    d.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=12,
                        fill=PANEL)
    d.rectangle([cx, cy, cx + card_w, cy + 6], fill=s["color"])
    px = cx + 16
    py = cy + 15
    py = chip(d, px, py, s["cat"], s["color"], f_cat)
    py = draw_lines(d, px, py + 2, wrap(d, s["head"], f_head, card_w - 32),
                    f_head, INK, 30)
    py = draw_lines(d, px, py + 3, wrap(d, s["fact"], f_fact_c, card_w - 32),
                    f_fact_c, MUTED, 23)
    # big number pinned to the card's bottom edge; facts are kept to
    # two lines so the two never collide
    by = cy + card_h - 40
    d.text((px, by), s["big"], font=f_big, fill=s["color"])
    bw = text_w(d, s["big"], f_big)
    d.text((px + bw + 10, by + 11), s["biglab"], font=f_biglab, fill=FAINT)

# --- footer --------------------------------------------------------------
foot_y = grid_y + rows * card_h + (rows - 1) * gap + 8
d.rectangle([MARGIN, foot_y, W - MARGIN, foot_y + 2], fill=RULE)
f_foot = font(F_COND, 21)
foot_l = "FRIDAY 20 NOVEMBER 2026 — THE DAY IN ONE PAGE"
d.text((MARGIN, foot_y + 12), foot_l, font=f_foot, fill=MUTED)
foot_r = "SOURCES: AP · REUTERS · AFP · UN · USGS"
fw = text_w(d, foot_r, f_foot)
d.text((W - MARGIN - fw, foot_y + 12), foot_r, font=f_foot, fill=FAINT)

img.save("entry.png", optimize=True)
print("entry.png written")

# 300px legibility preview
img.resize((300, 300), Image.LANCZOS).save("preview-300.png")
print("preview-300.png written")
