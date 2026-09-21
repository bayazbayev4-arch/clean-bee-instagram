#!/usr/bin/env python3
"""Render an on-brand Clean Bumble Bee Instagram post (1080x1080).

Follows the brand guideline (brand/brand.md): official logo on top, Manrope,
pastel service tint + icon or a high-key photo in the middle, headline <= 6 words,
Safe Blue CTA button at the bottom. The image model never draws text.

Layouts:
  tips   headline + 3 numbered tips on the service tint, icon chip top-right
  fact   eyebrow chip (МИФ / ФАКТ / СОВЕТ) + big headline + explanation + icon
  photo  rounded high-key photo, headline and subline underneath

Examples:
  python3 compose.py --layout tips --tint "#94EBE5" --icon ../../../brand/services/dry-cleaning.png \
      --headline "Как хранить пальто летом" \
      --tips "Почистите перед хранением|Используйте дышащий чехол|Держите вдали от солнца" \
      --button "Заказать на cleanbumblebee.com" --out image.png
  python3 compose.py --layout fact --eyebrow "МИФ" --tint "#BAEBFF" --icon ... \
      --headline "Химчистка портит вещи" --sub "Наоборот: ..." --out image.png
  python3 compose.py --layout photo --bg bg.png --headline "..." --sub "..." --out image.png
  python3 compose.py --lang kk --layout fact ... --out image-kk.png   # Kazakh slide (en = English)
"""
import argparse
import glob
import os
import re

from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BRAND = os.path.join(ROOT, "brand")
W = H = 1080
M = 56  # outer margin

SAFE_BLUE = "#0578CC"
NAVY = "#1E2B94"
INK = "#16233D"
TINT_HEAD = "#08528C"
TINT_BODY = "#3D4759"
HONEY = "#FFD16F"
ICE = "#BAEBFF"
WHITE = "#FFFFFF"


# ---------- text with per-glyph font fallback (Manrope ships as script subsets) ----------

# Manrope has no Ә Ғ Қ Ң Ұ, so Kazakh needs the Montserrat fallback. Montserrat is ~13% wider and
# a touch heavier, so its letters are narrowed, set 50 units lighter and caps enlarged 3% to sit
# inside Manrope words (matched by eye 21-09-2026).
FALLBACK_WIDTH = 0.87
FALLBACK_LIGHTER = 50
FALLBACK_CAPS = 1.03
WEIGHTS = {"ExtraLight": 200, "Light": 300, "Regular": 400, "Medium": 500,
           "SemiBold": 600, "Bold": 700, "ExtraBold": 800}

# Per-language labels compose.py draws itself (the skill passes headline/tips/sub/eyebrow/button).
CITY = {"ru": "Астана", "kk": "Астана", "en": "Astana"}
BUTTON = {"ru": "Заказать на cleanbumblebee.com",
          "kk": "cleanbumblebee.com сайтында тапсырыс беру",
          "en": "Order at cleanbumblebee.com"}


