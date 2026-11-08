# assets

README visuals for `es-raiz-vocab`.

## Current files

| File | What it is | Source |
| --- | --- | --- |
| `root_tree.svg` | Vector render of one generated root-family page | `mindmaps/raiz_v0_vid.md` |
| `root_tree_family.png` | Pure PNG render of the same page (1013 × 1600) | same Mermaid block |
| `root_tree.png` | Landscape README / social-preview card (1200 × 630), composed from the pure render | `scripts/make_root_tree_card.py` |
| `demo.gif` | **Labeled placeholder, not a recording** (1200 × 630) | `scripts/make_demo_placeholder.py` |

## Why the asset is rendered from a family page, not `root_tree.md`

`mindmaps/root_tree.md` is an **index** (tables of 232 roots). It contains **zero** fenced `mermaid` blocks, so `mmdc -i mindmaps/root_tree.md` has nothing to render.

The asset is therefore rendered from a real generated family page, `mindmaps/raiz_v0_vid.md` (`vid` = “to see”). It is a representative sample, not a synthetic illustration and not the full 232-root index.

## Regenerate

From the repository root:

```bash
mkdir -p assets

# 1. Extract the first Mermaid block from a generated family page
awk '/^```mermaid/{flag=1;next}/^```/{flag=0}flag' \
  mindmaps/raiz_v0_vid.md > /tmp/es-raiz-root_tree.mmd

# 2. Render the vector and the pure PNG.
#    Use `mmdc` if installed globally; otherwise use `npx -y @mermaid-js/mermaid-cli`.
PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  mmdc \
  -i /tmp/es-raiz-root_tree.mmd \
  -o assets/root_tree.svg \
  -b white

PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  mmdc \
  -i /tmp/es-raiz-root_tree.mmd \
  -o assets/root_tree_family.png \
  -b white \
  --size 1600

# 3. Compose the landscape README / social-preview card
pip install pillow   # optional, only for the composed assets
python scripts/make_root_tree_card.py

# 4. Regenerate the labeled demo placeholder (optional)
python scripts/make_demo_placeholder.py
```

On Linux, replace the Chrome path with the installed Chrome/Chromium executable, or let puppeteer manage its own browser.

## Social preview

`assets/root_tree.png` is a landscape 1200 × 630 card with the map on the right and the title on the left. Upload it manually in **Settings → Social preview**, then check that the text and graph are legible at small size. Do not claim it is active until the upload is confirmed.

## Rules

- Do not hand-edit generated Mermaid files to make a prettier screenshot.
- The composed card must use the unmodified real render; do not redraw or invent graph nodes.
- Do not present the placeholder GIF as a real recording.
- Do not fabricate a star count or user testimonial.
- Re-render the assets after changing the data or the Mermaid generator.
