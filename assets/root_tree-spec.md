# Social preview card spec — `assets/root_tree.png`

- Status: **base render ready; final 1280 × 640 card not yet produced**
- Last updated: 2026-11-08
- Target file: `assets/root_tree.png`
- Current `assets/root_tree.png`: still the old **1200 × 630** `vid` card. Replace it; do not upload it as the new GitHub Social preview.
- README reference: both `README.md` and `README.zh-CN.md` already point to `assets/root_tree.png`; keep that path.

## 1. Selected branch

| Field | Value |
| --- | --- |
| Root | `mut` |
| Latin origin | `mutare` (to change) |
| Index row | `mindmaps/root_tree.md` line 149 |
| Source page | [`mindmaps/raiz_b12_mut.md`](../mindmaps/raiz_b12_mut.md) |
| Derivatives | 5 |
| Graph nodes | 6 (root + 5 words) |
| Edges | 5 `derivar` edges |

Words and levels (exactly as generated):

| Word | CEFR |
| --- | --- |
| `mutación` | C1 |
| `mutante` | C1 |
| `mutar` | C1 |
| `inmutable` | C1 |
| `mutabilidad` | C2 |

Why this branch:

- all five derivatives are **C1/C2**, matching the B2/C2 preference;
- 6 nodes total, inside the 5–8 node range;
- short labels stay readable when the card is viewed as a small link preview;
- the family has one clear semantic idea (`change`), so the card does not need extra explanatory text.

`mindmaps/root_tree.md` is an **index** and contains no fenced Mermaid blocks. The block was extracted from the family page linked by that index, not invented.

## 2. Rendered files

| File | What it is | Status |
| --- | --- | --- |
| `assets/root_tree.svg` | Exact render of the extracted `mut` Mermaid block, `graph LR`; `click` lines removed so the SVG has no interactive links | Ready |
| `assets/root_tree-social-base.svg` | Top-down presentation layout (`graph TD`) of the same nodes, edges, labels, and classes; **only `rankdir` changed** | Ready |
| `assets/root_tree-social-base.png` | 1600 × 392 PNG of the top-down layout, intended as the image-to-image base for 豆包 | Ready |
| `assets/root_tree.png` | Final 1280 × 640 social card | **Still the old 1200 × 630 `vid` card; replace manually** |

The generated page remains `graph LR`. The `TD` version exists only because a left-to-right family graph stacks seven or more siblings vertically and becomes unreadable when fitted into a 2:1 social card. No node, edge, label, CEFR value, or color was changed.

## 3. GitHub Social preview hard specs

| Requirement | Value |
| --- | --- |
| Dimensions | **1280 × 640 px exactly** |
| Aspect ratio | 2:1 |
| File size | **< 1 MB** |
| Formats | PNG, JPG, or GIF (PNG recommended) |
| Color | sRGB; opaque background (no transparency) |
| Safe area | Keep all text and nodes at least 64 px from each edge |
| Old size | **Do not use 1200 × 630**; GitHub may crop it to 2:1 |

Check the uploaded card at small size, not only at full resolution. If the node labels are not readable in a 300 px-wide preview, the card is too dense.

## 4. Visual requirements

- **Main subject:** the local `mut` map with 6 nodes. It should occupy most of the card, not sit as a tiny inset.
- **Text:** only two blocks:
  1. project name: `es-raiz-vocab`
  2. one positioning sentence: `A structure-only Spanish root map.`
- No feature lists, statistics, star counts, testimonials, or “download” callouts.
- Keep the generated CEFR colors: C1 and C2 must stay visually distinct. Do not recolor nodes arbitrarily.
- Background: solid white or a near-white neutral. No gradients, glow, 3D, noise, paper texture, stock photos, or AI art filters.
- Preserve the base image’s aspect ratio. Do not stretch it to fill the canvas; add whitespace or extend the background instead.
- Do not crop the root node or any of the five word nodes.
- The root label contains `mutare (to change)`. If the layout wraps it, keep both lines; do not shorten it to `mutare` only.

Suggested composition:

```text
┌──────────────────────────────────────────────┐
│  es-raiz-vocab                               │
│  A structure-only Spanish root map.          │
│                                              │
│            [ mut / mutare (to change) ]      │
│              │    │    │    │    │           │
│         mutación mutante mutar inmutable ... │
│                                              │
│                                     (white)  │
└──────────────────────────────────────────────┘
```

The diagram can run full-width under the title. Leave the bottom area empty rather than adding more text.

## 5. Recommended workflow

