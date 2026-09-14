#!/usr/bin/env python3
"""Render a Clean Bumble Bee Instagram post (1080x1350) with Cyrillic text + logo.

The image model never draws text — it mangles Cyrillic. This script puts the
headline, subline and logo on top of a background.

Layouts:
  photo  — background image fills the frame, white card with text at the bottom
  card   — pastel colour background, big headline, optional icon/mascot bottom-right

Examples:
  python3 compose.py --layout photo --bg bg.png --headline "Пальто к зиме" \
      --sub "Заберём от двери и вернём чистым" --out image.png
  python3 compose.py --layout card --bgcolor "#BAEBFF" --icon ../../../brand/cbb-mascot.png \
      --headline "3 ошибки при стирке шерсти" --sub "Сохраните, чтобы не забыть" --out image.png
"""
import argparse
import glob
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BRAND = os.path.join(ROOT, "brand")
W, H = 1080, 1350
NAVY = "#1E2B94"
INK = "#16233D"
WHITE = "#FFFFFF"
MARGIN = 64


def font(size, weight):
    paths = sorted(glob.glob(os.path.join(BRAND, "fonts", "*.ttf")))
    manrope = [p for p in paths if "manrope" in p.lower()]
    path = (manrope or paths)[0]
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name(weight)
    except (OSError, ValueError, AttributeError):
        pass
    return f


def wrap(draw, text, fnt, max_w):
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=fnt) <= max_w or not line:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit(draw, text, max_w, max_lines, start, minimum, weight):
    size = start
    while size > minimum:
        fnt = font(size, weight)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines and all(draw.textlength(l, font=fnt) <= max_w for l in lines):
            return fnt, lines, size
        size -= 4
    fnt = font(minimum, weight)
    return fnt, wrap(draw, text, fnt, max_w), minimum


def cover(img):
    scale = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((left, top, left + W, top + H))


def paste_logo(canvas):
    logo = Image.open(os.path.join(BRAND, "cbb-logo-lockup.png")).convert("RGBA")
    target_w = 230
    logo = logo.resize((target_w, round(logo.height * target_w / logo.width)), Image.LANCZOS)
    pad = 14
    badge = Image.new("RGBA", (logo.width + pad * 2, logo.height + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(badge).rounded_rectangle([0, 0, badge.width - 1, badge.height - 1], 28, fill=WHITE)
    badge.paste(logo, (pad, pad), logo)
    canvas.alpha_composite(badge, (MARGIN - pad, MARGIN - pad))


def draw_lines(draw, lines, fnt, x, y, fill, spacing=1.12):
    size = fnt.size
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += round(size * spacing)
    return y


def layout_photo(args):
    canvas = cover(Image.open(args.bg).convert("RGB")).convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    inner_w = W - MARGIN * 2 - 96
    h_font, h_lines, h_size = fit(draw, args.headline, inner_w, 3, 84, 52, "ExtraBold")
    s_font, s_lines, s_size = (None, [], 0)
    if args.sub:
        s_font, s_lines, s_size = fit(draw, args.sub, inner_w, 3, 40, 30, "SemiBold")
    card_h = 48 + len(h_lines) * round(h_size * 1.12) + (24 + len(s_lines) * round(s_size * 1.3) if s_lines else 0) + 48
    top = H - MARGIN - card_h
    card = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([MARGIN, top, W - MARGIN, H - MARGIN], 44, fill=(255, 255, 255, 245))
    canvas.alpha_composite(card)
    draw = ImageDraw.Draw(canvas)
    y = draw_lines(draw, h_lines, h_font, MARGIN + 48, top + 40, NAVY)
    if s_lines:
        draw_lines(draw, s_lines, s_font, MARGIN + 48, y + 20, INK, 1.3)
    paste_logo(canvas)
    return canvas


def layout_card(args):
    canvas = Image.new("RGBA", (W, H), args.bgcolor)
    draw = ImageDraw.Draw(canvas)
    inner_w = W - MARGIN * 2
    h_font, h_lines, h_size = fit(draw, args.headline, inner_w, 5, 104, 60, "ExtraBold")
    y = draw_lines(draw, h_lines, h_font, MARGIN, 260, NAVY, 1.1)
    if args.sub:
        s_font, s_lines, _ = fit(draw, args.sub, inner_w, 4, 44, 32, "SemiBold")
        draw_lines(draw, s_lines, s_font, MARGIN, y + 36, INK, 1.3)
    if args.icon:
        icon = Image.open(args.icon).convert("RGBA")
        size = 420
        icon = icon.crop(icon.getbbox() or (0, 0, icon.width, icon.height))
        scale = size / max(icon.width, icon.height)
        icon = icon.resize((round(icon.width * scale), round(icon.height * scale)), Image.LANCZOS)
        canvas.alpha_composite(icon, (W - MARGIN - icon.width + 20, H - MARGIN - icon.height + 20))
    paste_logo(canvas)
    return canvas


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--layout", choices=["photo", "card"], required=True)
    p.add_argument("--headline", required=True)
    p.add_argument("--sub", default="")
    p.add_argument("--bg", help="background image (photo layout)")
    p.add_argument("--bgcolor", default="#BAEBFF", help="hex colour (card layout)")
    p.add_argument("--icon", help="PNG with transparency for the card layout")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    if args.layout == "photo" and not args.bg:
        p.error("--bg is required for the photo layout")
    img = layout_photo(args) if args.layout == "photo" else layout_card(args)
    img.convert("RGB").save(args.out, "PNG", optimize=True)
    print(args.out)


if __name__ == "__main__":
    main()
