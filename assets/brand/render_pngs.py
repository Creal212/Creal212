from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

out = Path(r"C:\Users\Tommy\Creal212\assets\brand")
out.mkdir(parents=True, exist_ok=True)


def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\georgia.ttf",
    ]
    for c in candidates:
        p = Path(c)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def georgia(size):
    p = Path(r"C:\Windows\Fonts\georgia.ttf")
    if p.exists():
        return ImageFont.truetype(str(p), size)
    return font(size, True)


# --- Banner ---
W, H = 1200, 360
base = Image.new("RGBA", (W, H), (11, 22, 18, 255))
d = ImageDraw.Draw(base)

for x in range(0, W, 40):
    d.line([(x, 0), (x, H)], fill=(124, 184, 154, 14))
for y in range(0, H, 40):
    d.line([(0, y), (W, y)], fill=(124, 184, 154, 14))

glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([700, -80, 1260, 220], fill=(124, 184, 154, 28))
gd.ellipse([-40, 220, 420, 440], fill=(124, 184, 154, 16))
base = Image.alpha_composite(base, glow)
d = ImageDraw.Draw(base)

d.rounded_rectangle([72, 118, 144, 190], radius=18, fill=(22, 53, 40, 255), outline=(124, 184, 154, 160), width=2)
d.line([(94, 166), (108, 140), (122, 166)], fill=(196, 163, 90, 255), width=3)
d.ellipse([104, 156, 112, 164], fill=(124, 184, 154, 255))
d.line([(90, 172), (126, 172)], fill=(124, 184, 154, 140), width=2)

d.text((168, 118), "Cyril Foday-Kailie", font=georgia(42), fill=(232, 239, 233, 255))
d.text(
    (168, 172),
    "Software Engineer  ·  Full-Stack  ·  AI Systems  ·  Product Design",
    font=font(18),
    fill=(159, 190, 174, 255),
)
d.line([(168, 214), (688, 216)], fill=(124, 184, 154, 220), width=2)
d.text(
    (168, 232),
    "I design and ship interfaces, data systems, and AI tools",
    font=font(16),
    fill=(215, 229, 220, 255),
)
d.text(
    (168, 258),
    "where the experience is as deliberate as the architecture.",
    font=font(16),
    fill=(215, 229, 220, 255),
)

for x1, y1, x2, y2 in [
    (40, 40, 70, 40),
    (40, 40, 40, 70),
    (1160, 40, 1130, 40),
    (1160, 40, 1160, 70),
    (40, 320, 70, 320),
    (40, 320, 40, 290),
    (1160, 320, 1130, 320),
    (1160, 320, 1160, 290),
]:
    d.line([(x1, y1), (x2, y2)], fill=(124, 184, 154, 90), width=2)

label = "ST. PAUL, MN  ·  OPEN TO WORK"
tw = d.textlength(label, font=font(13))
d.text((980 - tw / 2, 292), label, font=font(13), fill=(196, 163, 90, 255))
base.convert("RGB").save(out / "banner.png", optimize=True)
print("banner", (out / "banner.png").stat().st_size)


def card(filename, title, subtitle, bg, accent_rgb, draw_icon):
    w, h = 720, 240
    c = Image.new("RGBA", (w, h), (*bg, 255))
    cd = ImageDraw.Draw(c)
    cd.rounded_rectangle(
        [2, 2, w - 3, h - 3],
        radius=28,
        outline=(*accent_rgb, 120),
        width=2,
    )
    draw_icon(cd)
    cd.text((148, 78), title, font=font(34, True), fill=(245, 247, 246, 255))
    cd.text((148, 130), subtitle, font=font(22), fill=(168, 184, 176, 255))
    path = out / filename
    c.convert("RGB").save(path, optimize=True)
    print(filename, path.stat().st_size)


def book_icon(cd):
    cd.rounded_rectangle([44, 56, 116, 152], radius=6, fill=(232, 220, 195, 255))
    cd.rectangle([56, 70, 104, 76], fill=(139, 105, 20, 140))
    cd.rectangle([56, 86, 92, 91], fill=(139, 105, 20, 90))
    cd.rectangle([56, 100, 96, 105], fill=(139, 105, 20, 90))
    cd.ellipse([70, 120, 90, 140], outline=(42, 33, 24, 255), width=2)


def imperium_icon(cd):
    cx, cy = 80, 104
    pts = [
        (cx, cy - 40),
        (cx + 34, cy - 20),
        (cx + 34, cy + 20),
        (cx, cy + 40),
        (cx - 34, cy + 20),
        (cx - 34, cy - 20),
    ]
    cd.polygon(pts, fill=(59, 130, 246, 255))
    inner = [
        (cx, cy - 24),
        (cx + 18, cy - 12),
        (cx + 18, cy + 12),
        (cx, cy + 24),
        (cx - 18, cy + 12),
        (cx - 18, cy - 12),
    ]
    cd.polygon(inner, fill=(11, 18, 32, 90))


def wtf_icon(cd):
    cd.line([(44, 136), (68, 104), (92, 116), (116, 72), (140, 88)], fill=(52, 211, 153, 255), width=5)
    cd.ellipse([132, 80, 148, 96], fill=(167, 243, 208, 255))


def revops_icon(cd):
    cd.rounded_rectangle([48, 72, 84, 108], radius=6, fill=(45, 212, 191, 255))
    cd.rounded_rectangle([96, 84, 132, 120], radius=6, fill=(153, 246, 228, 160))
    cd.line([(84, 84), (96, 84)], fill=(236, 254, 255, 255), width=3)
    cd.line([(84, 100), (96, 100)], fill=(236, 254, 255, 255), width=3)
    cd.ellipse([60, 136, 72, 148], fill=(204, 251, 241, 255))
    cd.ellipse([108, 136, 120, 148], fill=(204, 251, 241, 255))
    cd.line([(66, 148), (66, 158), (114, 158), (114, 148)], fill=(204, 251, 241, 255), width=2)


card(
    "book-of-blocks.png",
    "Book of Blocks",
    "Crypto encyclopedia · Market observatory",
    (28, 22, 16),
    (196, 163, 90),
    book_icon,
)
card(
    "imperium.png",
    "I.M.P.E.R.I.U.M",
    "AI desktop workspace · Reviewable patches",
    (11, 18, 32),
    (59, 130, 246),
    imperium_icon,
)
card(
    "world-trade-factory.png",
    "World Trade Factory",
    "Live markets · Charts · Wallet-ready UX",
    (15, 28, 24),
    (52, 211, 153),
    wtf_icon,
)
card(
    "revops.png",
    "RevOps Data Sync",
    "Python · PostgreSQL · Metabase pipelines",
    (16, 24, 32),
    (94, 234, 212),
    revops_icon,
)
print("done")