1. Start from `assets/root_tree-social-base.png` (1600 × 392) or `assets/root_tree-social-base.svg`.
2. Use 豆包 / Seedream as an **image-to-image / canvas-expansion** tool, not as a text-to-image generator.
3. Expand the canvas to **1280 × 640**, keep the diagram unchanged, add only the project name and the one sentence.
4. Export PNG at 1280 × 640, sRGB, < 1 MB.
5. Verify every character manually against this spec and `mindmaps/raiz_b12_mut.md`.
6. Replace `assets/root_tree.png`. Do not change the README image path.
7. Upload the new file in **GitHub → Settings → Social preview**, then check new Reddit, old Reddit, and mobile.

Suggested 豆包 prompt (image-to-image):

```text
Use the provided diagram as the exact subject. Expand the canvas to 1280×640 with a clean white background. Add only two text blocks: "es-raiz-vocab" and "A structure-only Spanish root map." Do not redraw, add, remove, or rename any node. Keep every node label, CEFR level, arrow, and color exactly as provided. No decorative elements, no gradients, no AI art filters. Leave at least 64 px of empty margin around the diagram.
```

中文版：

```text
以我提供的导图为主体，把画布扩展到 1280×640，纯白背景。只添加两处文字："es-raiz-vocab" 和 "A structure-only Spanish root map."。不要重画、增加、删除或改名任何节点；所有节点文字、CEFR 级别、箭头和颜色必须与底图一致。不要装饰元素、渐变或 AI 艺术滤镜。导图四周至少留 64 px 空白。
```

## 6. Explicit prohibitions

- **Do not** ask 豆包 to “generate a Spanish root map” from a text prompt. Text-to-image will invent nodes, misspell Spanish words, and produce unreadable labels.
- **Do not** add definitions, translations, example sentences, star counts, user numbers, or testimonials.
- **Do not** apply AI art filters, glow, 3D, paper texture, or decorative icons.
- **Do not** change CEFR labels or colors to “look better”.
- **Do not** crop a node to make the diagram fit.
- **Do not** upload the old 1200 × 630 card as the new social preview.
- **Do not** claim the preview is live until the upload is confirmed.

## 7. Manual QA checklist

- [ ] File is exactly 1280 × 640 px.
- [ ] File is PNG/JPG/GIF and < 1 MB.
- [ ] Project name is spelled `es-raiz-vocab`.
- [ ] Sentence is exactly `A structure-only Spanish root map.`
- [ ] Root label reads `mut` and `mutare (to change)`.
- [ ] Five word labels read `mutación` (C1), `mutante` (C1), `mutar` (C1), `inmutable` (C1), `mutabilidad` (C2).
- [ ] No extra nodes, words, arrows, or levels were added.
- [ ] C1 and C2 colors are unchanged from the base.
- [ ] All text is readable at 25–50% zoom.
- [ ] No AI artifacts, duplicated letters, or garbled accents.
- [ ] At least 64 px safe margin around text and nodes.
- [ ] `README.md` and `README.zh-CN.md` still reference `assets/root_tree.png`.
- [ ] Social preview checked on new Reddit, old Reddit, and mobile.

## 8. Render commands used

```bash
# Extract the first mermaid block from the generated family page
python - <<'PY'
from pathlib import Path
src = Path("mindmaps/raiz_b12_mut.md").read_text(encoding="utf-8")
start = src.index("```mermaid") + len("```mermaid")
end = src.index("```", start)
block = src[start:end].strip()
kept = [line for line in block.splitlines() if not line.strip().startswith("click ")]
Path("/tmp/es-raiz-mut.mmd").write_text("\n".join(kept) + "\n", encoding="utf-8")
Path("/tmp/es-raiz-mut-td.mmd").write_text(
    "\n".join(["graph TD"] + kept[1:]) + "\n", encoding="utf-8"
)
PY

# Exact LR render (as generated)
mmdc -i /tmp/es-raiz-mut.mmd \
  -o assets/root_tree.svg \
  --size 1600 -b white \
  -p /tmp/puppeteer.json

# Top-down presentation base for the 2:1 card
mmdc -i /tmp/es-raiz-mut-td.mmd \
  -o assets/root_tree-social-base.svg \
  --size 1600 -b white \
  -p /tmp/puppeteer.json

mmdc -i /tmp/es-raiz-mut-td.mmd \
  -o assets/root_tree-social-base.png \
  --size 1600 -b white \
  -p /tmp/puppeteer.json
```

`mermaid-render` alternative, if `mmdc` is not installed:

```bash
mermaid-render -i /tmp/es-raiz-mut-td.mmd -o assets/root_tree-social-base.svg
```

Do not install a system-level renderer just for this asset; `mmdc` or `mermaid-render` is enough.
