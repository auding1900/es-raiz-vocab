#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create the clearly labeled demo-GIF placeholder used by the README.

This is *not* a recording. It exists so the README demo slot is not a broken
image and so nobody is tempted to fabricate a demo. Replace the output with a
real 60-second recording when it exists.

Optional dependency: Pillow (not required by the data pipeline).

Usage:
    python scripts/make_demo_placeholder.py
"""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    raise SystemExit("缺少 Pillow，请先执行：pip install pillow")

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "assets"
SOURCE = ASSETS / "root_tree_family.png"
OUTPUT = ASSETS / "demo.gif"

WIDTH, HEIGHT = 1200, 630


def load_font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> int:
    if not SOURCE.exists():
        raise SystemExit("缺少 assets/root_tree.png，请先按 assets/README.md 渲染")

    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#ffffff")
    draw = ImageDraw.Draw(canvas)
    ink = "#1a1a1a"
    muted = "#5f6368"
    accent = "#b71c1c"

    draw.rectangle([0, 0, WIDTH - 1, HEIGHT - 1], outline="#dadce0", width=2)
    draw.text((56, 58), "60-second demo", font=load_font(58, bold=True), fill=ink)
    draw.text(
        (58, 138),
        "PLACEHOLDER — NOT RECORDED YET",
        font=load_font(26, bold=True),
        fill=accent,
    )

    lines = [
        "This file is a labeled placeholder, not a recording.",
        "",
        "Shot list:",
        "docs/promo/demo-script.md",
        "",
        "After recording, replace this file with",
        "the real 60-second recording.",
    ]
    y = 208
    for line in lines:
        if line:
            draw.text((58, y), line, font=load_font(23), fill=ink if line == "Shot list:" else muted)
        y += 38

    map_image = Image.open(SOURCE).convert("RGB")
    max_height = 540
    scale = max_height / map_image.height
    map_image = map_image.resize(
        (max(1, int(map_image.width * scale)), max_height),
        Image.LANCZOS,
    )
    x = WIDTH - map_image.width - 56
    y = (HEIGHT - map_image.height) // 2
    canvas.paste(map_image, (x, y))
    draw.rectangle(
        [x - 1, y - 1, x + map_image.width, y + map_image.height],
        outline="#dadce0",
        width=2,
    )

    canvas.save(OUTPUT, format="GIF", optimize=True)
    print("written: {0} ({1}x{2})".format(OUTPUT.relative_to(REPO_ROOT), WIDTH, HEIGHT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
