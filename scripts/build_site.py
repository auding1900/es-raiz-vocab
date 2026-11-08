#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the static GitHub Pages site for es-raiz-vocab.

Output: site/index.html (single file, no frontend build tools).

Design notes:
* `mindmaps/root_tree.md` is an index, not a Mermaid file. This script reads the
  index tables for navigation metadata, then reads the linked family pages
  (`mindmaps/raiz_*.md`) for the actual Mermaid source.
* Mermaid is pinned to MERMAID_VERSION and loaded from jsDelivr.
* `site/` is generated in CI and is git-ignored. Do not edit it by hand.

Usage:
    python scripts/build_site.py
    python scripts/build_site.py --repo . --out site
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import parse_qs, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import generate_mermaid as gen  # noqa: E402

LEVELS: Tuple[str, ...] = ("A1", "A2", "B1", "B2", "C1", "C2")
REPO_URL = "https://github.com/auding1900/es-raiz-vocab"
PAGES_URL = "https://auding1900.github.io/es-raiz-vocab/"
MERMAID_VERSION = "11.4.1"
MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@{0}/dist/mermaid.min.js".format(MERMAID_VERSION)

MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)\n```", re.S)
ROOT_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|")
LINK = re.compile(r"\]\(([^)]+)\)")
LEVEL_ROW = re.compile(
    r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*\[豆包\]\((https?://[^)]+)\)\s*\|$"
)
NO_ROOT_ROW = re.compile(r"^-\s+(.+?)\s+\(([^)]+)\)\s*$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_mermaid(text: str) -> Optional[str]:
    match = MERMAID_BLOCK.search(text)
    if not match:
        return None
    return match.group(1).strip()


def cell_int(value: str) -> int:
    match = re.search(r"\d+", value)
    return int(match.group(0)) if match else 0


def clean_cell(value: str) -> str:
    return value.strip().strip("`* ").strip()


def section_label(raw: str) -> str:
    if "历史" in raw:
        return "Historical (v0)"
    match = re.search(r"`([^`]+)`", raw)
    if match:
        return "Batch {0}".format(match.group(1))
    return raw.strip() or "Other"


def parse_declared_word_count(repo: Path) -> int:
    """Read the deduplicated word total from root_tree.md's summary line."""
    text = read_text(repo / "mindmaps" / "root_tree.md")
    match = re.search(r"单词\s*([0-9,]+)\s*个", text)
    return int(match.group(1).replace(",", "")) if match else 0


def parse_root_index(repo: Path) -> List[Dict[str, Any]]:
    index_path = repo / "mindmaps" / "root_tree.md"
    text = read_text(index_path)
    section = "Other"
    roots: List[Dict[str, Any]] = []
    seen: set = set()

    for line in text.splitlines():
        if line.startswith("## "):
            section = section_label(line[3:].strip())
            continue
        if not ROOT_ROW.match(line):
            continue

        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        root_id = clean_cell(cells[0])
        if not root_id or root_id in seen:
            continue

        link_match = LINK.search(cells[5])
        if not link_match:
            continue
        filename = link_match.group(1).strip()
        page_path = repo / "mindmaps" / filename
        if not page_path.exists():
            continue
        source = extract_mermaid(read_text(page_path))
        if not source:
            continue

        seen.add(root_id)
        roots.append(
            {
                "id": root_id,
                "rootName": clean_cell(cells[1]),
                "latin": clean_cell(cells[2]),
                "words": cell_int(cells[3]),
                "relations": cell_int(cells[4]),
                "section": section,
                "file": filename,
                "source": source,
            }
        )

    if not roots:
        raise SystemExit("No root diagrams found. Run scripts/generate_mermaid.py first.")
    return roots


def extract_prompt(href: str) -> Optional[str]:
    query = parse_qs(urlparse(href).query).get("q", [""])[0]
    return query or None


def parse_levels(repo: Path) -> List[Dict[str, str]]:
    entries: List[Dict[str, str]] = []
    seen: set = set()
    for level in LEVELS:
        path = repo / "levels" / "{0}.md".format(level)
        if not path.exists():
            continue
        for line in read_text(path).splitlines():
            match = LEVEL_ROW.match(line)
            if not match:
                continue
            word = clean_cell(match.group(1))
            root = clean_cell(match.group(2))
            if root in {"—", "-", "–", "(none)", "null"}:
                root = ""
            href = match.group(3).strip()
            key = (level, word)
            if not word or key in seen:
                continue
            seen.add(key)
            prompt = extract_prompt(href) or gen.build_prompt(gen.PROMPT_TEMPLATE, word, root)
            entries.append(
                {
                    "word": word,
                    "root": root,
                    "level": level,
                    "doubao": href or gen.doubao_url(word, root),
                    "prompt": prompt,
                }
            )
    return entries


