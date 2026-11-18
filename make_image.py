#!/usr/bin/env python3
"""Draw a deterministic 1024x1024 news poster (entry.png).

Standard library + Pillow only. No network, no randomness, no timestamps.
The poster is composed at 2048x2048 and downsampled once with LANCZOS.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

S = 2048
OUT = 1024
ROOT = Path(__file__).resolve().parent

NAVY = (9, 17, 35)
PANEL = (19, 33, 58)
WHITE = (245, 248, 252)
MUTED = (214, 228, 244)
AMBER = (255, 194, 75)
RED = (255, 90, 90)
CYAN = (69, 217, 240)
TEAL = (63, 209, 167)

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, size, max_width, floor=46):
    """Largest deterministic font size that keeps text inside max_width."""
    while size > floor:
        f = font(path, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_width:
            return f
        size -= 2
    return font(path, floor)


def draw_icon(draw, kind, x, y, color):
    """Simple flat 160x160 icons, drawn with thick strokes for small-size legibility."""
    ox, oy = x, y
    w = 7

    def poly(points, fill=color):
        draw.polygon([(ox + px, oy + py) for px, py in points], fill=fill)

    def line(points, width=w, fill=color):
        draw.line([(ox + px, oy + py) for px, py in points], fill=fill, width=width, joint="curve")

    def ring(box, width=w, outline=color):
        draw.ellipse(
            (ox + box[0], oy + box[1], ox + box[2], oy + box[3]),
            outline=outline, width=width,
        )

    if kind == "plane":
        poly([(152, 80), (112, 70), (86, 28), (68, 28), (79, 70),
              (26, 76), (10, 88), (79, 95), (69, 134), (87, 134),
              (101, 97), (112, 91)])
    elif kind == "missile_ship":
        poly([(74, 18), (92, 34), (88, 62), (78, 62)])
        poly([(74, 18), (62, 34), (66, 48), (74, 44)], fill=color)
        poly([(92, 34), (104, 30), (100, 52), (88, 62)])
        line([(78, 66), (78, 88)], width=9)
        poly([(44, 108), (146, 108), (130, 140), (62, 140)])
        line([(86, 108), (86, 72)], width=6)
        line([(112, 108), (112, 84)], width=6)
    elif kind == "drone":
        poly([(62, 66), (98, 66), (98, 98), (62, 98)])
        line([(66, 70), (34, 40)], width=8)
        line([(94, 70), (126, 40)], width=8)
        line([(66, 94), (34, 124)], width=8)
        line([(94, 94), (126, 124)], width=8)
        ring((14, 22, 54, 58), width=8)
        ring((106, 22, 146, 58), width=8)
        ring((14, 106, 54, 142), width=8)
        ring((106, 106, 146, 142), width=8)
        ring((74, 98, 88, 112), width=6)
    elif kind == "aid_box":
        poly([(34, 52), (126, 52), (126, 138), (34, 138)], fill=NAVY)
        draw.rectangle((ox + 34, oy + 52, ox + 126, oy + 138), outline=color, width=8)
        line([(34, 78), (126, 78)], width=7)
        line([(80, 92), (80, 126)], width=10, fill=WHITE)
        line([(63, 109), (97, 109)], width=10, fill=WHITE)
    elif kind == "bacteria":
        ring((40, 38, 120, 122), width=9)
        for cx, cy in [(66, 68), (94, 62), (78, 96), (100, 98)]:
            ring((cx - 6, cy - 6, cx + 6, cy + 6), width=5)
        for p in [(80, 38, 80, 18), (120, 62, 142, 48),
                  (120, 98, 144, 112), (60, 122, 48, 145),
                  (40, 80, 18, 80)]:
            line([(p[0], p[1]), (p[2], p[3])], width=7)
    elif kind == "chip":
        draw.rectangle((ox + 42, oy + 42, ox + 118, oy + 118), outline=color, width=8)
        draw.rectangle((ox + 64, oy + 64, ox + 96, oy + 96), outline=color, width=6)
        for p in [(58, 42, 58, 18), (80, 42, 80, 18), (102, 42, 102, 18),
                  (58, 118, 58, 142), (80, 118, 80, 142), (102, 118, 102, 142),
                  (42, 58, 18, 58), (42, 80, 18, 80), (42, 102, 18, 102),
                  (118, 58, 142, 58), (118, 80, 142, 80), (118, 102, 142, 102)]:
            line([(p[0], p[1]), (p[2], p[3])], width=7)


CARDS = [
    ("plane", AMBER, "MANILA", "TRUMP IN ASIA", "QUAD, KIM, SHENZHEN"),
    ("missile_ship", RED, "IRAN WAR", "QESHM STRUCK", "BAHRAIN, HORMUZ"),
    ("drone", CYAN, "UKRAINE", "DRONE RECORD", "IMF 1.6B"),
    ("aid_box", TEAL, "MIDDLE EAST", "GAZA AID", "TELEGRAM BLOCKED"),
    ("bacteria", AMBER, "HEALTH", "SUPERBUGS", "39M BY 2050"),
    ("chip", CYAN, "TECH", "AI RISKS", "OUTAGES"),
]


def main():
    img = Image.new("RGB", (S, S), NAVY)
    draw = ImageDraw.Draw(img)

    draw.rectangle((80, 66, 1968, 80), fill=AMBER)
    draw.text((80, 116), "WORLD NEWS", font=font(BOLD, 196), fill=WHITE)
    draw.text((84, 356), "17 NOVEMBER 2026", font=font(BOLD, 84), fill=CYAN)
    draw.text((86, 466), "ONE DAY / SIX STORIES", font=font(REG, 56), fill=MUTED)
    draw.rectangle((80, 552, 1968, 558), fill=(60, 84, 118))

    margin, gap = 80, 28
    cw = (S - 2 * margin - gap) // 2
    top, ch, vgap = 600, 437, 28
    text_x_offset = 220
    text_width = cw - text_x_offset - 28

    for i, (kind, accent, line1, line2, line3) in enumerate(CARDS):
        col, row = i % 2, i // 2
        x = margin + col * (cw + gap)
        y = top + row * (ch + vgap)

        draw.rounded_rectangle((x, y, x + cw, y + ch), radius=18, fill=PANEL)
        draw.rectangle((x, y + 18, x + 10, y + ch - 18), fill=accent)

        draw_icon(draw, kind, x + 30, y + 138, accent)

        f1 = fit_font(draw, line1, BOLD, 76, text_width)
        f2 = fit_font(draw, line2, BOLD, 72, text_width)
        f3 = fit_font(draw, line3, REG, 64, text_width)
        tx = x + text_x_offset
        draw.text((tx, y + 26), line1, font=f1, fill=accent)
        draw.text((tx, y + 140), line2, font=f2, fill=WHITE)
        draw.text((tx, y + 266), line3, font=f3, fill=WHITE)

    out = img.resize((OUT, OUT), Image.Resampling.LANCZOS)
    target = ROOT / "entry.png"
    out.save(target, format="PNG", optimize=True)
    print(f"{target} {target.stat().st_size} bytes {out.width}x{out.height}")


if __name__ == "__main__":
    main()
