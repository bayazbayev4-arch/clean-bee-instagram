#!/usr/bin/env python3
"""Render an on-brand Clean Bumble Bee Instagram Story (1080x1920).

Brand guideline §08 for Stories: keep the top 250 px free of text (profile name
overlay) and the bottom 350 px free (reply bar). Everything sits between them.
Shares fonts, colours and logo handling with compose.py.

  --steps "a|b|c"   numbered steps in a white card (omit for a big-message story)
  --big "−25%"      optional huge figure above the headline

Example:
  python3 story.py --tint "#BAEBFF" --icon ../../../brand/cbb-mascot.png --eyebrow "Как это работает" \
      --headline "Химчистка без поездок" --steps "Выберите окно в 2 часа|Курьер заберёт вещи у двери|Привезём чистыми в ваше окно" \
      --out story.png
"""
import argparse
import os

from PIL import Image, ImageDraw

from compose import (BRAND, HONEY, NAVY, SAFE_BLUE, TINT_BODY, TINT_HEAD, WHITE, Face, block,
                     block_height, fit, paste_icon, trimmed, wrap)

W, H = 1080, 1920
SAFE_TOP, SAFE_BOTTOM = 250, 350
M = 72


def pill(draw, face, text, cx, y, fill, color, pad_x=40, height=None):
    height = height or round(face.size * 1.9)
    w = round(face.width(text)) + 2 * pad_x
    x0 = cx - w // 2
    draw.rounded_rectangle([x0, y, x0 + w, y + height], height // 2, fill=fill)
    face.draw(draw, (x0 + pad_x, y + (height - face.size * 1.25) / 2), text, color)
    return y + height


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tint", default="#BAEBFF")
    p.add_argument("--icon")
    p.add_argument("--eyebrow", default="")
    p.add_argument("--big", default="")
    p.add_argument("--headline", required=True)
    p.add_argument("--sub", default="")
    p.add_argument("--steps", default="")
    p.add_argument("--button", default="cleanbumblebee.com · ссылка в профиле")
    p.add_argument("--out", required=True)
    a = p.parse_args()

    canvas = Image.new("RGB", (W, H), a.tint)
    draw = ImageDraw.Draw(canvas)

    # Logo on its white rounded plate (never straight on a pastel or photo)
    logo = trimmed(os.path.join(BRAND, "logos", "primary-horizontal.png"))
    lh = 104
    logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
    plate = [(W - logo.width) // 2 - 40, SAFE_TOP, (W + logo.width) // 2 + 40, SAFE_TOP + lh + 48]
    draw.rounded_rectangle(plate, 40, fill=WHITE)
    canvas.paste(logo, (plate[0] + 40, plate[1] + 24))
    y = plate[3] + 64

    bottom = H - SAFE_BOTTOM
    btn_h = 104
    btn_face, _ = fit(a.button, W - 2 * M - 80, 1, 38, 26, "ExtraBold")
    btn_top = bottom - btn_h
    bw = round(btn_face.width(a.button)) + 96
    draw.rounded_rectangle([(W - bw) // 2, btn_top, (W + bw) // 2, bottom], btn_h // 2, fill=SAFE_BLUE)
    btn_face.draw(draw, ((W - btn_face.width(a.button)) / 2, btn_top + (btn_h - btn_face.size * 1.25) / 2), a.button, WHITE)

    if a.eyebrow:
        y = pill(draw, Face(34, "ExtraBold"), a.eyebrow.upper(), W // 2, y, HONEY, NAVY) + 40

    text_w = W - 2 * M
    if a.big:
        big_face, _ = fit(a.big, text_w, 1, 300, 160, "ExtraBold")
        big_face.draw(draw, ((W - big_face.width(a.big)) / 2, y - big_face.size * 0.12), a.big, TINT_HEAD)
        y += round(big_face.size * 1.08)

    h_face, h_lines = fit(a.headline, text_w, 3, 104 if not a.big else 76, 60, "ExtraBold")
    for line in h_lines:
        h_face.draw(draw, ((W - h_face.width(line)) / 2, y), line, TINT_HEAD)
        y += round(h_face.size * 1.1)
    y += 28

    if a.sub:
        s_face, s_lines = fit(a.sub, text_w - 40, 4, 46, 34, "Medium")
        for line in s_lines:
            s_face.draw(draw, ((W - s_face.width(line)) / 2, y), line, TINT_BODY)
            y += round(s_face.size * 1.32)
        y += 36

    icon_zone_bottom = btn_top - 48
    if a.steps:
        steps = [s.strip() for s in a.steps.split("|") if s.strip()]
        card_top = y + 12
        pad = 48
        inner = W - 2 * M - 2 * pad - 96
        t_face = Face(54, "SemiBold")
        wrapped = [wrap(t_face, s, inner) for s in steps]
        gap = 56
        content = sum(max(block_height(t_face, w_, 1.22), 72) for w_ in wrapped) + gap * (len(steps) - 1)
        card_bottom = card_top + content + 2 * pad
        draw.rounded_rectangle([M, card_top, W - M, card_bottom], 48, fill=WHITE)
        sy = card_top + pad
        n_face = Face(38, "ExtraBold")
        for i, lines in enumerate(wrapped, 1):
            r = 36
            cx, cy = M + pad + r, sy + r
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SAFE_BLUE)
            n_face.draw(draw, (cx - n_face.width(str(i)) / 2, cy - n_face.size * 0.66), str(i), WHITE)
            th = block_height(t_face, lines, 1.22)
            block(draw, t_face, lines, M + pad + 96, sy + max(0, (72 - th) // 2) - 4, TINT_BODY, 1.22)
            sy += max(th, 72) + gap
        y = card_bottom + 36

    if a.icon:
        size = min(420, icon_zone_bottom - y)
        if size >= 160:
            paste_icon(canvas, a.icon, size, ((W - size) // 2, y + (icon_zone_bottom - y - size) // 2))

    canvas.save(a.out, "PNG", optimize=True)
    print(a.out)


if __name__ == "__main__":
    main()
