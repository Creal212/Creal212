"""Woodland-themed animated GitHub profile banner — matches creal589.dev vibe."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent
W, H = 1000, 300
FRAMES = 36
DURATION_MS = 85
RNG = random.Random(589)


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
FONT_CHIP = load_font(11)
FONT_SMALL = load_font(10)

# Firefly positions (base x,y + speed phase)
FIREFLIES = [
    (RNG.uniform(40, 960), RNG.uniform(30, 270), RNG.uniform(0.6, 1.8), RNG.uniform(0, math.pi * 2))
    for _ in range(28)
]

# Soft leaf motes drifting
MOTES = [
    (RNG.uniform(0, W), RNG.uniform(0, H), RNG.uniform(0.4, 1.2), RNG.uniform(8, 18), RNG.uniform(0, math.pi * 2))
    for _ in range(18)
]

CHIPS = [
    (700, 48, "build in the woods"),
    (745, 110, "ship with care"),
    (710, 175, "design ∩ systems"),
    (760, 235, "Agent 589 nearby"),
]


def ease(t: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * t)


def vertical_gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img.convert("RGBA")


def draw_tree(d: ImageDraw.ImageDraw, base_x: int, ground_y: int, scale: float, shade: tuple, sway: float):
    """Simple layered pine/woodland silhouette."""
    trunk_w = max(3, int(6 * scale))
    trunk_h = int(40 * scale)
    lean = sway * 6 * scale
    top_x = base_x + lean
    d.rectangle(
        [base_x - trunk_w // 2, ground_y - trunk_h, base_x + trunk_w // 2, ground_y],
        fill=shade,
    )
    # canopy triangles
    for i, (w_mul, h_mul, y_off) in enumerate(
        ((1.0, 0.55, 0.0), (0.82, 0.48, 0.28), (0.62, 0.42, 0.52))
    ):
        cw = int(48 * scale * w_mul)
        ch = int(55 * scale * h_mul)
        cy = ground_y - trunk_h - int(y_off * 50 * scale) + int(8 * scale)
        cx = top_x + lean * (0.15 * i)
        d.polygon(
            [
                (cx, cy - ch),
                (cx - cw, cy + ch * 0.35),
                (cx + cw, cy + ch * 0.35),
            ],
            fill=shade,
        )


def make_frame(i: int) -> Image.Image:
    t = i / FRAMES
    phase = 2 * math.pi * t

    # Dusk-forest sky → deep moss floor (portfolio night woods feel)
    img = vertical_gradient(
        (W, H),
        top=(18, 32, 28),
        bottom=(8, 16, 12),
    )
    # Warm late-day wash on left (cabin light)
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    wd.ellipse([-120, -80, 420, 260], fill=(196, 163, 90, 28))
    wd.ellipse([520, -40, 1100, 220], fill=(90, 140, 110, 22))
    img = Image.alpha_composite(img, wash)

    # Soft mist bands
    mist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mist)
    for band, y0 in enumerate((90, 160, 230)):
        y = y0 + int(8 * math.sin(phase + band))
        md.ellipse([-80, y, W + 80, y + 55], fill=(180, 200, 185, 12 + band * 3))
    mist = mist.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, mist)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    # Distant tree line (right + edges) with gentle sway
    sway = math.sin(phase * 0.7)
    tree_specs = [
        (620, 0.55, (22, 48, 36, 210)),
        (670, 0.75, (18, 42, 30, 230)),
        (720, 0.95, (14, 36, 26, 240)),
        (780, 1.15, (12, 32, 22, 250)),
        (845, 1.35, (10, 28, 20, 255)),
        (910, 1.05, (14, 34, 24, 245)),
        (960, 0.7, (18, 40, 28, 220)),
        (40, 0.5, (20, 44, 32, 160)),
        (95, 0.65, (16, 38, 28, 180)),
    ]
    for bx, sc, shade in tree_specs:
        local_sway = sway * (0.4 + 0.6 * sc)
        draw_tree(d, int(bx + local_sway * 4), H - 8, sc, shade, local_sway)

    # Soft ground moss strip
    d.ellipse([-40, H - 50, W + 40, H + 40], fill=(12, 28, 18, 180))

    img = Image.alpha_composite(img, layer)
    d = ImageDraw.Draw(img)

    # Drifting leaf motes
    for mx, my, speed, amp, ph0 in MOTES:
        x = (mx + math.cos(phase * speed + ph0) * amp) % W
        y = (my + math.sin(phase * speed * 0.7 + ph0) * (amp * 0.6) + t * 12) % H
        a = int(40 + 50 * (0.5 + 0.5 * math.sin(phase + ph0)))
        d.ellipse([x - 2, y - 1, x + 2, y + 1], fill=(140, 170, 120, a))

    # Fireflies
    for fx, fy, speed, ph0 in FIREFLIES:
        x = fx + math.sin(phase * speed + ph0) * 18
        y = fy + math.cos(phase * speed * 0.8 + ph0) * 10
        glow = 0.35 + 0.65 * max(0, math.sin(phase * 2.2 * speed + ph0))
        if glow < 0.2:
            continue
        r = 1.5 + 2.5 * glow
        # outer glow
        d.ellipse([x - r * 3, y - r * 3, x + r * 3, y + r * 3], fill=(196, 220, 140, int(18 * glow)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(230, 255, 180, int(160 * glow)))

    # Soft moonlight / canopy shaft on right
    shaft = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shaft)
    pulse = 0.55 + 0.45 * math.sin(phase)
    sd.polygon(
        [(820, -20), (940, -20), (780, H), (620, H)],
        fill=(200, 220, 170, int(14 + 10 * pulse)),
    )
    shaft = shaft.filter(ImageFilter.GaussianBlur(12))
    img = Image.alpha_composite(img, shaft)
    d = ImageDraw.Draw(img)

    # Floating woodland chips (portfolio tone)
    for si, (cx, cy, text) in enumerate(CHIPS):
        wave = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(phase * 1.05 + si))
        drift = 8 * math.sin(phase + si * 0.8)
        tw = d.textlength(text, font=FONT_CHIP)
        chip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(chip)
        x0 = cx + drift
        cd.rounded_rectangle(
            [x0 - 8, cy - 4, x0 + tw + 8, cy + 14],
            radius=8,
            fill=(24, 40, 30, int(150 * wave)),
            outline=(160, 190, 140, int(70 * wave)),
            width=1,
        )
        cd.text((x0, cy), text, font=FONT_CHIP, fill=(220, 232, 210, int(190 * wave)))
        img = Image.alpha_composite(img, chip)
        d = ImageDraw.Draw(img)

    # Brand mark — woodland seal
    mark_pulse = 0.5 + 0.5 * math.sin(phase * 1.8)
    mg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mg)
    gr = int(20 + 10 * mark_pulse)
    md.ellipse([90 - gr, 125 - gr, 90 + gr, 125 + gr], fill=(160, 190, 120, int(14 + 16 * mark_pulse)))
    img = Image.alpha_composite(img, mg)
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([58, 95, 122, 159], radius=14, fill=(28, 48, 36, 240), outline=(180, 160, 100, 200), width=2)
    # tiny tree glyph in mark
    d.rectangle([87, 138, 93, 148], fill=(196, 163, 90, 255))
    d.polygon([(90, 108), (74, 136), (106, 136)], fill=(124, 168, 120, 255))
    d.polygon([(90, 118), (78, 138), (102, 138)], fill=(90, 140, 100, 255))

    # Typography — clear over soft woods
    # subtle text shadow plate
    plate = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plate)
    pd.rounded_rectangle([132, 88, 640, 250], radius=16, fill=(8, 16, 12, 95))
    plate = plate.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img, plate)
    d = ImageDraw.Draw(img)

    d.text((142, 95), "Cyril Foday-Kailie", font=FONT_NAME, fill=(236, 240, 230, 255))
    d.text(
        (142, 138),
        "Software Engineer  ·  Full-Stack  ·  AI Systems  ·  Product Design",
        font=FONT_ROLES,
        fill=(170, 190, 165, 255),
    )

    line_w = int(16 + 400 * ease((math.sin(phase) + 1) / 2))
    d.line([(142, 172), (142 + line_w, 174)], fill=(180, 160, 100, 220), width=2)
    d.ellipse([142 + line_w - 3, 171, 142 + line_w + 3, 177], fill=(210, 230, 160, 255))

    tag1 = "From St. Paul’s woods — I build AI tools, data systems,"
    tag2 = "and interfaces with the same care as the craft."
    d.text((142, 186), tag1, font=FONT_TAG, fill=(220, 230, 215, 255))
    d.text((142, 208), tag2, font=FONT_TAG, fill=(220, 230, 215, 255))
    if (i // 5) % 2 == 0:
        caret_x = 142 + d.textlength(tag2, font=FONT_TAG) + 4
        d.rectangle([caret_x, 208, caret_x + 7, 222], fill=(196, 163, 90, 220))

    # Soft corner brackets (lighter, less HUD)
    blink = int(40 + 35 * (0.5 + 0.5 * math.sin(phase * 2)))
    for x1, y1, x2, y2 in (
        (22, 22, 44, 22), (22, 22, 22, 44),
        (978, 22, 956, 22), (978, 22, 978, 44),
        (22, 278, 44, 278), (22, 278, 22, 256),
        (978, 278, 956, 278), (978, 278, 978, 256),
    ):
        d.line([(x1, y1), (x2, y2)], fill=(160, 180, 140, blink), width=2)

    label = "ST. PAUL, MN  ·  OPEN TO WORK"
    tw = d.textlength(label, font=FONT_STATUS)
    shimmer = 0.8 + 0.2 * math.sin(phase * 1.8)
    d.text(
        (820 - tw / 2, 262),
        label,
        font=FONT_STATUS,
        fill=(int(200 * shimmer), int(175 * shimmer), int(110 * shimmer), 255),
    )

    # Path / trail meter (woodland shipping)
    meter_x, meter_y, meter_w = 142, 248, 170
    d.rounded_rectangle([meter_x, meter_y, meter_x + meter_w, meter_y + 7], radius=3, outline=(160, 180, 140, 70), width=1)
    fill_w = int(meter_w * (0.5 + 0.5 * ease((math.sin(phase) + 1) / 2)))
    d.rounded_rectangle([meter_x, meter_y, meter_x + fill_w, meter_y + 7], radius=3, fill=(140, 170, 110, 190))
    d.text((meter_x + meter_w + 8, meter_y - 2), "on the trail", font=FONT_SMALL, fill=(170, 190, 160, 200))

    return img.convert("RGB")


def main():
    print("rendering woodland banner...")
    frames = [make_frame(i) for i in range(FRAMES)]
    shared = frames[0].quantize(colors=56, method=Image.Quantize.MEDIANCUT)
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
    frames[10].save(OUT / "banner.png", optimize=True)
    print(f"banner.gif {gif_path.stat().st_size/1024:.1f} KB")


if __name__ == "__main__":
    main()