class Face:
    _cache = {}
    _fb_cache = {}

    def __init__(self, size, weight):
        self.size = size
        self.fonts = []
        self.fb = None
        for path in sorted(glob.glob(os.path.join(BRAND, "fonts", "*"))):
            if not path.lower().endswith((".ttf", ".otf", ".woff2", ".woff")):
                continue
            f = ImageFont.truetype(path, size)
            try:
                f.set_variation_by_name(weight)
            except (OSError, ValueError, AttributeError):
                pass
            self.fonts.append(f)
            if "fallback" in os.path.basename(path):
                self.fb, self.fb_path = f, path
        self.fb_wght = WEIGHTS.get(weight, 700) - FALLBACK_LIGHTER

    def _fb_font(self, ch):
        size = round(self.size * (FALLBACK_CAPS if ch.isupper() else 1))
        key = (self.fb_path, size, self.fb_wght)
        if key not in Face._fb_cache:
            f = ImageFont.truetype(self.fb_path, size)
            try:
                f.set_variation_by_axes([self.fb_wght])
            except (OSError, ValueError, AttributeError):
                pass
            Face._fb_cache[key] = f
        return Face._fb_cache[key]

    def _length(self, font, text):
        if font is not self.fb:
            return font.getlength(text)
        return sum(self._fb_font(ch).getlength(ch) * FALLBACK_WIDTH if ch.isalpha() else font.getlength(ch)
                   for ch in text)

    def _has(self, font, ch):
        key = (id(font), ch)
        if key not in Face._cache:
            probe = Image.new("L", (self.size * 2, self.size * 2), 0)
            ImageDraw.Draw(probe).text((4, 4), ch, font=font, fill=255)
            empty = Image.new("L", probe.size, 0)
            ImageDraw.Draw(empty).text((4, 4), "", font=font, fill=255)
            Face._cache[key] = ch.isspace() or ImageChops.difference(probe, empty).getbbox() is not None
        return Face._cache[key]

    def runs(self, text):
        out = []
        for ch in text:
            font = next((f for f in self.fonts if self._has(f, ch)), self.fonts[-1])
            if out and out[-1][0] is font:
                out[-1][1] += ch
            else:
                out.append([font, ch])
        return out

    def width(self, text):
        return sum(self._length(f, t) for f, t in self.runs(text))

    def draw(self, draw, xy, text, fill):
        x, y = xy
        base = y + self.fonts[0].getmetrics()[0]  # Manrope baseline under the default top anchor
        for f, t in self.runs(text):
            if f is not self.fb:
                draw.text((x, y), t, font=f, fill=fill)
                x += f.getlength(t)
                continue
            for ch in t:  # fallback letters one by one, narrowed onto Manrope's baseline
                if not ch.isalpha():  # symbols (→, ₸) keep the plain fallback
                    draw.text((x, y), ch, font=f, fill=fill)
                    x += f.getlength(ch)
                    continue
                fb = self._fb_font(ch)
                adv, pad = fb.getlength(ch), self.size
                mask = Image.new("L", (int(adv) + 2 * pad, 3 * self.size), 0)
                ImageDraw.Draw(mask).text((pad, 2 * self.size), ch, font=fb, fill=255, anchor="ls")
                mask = mask.resize((max(1, round(mask.width * FALLBACK_WIDTH)), mask.height), Image.LANCZOS)
                draw.bitmap((round(x - pad * FALLBACK_WIDTH), base - 2 * self.size), mask, fill=fill)
                x += adv * FALLBACK_WIDTH


def wrap(face, text, max_w):
    # Keep numbers with the next word and short words with the previous one («3 шага», «в 2 часа»).
    text = re.sub(r"(\d+) ", "\\1\u00a0", " ".join(text.split()))
    text = re.sub(r"(?<=\s)(\S{1,2}) ", "\\1\u00a0", text)
    text = text.replace(" —", "\u00a0—")  # a dash never starts a line
    lines, line = [], ""
    for word in text.split(" "):
        test = f"{line} {word}".strip()
        if face.width(test) <= max_w or not line:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit(text, max_w, max_lines, start, minimum, weight):
    size = start
    while True:
        face = Face(size, weight)
        lines = wrap(face, text, max_w)
        if (len(lines) <= max_lines and all(face.width(l) <= max_w for l in lines)) or size <= minimum:
            return face, lines
        size -= 2


def block(draw, face, lines, x, y, fill, leading=1.18):
    step = round(face.size * leading)
    for line in lines:
        face.draw(draw, (x, y), line, fill)
        y += step
    return y


def block_height(face, lines, leading=1.18):
    return round(face.size * leading) * len(lines)


# ---------- brand pieces ----------

def trimmed(path):
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((2, 2)))
    box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 40 else 0).getbbox()
    return im.crop(box) if box else im


def logo_header(canvas, city="Астана"):
    """Primary horizontal lockup on white, top-left, with the Astana chip top-right."""
    logo = trimmed(os.path.join(BRAND, "logos", "primary-horizontal.png"))
    h = 84
    logo = logo.resize((round(logo.width * h / logo.height), h), Image.LANCZOS)
    canvas.paste(logo, (M, 44))
    draw = ImageDraw.Draw(canvas)
    face = Face(30, "Bold")
    label = city
    pw, ph = round(face.width(label)) + 48, 56
    x0, y0 = W - M - pw, 44 + (h - ph) // 2
    draw.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], ph // 2, fill=ICE)
    face.draw(draw, (x0 + 24, y0 + 9), label, TINT_HEAD)


