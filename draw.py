#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news image (1024x1024).

Design: one dominant lead panel (Shenzhen peace declaration) over five
large secondary cards. No text below 28 px. Every text draw is width
audited: the render fails loudly if a line would overflow its box.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

INK = (12, 18, 32)
PAPER = (250, 248, 242)
YELLOW = (255, 201, 40)
LEAD_BG = (13, 47, 110)
LEAD_PANEL = (18, 68, 150)


def font(size, bold=True):
    assert size >= 28, f"text below 28px forbidden: {size}"
    return ImageFont.truetype(BOLD if bold else REG, size)


def text(draw, xy, s, size, fill, box_w, bold=True, anchor="la"):
    f = font(size, bold)
    w = draw.textlength(s, font=f)
    assert w <= box_w, f"OVERFLOW {w:.0f}px > {box_w}px: {s!r} @{size}px"
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)
    return w


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=3)
    for i in range(7):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 0.5) * h / 7], fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.42, y + h * 0.54], fill=(30, 45, 120))
    for r in range(3):
        for c in range(4):
            cx, cy = x + 12 + c * (w * 0.42 - 20) / 3, y + 10 + r * (h * 0.54 - 18) / 2
            d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 20, 30), outline=INK, width=3)
    d.ellipse([x + 14, y + 10, x + 34, y + 30], fill=YELLOW)
    for dx, dy in [(48, 8), (56, 18), (56, 32), (48, 42)]:
        d.ellipse([x + dx, y + dy, x + dx + 9, y + dy + 9], fill=YELLOW)


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3)
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(30, 80, 180))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(200, 30, 45))


def globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 160, 230), outline=(255, 255, 255), width=6)
    d.ellipse([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r], outline=(255, 255, 255), width=4)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=4)
    for dy in (-0.55, 0.55):
        yy = cy + dy * r
        half = r * math.sqrt(1 - dy * dy)
        d.line([cx - half, yy, cx + half, yy], fill=(255, 255, 255), width=4)


def cyclone(d, cx, cy, r, color):
    pts = []
    steps = 90
    for i in range(steps + 1):
        t = i / steps
        ang = t * 4.2 * math.pi
        rr = 6 + t * (r - 6)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.line(pts, fill=color, width=13, joint="curve")
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=color)


def scales(d, cx, cy, s, color):
    d.line([cx, cy - s, cx, cy + s * 0.7], fill=color, width=10)
    d.line([cx - s, cy - s * 0.75, cx + s, cy - s * 0.75], fill=color, width=10)
    for sx in (-1, 1):
        px = cx + sx * s
        d.line([px, cy - s * 0.75, px - s * 0.32, cy - s * 0.05], fill=color, width=6)
        d.line([px, cy - s * 0.75, px + s * 0.32, cy - s * 0.05], fill=color, width=6)
        d.arc([px - s * 0.38, cy - s * 0.28, px + s * 0.38, cy + s * 0.3], 15, 165, fill=color, width=8)
    d.line([cx - s * 0.5, cy + s * 0.85, cx + s * 0.5, cy + s * 0.85], fill=color, width=10)


def clock(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=12)
    d.line([cx, cy, cx, cy - r * 0.62], fill=color, width=10)
    d.line([cx, cy, cx + r * 0.45, cy + r * 0.25], fill=color, width=10)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=color)


def bubbles(d, x, y, color):
    d.rounded_rectangle([x, y, x + 62, y + 44], 14, fill=color)
    d.polygon([(x + 12, y + 42), (x + 12, y + 62), (x + 34, y + 42)], fill=color)
    d.rounded_rectangle([x + 40, y + 38, x + 102, y + 82], 14, outline=color, width=8)
    d.polygon([(x + 90, y + 80), (x + 90, y + 100), (x + 68, y + 80)], fill=color)


def controller(d, x, y, color):
    d.rounded_rectangle([x, y, x + 190, y + 92], 42, fill=color)
    d.rectangle([x + 38, y + 38, x + 74, y + 52], fill=PAPER)
    d.rectangle([x + 49, y + 27, x + 63, y + 63], fill=PAPER)
    for dx, dy, c in [(140, 24, (255, 90, 90)), (162, 45, YELLOW), (118, 45, (90, 220, 140)), (140, 66, (90, 170, 255))]:
        d.ellipse([x + dx, y + dy, x + dx + 16, y + dy + 16], fill=c)


