# Launch checklist (manual)

This checklist covers Phase 1 assets, the Phase 2 static site/Pages workflow, and the manual GitHub steps. Nothing here has been executed automatically.

## Phase 1–2 status

| Item | Status | Evidence |
| --- | --- | --- |
| English landing page | Done | `README.md` |
| Chinese landing page | Done | `README.md.zh-CN.md` |
| Root map image | Done | `assets/root_tree.svg`, `assets/root_tree.png` |
| Demo GIF | **Placeholder only — record manually** | `assets/demo.gif` is a labeled placeholder, not a recording |
| PDF export | **Built locally** | `dist/pdf/` has 7 PDFs + `SHA256SUMS.txt`; git-ignored, not committed |
| Static site | **Built locally; CI workflow added** | `site/index.html`; `site/` is git-ignored |
| Release | **Not published** | Draft in `docs/promo/release-draft.md` |
| Pages | **Workflow added; not enabled** | `.github/workflows/pages.yml`; enable manually in Settings |
| Social preview | **Not uploaded** | Manual step below |
| Community posts | **Not created / not posted** | Phase 3 |

## Required human actions

### 1. Record `assets/demo.gif`

- [ ] Follow [`demo-script.md`](demo-script.md) shot by shot.
- [ ] Use 1920 × 1080, 30 fps, 55–60 seconds.
- [ ] Hide notifications, personal accounts, tokens, and unrelated tabs.
- [ ] Replace the current `assets/demo.gif` (a labeled placeholder) with the real recording, target ≤ 10 MB.
- [ ] The README already embeds `assets/demo.gif`; update the alt text only if the recording differs from the shot list.
- [ ] Verify the GIF plays on GitHub, not just locally.

### 2. Upload the social preview

- [ ] Open the repository on GitHub.
- [ ] **Settings → Social preview → Edit → Upload an image**.
- [ ] Upload `assets/root_tree.png` (landscape 1200 × 630).
- [ ] Check the text and the diagram are both legible at small size.
- [ ] Save and reload the repository page.
- [ ] Do **not** claim the preview is active until the upload is confirmed.

There is no API/CLI step here; GitHub social preview is a web-UI setting.

### 3. Enable GitHub Pages

Phase 2 adds `.github/workflows/pages.yml`. `site/` is generated in CI and is git-ignored.

- [ ] Merge/push the workflow to `main`.
- [ ] **Settings → Pages → Build and deployment → Source: GitHub Actions**.
- [ ] Trigger the workflow: push to `main`, or use **Actions → pages → Run workflow**.
- [ ] Wait for both the `build` and `deploy` jobs to succeed.
- [ ] Confirm the run uploaded a Pages artifact (`github-pages`) and the deploy step reports a page URL.
- [ ] Open <https://auding1900.github.io/es-raiz-vocab/>.
- [ ] Verify: map renders Mermaid, root search filters, A1–C2 tabs work, word search filters, “豆包” opens, “复制查询指令” copies, and the no-root view loads.
- [ ] If 404, check in this order:
  1. the workflow run succeeded (not only queued);
  2. the Pages artifact was uploaded;
  3. Pages is enabled with **Source: GitHub Actions**;
  4. the repository is public and the `github-pages` environment is allowed;
  5. the deploy job URL matches the repository name;
  6. try the URL with a trailing slash.
- [ ] Only then treat the README “Online demo” link as live.

### 4. Publish the PDF Release (if not already generated)

- [ ] Check `dist/pdf/A1.pdf` … `C2.pdf` and `index-toc.pdf` exist.
- [ ] If they do not exist, follow [`pdf-build.md`](pdf-build.md).
- [ ] Open each PDF and verify the cover, TOC, and one graph page.
- [ ] Generate `SHA256SUMS.txt`.
- [ ] Follow [`release-draft.md`](release-draft.md) to create a **draft** release.
- [ ] Upload all seven PDFs plus checksums.
- [ ] Publish only after human approval.
- [ ] After publishing, update both READMEs with the real release link.

Do not leave the README pointing at a release that does not exist. The current wording deliberately says PDFs are built locally and are not linked from a release.

### 5. Confirm the bilingual README links

- [ ] `README.md` top line links to `README.zh-CN.md`.
- [ ] `README.zh-CN.md` top line links to `README.md`.
- [ ] Both pages show the same stats and level counts.
- [ ] Both pages use the same online-demo URL.
- [ ] Both pages say the prompt works with any LLM, not only Doubao.
- [ ] Both pages say generated files must not be hand-edited.
- [ ] Both pages avoid claiming a published release or a live Pages site.

### 6. Verify the repository state

- [ ] `python scripts/generate_mermaid.py --check` passes.
- [ ] `python scripts/generate_mermaid.py` produces no unexpected diff.
- [ ] `python scripts/build_site.py` passes and writes `site/index.html`.
- [ ] `python -m py_compile scripts/*.py` passes.
- [ ] `git diff --check` passes.
- [ ] `LICENSE` still says “es-raiz-vocab contributors”.
- [ ] No `.env`, tokens, personal paths, or secrets are committed.
- [ ] `dist/` and `site/` are not committed.

### 7. Release 发布后回写 README

- [ ] Do **not** change the README Release wording before the release is public.
- [ ] After publishing the PDF Release, replace the “not linked from a release” wording in both READMEs with the real release URL.
- [ ] Re-check both READMEs for the same stats, online URL, and release link.

### 8. Deferred to Phase 4

- [ ] Phase 4 will create `docs/promo/github-metadata.md` with the Description, Topics, and `gh repo edit` commands.
- [ ] `gh repo edit` commands are human-executed only.
- [ ] Community posts are Phase 3 drafts only; no auto-posting.

## Final sign-off

| Check | Owner | Date | Result |
| --- | --- | --- | --- |
| Demo GIF recorded and embedded | | | |
| Social preview uploaded | | | |
| Pages enabled and URL verified | | | |
| First Pages workflow succeeded and artifact uploaded | | | |
| PDFs built and verified | | | |
| Release published and linked | | | |
| Bilingual README links confirmed | | | |