def cta_button(canvas, label):
    draw = ImageDraw.Draw(canvas)
    face, _ = fit(label + " →", W - 2 * M - 96, 1, 38, 26, "ExtraBold")
    text = label + " →"
    bh = 100
    bw = min(W - 2 * M, round(face.width(text)) + 96)
    x0, y0 = (W - bw) // 2, H - M - bh
    draw.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], bh // 2, fill=SAFE_BLUE)
    face.draw(draw, (x0 + (bw - face.width(text)) / 2, y0 + (bh - face.size * 1.25) / 2), text, WHITE)
    return y0


def paste_icon(canvas, path, size, xy):
    icon = Image.open(path).convert("RGBA")
    box = icon.getbbox()
    if box:
        icon = icon.crop(box)
    scale = size / max(icon.width, icon.height)
    icon = icon.resize((round(icon.width * scale), round(icon.height * scale)), Image.LANCZOS)
    x, y = xy
    canvas.paste(icon, (x + (size - icon.width) // 2, y + (size - icon.height) // 2), icon)


CARD_TOP = 168


# ---------- layouts ----------

def layout_tips(args):
    canvas = Image.new("RGB", (W, H), WHITE)
    logo_header(canvas, args.city)
    btn_top = cta_button(canvas, args.button)
    draw = ImageDraw.Draw(canvas)
    card = [M, CARD_TOP, W - M, btn_top - 36]
    draw.rounded_rectangle(card, 48, fill=args.tint)
    pad = 52
    chip = 196
    if args.icon:
        cx, cy = card[2] - pad - chip, card[1] + pad
        draw.rounded_rectangle([cx, cy, cx + chip, cy + chip], 44, fill=WHITE)
        paste_icon(canvas, args.icon, chip - 36, (cx + 18, cy + 18))
    head_w = card[2] - card[0] - 2 * pad - (chip + 32 if args.icon else 0)
    h_face, h_lines = fit(args.headline, head_w, 3, 68, 46, "ExtraBold")
    y = block(draw, h_face, h_lines, card[0] + pad, card[1] + pad - 6, TINT_HEAD, 1.1)
    y = max(y, card[1] + pad + (chip if args.icon else 0)) + 34
    tips = [t.strip() for t in args.tips.split("|") if t.strip()][:4]
    avail = card[3] - pad - y
    text_w = card[2] - card[0] - 2 * pad - 92
    size = 46
    while True:
        t_face = Face(size, "SemiBold")
        wrapped = [wrap(t_face, t, text_w) for t in tips]
        gap = 34
        total = sum(max(block_height(t_face, w, 1.22), 64) for w in wrapped) + gap * (len(tips) - 1)
        if total <= avail or size <= 28:
            break
        size -= 2
    y += max(0, (avail - total) // 2)  # centre the tips in the space left on the card
    n_face = Face(34, "ExtraBold")
    for i, lines in enumerate(wrapped, 1):
        r = 32
        cx, cy = card[0] + pad + r, y + r
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SAFE_BLUE)
        n_face.draw(draw, (cx - n_face.width(str(i)) / 2, cy - n_face.size * 0.66), str(i), WHITE)
        text_h = block_height(t_face, lines, 1.22)
        ty = y + max(0, (64 - text_h) // 2) - 4
        block(draw, t_face, lines, card[0] + pad + 92, ty, TINT_BODY, 1.22)
        y += max(text_h, 64) + gap
    return canvas


def layout_fact(args):
    canvas = Image.new("RGB", (W, H), WHITE)
    logo_header(canvas, args.city)
    btn_top = cta_button(canvas, args.button)
    draw = ImageDraw.Draw(canvas)
    card = [M, CARD_TOP, W - M, btn_top - 36]
    draw.rounded_rectangle(card, 48, fill=args.tint)
    pad = 56
    y = card[1] + pad
    if args.eyebrow:
        e_face = Face(28, "ExtraBold")
        label = args.eyebrow.upper()
        ew = round(e_face.width(label)) + 44
        draw.rounded_rectangle([card[0] + pad, y, card[0] + pad + ew, y + 54], 27, fill=HONEY)
        e_face.draw(draw, (card[0] + pad + 22, y + 9), label, NAVY)
        y += 54 + 30
    icon_size = 250 if args.icon else 0
    text_w = card[2] - card[0] - 2 * pad
    h_face, h_lines = fit(args.headline, text_w, 3, 84, 52, "ExtraBold")
    y = block(draw, h_face, h_lines, card[0] + pad, y - 6, TINT_HEAD, 1.08) + 22
    if args.sub:
        sub_w = text_w - (icon_size + 24 if args.icon else 0)
        avail_lines = max(2, (card[3] - pad - y) // 50)
        s_face, s_lines = fit(args.sub, sub_w, min(avail_lines, 6), 40, 28, "Medium")
        block(draw, s_face, s_lines, card[0] + pad, y, TINT_BODY, 1.3)
    if args.icon:
        paste_icon(canvas, args.icon, icon_size, (card[2] - pad - icon_size + 16, card[3] - pad - icon_size + 16))
    return canvas


def cover(img, w, h):
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


def layout_photo(args):
    canvas = Image.new("RGB", (W, H), WHITE)
    logo_header(canvas, args.city)
    btn_top = cta_button(canvas, args.button)
    draw = ImageDraw.Draw(canvas)
    text_w = W - 2 * M - 16
    h_face, h_lines = fit(args.headline, text_w, 2, 62, 44, "ExtraBold")
    s_face, s_lines = (None, [])
    if args.sub:
        s_face, s_lines = fit(args.sub, text_w, 2, 36, 28, "Medium")
    text_h = block_height(h_face, h_lines, 1.1) + (14 + block_height(s_face, s_lines, 1.28) if s_lines else 0)
    text_top = btn_top - 34 - text_h
    ph = text_top - 30 - CARD_TOP
    photo = cover(Image.open(args.bg).convert("RGB"), W - 2 * M, ph)
    mask = Image.new("L", photo.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, photo.width - 1, photo.height - 1], 44, fill=255)
    canvas.paste(photo, (M, CARD_TOP), mask)
    y = block(draw, h_face, h_lines, M + 8, text_top, NAVY, 1.1)
    if s_lines:
        block(draw, s_face, s_lines, M + 8, y + 14, INK, 1.28)
    return canvas


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--layout", choices=["tips", "fact", "photo"], required=True)
    p.add_argument("--headline", required=True)
    p.add_argument("--sub", default="")
    p.add_argument("--tips", default="", help="tips separated by |")
    p.add_argument("--eyebrow", default="", help="short chip label, e.g. МИФ / ФАКТ / СОВЕТ")
    p.add_argument("--tint", default=ICE, help="service pastel hex")
    p.add_argument("--icon", help="service icon PNG (transparent)")
    p.add_argument("--bg", help="background photo (photo layout)")
    p.add_argument("--lang", choices=sorted(CITY), default="ru", help="slide language: city chip + default button")
    p.add_argument("--button", help="CTA label; default = the --lang label")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    args.city = CITY[args.lang]
    args.button = args.button or BUTTON[args.lang]
    if args.layout == "photo" and not args.bg:
        p.error("--bg is required for the photo layout")
    if args.layout == "tips" and not args.tips:
        p.error("--tips is required for the tips layout")
    build = {"tips": layout_tips, "fact": layout_fact, "photo": layout_photo}[args.layout]
    image = build(args)
    image.save(args.out, "PNG", optimize=True)
    # TikTok photo posts reject PNG ("use 'image/jpeg' or 'image/webp'"), so every post also gets a JPEG twin.
    jpg = os.path.splitext(args.out)[0] + ".jpg"
    if image.mode != "RGB":
        flat = Image.new("RGB", image.size, WHITE)
        flat.paste(image.convert("RGBA"), mask=image.convert("RGBA").getchannel("A"))
        image = flat
    image.save(jpg, "JPEG", quality=92, subsampling=0, optimize=True)
    print(args.out)
    print(jpg)


if __name__ == "__main__":
    main()
