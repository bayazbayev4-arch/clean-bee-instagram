#!/usr/bin/env python3
"""Add the Clean Bumble Bee end card to a generated Reel.

Video models warp logos and letters, so the brand only appears on this card,
rendered from the official files (same rule as compose.py): white background,
stacked logo, one short Russian line, Safe Blue pill with the site and
«Ссылка в профиле» underneath. The card fades in over the last frames of the
video while the video's own sound fades out.

Needs ffmpeg: the system one, or `pip install imageio-ffmpeg` (cloud routine).

Example:
  python3 skills/daily-reel/scripts/endcard.py --in reels/<folder>/raw.mp4 \
      --out reels/<folder>/final.mp4 --line "Пятно? Курьер заберёт у двери"
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# Reuse the feed renderer's fonts, colours and text fitting so the card matches the posts.
_spec = importlib.util.spec_from_file_location(
    "compose", os.path.join(ROOT, "skills", "daily-ig-post", "scripts", "compose.py"))
compose = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(compose)


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
    except ImportError:
        sys.exit("ffmpeg not found — install it or run: pip install imageio-ffmpeg")
    return imageio_ffmpeg.get_ffmpeg_exe()


def probe(ff, path):
    """Size, fps, duration and audio presence, read from `ffmpeg -i` (ffprobe isn't always installed)."""
    info = subprocess.run([ff, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    dur = re.search(r"Duration: (\d+):(\d+):(\d+(?:\.\d+)?)", info)
    video = re.search(r"Stream #.*Video:.*", info)
    if not dur or not video:
        sys.exit(f"can't read video info from {path}")
    line = video.group(0)
    size = re.search(r", (\d{2,5})x(\d{2,5})[ ,\[]", line)
    fps = re.search(r", (\d+(?:\.\d+)?) fps", line) or re.search(r", (\d+(?:\.\d+)?) tbr", line)
    h, m, s = dur.groups()
    return {
        "duration": round(int(h) * 3600 + int(m) * 60 + float(s), 3),
        "width": int(size.group(1)),
        "height": int(size.group(2)),
        "fps": float(fps.group(1)) if fps else 24.0,
        "audio": re.search(r"Stream #.*Audio:", info) is not None,
    }


def logo_image(path):
    """Official logo flattened onto white and trimmed to its artwork.

    The stacked PNG carries a faint off-white texture around the artwork that shows as
    a grey haze on a pure white card, so near-white pixels are snapped to white.
    """
    im = Image.open(path).convert("RGBA")
    flat = Image.alpha_composite(Image.new("RGBA", im.size, "white"), im).convert("RGB")
    r, g, b = flat.split()
    darkest = ImageChops.darker(ImageChops.darker(r, g), b)
    flat.paste((255, 255, 255), mask=darkest.point(lambda v: 255 if v >= 232 else 0))
    mask = ImageChops.difference(flat, Image.new("RGB", flat.size, "white")).convert("L")
    box = mask.point(lambda v: 255 if v > 24 else 0).getbbox()
    return flat.crop(box) if box else flat


def centred(draw, face, lines, cx, y, fill, leading):
    step = round(face.size * leading)
    for text in lines:
        face.draw(draw, (cx - face.width(text) / 2, y), text, fill)
        y += step
    return y


def render_card(w, h, line, site, hint):
    s = w / 1080  # designed at 1080 wide, scaled to the video
    card = Image.new("RGB", (w, h), compose.WHITE)
    draw = ImageDraw.Draw(card)

    logo = logo_image(os.path.join(compose.BRAND, "logos", "stacked-centred.png"))
    lw = round(560 * s)
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)

    l_face, l_lines = compose.fit(line, round(900 * s), 2, round(76 * s), round(48 * s), "ExtraBold")
    p_face = compose.Face(round(44 * s), "ExtraBold")
    h_face = compose.Face(round(34 * s), "Medium")
    pill_h = round(104 * s)
    pill_w = round(p_face.width(site) + 112 * s)

    gap_logo, gap_pill, gap_hint = round(72 * s), round(56 * s), round(30 * s)
    text_h = round(l_face.size * 1.12) * len(l_lines)
    total = logo.height + gap_logo + text_h + gap_pill + pill_h + gap_hint + round(h_face.size * 1.3)
    y = (h - total) // 2

    card.paste(logo, ((w - logo.width) // 2, y))
    y += logo.height + gap_logo
    y = centred(draw, l_face, l_lines, w / 2, y, compose.NAVY, 1.12) + gap_pill
    x0 = (w - pill_w) // 2
    draw.rounded_rectangle([x0, y, x0 + pill_w, y + pill_h], pill_h // 2, fill=compose.SAFE_BLUE)
    p_face.draw(draw, ((w - p_face.width(site)) / 2, y + (pill_h - p_face.size * 1.25) / 2), site, compose.WHITE)
    y += pill_h + gap_hint
    centred(draw, h_face, [hint], w / 2, y, compose.INK, 1.3)
    return card


def build(ff, src, out, card_png, info, card_seconds, fade):
    w, h, fps, dur = info["width"], info["height"], info["fps"], info["duration"]
    cmd = [ff, "-y", "-hide_banner", "-loglevel", "error",
           "-i", src,
           "-loop", "1", "-framerate", f"{fps}", "-t", f"{card_seconds}", "-i", card_png,
           "-f", "lavfi", "-t", f"{card_seconds}", "-i", "anullsrc=r=48000:cl=stereo"]
    if info["audio"]:
        a0 = "[0:a]"
    else:  # silent video: give it a silent track so the crossfade still works
        cmd += ["-f", "lavfi", "-t", f"{dur}", "-i", "anullsrc=r=48000:cl=stereo"]
        a0 = "[3:a]"
    graph = (
        f"[0:v]fps={fps},scale={w}:{h},setsar=1,format=yuv420p,settb=AVTB[v0];"
        f"[1:v]fps={fps},scale={w}:{h},setsar=1,format=yuv420p,settb=AVTB[v1];"
        f"[v0][v1]xfade=transition=fade:duration={fade}:offset={max(0.0, dur - fade):.3f}[v];"
        f"{a0}aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,apad,atrim=0:{dur:.3f},"
        f"afade=t=out:st={max(0.0, dur - 0.8):.3f}:d=0.8[a0];"
        f"[2:a]aformat=sample_fmts=fltp:channel_layouts=stereo[a1];"
        f"[a0][a1]acrossfade=d={fade}[a]"
    )
    cmd += ["-filter_complex", graph, "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)


def main():
    p = argparse.ArgumentParser(description="Add the Clean Bumble Bee end card to a Reel.")
    p.add_argument("--in", dest="src", required=True, help="generated video")
    p.add_argument("--out", required=True)
    p.add_argument("--line", required=True, help="short Russian line, max 6 words")
    p.add_argument("--site", default="cleanbumblebee.com")
    p.add_argument("--hint", default="Ссылка в профиле")
    p.add_argument("--seconds", type=float, default=2.0, help="how long the card stays on screen")
    p.add_argument("--fade", type=float, default=0.35)
    p.add_argument("--card-png", help="also save the card image here, to look at it")
    args = p.parse_args()

    ff = ffmpeg_exe()
    info = probe(ff, args.src)
    card = render_card(info["width"], info["height"], args.line, args.site, args.hint)
    if args.card_png:
        card.save(args.card_png)
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, "card.png")
        card.save(png)
        build(ff, args.src, args.out, png, info, args.seconds, args.fade)
    print(json.dumps({"out": args.out, **probe(ff, args.out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