def card(d, x, y, w, h, bg, fg, kicker, lines, sub, big=None):
    """Card with a 120px icon column on the left; text never enters it."""
    d.rounded_rectangle([x, y, x + w, y + h], 22, fill=bg)
    tx = x + 120
    tw = w - 120 - 20
    text(d, (tx, y + 14), kicker, 28, fg, tw)
    yy = y + 50
    for ln in lines:
        text(d, (tx, yy), ln, 38, fg, tw)
        yy += 46
    if big:
        text(d, (tx, yy), big, 54, fg, tw)
        yy += 62
    text(d, (tx, yy + 2), sub, 28, fg, tw, bold=False)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    text(d, (28, 14), "THE WORLD TODAY", 62, (255, 255, 255), 620)
    text(d, (28, 76), "FRIDAY 20 NOVEMBER 2026", 34, YELLOW, 620)
    d.rounded_rectangle([700, 22, 996, 96], 16, fill=YELLOW)
    text(d, (848, 32), "WORLD", 28, INK, 280, anchor="ma")
    text(d, (848, 62), "CHILDREN'S DAY", 28, INK, 280, anchor="ma")

    # ---- Lead panel ----
    d.rectangle([0, 118, W, 540], fill=LEAD_BG)
    d.rectangle([0, 118, W, 132], fill=YELLOW)
    text(d, (28, 146), "LEAD STORY · SHENZHEN", 30, YELLOW, 600)
    text(d, (28, 182), "3 ISSUE 'PEACE'", 78, (255, 255, 255), 640)
    text(d, (28, 262), "DECLARATION", 78, (255, 255, 255), 640)
    text(d, (28, 352), "Trump · Xi · Putin — first 3-way summit", 34, (255, 255, 255), 640, bold=False)
    text(d, (28, 392), '"Nuclear war must never be fought"', 36, YELLOW, 640)
    text(d, (28, 438), "But no mention of Ukraine or Iran wars", 34, (255, 255, 255), 640)
    text(d, (28, 480), "4-point declaration: UN reform · oil · courts", 30, (190, 215, 255), 640, bold=False)
    globe(d, 815, 248, 100)
    flag_us(d, 668, 372, 128, 80)
    flag_cn(d, 812, 372, 128, 80)
    flag_ru(d, 740, 460, 128, 62)

    # ---- Secondary cards ----
    # Row 1
    card(d, 16, 556, 488, 196, (255, 255, 255), INK, "INDIA · AKVAN",
         ["CYCLONE LANDS"], "evacuated in Odisha", big="300,000")
    cyclone(d, 72, 654, 46, (220, 60, 40))
    card(d, 520, 556, 488, 196, (255, 255, 255), INK, "WORLD COURT · ICJ",
         ["MYANMAR GUILTY"], "First ever: Rohingya", big="GENOCIDE")
    scales(d, 578, 650, 36, (120, 70, 180))
    # Row 2
    card(d, 16, 764, 488, 130, (255, 240, 210), INK, "IRAN WAR",
         ["TRUMP: NO RUSH"], "Decision waits to 2027")
    clock(d, 72, 829, 40, (200, 120, 10))
    card(d, 520, 764, 488, 130, (225, 240, 255), INK, "UKRAINE · EUROPE",
         ["READY TO TALK"], "Back talks with Russia")
    bubbles(d, 532, 788, (20, 90, 180))
    # Wide card
    d.rounded_rectangle([16, 906, 1008, 1008], 22, fill=(30, 30, 38))
    text(d, (40, 922), "GTA 6: EST. $1.84 BILLION IN A DAY", 36, (255, 255, 255), 730)
    text(d, (40, 966), "19M copies · Sensor Tower estimate", 28, (200, 200, 210), 730, bold=False)
    controller(d, 792, 910, (110, 60, 200))

    img.save("entry.png", optimize=True)
    img.resize((300, 300), Image.LANCZOS).save("preview-300.png", optimize=True)
    print("rendered entry.png + preview-300.png")


if __name__ == "__main__":
    main()
