#!/usr/bin/env python3
"""Draw THE WORLD front page for Wednesday 25 November 2026.

Pure Pillow, system fonts only, no network, no timestamps: two runs
produce byte-identical PNGs. Run: python3 draw_poster.py
Writes entry.png next to this script.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width

PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (164, 30, 34)
BLUE = (31, 58, 95)
GREY = (90, 88, 82)
LIGHT_GREY = (120, 118, 110)
SKY = (176, 208, 224)
SEA = (46, 92, 122)
DARK_SKY = (24, 38, 66)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(text, fnt, max_w, draw):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def flame(draw, cx, base_y, w, h):
    """Layered flame: red outer, orange mid, yellow core."""
    draw.polygon(
        [(cx - w // 2, base_y), (cx - w // 4, base_y - h),
         (cx, base_y - h - h // 4), (cx + w // 4, base_y - h),
         (cx + w // 2, base_y)],
        fill=(200, 60, 20))
    draw.polygon(
        [(cx - w // 3, base_y), (cx - w // 6, base_y - int(h * 0.7)),
         (cx, base_y - h), (cx + w // 6, base_y - int(h * 0.7)),
         (cx + w // 3, base_y)],
        fill=(240, 140, 30))
    draw.polygon(
        [(cx - w // 5, base_y), (cx, base_y - int(h * 0.55)),
         (cx + w // 5, base_y)],
        fill=(250, 210, 80))


def smoke(draw, x, y, puffs, color=(150, 148, 142)):
    for i, (dx, dy, r) in enumerate(puffs):
        shade = tuple(max(0, c - i * 6) for c in color)
        draw.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r],
                     fill=shade)


def bird(draw, x, y, s=8, fill=INK):
    draw.arc([x - s, y - s // 2, x, y + s // 2], 200, 340, fill=fill, width=2)
    draw.arc([x, y - s // 2, x + s, y + s // 2], 200, 340, fill=fill, width=2)


def sky_band(draw, box, top, bottom):
    """Vertical gradient sky inside box."""
    x0, y0, x1, y1 = box
    steps = y1 - y0
    for i in range(steps):
        t = i / max(1, steps - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


# ---------------------------------------------------------------- art pieces

def art_lead(draw, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sky_band(draw, box, (232, 190, 130), (196, 140, 100))
    # sun low on the horizon
    draw.ellipse([x0 + w - 110, y0 + 26, x0 + w - 62, y0 + 74],
                 fill=(250, 200, 90))
    # clouds
    for cx, cy, r in [(x0 + 60, y0 + 30, 16), (x0 + 90, y0 + 24, 20),
                      (x0 + 250, y0 + 44, 14), (x0 + 280, y0 + 38, 18)]:
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                     fill=(245, 235, 220))
    bird(draw, x0 + 150, y0 + 34)
    bird(draw, x0 + 180, y0 + 26, s=6)
    bird(draw, x0 + 330, y0 + 30, s=7)
    # refinery towers on the right shore
    shore_y = y0 + int(h * 0.52)
    draw.rectangle([x0, shore_y, x1, y0 + int(h * 0.60)], fill=(70, 60, 52))
    for tx in (x1 - 120, x1 - 96, x1 - 72):
        draw.rectangle([tx, shore_y - 52, tx + 14, shore_y], fill=(58, 52, 46))
        draw.rectangle([tx + 2, shore_y - 62, tx + 12, shore_y - 52],
                       fill=(58, 52, 46))
    smoke(draw, x1 - 100, shore_y - 78,
          [(0, 0, 12), (10, -14, 14), (24, -26, 16), (40, -36, 18)])
    # sea
    draw.rectangle([x0, y0 + int(h * 0.60), x1, y1], fill=SEA)
    for wy in range(y0 + int(h * 0.64), y1 - 6, 14):
        for wx in range(x0 + 8, x1 - 20, 46):
            draw.arc([wx, wy, wx + 30, wy + 8], 0, 180, fill=(140, 190, 210),
                     width=2)
    # tanker 1 (left, burning)
    hx, hy = x0 + 30, y0 + int(h * 0.66)
    draw.rectangle([hx, hy, hx + 190, hy + 26], fill=(40, 38, 36))
    draw.rectangle([hx + 6, hy - 14, hx + 60, hy], fill=(120, 40, 30))
    draw.rectangle([hx + 150, hy - 22, hx + 184, hy], fill=(200, 200, 195))
    for px in range(hx + 154, hx + 182, 8):
        draw.rectangle([px, hy - 18, px + 4, hy - 12], fill=(40, 60, 90))
    draw.rectangle([hx + 96, hy - 8, hx + 104, hy], fill=(90, 88, 82))
    flame(draw, hx + 60, hy - 12, 34, 52)
    flame(draw, hx + 100, hy - 6, 22, 34)
    smoke(draw, hx + 60, hy - 66, [(0, 0, 12), (-8, -14, 14), (-18, -26, 16)])
    # tanker 2 (right, burning)
    hx2, hy2 = x0 + 250, y0 + int(h * 0.74)
    draw.rectangle([hx2, hy2, hx2 + 160, hy2 + 22], fill=(52, 48, 44))
    draw.rectangle([hx2 + 8, hy2 - 12, hx2 + 52, hy2], fill=(30, 70, 110))
    draw.rectangle([hx2 + 118, hy2 - 18, hx2 + 148, hy2], fill=(200, 200, 195))
    flame(draw, hx2 + 30, hy2 - 10, 30, 46)
    flame(draw, hx2 + 130, hy2 - 16, 24, 38)
    smoke(draw, hx2 + 130, hy2 - 56, [(0, 0, 11), (8, -12, 13), (18, -22, 15)])
    # small patrol boat
    bx, by = x0 + 210, y0 + int(h * 0.88)
    draw.polygon([(bx, by), (bx + 44, by), (bx + 36, by + 10), (bx + 8, by + 10)],
                 fill=(200, 200, 195))
    draw.rectangle([bx + 14, by - 8, bx + 28, by], fill=(200, 200, 195))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def art_tariffs(draw, box):
    x0, y0, x1, y1 = box
    sky_band(draw, box, (214, 228, 238), (176, 200, 216))
    # globe
    cx, cy, r = x0 + 42, y0 + 44, 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 140, 180),
                 outline=INK, width=2)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(220, 230, 240), width=1)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(220, 230, 240), width=1)
    draw.arc([cx - r + 6, cy - r + 4, cx + r - 6, cy + r - 4], 200, 340,
             fill=(60, 160, 90), width=3)
    draw.arc([cx - r + 10, cy - r + 12, cx + r - 10, cy + r - 12], 20, 160,
             fill=(60, 160, 90), width=3)
    # stacked containers (kept inside the 150px art box)
    cols = [(200, 70, 50), (40, 90, 140), (60, 130, 80), (180, 140, 40)]
    base_y = y1 - 14
    for row in range(3):
        for col in range(3 - row):
            c = cols[(row + col) % 4]
            px = x0 + 78 + col * 24 + row * 6
            py = base_y - (row + 1) * 22
            draw.rectangle([px, py, px + 22, py + 20], fill=c, outline=INK, width=1)
            for lx in range(px + 5, px + 20, 5):
                draw.line([(lx, py + 2), (lx, py + 18)], fill=(0, 0, 0, 60), width=1)
    # rate tag
    draw.rectangle([x0 + 96, y0 + 8, x0 + 154, y0 + 30], fill=RED)
    draw.text((x0 + 101, y0 + 11), "20-40%", font=SANS_B(13), fill=(255, 255, 255))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def art_huawei(draw, box):
    x0, y0, x1, y1 = box
    sky_band(draw, box, (226, 224, 214), (196, 190, 176))
    # courthouse
    draw.polygon([(x0 + 14, y0 + 34), (x0 + 76, y0 + 10), (x0 + 138, y0 + 34)],
                 fill=(150, 140, 120), outline=INK, width=2)
    draw.ellipse([x0 + 68, y0 + 18, x0 + 84, y0 + 32], fill=(90, 80, 66))
    for i, cx in enumerate((x0 + 28, x0 + 56, x0 + 96, x0 + 124)):
        draw.rectangle([cx - 6, y0 + 36, cx + 6, y0 + 84], fill=(220, 212, 196),
                       outline=INK, width=1)
    draw.rectangle([x0 + 14, y0 + 84, x0 + 138, y0 + 90], fill=(150, 140, 120),
                   outline=INK, width=1)
    for sy in range(3):
        draw.rectangle([x0 + 10, y0 + 92 + sy * 6, x0 + 142, y0 + 97 + sy * 6],
                       fill=(120, 112, 96))
    # gavel
    draw.rectangle([x0 + 96, y0 + 98, x0 + 128, y0 + 106], fill=(90, 60, 30),
                   outline=INK, width=1)
    draw.line([(x0 + 112, y0 + 106), (x0 + 122, y0 + 118)], fill=(90, 60, 30),
              width=4)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def art_space(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=DARK_SKY)
    # stars
    for sx, sy, r in [(x0 + 14, y0 + 14, 2), (x0 + 40, y0 + 30, 1),
                      (x0 + 70, y0 + 12, 2), (x0 + 110, y0 + 22, 1),
                      (x0 + 132, y0 + 44, 2), (x0 + 26, y0 + 52, 1),
                      (x0 + 96, y0 + 60, 1), (x0 + 140, y0 + 70, 2),
                      (x0 + 58, y0 + 74, 1), (x0 + 120, y0 + 8, 1)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    # Earth curve, clipped inside the art box: arc of a circle whose
    # centre sits below the box, so no pixel leaves the frame.
    import math
    ecx, ecy, er = x0 + 75, y1 + 110, 130
    pts = []
    for deg in range(237, 304, 3):
        a = math.radians(deg)
        pts.append((ecx + er * math.cos(a), ecy + er * math.sin(a)))
    pts.append((x1, y1))
    pts.append((x0, y1))
    draw.polygon(pts, fill=(50, 110, 170))
    draw.line(pts[:-2], fill=(140, 190, 230), width=2)
    draw.arc([ecx - er, ecy - er, ecx + er, ecy + er], 258, 282,
             fill=(90, 170, 110), width=4)
    # rocket
    rx, ry = x0 + 96, y0 + 26
    draw.polygon([(rx, ry), (rx - 9, ry + 18), (rx + 9, ry + 18)],
                 fill=(200, 40, 40))
    draw.rectangle([rx - 9, ry + 18, rx + 9, ry + 52], fill=(235, 235, 230),
                   outline=INK, width=1)
    draw.ellipse([rx - 4, ry + 30, rx + 4, ry + 38], fill=(120, 180, 220),
                 outline=INK, width=1)
    draw.polygon([(rx - 9, ry + 44), (rx - 18, ry + 58), (rx - 9, ry + 52)],
                 fill=(200, 40, 40))
    draw.polygon([(rx + 9, ry + 44), (rx + 18, ry + 58), (rx + 9, ry + 52)],
                 fill=(200, 40, 40))
    flame(draw, rx, ry + 58, 16, 22)
    # station modules
    draw.rectangle([x0 + 12, y0 + 66, x0 + 58, y0 + 78], fill=(200, 200, 195),
                   outline=INK, width=1)
    draw.ellipse([x0 + 58, y0 + 64, x0 + 74, y0 + 80], fill=(180, 180, 175),
                 outline=INK, width=1)
    draw.rectangle([x0 + 20, y0 + 58, x0 + 50, y0 + 66], fill=(40, 80, 160),
                   outline=INK, width=1)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def art_cairo(draw, box):
    x0, y0, x1, y1 = box
    sky_band(draw, box, (240, 200, 150), (214, 170, 130))
    # skyline
    for bx, bw, bh in [(x0 + 4, 22, 34), (x0 + 30, 16, 46), (x0 + 50, 26, 28),
                       (x0 + 118, 20, 40), (x0 + 140, 14, 30)]:
        draw.rectangle([bx, y1 - 62 - bh, bx + bw, y1 - 62], fill=(120, 104, 88))
        for wy in range(y1 - 62 - bh + 6, y1 - 66, 10):
            for wx in range(bx + 4, bx + bw - 4, 8):
                draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 220, 140))
    # road
    draw.polygon([(x0, y1 - 62), (x1, y1 - 62), (x1, y1), (x0, y1)],
                 fill=(70, 68, 64))
    draw.line([(x0, y1 - 30), (x1, y1 - 30)], fill=(240, 230, 200), width=2)
    for dx in range(6, 150, 26):
        draw.line([(x0 + dx, y1 - 12), (x0 + dx + 12, y1 - 12)],
                  fill=(240, 230, 200), width=3)
    # tipped tanker truck
    tx, ty = x0 + 26, y1 - 56
    draw.ellipse([tx, ty, tx + 62, ty + 18], fill=(180, 60, 40), outline=INK, width=2)
    draw.rectangle([tx + 62, ty - 6, tx + 92, ty + 14], fill=(200, 200, 195),
                   outline=INK, width=1)
    draw.rectangle([tx + 66, ty - 2, tx + 76, ty + 6], fill=(120, 180, 220))
    draw.ellipse([tx + 70, ty + 12, tx + 80, ty + 22], fill=(20, 20, 20))
    flame(draw, tx + 30, ty, 40, 46)
    flame(draw, tx + 58, ty + 2, 26, 32)
    smoke(draw, tx + 40, ty - 44, [(0, 0, 11), (10, -12, 13), (22, -20, 15)])
    # small cars caught in the fire
    for cx in (x0 + 104, x0 + 128):
        draw.rectangle([cx, y1 - 26, cx + 20, y1 - 16], fill=(40, 60, 110))
        draw.ellipse([cx + 3, y1 - 16, cx + 8, y1 - 11], fill=(20, 20, 20))
        draw.ellipse([cx + 13, y1 - 16, cx + 18, y1 - 11], fill=(20, 20, 20))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def art_solomons(draw, box):
    x0, y0, x1, y1 = box
    sky_band(draw, box, (200, 222, 236), (168, 196, 214))
    # ground
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(90, 130, 80))
    # Australia flag (stylised): blue field, stars, Union Jack corner
    fx, fy = x0 + 14, y0 + 16
    draw.rectangle([fx, fy, fx + 56, fy + 34], fill=(20, 40, 120), outline=INK, width=1)
    draw.rectangle([fx, fy, fx + 26, fy + 16], fill=(200, 40, 40))
    draw.line([(fx, fy), (fx + 26, fy + 16)], fill=(255, 255, 255), width=2)
    draw.line([(fx + 26, fy), (fx, fy + 16)], fill=(255, 255, 255), width=2)
    for sx, sy in [(fx + 44, fy + 10), (fx + 38, fy + 24), (fx + 50, fy + 26)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    draw.line([(fx + 2, fy + 34), (fx + 2, y1 - 26)], fill=INK, width=2)
    # Solomon Islands flag (stylised): blue over green, diagonal, stars
    gx, gy = x0 + 82, y0 + 16
    draw.rectangle([gx, gy, gx + 56, gy + 34], fill=(30, 120, 70), outline=INK, width=1)
    draw.polygon([(gx, gy), (gx + 56, gy), (gx, gy + 34)], fill=(20, 60, 160))
    for sx, sy in [(gx + 14, gy + 10), (gx + 26, gy + 8), (gx + 20, gy + 20),
                   (gx + 34, gy + 14), (gx + 44, gy + 10)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    draw.line([(gx + 2, gy + 34), (gx + 2, y1 - 26)], fill=INK, width=2)
    # treaty document
    dx, dy = x0 + 52, y1 - 52
    draw.rectangle([dx, dy, dx + 48, dy + 30], fill=(250, 246, 236),
                   outline=INK, width=1)
    draw.line([(dx + 8, dy + 8), (dx + 40, dy + 8)], fill=INK, width=1)
    draw.line([(dx + 8, dy + 14), (dx + 40, dy + 14)], fill=INK, width=1)
    draw.line([(dx + 8, dy + 20), (dx + 28, dy + 20)], fill=INK, width=1)
    draw.ellipse([dx + 34, dy + 19, dx + 42, dy + 27], fill=RED, outline=INK, width=1)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def art_sudan(draw, box):
    x0, y0, x1, y1 = box
    sky_band(draw, box, (238, 214, 170), (216, 186, 140))
    # rooftops
    for bx, bw, bh in [(x0 + 4, 34, 26), (x0 + 42, 28, 34), (x0 + 74, 36, 22),
                       (x0 + 114, 30, 30)]:
        draw.rectangle([bx, y1 - 30 - bh, bx + bw, y1 - 30], fill=(150, 120, 88))
        draw.polygon([(bx, y1 - 30 - bh), (bx + bw // 2, y1 - 40 - bh),
                      (bx + bw, y1 - 30 - bh)], fill=(110, 84, 60))
        draw.rectangle([bx + 8, y1 - 44, bx + 14, y1 - 38], fill=(60, 50, 40))
    draw.rectangle([x0, y1 - 30, x1, y1], fill=(120, 100, 70))
    # dust clouds from strikes
    smoke(draw, x0 + 40, y1 - 52, [(0, 0, 10), (12, -8, 12), (24, -14, 13)],
          color=(190, 170, 140))
    smoke(draw, x0 + 108, y1 - 56, [(0, 0, 9), (-10, -8, 11), (-20, -14, 12)],
          color=(190, 170, 140))
    # drone silhouette
    dx, dy = x0 + 72, y0 + 22
    draw.ellipse([dx - 16, dy - 5, dx + 16, dy + 5], fill=(40, 40, 40))
    draw.ellipse([dx - 4, dy - 8, dx + 4, dy + 8], fill=(60, 60, 60))
    for ox in (-22, 22):
        draw.line([(dx + ox - 10, dy - 4), (dx + ox + 10, dy - 4)],
                  fill=(40, 40, 40), width=2)
        draw.ellipse([dx + ox - 4, dy - 8, dx + ox + 4, dy], fill=(40, 40, 40))
    draw.line([(dx, dy + 5), (dx, dy + 14)], fill=(40, 40, 40), width=2)
    draw.ellipse([dx - 3, dy + 14, dx + 3, dy + 20], fill=(40, 40, 40))
    bird(draw, x0 + 18, y0 + 18, s=6)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---------------------------------------------------------------- layout

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    mast = SERIF_B(86)
    d.text((W // 2, 26), "THE WORLD", font=mast, fill=INK, anchor="ma")
    hrule(d, MARGIN, W - MARGIN, 128, width=3)
    d.text((MARGIN, 134), "No. 330", font=SANS(13), fill=GREY)
    d.text((W // 2, 134), "WEDNESDAY, 25 NOVEMBER 2026",
           font=SANS_B(15), fill=INK, anchor="ma")
    d.text((W - MARGIN, 134), "WORLD EDITION", font=SANS(13), fill=GREY,
           anchor="ra")
    hrule(d, MARGIN, W - MARGIN, 158, width=1)

    # ---- lead story
    y = 168
    d.text((MARGIN, y), "LEAD STORY  —  THE MIDDLE EAST",
           font=SANS_B(13), fill=RED)
    y += 22
    art_lead(d, (MARGIN, y, MARGIN + 442, y + 240))
    tx = MARGIN + 458
    tw = W - MARGIN - tx
    head_lines = wrap("TANKERS ABLAZE IN HORMUZ AS WAR SPREADS TO "
                      "SAUDI OIL HEARTLAND", SERIF_B(29), tw, d)
    y2 = draw_lines(d, head_lines, tx, y + 2, SERIF_B(29), INK, 35)
    hrule(d, tx, W - MARGIN, y2 + 6, width=1, fill=GREY)
    summary = ("Iran's Revolutionary Guards Navy said two oil tankers struck "
               "naval mines and caught fire in the Strait of Hormuz. The same "
               "day Yemen's Houthis said they hit Ras Tanura, Saudi Arabia's "
               "largest refinery, a day after a strike on a Riyadh tower "
               "injured 11 people.")
    draw_lines(d, wrap(summary, SANS(16), tw, d), tx, y2 + 16, SANS(16),
               INK, 21)
    lead_bottom = y + 240

    # ---- grid 2x3
    hrule(d, MARGIN, W - MARGIN, lead_bottom + 12, width=2)
    stories = [
        ("TRADE — WASHINGTON", "TRUMP HITS 14 PARTNERS WITH NEW TARIFFS",
         "New duties proposed after an eight-month probe into 'excess "
         "industrial capacity'. Top rates of 20-40%; trade deals generally "
         "cap them at 10-20%.", art_tariffs),
        ("TECH — NEW YORK", "HUAWEI GUILTY ON 10 OF 12 COUNTS",
         "A Brooklyn jury convicts on fraud and sanctions charges, but "
         "clears the firm of racketeering. Sentencing set for 14 September "
         "2027.", art_huawei),
        ("SPACE — JIUQUAN", "PAKISTAN'S FIRST ASTRONAUT REACHES TIANGONG",
         "Shenzhou-24 docks about 3.5 hours after launch. Muhammad Zeeshan "
         "Ali is the first foreign astronaut ever to visit the station.",
         art_space),
        ("DISASTER — CAIRO", "31 KILLED AS TANKER FIRE ENGULFS RING ROAD",
         "A fuel tanker overturns and burns in Al-Warraq, Giza; 21 injured "
         "and 27 vehicles caught in the flames, officials say.", art_cairo),
        ("DIPLOMACY — CANBERRA",
         "AUSTRALIA LOCKS IN SOLOMONS AS TOP SECURITY PARTNER",
         "A treaty signed by Albanese and Wale makes Australia the primary "
         "security partner and bars any foreign military base on the "
         "islands.", art_solomons),
        ("CONFLICT — SUDAN", "19 CIVILIANS KILLED IN SUDAN DRONE STRIKES",
         "RSF drones hit Damazin and Roseires in Blue Nile state, striking "
         "homes, power facilities and a dam. Twenty more were wounded.",
         art_sudan),
    ]
    grid_y = lead_bottom + 24
    cell_w = (CW - 16) // 2
    cell_h = 128
    gap = 6
    for i, (kicker, headline, body, art) in enumerate(stories):
        row, col = divmod(i, 2)
        cx = MARGIN + col * (cell_w + 16)
        cy = grid_y + row * (cell_h + gap)
        art(d, (cx, cy + 16, cx + 150, cy + 16 + 110))
        tx2 = cx + 162
        tw2 = cx + cell_w - tx2
        d.text((tx2, cy), kicker, font=SANS_B(11), fill=RED)
        hl = wrap(headline, SERIF_B(18), tw2, d)
        hy = draw_lines(d, hl, tx2, cy + 16, SERIF_B(18), INK, 21)
        draw_lines(d, wrap(body, SANS(13), tw2, d), tx2, hy + 4, SANS(13),
                   INK, 16)
        if col == 0:
            d.line([(cx + cell_w + 8, cy), (cx + cell_w + 8, cy + cell_h)],
                   fill=LIGHT_GREY, width=1)
    grid_bottom = grid_y + 3 * cell_h + 2 * gap

    # ---- also today strip
    hrule(d, MARGIN, W - MARGIN, grid_bottom + 10, width=2)
    sy = grid_bottom + 20
    d.text((MARGIN, sy), "ALSO TODAY", font=SANS_B(13), fill=RED)
    sy += 20
    strip = [
        ("US ECONOMY RUNS HOT",
         "October inflation 3.8%; Q3 GDP revised up to 4.3%, the fastest in "
         "three years."),
        ("BRAZIL",
         "Lower house approves a fiscal package capping spending growth at "
         "2%."),
        ("BOGOR MINE FLOOD",
         "9 dead, 17 believed trapped after a flood swamps a gold mine "
         "shaft in Pongkor, West Java."),
    ]
    col_w = CW // 3
    for i, (head, body) in enumerate(strip):
        sx = MARGIN + i * col_w
        sw = col_w - 14
        d.text((sx, sy), head, font=SANS_B(13), fill=INK)
        draw_lines(d, wrap(body, SANS(13), sw, d), sx, sy + 17, SANS(13),
                   INK, 16)
        if i:
            d.line([(sx - 8, sy), (sx - 8, sy + 62)], fill=LIGHT_GREY, width=1)
    strip_bottom = sy + 66

    # ---- footer
    hrule(d, MARGIN, W - MARGIN, strip_bottom + 10, width=2)
    fy = strip_bottom + 18
    d.text((W // 2, fy),
           "Sources: Reuters · AP · CNN · Xinhua · Just Security",
           font=SANS(12), fill=GREY, anchor="ma")
    d.text((W // 2, fy + 17),
           "THE WORLD — Wednesday 25 November 2026 · All stories reported "
           "on 25 November 2026.",
           font=SANS(12), fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