def parse_no_root(repo: Path) -> List[Dict[str, str]]:
    path = repo / "no-raiz-vocab.md"
    if not path.exists():
        return []
    entries: List[Dict[str, str]] = []
    level = ""
    for line in read_text(path).splitlines():
        if line.startswith("### "):
            candidate = line[4:].strip()
            level = candidate if candidate in LEVELS else ""
            continue
        if not level:
            continue
        match = NO_ROOT_ROW.match(line.strip())
        if not match:
            continue
        word = clean_cell(match.group(1))
        pos = clean_cell(match.group(2))
        if not word:
            continue
        entries.append(
            {
                "word": word,
                "pos": pos,
                "level": level,
                "doubao": gen.doubao_url(word, ""),
                "prompt": gen.build_prompt(gen.PROMPT_TEMPLATE, word, ""),
            }
        )
    return entries


def safe_json(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return (
        text.replace("</", "<\\/")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


HTML_TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A navigable Spanish root map: 232 roots, 1,423 words, CEFR A1–C2. Structure only; meanings generated on demand.">
<title>es-raiz-vocab · Spanish root map</title>
<script src="__MERMAID_CDN__"></script>
<style>
:root {
  --bg: #f7f8fa;
  --panel: #ffffff;
  --ink: #1a1a1a;
  --muted: #5f6368;
  --line: #e3e6eb;
  --blue: #1565c0;
  --blue-soft: #e8f1fb;
  --green: #2e7d32;
  --yellow: #f9a825;
  --orange: #ef6c00;
  --red: #b71c1c;
  --shadow: 0 8px 24px rgba(17, 24, 39, .06);
  --radius: 14px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
}
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
button, input { font: inherit; }
button { cursor: pointer; }
[hidden] { display: none !important; }
.skip { position: absolute; left: -9999px; top: 0; background: #fff; padding: 8px 12px; z-index: 100; }
.skip:focus { left: 12px; top: 12px; }
.topbar {
  position: sticky; top: 0; z-index: 20;
  display: flex; align-items: center; gap: 18px;
  padding: 10px 22px;
  background: rgba(255,255,255,.94);
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(8px);
}
.brand { font-weight: 800; letter-spacing: -.02em; color: var(--ink); white-space: nowrap; }
.brand span { color: var(--blue); }
.nav { display: flex; gap: 4px; flex-wrap: wrap; }
.nav a {
  padding: 7px 10px; border-radius: 999px; color: var(--muted); font-size: 14px;
}
.nav a:hover { background: var(--blue-soft); color: var(--blue); text-decoration: none; }
.nav a.active { background: var(--blue-soft); color: var(--blue); font-weight: 700; }
.gh { margin-left: auto; font-size: 14px; white-space: nowrap; }
main { max-width: 1240px; margin: 0 auto; padding: 26px 22px 54px; }
.hero { padding: 24px 0 18px; }
.eyebrow { margin: 0 0 8px; color: var(--blue); font-weight: 700; font-size: 13px; letter-spacing: .06em; text-transform: uppercase; }
h1 { margin: 0 0 10px; font-size: clamp(34px, 6vw, 62px); line-height: 1.02; letter-spacing: -.035em; }
.lede { max-width: 820px; margin: 0 0 18px; color: var(--muted); font-size: 18px; }
.stats { display: flex; flex-wrap: wrap; gap: 8px 18px; color: var(--muted); font-size: 14px; }
.stats strong { color: var(--ink); }
.hero-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  min-height: 36px; padding: 7px 12px;
  border: 1px solid var(--line); border-radius: 9px;
  background: #fff; color: var(--ink); font-size: 14px; font-weight: 600;
  text-decoration: none; white-space: nowrap;
}
.btn:hover { border-color: #c7d2e0; background: #fbfcfe; text-decoration: none; }
.btn-primary { background: var(--blue); border-color: var(--blue); color: #fff; }
.btn-primary:hover { background: #0d47a1; border-color: #0d47a1; }
.btn-doubao { color: #8a4b00; background: #fff8e1; border-color: #f3d38a; }
.btn-copy { color: var(--blue); background: var(--blue-soft); border-color: #cfe0f7; }
.section-head { margin: 6px 0 16px; }
h2 { margin: 0 0 6px; font-size: 27px; letter-spacing: -.02em; }
h3 { margin: 0 0 6px; font-size: 18px; }
.muted { color: var(--muted); }
.small { font-size: 13px; }
.note {
  margin: 12px 0; padding: 11px 13px;
  background: #fff; border: 1px solid var(--line); border-left: 4px solid var(--blue);
  border-radius: 10px; color: var(--muted); font-size: 14px;
}
.map-layout { display: grid; grid-template-columns: 330px minmax(0, 1fr); gap: 18px; align-items: start; }
.root-panel, .diagram-panel, .card, .table-card {
  background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow);
}
.root-panel { padding: 14px; position: sticky; top: 74px; }
.field { display: block; margin-bottom: 8px; font-size: 12px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }
input[type="search"] {
  width: 100%; padding: 9px 11px;
  border: 1px solid var(--line); border-radius: 9px; background: #fff; color: var(--ink);
}
input[type="search"]:focus { outline: 2px solid #c7d9ee; border-color: var(--blue); }
.root-list { max-height: 68vh; overflow: auto; margin-top: 10px; padding-right: 4px; }
.root-section { margin: 12px 0 5px; color: var(--muted); font-size: 11px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }
.root-item {
  display: flex; align-items: baseline; gap: 8px; width: 100%;
  padding: 6px 8px; border: 0; border-radius: 8px; background: transparent;
  color: var(--ink); text-align: left; font-size: 14px;
}
.root-item:hover { background: #f4f6f9; }
.root-item.active { background: var(--blue-soft); color: var(--blue); font-weight: 700; }
.root-item code { font-size: 13px; }
.root-item .count { margin-left: auto; color: var(--muted); font-size: 11px; }
.diagram-panel { padding: 16px; min-height: 520px; }
.diagram-head { display: flex; align-items: flex-start; gap: 12px; flex-wrap: wrap; margin-bottom: 8px; }
.diagram-head h3 { margin: 0; }
.diagram-meta { margin: 2px 0 0; color: var(--muted); font-size: 13px; }
.diagram-area { min-height: 420px; overflow: auto; padding: 8px 2px; }
.diagram-area svg { max-width: 100%; height: auto; }
pre.mermaid { margin: 0; white-space: pre-wrap; overflow: auto; color: var(--muted); font-size: 12px; }
.diagram-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.diagram-error { padding: 14px; border: 1px dashed #d9a3a3; border-radius: 10px; background: #fff5f5; color: #7a1f1f; }
.toolbar { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin: 12px 0; }
.tabs { display: flex; flex-wrap: wrap; gap: 6px; }
.tab {
  padding: 7px 11px; border: 1px solid var(--line); border-radius: 999px;
  background: #fff; color: var(--muted); font-size: 13px; font-weight: 700;
}
.tab:hover { border-color: #c7d2e0; }
.tab.active { background: var(--blue); border-color: var(--blue); color: #fff; }
.toolbar input[type="search"] { width: min(320px, 100%); }
.table-card { overflow: hidden; }
.table-wrap { overflow: auto; max-height: 72vh; }
table { width: 100%; border-collapse: collapse; min-width: 620px; }
th, td { padding: 9px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: middle; }
th { position: sticky; top: 0; z-index: 1; background: #fbfcfe; color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }
tbody tr:hover { background: #fafbfd; }
td.word { font-weight: 700; }
td.root code { color: var(--muted); }
td.actions { white-space: nowrap; }
td.actions .btn { margin-right: 6px; }
.pill { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 800; }
.lvl-A1 { background: #e8f5e9; color: #2e7d32; }
.lvl-A2 { background: #c8e6c9; color: #2e7d32; }
.lvl-B1 { background: #fff8e1; color: #8a6100; }
.lvl-B2 { background: #ffe0b2; color: #a34c00; }
.lvl-C1 { background: #ffccbc; color: #b03a12; }
.lvl-C2 { background: #ffcdd2; color: #b71c1c; }
.empty { padding: 28px 12px; color: var(--muted); text-align: center; }
.cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin: 14px 0 20px; }
.card { padding: 16px; }
.card h3 { margin-bottom: 4px; }
.card p { margin: 0; color: var(--muted); font-size: 14px; }
.card .zh { display: block; margin-top: 4px; color: var(--muted); font-size: 13px; }
.about-grid { display: grid; grid-template-columns: 1.1fr .9fr; gap: 18px; }
.about-grid .card { box-shadow: none; }
.about-grid ul { margin: 8px 0 0; padding-left: 20px; color: var(--muted); }
.about-grid li { margin: 6px 0; }
footer { max-width: 1240px; margin: 0 auto; padding: 0 22px 34px; color: var(--muted); font-size: 13px; }
footer p { margin: 4px 0; }
.toast {
  position: fixed; left: 50%; bottom: 24px; transform: translateX(-50%) translateY(12px);
  padding: 10px 14px; border-radius: 10px; background: #20242b; color: #fff;
  font-size: 14px; opacity: 0; pointer-events: none; transition: .18s ease;
  max-width: min(92vw, 680px); text-align: center; z-index: 50;
}
.toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
@media (max-width: 920px) {
  .map-layout { grid-template-columns: 1fr; }
  .root-panel { position: static; }
  .root-list { max-height: 260px; }
  .cards, .about-grid { grid-template-columns: 1fr; }
  .gh { display: none; }
}
@media (max-width: 640px) {
  main { padding: 18px 14px 44px; }
  .topbar { padding: 9px 14px; gap: 10px; }
  .brand { font-size: 15px; }
  .nav a { padding: 6px 8px; font-size: 13px; }
  .lede { font-size: 16px; }
  th, td { padding: 8px 9px; }
}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="#map">es-raiz<span>-vocab</span></a>
  <nav class="nav" aria-label="Views">
    <a href="#map" data-nav="map">Map · 导图</a>
    <a href="#levels" data-nav="levels">Levels · 分级</a>
    <a href="#no-root" data-nav="no-root">No-root · 补充</a>
    <a href="#about" data-nav="about">About · 说明</a>
  </nav>
  <a class="gh" href="__REPO_URL__" target="_blank" rel="noopener">GitHub ↗</a>
</header>

<main id="main">
  <div class="hero">
    <p class="eyebrow">Spanish root map · 西语词根地图</p>
    <h1>Not another vocabulary app.</h1>
    <p class="lede">
      A navigable map of __ROOT_COUNT__ Latin/Greek roots and __WORD_COUNT__ words.
      The repository stores <strong>structure only</strong>; meanings and examples are generated on demand.
    </p>
    <div class="stats">
      <span><strong>__ROOT_COUNT__</strong> roots</span>
      <span><strong>__WORD_COUNT__</strong> words</span>
      <span><strong>__RELATION_COUNT__</strong> typed relations</span>
      <span><strong>__LEVEL_COUNT__</strong> CEFR-tagged words</span>
      <span><strong>__NOROOT_COUNT__</strong> no-root words</span>
    </div>
    <div class="hero-actions">
      <a class="btn btn-primary" href="#map">Browse the map · 浏览导图</a>
      <a class="btn" href="#levels">A1–C2 lists · 分级清单</a>
      <a class="btn" href="__REPO_URL__" target="_blank" rel="noopener">Source on GitHub ↗</a>
    </div>
  </div>

  <section id="view-map" class="view" aria-labelledby="map-title">
    <div class="section-head">
      <h2 id="map-title">Root map · 词根导图</h2>
      <p class="muted">One page per family. Pick a root on the left; the diagram is rendered from its real generated Mermaid source.</p>
    </div>
    <div class="map-layout">
      <aside class="root-panel">
        <label class="field" for="root-search">Find a root · 搜索词根</label>
        <input id="root-search" type="search" placeholder="vid, pac, mover…" autocomplete="off">
        <div id="root-count" class="small muted"></div>
        <div id="root-list" class="root-list"></div>
      </aside>
      <article class="diagram-panel">
        <div class="diagram-head">
          <div>
            <h3 id="diagram-title">Root family</h3>
            <p id="diagram-meta" class="diagram-meta"></p>
          </div>
        </div>
        <div id="diagram-area" class="diagram-area">
          <pre class="mermaid" id="initial-diagram">__DEFAULT_SOURCE__</pre>
        </div>
        <div class="diagram-actions">
          <a id="family-link" class="btn" href="__REPO_URL__" target="_blank" rel="noopener">Open family Markdown ↗</a>
          <span class="small muted">Word nodes link to Doubao when the renderer allows it.</span>
        </div>
        <p class="note">GitHub ignores Mermaid <code>click</code> directives; this site renders with Mermaid <code>securityLevel: loose</code> so word nodes can open the default Doubao lookup. The word tables below always provide <strong>豆包</strong> and <strong>复制查询指令</strong>.</p>
      </article>
    </div>
  </section>

  <section id="view-levels" class="view" hidden aria-labelledby="levels-title">
    <div class="section-head">
      <h2 id="levels-title">Levels · A1–C2</h2>
      <p class="muted">Search by word or root. Switch levels; “All” searches every tagged word.</p>
    </div>
    <p class="note">豆包 is the default lookup. The <strong>复制查询指令</strong> button copies the prepared prompt, which can be pasted into <strong>any LLM</strong> (ChatGPT / Claude / Gemini 等). 不需要豆包也可以使用。</p>
    <div class="toolbar">
      <div id="level-tabs" class="tabs" role="tablist" aria-label="CEFR levels"></div>
      <label class="skip" for="level-search">Search words</label>
      <input id="level-search" type="search" placeholder="Search word or root…" autocomplete="off">
      <span id="level-count" class="small muted"></span>
    </div>
    <div class="table-card">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Word</th><th>Root</th><th>Level</th><th>Lookup</th></tr></thead>
          <tbody id="level-rows"></tbody>
        </table>
      </div>
    </div>
  </section>

  <section id="view-no-root" class="view" hidden aria-labelledby="noroot-title">
    <div class="section-head">
      <h2 id="noroot-title">No-root words · 补充词表</h2>
      <p class="muted">High-frequency words that cannot be decomposed by Latin roots: native words, loans, function words, and irregular verbs.</p>
    </div>
    <p class="note">These entries have no root. The copied prompt omits the root clause and still works with any LLM. 复制后粘贴到 ChatGPT / Claude / Gemini 等任意 LLM 即可。</p>
    <div class="toolbar">
      <div id="noroot-tabs" class="tabs" role="tablist" aria-label="CEFR levels for no-root words"></div>
      <label class="skip" for="noroot-search">Search no-root words</label>
      <input id="noroot-search" type="search" placeholder="Search word or POS…" autocomplete="off">
      <span id="noroot-count" class="small muted"></span>
    </div>
    <div class="table-card">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Word</th><th>POS</th><th>Level</th><th>Lookup</th></tr></thead>
          <tbody id="noroot-rows"></tbody>
        </table>
      </div>
    </div>
  </section>

  <section id="view-about" class="view" hidden aria-labelledby="about-title">
    <div class="section-head">
      <h2 id="about-title">What this is · 这是什么</h2>
      <p class="muted">A vocabulary project built around word families, not word lists.</p>
    </div>
    <div class="cards">
      <div class="card">
        <h3>No definitions</h3>
        <span class="zh">不存释义</span>
        <p>No definition, translation, gloss, or Chinese explanation fields. The validator rejects them.</p>
      </div>
      <div class="card">
        <h3>No example sentences</h3>
        <span class="zh">不存例句</span>
        <p>Not one Spanish example sentence is stored in the repository.</p>
      </div>
      <div class="card">
        <h3>Structure only</h3>
        <span class="zh">只存结构</span>
        <p>Root, word form, relation type, CEFR level, and Latin origin. Nothing else.</p>
      </div>
    </div>
    <div class="about-grid">
      <div class="card">
        <h3>Repository · 仓库</h3>
        <ul>
          <li><a href="__REPO_URL__" target="_blank" rel="noopener">GitHub repository</a></li>
          <li><a href="__README_URL__" target="_blank" rel="noopener">README (English)</a> · <a href="__README_ZH_URL__" target="_blank" rel="noopener">中文</a></li>
          <li><a href="__ROOT_TREE_URL__" target="_blank" rel="noopener">Root index (root_tree.md)</a></li>
          <li><a href="__LEVELS_URL__" target="_blank" rel="noopener">levels/ A1–C2</a></li>
          <li><a href="__NOROOT_URL__" target="_blank" rel="noopener">no-raiz-vocab.md</a></li>
          <li><a href="__LICENSE_URL__" target="_blank" rel="noopener">MIT License</a></li>
        </ul>
      </div>
      <div class="card">
        <h3>Online and offline · 在线与离线</h3>
        <ul>
          <li>This site loads Mermaid __MERMAID_VERSION__ from a pinned jsDelivr CDN; the first render needs network access.</li>
          <li>The repository and VSCode preview work offline; meanings, examples, and lookups need network access.</li>
          <li>No analytics, cookies, accounts, or server-side storage.</li>
          <li>CEFR tags are teaching-oriented reference points, not an official DELE syllabus. Not affiliated with Instituto Cervantes.</li>
        </ul>
      </div>
    </div>
    <p class="note">Site notes, build details, and the relative-path/CDN policy: <a href="__SITE_NOTES_URL__" target="_blank" rel="noopener">docs/promo/site-notes.md</a>. Data source: the generated <code>mindmaps/</code> and <code>levels/</code> files. Do not edit <code>site/</code> by hand.</p>
  </section>
</main>

<footer>
  <p><strong>es-raiz-vocab</strong> · structure only · no definitions or example sentences.</p>
  <p><a href="__PAGES_URL__">Online site</a> · <a href="__REPO_URL__" target="_blank" rel="noopener">GitHub</a> · <a href="__LICENSE_URL__" target="_blank" rel="noopener">MIT</a></p>
</footer>

<div id="toast" class="toast" role="status" aria-live="polite"></div>

<script type="application/json" id="diagram-data">__DIAGRAMS_JSON__</script>
<script type="application/json" id="level-data">__LEVELS_JSON__</script>
<script type="application/json" id="noroot-data">__NOROOT_JSON__</script>
<script>
(function () {
  "use strict";

  const DIAGRAMS = JSON.parse(document.getElementById("diagram-data").textContent);
  const LEVELS = JSON.parse(document.getElementById("level-data").textContent);
  const NOROOT = JSON.parse(document.getElementById("noroot-data").textContent);
  const REPO_URL = "__REPO_URL__";
  const DEFAULT_ID = "__DEFAULT_ID__";
  const LEVEL_ORDER = ["A1", "A2", "B1", "B2", "C1", "C2"];

  const state = {
    view: "map",
    rootId: DEFAULT_ID,
    rootQuery: "",
    level: "A1",
    levelQuery: "",
    norootLevel: "A1",
    norootQuery: ""
  };
  let initialRendered = false;
  let renderSeq = 0;

  const $ = (id) => document.getElementById(id);
  const norm = (value) => (value || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[ch]));

  function toast(message) {
    const node = $("toast");
    node.textContent = message;
    node.classList.add("show");
    window.clearTimeout(toast._timer);
    toast._timer = window.setTimeout(() => node.classList.remove("show"), 2600);
  }

  function viewFromHash() {
    const hash = (location.hash || "").replace(/^#/, "");
    return ["map", "levels", "no-root", "about"].includes(hash) ? hash : "map";
  }

  function showView(view) {
    state.view = view;
    ["map", "levels", "no-root", "about"].forEach((name) => {
      const section = $("view-" + name);
      if (section) section.hidden = name !== view;
    });
    document.querySelectorAll("[data-nav]").forEach((link) => {
      link.classList.toggle("active", link.getAttribute("data-nav") === view);
    });
    if (view === "map") ensureInitialDiagram();
  }

  function initializeMermaid() {
    if (!window.mermaid) return false;
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      theme: "base",
      themeVariables: {
        fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
      }
    });
    return true;
  }

  function bindLinks(container) {
    container.querySelectorAll("a").forEach((anchor) => {
      // Mermaid creates SVG <a> elements; their .target property is read-only.
      if (anchor.namespaceURI === "http://www.w3.org/1999/xhtml") {
        anchor.target = "_blank";
        anchor.rel = "noopener";
      }
    });
  }

  function showDiagramError(error) {
    $("diagram-area").innerHTML = '<div class="diagram-error">Mermaid could not render this diagram. ' +
      'The source file is still available on GitHub. <br><span class="small">' +
      escapeHtml(String(error && error.message ? error.message : error)) + "</span></div>";
  }

  async function ensureInitialDiagram() {
    if (initialRendered) return;
    initialRendered = true;
    const node = $("initial-diagram");
    if (!node) return;
    if (!initializeMermaid()) {
      $("diagram-area").innerHTML = '<div class="diagram-error">Mermaid CDN did not load. ' +
        'The graph source is still in the page source, and the same data is available in the GitHub repository.</div>';
      return;
    }
    try {
      await window.mermaid.run({ nodes: [node] });
      bindLinks($("diagram-area"));
    } catch (error) {
      showDiagramError(error);
    }
    const first = DIAGRAMS.find((item) => item.id === DEFAULT_ID) || DIAGRAMS[0];
    updateDiagramMeta(first);
  }

  function updateDiagramMeta(diagram) {
    if (!diagram) return;
    $("diagram-title").textContent = diagram.rootName + " · " + diagram.latin;
    $("diagram-meta").textContent = diagram.words + " words · " + diagram.relations +
      " relations · " + diagram.section;
    $("family-link").href = REPO_URL + "/blob/main/mindmaps/" + diagram.file;
  }

  async function renderDiagram(diagram) {
    if (!diagram) return;
    state.rootId = diagram.id;
    initialRendered = true;
    updateDiagramMeta(diagram);
    document.querySelectorAll(".root-item").forEach((button) => {
      button.classList.toggle("active", button.getAttribute("data-root") === diagram.id);
    });
    const area = $("diagram-area");
    if (!window.mermaid) {
      area.innerHTML = '<div class="diagram-error">Mermaid CDN did not load. ' +
        'The graph source is available in the GitHub repository.</div>';
      return;
    }
    initializeMermaid();
    const renderId = "mermaid-" + (++renderSeq);
    try {
      const result = await window.mermaid.render(renderId, diagram.source);
      area.innerHTML = result.svg;
      if (result.bindFunctions) result.bindFunctions(area);
      bindLinks(area);
    } catch (error) {
      showDiagramError(error);
    }
  }

  function buildRootList() {
    const query = norm(state.rootQuery);
    const list = $("root-list");
    const groups = new Map();
    DIAGRAMS.forEach((diagram) => {
      const haystack = norm(diagram.id + " " + diagram.rootName + " " + diagram.latin);
      if (query && !haystack.includes(query)) return;
      if (!groups.has(diagram.section)) groups.set(diagram.section, []);
      groups.get(diagram.section).push(diagram);
    });
    let count = 0;
    list.innerHTML = "";
    const fragment = document.createDocumentFragment();
    groups.forEach((items, section) => {
      const heading = document.createElement("div");
      heading.className = "root-section";
      heading.textContent = section;
      fragment.appendChild(heading);
      items.forEach((diagram) => {
        count += 1;
        const button = document.createElement("button");
        button.type = "button";
        button.className = "root-item" + (diagram.id === state.rootId ? " active" : "");
        button.setAttribute("data-root", diagram.id);
        button.title = diagram.rootName + " — " + diagram.latin;
        button.innerHTML = "<code>" + escapeHtml(diagram.id) + "</code><span>" +
          escapeHtml(diagram.rootName) + "</span><span class=\"count\">" + diagram.words + "</span>";
        fragment.appendChild(button);
      });
    });
    list.appendChild(fragment);
    $("root-count").textContent = count + " / " + DIAGRAMS.length + " roots";
    if (!count) {
      list.innerHTML = '<p class="empty">No root matches this search.</p>';
      return;
    }
    const active = list.querySelector(".root-item.active");
    if (active) {
      const listRect = list.getBoundingClientRect();
      const activeRect = active.getBoundingClientRect();
      if (activeRect.top < listRect.top || activeRect.bottom > listRect.bottom) {
        list.scrollTop += activeRect.top - listRect.top - 8;
      }
    }
  }

  function buildTabs(container, prefix, current) {
    const all = ["ALL"].concat(LEVEL_ORDER);
    container.innerHTML = all.map((level) => {
      const label = level === "ALL" ? "All" : level;
      const active = level === current ? " active" : "";
      return '<button type="button" class="tab' + active + '" role="tab" aria-selected="' +
        (level === current) + '" data-' + prefix + '="' + level + '">' + label + "</button>";
    }).join("");
  }

  function rowHtml(entry, includePos) {
    const posCell = includePos ? "<td>" + escapeHtml(entry.pos) + "</td>" : "";
    const rootCell = entry.root
      ? "<code>" + escapeHtml(entry.root) + "</code>"
      : '<span class="muted">—</span>';
    return "<tr>" +
      '<td class="word">' + escapeHtml(entry.word) + "</td>" +
      posCell +
      '<td class="root">' + rootCell + "</td>" +
      '<td><span class="pill lvl-' + escapeHtml(entry.level) + '">' + escapeHtml(entry.level) + "</span></td>" +
      '<td class="actions">' +
        '<a class="btn btn-doubao" href="' + escapeHtml(entry.doubao) + '" target="_blank" rel="noopener">豆包</a>' +
        '<button class="btn btn-copy" type="button" data-copy="' + escapeHtml(entry.prompt) + '">复制查询指令</button>' +
      "</td>" +
    "</tr>";
  }

  function renderLevels() {
    const query = norm(state.levelQuery);
    const rows = LEVELS.filter((entry) => {
      if (state.level !== "ALL" && entry.level !== state.level) return false;
      if (!query) return true;
      return norm(entry.word + " " + entry.root).includes(query);
    });
    $("level-rows").innerHTML = rows.length
      ? rows.map((entry) => rowHtml(entry, false)).join("")
      : '<tr><td colspan="4" class="empty">No word matches this level and search.</td></tr>';
    $("level-count").textContent = rows.length + " words";
  }

  function renderNoRoot() {
    const query = norm(state.norootQuery);
    const rows = NOROOT.filter((entry) => {
      if (state.norootLevel !== "ALL" && entry.level !== state.norootLevel) return false;
      if (!query) return true;
      return norm(entry.word + " " + entry.pos).includes(query);
    });
    $("noroot-rows").innerHTML = rows.length
      ? rows.map((entry) => rowHtml(entry, true)).join("")
      : '<tr><td colspan="4" class="empty">No word matches this level and search.</td></tr>';
    $("noroot-count").textContent = rows.length + " words";
  }

  async function copyText(text, button) {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const area = document.createElement("textarea");
        area.value = text;
        area.setAttribute("readonly", "");
        area.style.position = "fixed";
        area.style.left = "-9999px";
        document.body.appendChild(area);
        area.select();
        document.execCommand("copy");
        document.body.removeChild(area);
      }
      if (button) {
        const original = button.textContent;
        button.textContent = "已复制";
        window.setTimeout(() => { button.textContent = original; }, 1300);
      }
      toast("已复制查询指令。可粘贴到任意 LLM（ChatGPT / Claude / Gemini 等）。");
    } catch (error) {
      toast("复制失败，请手动选择并复制。");
    }
  }

  function wireEvents() {
    document.querySelectorAll("[data-nav]").forEach((link) => {
      link.addEventListener("click", () => showView(link.getAttribute("data-nav")));
    });
    window.addEventListener("hashchange", () => showView(viewFromHash()));

    $("root-search").addEventListener("input", (event) => {
      state.rootQuery = event.target.value;
      buildRootList();
    });
    $("root-list").addEventListener("click", (event) => {
      const button = event.target.closest("[data-root]");
      if (!button) return;
      const diagram = DIAGRAMS.find((item) => item.id === button.getAttribute("data-root"));
      if (diagram) renderDiagram(diagram);
    });

    $("level-tabs").addEventListener("click", (event) => {
      const button = event.target.closest("[data-level]");
      if (!button) return;
      state.level = button.getAttribute("data-level");
      buildTabs($("level-tabs"), "level", state.level);
      renderLevels();
    });
    $("level-search").addEventListener("input", (event) => {
      state.levelQuery = event.target.value;
      renderLevels();
    });

    $("noroot-tabs").addEventListener("click", (event) => {
      const button = event.target.closest("[data-noroot]");
      if (!button) return;
      state.norootLevel = button.getAttribute("data-noroot");
      buildTabs($("noroot-tabs"), "noroot", state.norootLevel);
      renderNoRoot();
    });
    $("noroot-search").addEventListener("input", (event) => {
      state.norootQuery = event.target.value;
      renderNoRoot();
    });

    document.addEventListener("click", (event) => {
      const button = event.target.closest("[data-copy]");
      if (!button) return;
      copyText(button.getAttribute("data-copy"), button);
    });
  }

  function init() {
    // Disable Mermaid's auto-run before any view is shown; otherwise a direct
    // #levels or #about link would render the hidden map with zero dimensions.
    initializeMermaid();
    state.rootId = DEFAULT_ID;
    buildRootList();
    buildTabs($("level-tabs"), "level", state.level);
    buildTabs($("noroot-tabs"), "noroot", state.norootLevel);
    renderLevels();
    renderNoRoot();
    wireEvents();
    showView(viewFromHash());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>
</body>
</html>
"""


def build_html(repo: Path) -> Tuple[str, Dict[str, int]]:
    roots = parse_root_index(repo)
    levels = parse_levels(repo)
    noroot = parse_no_root(repo)

    preferred = next((root for root in roots if root["id"] == "vid"), roots[0])
    default_source = html.escape(preferred["source"], quote=False)

    root_count = len(roots)
    word_count = parse_declared_word_count(repo) or sum(root["words"] for root in roots)
    relation_count = sum(root["relations"] for root in roots)
    level_count = len(levels)
    noroot_count = len(noroot)

    replacements = {
        "__MERMAID_CDN__": MERMAID_CDN,
        "__MERMAID_VERSION__": MERMAID_VERSION,
        "__REPO_URL__": REPO_URL,
        "__PAGES_URL__": PAGES_URL,
        "__README_URL__": REPO_URL + "/blob/main/README.md",
        "__README_ZH_URL__": REPO_URL + "/blob/main/README.zh-CN.md",
        "__ROOT_TREE_URL__": REPO_URL + "/blob/main/mindmaps/root_tree.md",
        "__LEVELS_URL__": REPO_URL + "/tree/main/levels",
        "__NOROOT_URL__": REPO_URL + "/blob/main/no-raiz-vocab.md",
        "__LICENSE_URL__": REPO_URL + "/blob/main/LICENSE",
        "__SITE_NOTES_URL__": REPO_URL + "/blob/main/docs/promo/site-notes.md",
        "__ROOT_COUNT__": "{:,}".format(root_count),
        "__WORD_COUNT__": "{:,}".format(word_count),
        "__RELATION_COUNT__": "{:,}".format(relation_count),
        "__LEVEL_COUNT__": "{:,}".format(level_count),
        "__NOROOT_COUNT__": "{:,}".format(noroot_count),
        "__DEFAULT_SOURCE__": default_source,
        "__DEFAULT_ID__": preferred["id"],
        "__DIAGRAMS_JSON__": safe_json(roots),
        "__LEVELS_JSON__": safe_json(levels),
        "__NOROOT_JSON__": safe_json(noroot),
    }

    output = HTML_TEMPLATE
    for key, value in replacements.items():
        output = output.replace(key, value)

    stats = {
        "roots": root_count,
        "words": word_count,
        "relations": relation_count,
        "level_words": level_count,
        "no_root_words": noroot_count,
    }
    return output, stats


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build the static es-raiz-vocab site")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT, help="repository root")
    parser.add_argument("--out", type=Path, default=None, help="output directory (default: <repo>/site)")
    args = parser.parse_args(argv)

    repo = args.repo.resolve()
    out = (args.out or (repo / "site")).resolve()
    output, stats = build_html(repo)

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    index_path = out / "index.html"
    with index_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(output)

    print("[site] roots: {roots}".format(**stats))
    print("[site] words from root index: {words}".format(**stats))
    print("[site] relations: {relations}".format(**stats))
    print("[site] CEFR-tagged words: {level_words}".format(**stats))
    print("[site] no-root words: {no_root_words}".format(**stats))
    print("[site] written: {0}".format(index_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
