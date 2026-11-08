#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the landscape README / social-preview card from a real family render.

Input:  assets/root_tree_family.png  (pure Mermaid render, portrait)
Output: assets/root_tree.png         (1200x630 card with title + the same map)

The card is a presentation layer, not a synthetic graph: the diagram on the
right is the unmodified render of a generated page.

Optional dependency: Pillow (not required by the data pipeline).

Usage:
    python scripts/make_root_tree_card.py
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
OUTPUT = ASSETS / "root_tree.png"

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
        raise SystemExit("缺少 assets/root_tree_family.png，请先按 assets/README.md 渲染")

    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#ffffff")
    draw = ImageDraw.Draw(canvas)

    ink = "#1a1a1a"
    muted = "#5f6368"
    blue = "#1565c0"

    draw.rectangle([0, 0, WIDTH - 1, HEIGHT - 1], outline="#dadce0", width=2)
    draw.text((56, 52), "es-raiz-vocab", font=load_font(20, bold=True), fill=blue)
    draw.text((56, 92), "Spanish root map", font=load_font(52, bold=True), fill=ink)
    draw.text((56, 162), "Not another vocabulary app.", font=load_font(26), fill=muted)

    draw.line([56, 222, 730, 222], fill="#dadce0", width=2)
    draw.text((56, 252), "232 roots  ·  1,423 words", font=load_font(24, bold=True), fill=ink)
    draw.text((56, 292), "1,513 typed relations  ·  A1–C2", font=load_font(24), fill=ink)
    draw.text((56, 332), "Structure only. Meanings on demand.", font=load_font(24), fill=muted)

    draw.text((56, 408), "Example family:", font=load_font(19, bold=True), fill=muted)
    draw.text((56, 440), "vid  ·  videre (to see)", font=load_font(24), fill=ink)
    draw.text((56, 478), "ver · vista · visible · prever", font=load_font(21), fill=muted)

    draw.text(
        (56, 564),
        "Real render: mindmaps/raiz_v0_vid.md",
        font=load_font(17),
        fill="#80868b",
    )

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

    canvas.save(OUTPUT, format="PNG", optimize=True)
    print("written: {0} ({1}x{2})".format(OUTPUT.relative_to(REPO_ROOT), WIDTH, HEIGHT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
