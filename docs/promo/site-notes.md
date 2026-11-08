# Static site notes

- Build command: `python scripts/build_site.py`
- Output: `site/index.html` (single file, generated; `site/` is git-ignored)
- Current build: 232 roots · 1,423 words · 1,513 relations · 1,419 CEFR-tagged words · 364 no-root words; about 3.4 MB uncompressed
- Deployment: `.github/workflows/pages.yml` builds on `main` pushes and `workflow_dispatch`
- Pages URL: <https://auding1900.github.io/es-raiz-vocab/>

## Why `root_tree.md` is not embedded directly

`mindmaps/root_tree.md` is an **index** of 232 roots, not a Mermaid file. It contains **zero** fenced `mermaid` blocks.

`build_site.py` therefore:

1. parses the tables in `mindmaps/root_tree.md` for root id, Latin origin, word/relation counts, batch grouping, and the linked family file;
2. reads each linked `mindmaps/raiz_*.md` and extracts its real Mermaid block;
3. embeds the default family (preferring `vid`) as `<pre class="mermaid">` and stores all family sources as inline JSON;
4. renders the selected family on demand with Mermaid.

This keeps the site complete (all 232 families are selectable) without rendering 232 diagrams at once.

## Views

| View | Data source | Interaction |
| --- | --- | --- |
| Map · 导图 | `mindmaps/root_tree.md` + `mindmaps/raiz_*.md` | Search the root list; select a root; render its Mermaid diagram; word nodes may open Doubao |
| Levels · 分级 | `levels/A1.md` … `levels/C2.md` | A1–C2 tabs + “All”; search word/root; Doubao link + copy prompt per row |
| No-root · 补充 | `no-raiz-vocab.md` | A1–C2 tabs + “All”; search word/POS; Doubao link + copy prompt per row |
| About · 说明 | static | Three hard constraints, project links, offline/CDN notes, CEFR disclaimer |

## Search

- Pure client-side filtering with native JavaScript.
- Accent-insensitive normalization: NFD + removal of combining marks, then lowercase.
- Root search matches `id`, `rootName`, and `latin`.
- Level search matches `word` and `root`.
- No-root search matches `word` and `pos`.
- No search index, network call, or server-side query is involved.

## Copy-prompt behavior

- Each level row and no-root row has a **复制查询指令** button.
- The prompt is extracted from the row’s generated Doubao URL (`q` query parameter), so custom `prompt_template` values are preserved.
- No-root words use the default template with the root clause removed.
- Clipboard API is used when available; a hidden textarea + `execCommand("copy")` is the fallback for `file://` or older browsers.
- The toast explicitly says the prompt can be pasted into any LLM (ChatGPT / Claude / Gemini 等).
- No prompt text is stored outside the generated `site/index.html`.

## Relative paths and base path

- The site is a single `site/index.html` with inline CSS and JS.
- Internal navigation uses hash views (`#map`, `#levels`, `#no-root`, `#about`) and JavaScript, so there is **no** absolute `/assets/...` path and no GitHub Pages base-path risk.
- External links (GitHub, Doubao, CDN) are absolute by design.
- No `base` element, no service worker, no relative fetch of JSON.

## CDN dependency

- Mermaid is pinned to **11.4.1** from jsDelivr:
  `https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js`
- The first diagram render needs network access to the CDN.
- If the CDN is blocked, the page shows a clear error; the raw Mermaid source remains in the page and the same data is in the GitHub repository.
- `securityLevel: "loose"` is used so generated `click` directives can open Doubao. The Mermaid source is generated and trusted; do not feed untrusted Mermaid into this page.

## Privacy and content boundary

- No analytics, cookies, accounts, or server-side storage.
- The site displays only root/word structure, relation types, CEFR tags, Latin origins, and generated lookup prompts.
- It does not copy dictionary definitions, translations, or example sentences.
- Doubao and any other LLM are external services; their output is not stored by this site.

## Local preview

```bash
python scripts/build_site.py
python -m http.server 8000 --directory site
# open http://localhost:8000/
```

Opening `site/index.html` directly with `file://` also works for the Mermaid CDN and local filtering; clipboard may fall back to `execCommand`.

## CI

`.github/workflows/pages.yml`:

1. `actions/checkout@v5`
2. `actions/setup-python@v6` (Python 3.11)
3. `pip install -r requirements.txt`
4. `python scripts/generate_mermaid.py`
5. `python scripts/build_no_raiz.py`
6. `python scripts/build_site.py`
7. `actions/configure-pages@v6`
8. `actions/upload-pages-artifact@v5` with `path: site`
9. `actions/deploy-pages@v5`

All action versions target the Node 24 runtime. `site/` is generated in CI and is not committed. Do not hand-edit it.

## Known limits

- Mermaid rendering is client-side; very large graphs may take a moment.
- The root list renders all 232 entries; the level table can show 1,419 rows under “All”.
- GitHub Pages must be enabled manually in **Settings → Pages → Source: GitHub Actions**.
- The release PDFs are built separately (`scripts/export_pdf.py`) and are not part of the site.
