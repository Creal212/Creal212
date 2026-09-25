"""Lean animated GitHub profile banner GIF."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W, H = 1000, 300
FRAMES = 32
DURATION_MS = 90


def load_font(size: int, bold: bool = False):
    for path in (
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def load_georgia(size: int):
    path = Path(r"C:\Windows\Fonts\georgia.ttf")
    return ImageFont.truetype(str(path), size) if path.exists() else load_font(size, True)


FONT_NAME = load_georgia(34)
FONT_ROLES = load_font(14)
FONT_TAG = load_font(13)
FONT_STATUS = load_font(11)
FONT_CODE = load_font(11)
FONT_SMALL = load_font(10)

NODES = [
    (700, 70),
    (770, 55),
    (840, 80),
    (910, 60),
    (730, 125),
    (810, 120),
    (890, 145),
    (750, 185),
    (830, 195),
    (905, 210),
    (785, 245),
    (870, 250),
]
EDGES = [
    (0, 1), (1, 2), (2, 3), (0, 4), (1, 5), (2, 6),
    (4, 5), (5, 6), (4, 7), (5, 8), (6, 9), (7, 8),
    (8, 9), (7, 10), (8, 11), (9, 11),
]
CHIPS = [
    (655, 40, "design → system"),
    (720, 100, "await ship(idea)"),
    (680, 160, "review(patch)"),
    (730, 220, "ux ∩ architecture"),
]


def ease(t: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * t)


def lerp(a, b, t):
    return a + (b - a) * t


def make_frame(i: int) -> Image.Image:
    t = i / FRAMES
    phase = 2 * math.pi * t

    img = Image.new("RGBA", (W, H), (8, 16, 13, 255))
    d = ImageDraw.Draw(img)

    grid_a = int(10 + 6 * math.sin(phase))
    for x in range(0, W, 36):
        d.line([(x, 0), (x, H)], fill=(124, 184, 154, grid_a))
    for y in range(0, H, 36):
        d.line([(0, y), (W, y)], fill=(124, 184, 154, grid_a))

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    ox = int(28 * math.sin(phase))
    gd.ellipse([600 + ox, -90, 1100 + ox, 200], fill=(124, 184, 154, 22))
    gd.ellipse([-60, 160, 300, 380], fill=(196, 163, 90, 10))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)

    # Scan beam
    scan_y = int((H + 60) * t) - 30
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    for k, a in ((28, 14), (12, 32), (2, 80)):
        bd.rectangle([0, scan_y - k, W, scan_y + k], fill=(124, 184, 154, a))
    img = Image.alpha_composite(img, beam)
    d = ImageDraw.Draw(img)

    # Graph
    edge_pulse = (t * len(EDGES)) % len(EDGES)
    for ei, (a, b) in enumerate(EDGES):
        bob1 = 3 * math.sin(phase + a)
        bob2 = 3 * math.sin(phase + b + 1)
        p1 = (NODES[a][0], NODES[a][1] + bob1)
        p2 = (NODES[b][0], NODES[b][1] + bob2)
        dist = min(abs(ei - edge_pulse), len(EDGES) - abs(ei - edge_pulse))
        strength = max(0.2, 1.0 - dist * 0.4)
        d.line([p1, p2], fill=(124, 184, 154, int(35 + 110 * strength)), width=2 if strength > 0.75 else 1)

    for ni, (nx, ny) in enumerate(NODES):
        bob = 3 * math.sin(phase + ni)
        pulse = 0.55 + 0.45 * math.sin(phase * 1.4 + ni)
        r = 3
        d.ellipse([nx - r, ny + bob - r, nx + r, ny + bob + r], fill=(196, 163, 90, int(130 + 70 * pulse)))

    pe = int(t * len(EDGES)) % len(EDGES)
    lt = (t * len(EDGES)) % 1.0
    a, b = EDGES[pe]
    x = lerp(NODES[a][0], NODES[b][0], lt)
    y = lerp(NODES[a][1], NODES[b][1], lt)
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(167, 243, 208, 230))

    # Code chips fade in/out
    for si, (cx, cy, text) in enumerate(CHIPS):
        wave = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(phase * 1.1 + si))
        drift = 10 * math.sin(phase + si)
        alpha = int(180 * wave)
        tw = d.textlength(text, font=FONT_CODE)
        chip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(chip)
        x0 = cx + drift
        cd.rounded_rectangle(
            [x0 - 8, cy - 4, x0 + tw + 8, cy + 14],
            radius=6,
            fill=(16, 36, 28, int(130 * wave)),
            outline=(124, 184, 154, int(70 * wave)),
            width=1,
        )
        cd.text((x0, cy), text, font=FONT_CODE, fill=(215, 229, 220, alpha))
        img = Image.alpha_composite(img, chip)
        d = ImageDraw.Draw(img)

    # Mark pulse
    mark_pulse = 0.5 + 0.5 * math.sin(phase * 2)
    mg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mg)
    gr = int(22 + 12 * mark_pulse)
    md.ellipse([90 - gr, 125 - gr, 90 + gr, 125 + gr], fill=(124, 184, 154, int(16 + 18 * mark_pulse)))
    img = Image.alpha_composite(img, mg)
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([58, 95, 122, 159], radius=14, fill=(22, 53, 40, 255), outline=(124, 184, 154, 180), width=2)
    lift = 1.5 * math.sin(phase * 2)
    d.line([(78, 140), (90, 116 - lift), (102, 140)], fill=(196, 163, 90, 255), width=3)
    d.ellipse([86, 132, 94, 140], fill=(124, 184, 154, 255))
    d.line([(74, 146), (106, 146)], fill=(124, 184, 154, 150), width=2)

    d.text((142, 95), "Cyril Foday-Kailie", font=FONT_NAME, fill=(232, 239, 233, 255))
    d.text(
        (142, 138),
        "Software Engineer  ·  Full-Stack  ·  AI Systems  ·  Product Design",
        font=FONT_ROLES,
        fill=(159, 190, 174, 255),
    )

    line_w = int(16 + 420 * ease((math.sin(phase) + 1) / 2))
    d.line([(142, 172), (142 + line_w, 174)], fill=(124, 184, 154, 230), width=2)
    d.ellipse([142 + line_w - 3, 171, 142 + line_w + 3, 177], fill=(196, 163, 90, 255))

    tag1 = "I design and ship interfaces, data systems, and AI tools"
    tag2 = "where experience is as deliberate as architecture."
    d.text((142, 186), tag1, font=FONT_TAG, fill=(215, 229, 220, 255))
    d.text((142, 208), tag2, font=FONT_TAG, fill=(215, 229, 220, 255))
    if (i // 5) % 2 == 0:
        caret_x = 142 + d.textlength(tag2, font=FONT_TAG) + 4
        d.rectangle([caret_x, 208, caret_x + 7, 222], fill=(196, 163, 90, 220))

    blink = int(60 + 45 * (0.5 + 0.5 * math.sin(phase * 3)))
    for x1, y1, x2, y2 in (
        (28, 28, 52, 28), (28, 28, 28, 52),
        (972, 28, 948, 28), (972, 28, 972, 52),
        (28, 272, 52, 272), (28, 272, 28, 248),
        (972, 272, 948, 272), (972, 272, 972, 248),
    ):
        d.line([(x1, y1), (x2, y2)], fill=(124, 184, 154, blink), width=2)

    label = "ST. PAUL, MN  ·  OPEN TO WORK"
    tw = d.textlength(label, font=FONT_STATUS)
    shimmer = 0.75 + 0.25 * math.sin(phase * 2)
    d.text((820 - tw / 2, 250), label, font=FONT_STATUS, fill=(int(196 * shimmer), int(163 * shimmer), int(90 * shimmer), 255))

    meter_x, meter_y, meter_w = 142, 248, 180
    d.rounded_rectangle([meter_x, meter_y, meter_x + meter_w, meter_y + 7], radius=3, outline=(124, 184, 154, 70), width=1)
    fill_w = int(meter_w * (0.5 + 0.5 * ease((math.sin(phase) + 1) / 2)))
    d.rounded_rectangle([meter_x, meter_y, meter_x + fill_w, meter_y + 7], radius=3, fill=(124, 184, 154, 180))
    d.text((meter_x + meter_w + 8, meter_y - 2), "shipping", font=FONT_SMALL, fill=(159, 190, 174, 190))

    return img.convert("RGB")


def main():
    print("rendering...")
    frames = [make_frame(i) for i in range(FRAMES)]
    shared = frames[0].quantize(colors=48, method=Image.Quantize.MEDIANCUT)
    q = [fr.quantize(palette=shared, dither=Image.Dither.NONE) for fr in frames]

    gif_path = OUT / "banner.gif"
    q[0].save(
        gif_path,
        save_all=True,
        append_images=q[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    frames[8].save(OUT / "banner.png", optimize=True)
    print(f"banner.gif {gif_path.stat().st_size/1024:.1f} KB  ({FRAMES} frames @ {W}x{H})")


if __name__ == "__main__":
    main()
