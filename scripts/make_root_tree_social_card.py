#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compose the 1280x640 GitHub social card from the real Mermaid base render.

Input:  assets/root_tree-social-base.png  (mmdc render of the real `mut` family)
Output: assets/root_tree.png              (1280x640 card, no image model)

The diagram is pasted unchanged apart from uniform scaling. No node is added,
removed, renamed, or recolored.

Optional dependency: Pillow (not required by the data pipeline).

Usage:
    python scripts/make_root_tree_social_card.py
"""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    raise SystemExit("缺少 Pillow，请先执行：pip install pillow")

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE = REPO_ROOT / "assets" / "root_tree-social-base.png"
OUTPUT = REPO_ROOT / "assets" / "root_tree.png"

WIDTH, HEIGHT = 1280, 640
MARGIN = 72

INK = "#1a1a1a"
BLUE = "#1565c0"
LINE = "#dadce0"
WHITE = "#ffffff"

PROJECT_NAME = "es-raiz-vocab"
TAGLINE = "A structure-only Spanish root map."


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
    if not BASE.exists():
        raise SystemExit(
            "缺少 assets/root_tree-social-base.png，请先按 assets/root_tree-spec.md 渲染"
        )

    canvas = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(canvas)

    draw.text((MARGIN, 64), PROJECT_NAME, font=load_font(30, bold=True), fill=BLUE)
    draw.text((MARGIN, 116), TAGLINE, font=load_font(42, bold=True), fill=INK)
    draw.line([MARGIN, 192, WIDTH - MARGIN, 192], fill=LINE, width=2)

    diagram = Image.open(BASE).convert("RGB")
    max_width = WIDTH - 2 * MARGIN
    scale = min(1.0, max_width / diagram.width)
    new_size = (
        max(1, int(diagram.width * scale)),
        max(1, int(diagram.height * scale)),
    )
    diagram = diagram.resize(new_size, Image.LANCZOS)

    x = (WIDTH - new_size[0]) // 2
    top = 220
    bottom = HEIGHT - 48
    y = top + (bottom - top - new_size[1]) // 2

    canvas.paste(diagram, (x, y))
    draw.rectangle(
        [x - 1, y - 1, x + new_size[0], y + new_size[1]],
        outline=LINE,
        width=2,
    )

    canvas.save(OUTPUT, format="PNG", optimize=True)
    print("written: {0} ({1}x{2})".format(OUTPUT.relative_to(REPO_ROOT), WIDTH, HEIGHT))
    print("diagram: {0}x{1} at ({2}, {3})".format(new_size[0], new_size[1], x, y))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
