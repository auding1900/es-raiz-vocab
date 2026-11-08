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
| Static site | **Built locally; deployed** | `site/index.html`; `site/` is git-ignored; Pages workflow runs from `main` |
| Release | **Published — 2026-11-08** | <https://github.com/auding1900/es-raiz-vocab/releases/tag/v0.29.1>; 8 assets |
| Pages | **Live — verified 2026-11-08** | <https://auding1900.github.io/es-raiz-vocab/> returns the site |
| Social preview | **Not verified** | No CLI/API evidence; manual step below |
| Community posts | **Drafts written; not posted** | `docs/promo/reddit-coolgithubprojects.md`, `reddit-spanish-learners.md`, `xiaohongshu.md`, `forum-zh.md`, `producthunt.md`, `awesome-list-pr.md` |

## Phase 3 prerequisite check (2026-11-08)

| Prerequisite | Result | Evidence | Effect on drafts |
| --- | --- | --- | --- |
| Pages enabled and reachable | **OK** | Site loads and renders the root map | Real Pages URL is used; `{{PAGES_URL}}` is not needed |
| PDF Release published | **OK** | v0.29.1 published with 8 assets | Real Release URL is used; no `{{RELEASE_URL}}` remains |
| Real demo GIF recorded | **BLOCKED** | `assets/demo.gif` is a labeled placeholder | Product Hunt must not upload it as a demo video; gallery uses screenshots only |
| Social preview uploaded | **UNVERIFIED** | No API/CLI check available | Reddit link cards may show a default GitHub image; verify manually before posting |
| `site/` and `dist/` not committed | **OK** | Both are git-ignored | No generated artifacts in the repo |

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

### 3. Verify GitHub Pages (already live as of 2026-11-08)

Phase 2 adds `.github/workflows/pages.yml`; `site/` is generated in CI and is git-ignored. The site was reachable on 2026-11-08, so keep these steps for re-verification after workflow or data changes.

- [ ] Confirm the workflow is on `main`.
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
- [ ] Re-check the README “Online demo” link after any workflow or data change.

### 4. Verify the PDF Release (published 2026-11-08)

The PDF release is published as `v0.29.1` with 8 assets. Both READMEs link to it; see <https://github.com/auding1900/es-raiz-vocab/releases/tag/v0.29.1>.

- [x] Check `dist/pdf/A1.pdf` … `C2.pdf` and `index-toc.pdf` exist.
- [x] Verify page counts: A1 10 / A2 36 / B1 62 / B2 76 / C1 51 / C2 12 / index 6.
- [x] Generate and verify `SHA256SUMS.txt` (`shasum -a 256 -c` passes).
- [x] Create a draft release and upload all seven PDFs plus checksums.
- [x] Verify every uploaded asset size against `dist/pdf/` (8/8 matched).
- [x] Publish the release.
- [x] Update both READMEs with the real release link.

Release record: id `438154786`, tag `v0.29.1` at commit `886a5ec`.

### 5. Confirm the bilingual README links

- [ ] `README.md` top line links to `README.zh-CN.md`.
- [ ] `README.zh-CN.md` top line links to `README.md`.
- [ ] Both pages show the same stats and level counts.
- [ ] Both pages use the same online-demo URL.
- [ ] Both pages say the prompt works with any LLM, not only Doubao.
- [ ] Both pages say generated files must not be hand-edited.
- [ ] Both pages link to the same release (`v0.29.1`) and the same live Pages URL.

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

## 9. Phase 3 cross-channel timeline

### T−14 days

- [ ] Confirm Pages is reachable and the map, levels, search, and copy-prompt button work on desktop and mobile.
- [ ] Confirm the published Release URL is reachable and the 8 assets are downloadable.
- [ ] Upload the Social preview and check the card on new Reddit, old Reddit, and mobile.
- [ ] Replace `assets/demo.gif` with a real recording; re-check the file size and playback on GitHub.
- [ ] Re-read every target community's current rules; rules change faster than drafts.
- [ ] Start or continue 2–4 weeks of genuine participation in the target subreddits and on Product Hunt.

### T−7 days

- [ ] Submit the first awesome-list PR (start with `jqhoogland/awesome-language-learning`).
- [ ] Submit at most one more awesome-list PR; do not batch.
- [ ] Continue non-promotional participation in r/Spanish and r/learnspanish.
- [ ] Verify account age/karma against each community's (often unpublished) thresholds.
- [ ] Prepare the Reddit link post and read it once as a stranger: does it stand without the link?

### T−1 day

- [ ] Finish the Product Hunt draft: tagline, short description, gallery, Maker comment, topics.
- [ ] Confirm the gallery is 1270 × 760 and contains no placeholder GIF frames.
- [ ] Human read-through of every Reddit and Xiaohongshu draft; remove marketing tone and absolutes.
- [ ] Confirm no draft contains a visible `releases/...` link unless the channel actually needs the PDF bundle.
- [ ] Decide the exact publish order and times; write them down.

### T day

- [ ] Publish one channel at a time, in this order: awesome-list PR → Chinese developer post → Xiaohongshu → Reddit (megathread first) → Product Hunt.
- [ ] Do not post the same link in two subreddits on the same day.
- [ ] Record the published URL, timestamp, and channel for each post.
- [ ] Stay online for the first 2 hours after each post; reply to every substantive comment.

### T+1 to T+7

- [ ] Reply to comments daily; do not argue with criticism.
- [ ] Check GitHub Traffic → Referrers; record which channels actually send visitors.
- [ ] Do not repost the same link in the same community.
- [ ] If a post was removed, read the reason before considering any follow-up; wait at least 7 days.
- [ ] Record real numbers only (visitors, referrers, comments); never convert them into marketing claims.

## 10. Never do

- [ ] Never buy upvotes, stars, comments, or reviews.
- [ ] Never fabricate testimonials, user counts, learning outcomes, or “used by N people”.
- [ ] Never use multiple accounts to post or upvote the same link.
- [ ] Never post self-promotion in a subreddit that forbids it, or outside its designated megathread.
- [ ] Never beg for upvotes on Product Hunt launch day, by DM, email, Discord, or group chat.
- [ ] Never promise “passes DELE”, “most effective”, or any absolute learning result.
- [ ] Never publish a Release link before the Release exists.
- [ ] Never present the placeholder `assets/demo.gif` as a real demo.
- [ ] Never mass-submit the same PR to multiple awesome lists.
- [ ] Never buy a V2EX invite code or account just to post.

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
| Phase 3 channel drafts reviewed | | | |
| Social preview verified on three Reddit surfaces | | | |
| Real demo GIF recorded | | | |
| First awesome-list PR submitted | | | |
