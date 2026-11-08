# Building the offline PDFs

- Purpose: produce `A1.pdf` … `C2.pdf` + `index-toc.pdf` for a GitHub Release
- Output: `dist/pdf/` (git-ignored)
- Prebuilt PDFs are **not committed** and are **not** linked from a published release yet

## Environment verified on 2026-11-08

| Dependency | Version / path |
| --- | --- |
| Python | 3.9.2 (`.env/bin/python`) |
| PyYAML | installed in `.env` |
| ReportLab | 4.5.1 |
| Node / npm | installed |
| mermaid-cli | installed globally at `/usr/local/bin/mmdc` (12.2.0) during Phase 1 |
| Chrome | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |

`export_pdf.py` falls back to `npx` when `mmdc` is not on `PATH`. Installing `mmdc` globally is much faster than launching `npx` for every graph.

## Build commands

From the repository root:

```bash
# Python dependencies
pip install -r requirements.txt

# Optional: install mermaid-cli globally; otherwise the script uses npx
npm install -g @mermaid-js/mermaid-cli

# Plan only: scan volumes, render nothing
python scripts/export_pdf.py --dry-run

# Smoke test the smallest volume
python scripts/export_pdf.py \
  --only C2 \
  --chrome "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --mmdc "$(which mmdc)"

# Full build (all six volumes + index)
python scripts/export_pdf.py \
  --chrome "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --mmdc "$(which mmdc)"
```

Other useful flags:

```bash
python scripts/export_pdf.py --only A1,B1
python scripts/export_pdf.py --timeout 300
python scripts/export_pdf.py --engine weasyprint   # requires weasyprint + pango
```

## Volume plan (current data)

| Volume | Root pages | Notes |
| --- | ---: | --- |
| A1 | 8 | |
| A2 | 34 | |
| B1 | 59 | |
| B2 | 73 | |
| C1 | 48 | |
| C2 | 10 | |
| **Total** | **232** | plus `index-toc.pdf` |

## Build log (2026-11-08)

| Volume | Root pages | PDF pages | Size |
| --- | ---: | ---: | ---: |
| A1 | 8 | 10 | 603 KB |
| A2 | 34 | 36 | 2.7 MB |
| B1 | 59 | 62 | 4.6 MB |
| B2 | 73 | 76 | 1.6 MB |
| C1 | 48 | 51 | 794 KB |
| C2 | 10 | 12 | 161 KB |
| `index-toc.pdf` | — | 6 | 14 KB |

- `--dry-run` and the C2 smoke test passed before the full build.
- The full build completed with 232 graph images and seven PDFs.
- `dist/pdf/SHA256SUMS.txt` was generated for the seven PDFs.
- `dist/` remains git-ignored; nothing from it is committed.
- `--reuse-images` was added to `export_pdf.py` so a batch-rendered image set can be assembled without re-rendering every graph:
  ```bash
  python scripts/export_pdf.py --reuse-images
  ```

## Output

```text
dist/
├── src/<level>/*.mmd     # Mermaid extracted from mindmaps/
├── img/<level>/*.png     # rendered graph images
└── pdf/
    ├── A1.pdf
    ├── A2.pdf
    ├── B1.pdf
    ├── B2.pdf
    ├── C1.pdf
    ├── C2.pdf
    └── index-toc.pdf
```

`dist/` is listed in `.gitignore`; do not force-add it to the repository.

## Verification before release

1. All seven PDF files exist and are non-zero.
2. Each PDF opens without a password.
3. Check the cover, the table of contents, and at least one graph page per volume.
4. Confirm the PDF is a static snapshot: there are no clickable lookup links.
5. Generate checksums:

   ```bash
   cd dist/pdf
   shasum -a 256 A1.pdf A2.pdf B1.pdf B2.pdf C1.pdf C2.pdf index-toc.pdf > SHA256SUMS.txt
   ```

6. Follow [`release-draft.md`](release-draft.md) to create a draft release.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `could not find chrome-headless-shell` | Pass `--chrome` with the system Chrome path, or run `npx puppeteer browsers install chrome-headless-shell` |
| `mmdc` not found | Install `@mermaid-js/mermaid-cli` globally, keep `npx` available, or pass `--mmdc` |
| `reportlab` missing | Use `.env/bin/python`, or `pip install -r requirements.txt` |
| A single graph fails | The exporter warns and skips it; inspect `dist/src/<level>/` and re-render that `.mmd` manually |
| Chinese glyphs missing | ReportLab uses the built-in `STSong-Light` CID font; if using WeasyPrint, install suitable CJK fonts |

## Release wording

The release is published as `v0.29.1` (<https://github.com/auding1900/es-raiz-vocab/releases/tag/v0.29.1>). Both READMEs link to it. If you rebuild PDFs for a future release, do not change the README link until that release is actually public.
