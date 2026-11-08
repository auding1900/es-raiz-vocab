# GitHub Release — published record

- Status: **published** on 2026-11-08
- URL: <https://github.com/auding1900/es-raiz-vocab/releases/tag/v0.29.1>
- Release id: `438154786`
- Tag: `v0.29.1` → commit `886a5ec`
- Assets: 8 files = 7 PDFs (`A1.pdf` … `C2.pdf`, `index-toc.pdf`) + `SHA256SUMS.txt`; every uploaded size was checked against `dist/pdf/`
- PDFs were built locally on 2026-11-08 (A1 10 / A2 36 / B1 62 / B2 76 / C1 51 / C2 12 pages; `index-toc.pdf` 6 pages). They are in `dist/pdf/` and are **not** committed.
- Both `README.md` and `README.zh-CN.md` now link to this release.

## Published tag and title

| Field | Value |
| --- | --- |
| Tag | `v0.29.1` |
| Target | `886a5ec` |
| Title | `v0.29.1 — A navigable Spanish root map (232 roots / 1,423 words)` |
| Type | Published (draft created, assets verified, then published) |

`v0.29.0` already exists as a tag (it points to the C2 data batch, commit `ec3d2df`), so this release uses `v0.29.1` instead of reusing or moving that tag. `CHANGELOG.md` has the matching `0.29.1` entry.

## Published release body

```markdown
## A navigable Spanish root map

**Not another vocabulary app.** This release packages the current root map and the offline PDF bundles.

- **232** Latin/Greek roots
- **1,423** words
- **1,513** typed relations (`derivar` / `asociar` / `confundir`)
- **1,419** words with CEFR tags (A1 77 / A2 218 / B1 326 / B2 406 / C1 300 / C2 92)

### What is in the repository

- `data/*.yaml`: roots, affixes, and relation edges — the source of truth
- `mindmaps/`: one Mermaid page per root family
- `levels/`: A1–C2 word lists
- `no-raiz-vocab.md`: high-frequency words that cannot be decomposed by Latin roots

The repository stores **structure only**. It contains no definitions, translations, or example sentences. Generated links open Doubao by default, and the same prompt works with ChatGPT, Claude, Gemini, or any other LLM.

### Offline PDFs

This release attaches the static PDF bundles:

- `A1.pdf` … `C2.pdf`
- `index-toc.pdf`

PDFs are snapshots and do not preserve clickable lookup links. Build them locally with `python scripts/export_pdf.py`; see `docs/promo/pdf-build.md`.

### Notes

- CEFR levels are teaching-oriented reference points, not an official DELE syllabus.
- This project is not affiliated with Instituto Cervantes.
- Licensed under MIT.

**Full README:** https://github.com/auding1900/es-raiz-vocab/blob/main/README.md
```

## Assets to attach

| Asset | Expected source |
| --- | --- |
| `A1.pdf` | `dist/pdf/A1.pdf` |
| `A2.pdf` | `dist/pdf/A2.pdf` |
| `B1.pdf` | `dist/pdf/B1.pdf` |
| `B2.pdf` | `dist/pdf/B2.pdf` |
| `C1.pdf` | `dist/pdf/C1.pdf` |
| `C2.pdf` | `dist/pdf/C2.pdf` |
| `index-toc.pdf` | `dist/pdf/index-toc.pdf` |

Generate checksums after the build:

```bash
cd dist/pdf
shasum -a 256 A1.pdf A2.pdf B1.pdf B2.pdf C1.pdf C2.pdf index-toc.pdf > SHA256SUMS.txt
```

Attach `SHA256SUMS.txt` too. Verify each PDF opens and has the expected page count before uploading.

## Manual publish steps (kept for the next release)

1. Build the PDFs and confirm all seven files exist.
2. Open each PDF once; check the cover, table of contents, and at least one graph page.
3. Generate `SHA256SUMS.txt`.
4. Create a **draft** release in the GitHub web UI or via the API.
5. Upload the seven PDFs plus `SHA256SUMS.txt`.
6. Verify asset sizes and names against `dist/pdf/`.
7. Publish.
8. Update both README files with the release link.

Command template for the next release (the `gh` CLI was unavailable on 2026-11-08; `v0.29.1` was created through the GitHub REST API with the same payload, then published after asset verification):

```bash
gh release create v0.29.1 \
  dist/pdf/A1.pdf dist/pdf/A2.pdf dist/pdf/B1.pdf \
  dist/pdf/B2.pdf dist/pdf/C1.pdf dist/pdf/C2.pdf \
  dist/pdf/index-toc.pdf dist/pdf/SHA256SUMS.txt \
  --title "v0.29.1 — A navigable Spanish root map" \
  --draft
```

Then paste the release body above in the web UI.

## Do not

- Claim downloads, stars, users, or testimonials that do not exist.
- Describe the PDFs as interactive.
- Say the release covers the full DELE syllabus.
- Publish a release whose PDFs failed to render or whose page counts are wrong.
