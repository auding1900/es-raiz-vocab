# assets

README visuals for `es-raiz-vocab`.

## Current files

| File | What it is | Source |
| --- | --- | --- |
| `root_tree.svg` | Vector render of the selected `mut` family (exact generated Mermaid, `graph LR`) | `mindmaps/raiz_b12_mut.md` |
| `root_tree-social-base.svg` | Top-down (`graph TD`) presentation render of the same `mut` nodes, for a 2:1 card | same Mermaid block; only `rankdir` changed |
| `root_tree-social-base.png` | 1600 × 392 PNG base for the 1280 × 640 social card | same |
| `root_tree_family.png` | Pure PNG render of the older `vid` family (1013 × 1600) | `mindmaps/raiz_v0_vid.md` |
| `root_tree.png` | **Legacy** 1200 × 630 `vid` card; replace it with the 1280 × 640 card described in `root_tree-spec.md` | `scripts/make_root_tree_card.py` |
| `root_tree-spec.md` | Social preview spec, selected branch, render commands, and QA checklist | handwritten |
| `demo.gif` | **Labeled placeholder, not a recording** (1200 × 630) | `scripts/make_demo_placeholder.py` |

## Why the asset is rendered from a family page, not `root_tree.md`

`mindmaps/root_tree.md` is an **index** (tables of 232 roots). It contains **zero** fenced `mermaid` blocks, so `mmdc -i mindmaps/root_tree.md` has nothing to render.

The new base assets are rendered from a real generated family page, `mindmaps/raiz_b12_mut.md` (`mut` = “to change”, 5 derivatives, all C1/C2). The older `root_tree_family.png` and `root_tree.png` still use `vid`; the 1200 × 630 card is legacy and should be replaced with the 1280 × 640 card described in [`root_tree-spec.md`](root_tree-spec.md).

## Regenerate

From the repository root:

```bash
mkdir -p assets

# 1. Extract the selected mut Mermaid block (drop interactive click lines)
awk '/^```mermaid/{flag=1;next}/^```/{flag=0}flag' \
  mindmaps/raiz_b12_mut.md | grep -v '^[[:space:]]*click ' \
  > /tmp/es-raiz-mut.mmd

# 2. Exact LR render, as generated
PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  mmdc \
  -i /tmp/es-raiz-mut.mmd \
  -o assets/root_tree.svg \
  -b white \
  --size 1600

# 3. Top-down presentation base for the 1280 × 640 card.
#    Only the layout direction changes; nodes, edges, labels, and classes stay identical.
sed '1s/^graph LR$/graph TD/' /tmp/es-raiz-mut.mmd > /tmp/es-raiz-mut-td.mmd

PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  mmdc -i /tmp/es-raiz-mut-td.mmd \
  -o assets/root_tree-social-base.svg \
  -b white --size 1600

PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  mmdc -i /tmp/es-raiz-mut-td.mmd \
  -o assets/root_tree-social-base.png \
  -b white --size 1600

# 4. Regenerate the labeled demo placeholder (optional)
python scripts/make_demo_placeholder.py
```

Legacy assets: `root_tree_family.png` and `root_tree.png` still come from the older `vid` render and `scripts/make_root_tree_card.py` (1200 × 630). Do not use that script for the new 1280 × 640 card; see [`root_tree-spec.md`](root_tree-spec.md).

On Linux, replace the Chrome path with the installed Chrome/Chromium executable, or let puppeteer manage its own browser.

## Social preview

`assets/root_tree.png` is currently the **legacy 1200 × 630 `vid` card**. Do not upload it as the new preview. Follow [`root_tree-spec.md`](root_tree-spec.md): use `root_tree-social-base.png` to produce a **1280 × 640** card, then upload it manually in **Settings → Social preview** and check that the text and graph are legible at small size. Do not claim it is active until the upload is confirmed.

## Rules

- Do not hand-edit generated Mermaid files to make a prettier screenshot.
- The composed card must use the unmodified real render; do not redraw or invent graph nodes.
- Do not ask an image model to generate the graph structure from a text prompt; use the rendered base and image-to-image expansion only.
- Do not crop a node or change a CEFR label/color to make the card fit.
- Do not upload the legacy 1200 × 630 card as the new social preview.
- Do not present the placeholder GIF as a real recording.
- Do not fabricate a star count or user testimonial.
- Re-render the assets after changing the data or the Mermaid generator.
