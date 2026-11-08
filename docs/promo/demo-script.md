# Demo script (target: 60 seconds; actual file: 10 seconds)

- Status: **recorded — 2026-11-08**
- Actual file: `assets/demo.gif` (640 × 640, 23 frames, 10.02 s, ≈2.3 fps average, 162,870 bytes)
- Target output: `assets/demo.gif`
- Audience: Spanish learners, etymology fans, and open-source maintainers who have never seen the repo
- Goal: in 60 seconds, show that this is a **navigable map**, not a word list, and that the repo stores structure while an LLM produces the content

## Recording setup

| Item | Recommended |
| --- | --- |
| Resolution | 1920 × 1080, 30 fps |
| Aspect | 16:9; crop browser chrome |
| Audio | None; use on-screen captions |
| Length | 55–60 s |
| Final file | `assets/demo.gif`, aim for ≤ 10 MB |
| Fallback tool | QuickTime + `ffmpeg` / `gifski` |
| Hide | notifications, bookmarks, personal account avatars, tokens, unrelated tabs |

If GitHub Pages is not enabled yet, record the same flow in VSCode Markdown Preview with Mermaid support. Do not fake a live site.

## Recorded file (actual)

| Field | Value |
| --- | --- |
| Dimensions | 640 × 640 |
| Frames | 23 |
| Duration | 10.02 s |
| Average frame rate | ≈2.3 fps (GIF frame delays vary) |
| Size | 162,870 bytes (≈159 KiB) |
| Recorded | 2026-11-08 |

The current file is a compressed, square, 10-second capture. It does **not** match the original 55–60 s / 1920 × 1080 / 30 fps plan below; keep the shot list as the specification for a future high-resolution re-record. Do not run `scripts/make_demo_placeholder.py` while the real GIF is present, because it would overwrite it.

## Shot list

| Time | Screen | Action | Caption |
| --- | --- | --- | --- |
| 0–5 s | GitHub README hero | Hold on the root-family image, then scroll one notch | “Not another vocabulary app.” |
| 5–12 s | `mindmaps/root_tree.md` | Scroll the root index, hover one batch table | “232 Latin/Greek roots. One page per family.” |
| 12–22 s | `mindmaps/raiz_b9_pac.md` | Open a family page; point to the root node, a green A2 node, and a red C2 node | “Color = CEFR level. Lines = derivation, association, confusion.” |
| 22–30 s | Same page, bottom | Scroll to the **word link table**; hover the `豆包` link | “GitHub ignores Mermaid clicks — use the link table.” |
| 30–40 s | `levels/A2.md` | Open a level list; search one word; hover its lookup link | “A1–C2 lists, one row per word.” |
| 40–48 s | Browser address bar / prompt box | Show the generated prompt; paste the same prompt into a second LLM tab, but do **not** show a generated answer | “Doubao is the default. The prompt works with any LLM.” |
| 48–55 s | VSCode with `mindmaps/root_tree.md` preview, network off if possible | Show the graph rendering offline | “Structure works offline.” |
| 55–60 s | End card | Repo name + `github.com/auding1900/es-raiz-vocab` + “MIT” | “Structure only. Meanings on demand.” |

## Voice-over / caption copy (optional)

> This is a Spanish root map, not a word list.
> 232 roots, 1,423 words, A1 to C2.
> Every root gets a page: derivatives, associations, confusions, and a level color.
> Pick a word, send the prepared prompt to Doubao or any LLM.
> The repo stores the map. The model writes the meaning.
> Offline, the map still works.

## Do not show or claim

- Dictionary definitions, example sentences, or copied dictionary UI.
- Star counts, user counts, testimonials, or “used by N people”.
- “Covers the full DELE syllabus.”
- A Pages URL that is still 404.
- Personal account names, tokens, or private repositories.

## After recording (done for the current file)

- [x] Export to `assets/demo.gif`.
- [x] Confirm file size (162,870 bytes; well under 10 MB).
- [x] Replace the placeholder; the README path is unchanged.
- [x] Update the alt text in both READMEs to describe the 10-second capture.
- [x] Add `assets/demo.gif` to the same commit as the README/docs update.
- [ ] Confirm the GIF plays on GitHub after the push (not just locally).
- [x] Do not run `make_demo_placeholder.py` while the real file is present.
