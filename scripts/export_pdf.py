#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 CEFR 等级导出静态 PDF（A1/A2/B1/B2/C1/C2 + index-toc.pdf）。

流程：
1) 扫描仓库，把词根导图按等级分册（不硬编码任何词根清单）；
2) 从 markdown 中抽出 ```mermaid 代码块，写到 dist/src/<level>/*.mmd；
3) 调 mermaid-cli（mmdc）把每个 .mmd 渲染成 dist/img/<level>/*.png；
4) 用 ReportLab（默认，无系统依赖）或 WeasyPrint 组装 PDF，目录页码由排版引擎自动回填。

产物只落在 dist/（已加入 .gitignore），不提交主分支；分发请手动上传到 GitHub Releases。
PDF 是静态版本，不保留网页上的豆包跳转。

用法：
    python scripts/export_pdf.py                  # 全量导出
    python scripts/export_pdf.py --dry-run        # 只扫描并打印计划
    python scripts/export_pdf.py --only C2        # 只导某一册
    python scripts/export_pdf.py --engine weasyprint   # 换排版引擎（需额外系统库）
"""

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("缺少依赖 PyYAML，请先执行：pip install -r requirements.txt\n")
    raise

LEVELS: Tuple[str, ...] = ("A1", "A2", "B1", "B2", "C1", "C2")
MERMAID_BLOCK = re.compile(r"```mermaid\n(.*?)```", re.S)
H1_LINE = re.compile(r"^#\s+(.+)$", re.M)
DEFAULT_BATCH = "v0"

NOTICE = (
    "本 PDF 为离线静态版本，仅用于浏览词根图谱结构。"
    "PDF 无法保留网页交互：单词查询（释义、搭配、近义词辨析、公版例句）"
    "请访问仓库原版 Mermaid 文件中的豆包链接。"
)

CJK_FONT = "STSong-Light"  # ReportLab 内置 CJK 字体，无需外部字体文件


def log(message: str) -> None:
    print("[export] {0}".format(message), flush=True)


def warn(message: str) -> None:
    sys.stderr.write("[warn] {0}\n".format(message))
    sys.stderr.flush()


# ---------------------------------------------------------------------------
# 数据（只读 data/*.yaml，不修改任何源文件）
# ---------------------------------------------------------------------------


def read_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_word_levels(repo: Path) -> Dict[str, str]:
    data = read_yaml(repo / "data" / "relations.yaml")
    levels: Dict[str, str] = {}
    for item in data.get("relations", []) or []:
        target = str(item.get("target") or "").strip()
        level = item.get("cefr_level")
        if target and level and target not in levels:
            levels[target] = str(level).upper()
    return levels


def load_families(repo: Path) -> Dict[str, List[str]]:
    data = read_yaml(repo / "data" / "relations.yaml")
    families: Dict[str, List[str]] = {}
    for item in data.get("relations", []) or []:
        if str(item.get("rel_type") or "").lower() != "derivar":
            continue
        source = str(item.get("source") or "").strip()
        target = str(item.get("target") or "").strip()
        if source and target:
            families.setdefault(source, []).append(target)
    return families


def load_roots(repo: Path) -> List[Tuple[str, str]]:
    data = read_yaml(repo / "data" / "raices.yaml")
    roots: List[Tuple[str, str]] = []
    for item in data.get("raices", []) or []:
        root_id = str(item.get("id") or "").strip()
        if not root_id:
            continue
        batch = str(item.get("batch") or DEFAULT_BATCH).strip() or DEFAULT_BATCH
        roots.append((root_id, batch))
    return roots


# ---------------------------------------------------------------------------
# 扫描与分册
# ---------------------------------------------------------------------------


def discover_level_dirs(repo: Path, level: str) -> List[Path]:
    """若存在以等级命名的目录（如 A1/、mindmaps/A1/），收集其中的图源文件。"""
    found: List[Path] = []
    for base in (repo, repo / "mindmaps", repo / "source", repo / "src"):
        folder = base / level
        if folder.is_dir():
            for pattern in ("**/*.mmd", "**/*.mermaid", "**/*.md"):
                found.extend(sorted(folder.glob(pattern)))
    return sorted(set(found))


def page_title(md_path: Path, fallback: str) -> str:
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError:
        return fallback
    match = H1_LINE.search(text)
    if not match:
        return fallback
    title = match.group(1).strip().replace("`", "")
    return title or fallback


def plan_volumes(repo: Path, rule: str) -> Dict[str, List[Tuple[str, Path]]]:
    """等级 -> [(标题, 源文件)]。

    优先识别 <等级>/ 目录；仓库没有等级目录时，按词族中单词的 CEFR 级别归册
    （默认取众数，避免所有词族堆到同一册）。
    """
    word_levels = load_word_levels(repo)
    families = load_families(repo)
    roots = load_roots(repo)
    volumes: Dict[str, List[Tuple[str, Path]]] = {level: [] for level in LEVELS}
    level_dir_files = {level: discover_level_dirs(repo, level) for level in LEVELS}

    for root_id, batch in roots:
        page = repo / "mindmaps" / "raiz_{0}_{1}.md".format(batch, root_id)
        placed = False
        for candidate_level in LEVELS:
            for path in level_dir_files[candidate_level]:
                if path.stem == root_id or path.stem.endswith("_" + root_id):
                    volumes[candidate_level].append((page_title(path, path.stem), path))
                    placed = True
                    break
            if placed:
                break
        if placed:
            continue

        words = families.get(root_id, [])
        levels = [word_levels[word] for word in words if word in word_levels]
        level = ""
        if levels:
            if rule == "highest":
                level = max(levels, key=LEVELS.index)
            elif rule == "lowest":
                level = min(levels, key=LEVELS.index)
            else:  # mode
                counter = Counter(levels)
                level = sorted(counter.items(), key=lambda kv: (-kv[1], LEVELS.index(kv[0])))[0][0]
        if not level:
            warn("词根 {0} 没有可用级别，跳过".format(root_id))
            continue
        if not page.exists():
            warn("缺少导图页 {0}，跳过".format(page.relative_to(repo)))
            continue
        volumes[level].append((page_title(page, page.stem), page))

    for level in LEVELS:
        volumes[level].sort(key=lambda item: item[1].name)
    return volumes


# ---------------------------------------------------------------------------
# mermaid -> png
# ---------------------------------------------------------------------------


def extract_mermaid(md_path: Path) -> List[str]:
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError as exc:
        warn("读取失败 {0}：{1}".format(md_path, exc))
        return []
    return [block.strip() for block in MERMAID_BLOCK.findall(text) if block.strip()]


def write_mmd_files(
    repo: Path, dist: Path, volumes: Dict[str, List[Tuple[str, Path]]], levels: Sequence[str] = LEVELS
) -> Dict[str, List[Tuple[str, Path, Path]]]:
    """等级 -> [(标题, mmd 路径, png 路径)]；只为待导出的等级落盘。"""
    jobs: Dict[str, List[Tuple[str, Path, Path]]] = {level: [] for level in LEVELS}
    for level in levels:
        for title, source in volumes[level]:
            if source.suffix.lower() in (".mmd", ".mermaid"):
                blocks = [source.read_text(encoding="utf-8").strip()]
            else:
                blocks = extract_mermaid(source)
            if not blocks:
                warn("没有 mermaid 代码块，跳过 {0}".format(source))
                continue
            for index, block in enumerate(blocks, 1):
                suffix = "" if len(blocks) == 1 else "_{0}".format(index)
                mmd_path = dist / "src" / level / "{0}{1}.mmd".format(source.stem, suffix)
                mmd_path.parent.mkdir(parents=True, exist_ok=True)
                with mmd_path.open("w", encoding="utf-8", newline="\n") as handle:
                    handle.write(block + "\n")
                png_path = dist / "img" / level / "{0}{1}.png".format(source.stem, suffix)
                png_path.parent.mkdir(parents=True, exist_ok=True)
                label = title if len(blocks) == 1 else "{0}（图 {1}）".format(title, index)
                jobs[level].append((label, mmd_path, png_path))
    return jobs


def find_mmdc(explicit: Optional[str]) -> Optional[List[str]]:
    if explicit:
        return [explicit]
    found = shutil.which("mmdc")
    if found:
        return [found]
    if shutil.which("npx"):
        warn("未找到 mmdc，改用 npx 临时调用 mermaid-cli（首次运行需联网下载）")
        return ["npx", "-y", "@mermaid-js/mermaid-cli"]
    return None


CHROME_CANDIDATES: Tuple[str, ...] = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
)


def detect_chrome(explicit: Optional[str]) -> Optional[str]:
    """优先用 --chrome / 环境变量，其次探测系统已装浏览器。

    puppeteer 默认想用自己下载的 chrome-headless-shell；没装就会报
    “Could not find chrome-headless-shell”。直接用系统 Chrome 可以免掉这一步。
    """
    for value in (explicit, os.environ.get("ES_RAIZ_CHROME"), os.environ.get("PUPPETEER_EXECUTABLE_PATH")):
        if value and Path(value).exists():
            return value
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def ensure_puppeteer_config(dist: Path, chrome: Optional[str]) -> Path:
    path = dist / "puppeteer.json"
    config = {"args": ["--no-sandbox", "--disable-setuid-sandbox"]}
    if chrome:
        config["executablePath"] = chrome
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return path


def _error_line(text: str) -> str:
    """从 mmdc 输出里挑一行最有信息量的错误。"""
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    for line in lines:
        if line.lower().startswith("error"):
            return line
    for line in reversed(lines):
        if not line.startswith("at "):
            return line
    return "unknown"


def mmdc_option_variants(puppeteer: Path) -> List[List[str]]:
    """不同版本 mermaid-cli 的尺寸参数不一样：

    - v11+ 用 `--size <px>`（`-w/--width` 已移除）
    - v10 及以前用 `-w <px>`
    - 兜底：只给输入 / 输出，尺寸由 mermaid 自己决定
    """
    return [
        ["--size", "2000", "-b", "white", "-p", str(puppeteer)],
        ["-w", "2000", "-b", "white", "-p", str(puppeteer)],
        ["-b", "white"],
    ]


_OPTION_VARIANT_INDEX = None  # 记住第一个可用的参数组合，避免每个文件都试错


def render_png(mmdc: Sequence[str], mmd_path: Path, png_path: Path, puppeteer: Path, timeout: int) -> bool:
    global _OPTION_VARIANT_INDEX

    variants = mmdc_option_variants(puppeteer)
    order = [_OPTION_VARIANT_INDEX] if _OPTION_VARIANT_INDEX is not None else list(range(len(variants)))
    last_error = ""

    for index in order:
        cmd = list(mmdc) + ["-i", str(mmd_path), "-o", str(png_path)] + variants[index]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            warn("渲染超时（{0}s），跳过 {1}".format(timeout, mmd_path.name))
            return False
        except OSError as exc:
            warn("无法执行 mmdc：{0}".format(exc))
            return False

        if result.returncode == 0 and png_path.exists():
            _OPTION_VARIANT_INDEX = index
            return True

        last_error = _error_line(result.stderr or result.stdout)
        # 只有“参数不认”才换下一套参数；真正的渲染错误直接跳过
        if "unknown option" not in last_error.lower():
            break

    warn("渲染失败跳过 {0}：{1}".format(mmd_path.name, last_error))
    if "chrome" in last_error.lower():
        warn("提示：puppeteer 找不到浏览器。可先执行 npx puppeteer browsers install chrome-headless-shell，"
             "或用 --chrome 指定本机 Chrome 路径")
    return False


# ---------------------------------------------------------------------------
# ReportLab 组装（默认引擎，无系统依赖）
# ---------------------------------------------------------------------------


def _register_cjk() -> None:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont

    try:
        pdfmetrics.getFont(CJK_FONT)
    except Exception:
        pdfmetrics.registerFont(UnicodeCIDFont(CJK_FONT))


def _rl_styles():
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.styles import ParagraphStyle

    return {
        "title": ParagraphStyle("Title", fontName=CJK_FONT, fontSize=26, leading=34,
                                alignment=TA_CENTER, spaceAfter=10, textColor=colors.HexColor("#0d47a1")),
        "sub": ParagraphStyle("Sub", fontName=CJK_FONT, fontSize=12, leading=18,
                              alignment=TA_CENTER, textColor=colors.HexColor("#455a64"), spaceAfter=18),
        "notice": ParagraphStyle("Notice", fontName=CJK_FONT, fontSize=10.5, leading=17,
                                 textColor=colors.HexColor("#5d4037")),
        "h1": ParagraphStyle("H1", fontName=CJK_FONT, fontSize=18, leading=24, spaceAfter=12),
        "entry": ParagraphStyle("Entry", fontName=CJK_FONT, fontSize=13, leading=18, spaceAfter=6),
        "small": ParagraphStyle("Small", fontName=CJK_FONT, fontSize=8.5, leading=12,
                                textColor=colors.HexColor("#777777")),
        "cell": ParagraphStyle("Cell", fontName=CJK_FONT, fontSize=9.5, leading=13),
    }


def _rl_template(out_pdf: Path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph

    class NumberedDoc(BaseDocTemplate):
        def __init__(self, filename, **kwargs):
            BaseDocTemplate.__init__(self, filename, pagesize=A4,
                                     leftMargin=16 * mm, rightMargin=16 * mm,
                                     topMargin=16 * mm, bottomMargin=18 * mm, **kwargs)
            frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
            self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=self._footer)])

        def afterFlowable(self, flowable):
            # 把每一页的小标题登记为目录项，页码由 multiBuild 回填
            if isinstance(flowable, Paragraph) and flowable.style.name == "Entry":
                self.notify("TOCEntry", (0, flowable.getPlainText(), self.page))

        def _footer(self, canvas, doc):
            canvas.saveState()
            canvas.setFont(CJK_FONT, 8)
            canvas.setFillColorRGB(0.55, 0.55, 0.55)
            canvas.drawCentredString(A4[0] / 2.0, 10 * mm, "第 {0} 页".format(doc.page))
            canvas.restoreState()

    return NumberedDoc(str(out_pdf))


def build_volume_pdf(level: str, entries: List[Tuple[str, Path, Path]], out_pdf: Path, generated: str) -> int:
    """entries: [(标题, png, mmd)]，返回页数。"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import Image, PageBreak, Paragraph, Spacer, Table, TableStyle
    from reportlab.platypus.tableofcontents import TableOfContents

    _register_cjk()
    styles = _rl_styles()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc = _rl_template(out_pdf)

    story = [Spacer(1, 26 * mm),
             Paragraph("es-raiz-vocab · {0}".format(level), styles["title"]),
             Paragraph("西班牙语词根词族导图 · 离线静态版", styles["sub"])]

    notice = Table([[Paragraph("<b>说明：</b>" + NOTICE, styles["notice"])]], colWidths=[doc.width])
    notice.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#c9a227")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fffbea")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(notice)
    story.append(Spacer(1, 8 * mm))

    meta = Table(
        [
            [Paragraph("生成时间", styles["cell"]), Paragraph(generated, styles["cell"])],
            [Paragraph("本册内容", styles["cell"]), Paragraph("{0} 张图".format(len(entries)), styles["cell"])],
            [Paragraph("数据来源", styles["cell"]),
             Paragraph("mindmaps/ 下的 Mermaid 导图（只读渲染，未改动源文件）", styles["cell"])],
        ],
        colWidths=[30 * mm, doc.width - 30 * mm],
    )
    meta.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f4f4f4")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(meta)
    story.append(PageBreak())

    story.append(Paragraph("目录", styles["h1"]))
    toc = TableOfContents()
    toc.levelStyles = [styles["cell"]]
    story.append(toc)
    story.append(PageBreak())

    max_w = doc.width
    max_h = A4[1] - 60 * mm
    for title, png, mmd in entries:
        story.append(Paragraph(html.escape(title), styles["entry"]))
        try:
            img_w, img_h = ImageReader(str(png)).getSize()
        except Exception as exc:
            warn("图片无法读取，跳过 {0}：{1}".format(png.name, exc))
            continue
        scale = min(max_w / float(img_w), max_h / float(img_h), 1.0)
        story.append(Image(str(png), width=img_w * scale, height=img_h * scale))
        story.append(Spacer(1, 2 * mm))
        story.append(Paragraph("来源：{0}".format(html.escape(mmd.name)), styles["small"]))
        story.append(PageBreak())

    doc.multiBuild(story)
    return doc.page


def build_index_pdf(summary: List[Tuple[str, int, int, int]], detail: Dict[str, List[str]],
                    out_pdf: Path, generated: str) -> int:
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle

    _register_cjk()
    styles = _rl_styles()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc = _rl_template(out_pdf)

    total_roots = sum(item[1] for item in summary)
    total_images = sum(item[2] for item in summary)
    total_pages = sum(item[3] for item in summary)

    story = [Spacer(1, 26 * mm),
             Paragraph("es-raiz-vocab · 分册总目录", styles["title"]),
             Paragraph("A1–C2 词根导图离线 PDF 合集索引", styles["sub"])]

    notice = Table([[Paragraph("<b>说明：</b>" + NOTICE, styles["notice"])]], colWidths=[doc.width])
    notice.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#c9a227")),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fffbea")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(notice)
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "共 {0} 册 / {1} 个词根页 / {2} 张图 / {3} 页 · 生成于 {4}".format(
            len(summary), total_roots, total_images, total_pages, generated), styles["cell"]))
    story.append(Spacer(1, 6 * mm))

    rows = [[Paragraph("册别", styles["cell"]), Paragraph("词根页", styles["cell"]),
             Paragraph("图数", styles["cell"]), Paragraph("页数", styles["cell"]),
             Paragraph("文件", styles["cell"])]]
    for level, roots, images, pages in summary:
        rows.append([Paragraph(level, styles["cell"]), Paragraph(str(roots), styles["cell"]),
                     Paragraph(str(images), styles["cell"]), Paragraph(str(pages), styles["cell"]),
                     Paragraph("{0}.pdf".format(level), styles["cell"])])
    table = Table(rows, colWidths=[22 * mm, 25 * mm, 20 * mm, 20 * mm, doc.width - 87 * mm])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f4f4f4")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(table)
    story.append(PageBreak())

    story.append(Paragraph("分册明细", styles["h1"]))
    for level, roots, images, pages in summary:
        story.append(Paragraph("{0}（{1} 个词根页）".format(level, roots), styles["entry"]))
        for name in detail.get(level, []):
            story.append(Paragraph("· {0}".format(html.escape(name)), styles["cell"]))
        story.append(Spacer(1, 4 * mm))

    doc.multiBuild(story)
    return doc.page


# ---------------------------------------------------------------------------
# WeasyPrint 组装（可选引擎）
# ---------------------------------------------------------------------------

CSS = """
@page { size: A4; margin: 16mm 14mm; @bottom-center { content: counter(page) " / " counter(pages); font-size: 9pt; color: #666; } }
body { font-family: "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", sans-serif; color: #1a1a1a; }
.cover { page-break-after: always; padding-top: 40mm; }
.cover h1 { font-size: 26pt; margin: 0 0 6mm 0; }
.cover .sub { font-size: 11pt; color: #555; margin-bottom: 12mm; }
.notice { border: 1px solid #c9a227; background: #fffbea; padding: 6mm; font-size: 10.5pt; line-height: 1.7; }
.toc { page-break-after: always; }
.toc h1 { font-size: 18pt; margin: 0 0 8mm 0; }
.toc ol { padding-left: 6mm; }
.toc li { margin: 2.4mm 0; font-size: 11pt; }
.toc a { color: #1a1a1a; text-decoration: none; }
.toc a::after { content: leader(".") target-counter(attr(href), page); color: #666; }
.page { page-break-before: always; }
.page h2 { font-size: 13pt; margin: 0 0 4mm 0; border-bottom: 1px solid #ddd; padding-bottom: 2mm; }
.page img { max-width: 100%; max-height: 225mm; display: block; margin: 0 auto; }
.page .src { font-size: 8.5pt; color: #888; margin-top: 3mm; word-break: break-all; }
"""


def build_volume_pdf_weasy(level: str, entries: List[Tuple[str, Path, Path]], out_pdf: Path,
                           generated: str) -> int:
    try:
        from weasyprint import HTML  # type: ignore
    except Exception as exc:  # pragma: no cover
        warn("WeasyPrint 不可用（{0}）。可改用默认 --engine reportlab".format(exc))
        return 0
    parts = ["<!doctype html><html><head><meta charset='utf-8'><style>{0}</style></head><body>".format(CSS)]
    parts.append(
        "<section class='cover'><h1>es-raiz-vocab · {0}</h1>"
        "<p class='sub'>西班牙语词根词族导图 · 离线静态版</p>"
        "<div class='notice'><b>说明：</b>{1}</div>"
        "<p class='sub'>生成时间：{2} · 本册 {3} 张图</p></section>".format(
            html.escape(level), html.escape(NOTICE), html.escape(generated), len(entries))
    )
    parts.append("<section class='toc'><h1>目录</h1><ol>")
    for index, (title, _, _) in enumerate(entries, 1):
        parts.append("<li><a href='#e{0}'>{1}</a></li>".format(index, html.escape(title)))
    parts.append("</ol></section>")
    for index, (title, png, mmd) in enumerate(entries, 1):
        parts.append("<section class='page' id='e{0}'><h2>{1}</h2>".format(index, html.escape(title)))
        parts.append("<img src='{0}'>".format(html.escape(png.as_uri())))
        parts.append("<p class='src'>来源：{0}</p></section>".format(html.escape(mmd.name)))
    parts.append("</body></html>")
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    document = HTML(string="".join(parts)).render()
    document.write_pdf(str(out_pdf))
    return len(document.pages)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def preflight(engine: str) -> bool:
    """渲染前先检查依赖，避免花几分钟渲染完图像才在组装 PDF 时崩溃。"""
    problems: List[str] = []

    try:
        import yaml  # noqa: F401
    except ImportError:
        problems.append("PyYAML")

    if engine == "reportlab":
        try:
            import reportlab  # noqa: F401
        except ImportError:
            problems.append("reportlab")
    else:
        try:
            import weasyprint  # noqa: F401
        except Exception:
            problems.append("weasyprint（或系统库 pango 缺失）")

    if not problems:
        return True

    sys.stderr.write(
        "\n[error] 当前 Python 缺少依赖：{0}\n"
        "        解释器：{1}\n"
        "        修复：pip install -r requirements.txt\n"
        "        若仓库里有虚拟环境，请用它的解释器执行：.env/bin/python scripts/export_pdf.py\n\n".format(
            "、".join(problems), sys.executable
        )
    )
    return False


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="按 CEFR 等级导出静态 PDF（产物不进主分支）")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent, help="仓库根目录")
    parser.add_argument("--dist", type=Path, default=None, help="产物目录，默认 <repo>/dist")
    parser.add_argument("--only", default="", help="只导指定分册，逗号分隔，如 A1,B1")
    parser.add_argument("--level-rule", choices=("lowest", "highest", "mode"), default="mode",
                        help="无等级目录时按词族单词级别的哪种统计归册（默认 mode 众数）")
    parser.add_argument("--engine", choices=("reportlab", "weasyprint"), default="reportlab",
                        help="PDF 排版引擎（默认 reportlab，无需系统库）")
    parser.add_argument("--mmdc", default=None, help="mmdc 可执行文件路径（默认自动探测）")
    parser.add_argument("--chrome", default=None, help="传给 puppeteer 的浏览器路径（默认自动探测系统 Chrome）")
    parser.add_argument("--timeout", type=int, default=180, help="单个 mmd 渲染超时秒数")
    parser.add_argument("--reuse-images", action="store_true",
                        help="复用 dist/img 下已有 PNG，不重新渲染（适合分批渲染后统一组装）")
    parser.add_argument("--dry-run", action="store_true", help="只扫描并打印计划")
    args = parser.parse_args(argv)

    repo = args.repo.resolve()
    dist = (args.dist or (repo / "dist")).resolve()
    generated = time.strftime("%Y-%m-%d %H:%M")

    wanted = [item.strip().upper() for item in args.only.split(",") if item.strip()] or list(LEVELS)
    for level in wanted:
        if level not in LEVELS:
            sys.stderr.write("未知等级：{0}\n".format(level))
            return 2

    if not preflight(args.engine):
        return 4

    log("扫描仓库：{0}".format(repo))
    volumes = plan_volumes(repo, args.level_rule)
    for level in LEVELS:
        log("  {0}: {1} 个词根页".format(level, len(volumes[level])))

    if args.dry_run:
        for level in wanted:
            for title, source in volumes[level][:3]:
                log("  {0} · {1} <- {2}".format(level, title, source.relative_to(repo)))
            if len(volumes[level]) > 3:
                log("  {0} · … 其余 {1} 个".format(level, len(volumes[level]) - 3))
        log("--dry-run：未渲染、未写 PDF")
        return 0

    jobs = write_mmd_files(repo, dist, volumes, wanted)
    mmdc = find_mmdc(args.mmdc)
    if mmdc is None and not args.reuse_images:
        warn("未找到 mermaid-cli，请先 npm i -g @mermaid-js/mermaid-cli 或用 --mmdc 指定")
        return 3
    puppeteer = ensure_puppeteer_config(dist, detect_chrome(args.chrome)) if mmdc else None
    if mmdc and detect_chrome(args.chrome):
        log("使用浏览器：{0}".format(detect_chrome(args.chrome)))

    builder = build_volume_pdf_weasy if args.engine == "weasyprint" else build_volume_pdf
    summary: List[Tuple[str, int, int, int]] = []
    detail: Dict[str, List[str]] = {}

    for level in wanted:
        entries = jobs.get(level, [])
        log("{0}：渲染 {1} 张图".format(level, len(entries)))
        rendered: List[Tuple[str, Path, Path]] = []
        for title, mmd_path, png_path in entries:
            if args.reuse_images and png_path.exists():
                log("  = {0}（复用）".format(png_path.relative_to(dist)))
                rendered.append((title, png_path, mmd_path))
                continue
            log("  - {0} -> {1}".format(mmd_path.name, png_path.relative_to(dist)))
            if mmdc is not None and render_png(mmdc, mmd_path, png_path, puppeteer, args.timeout):
                rendered.append((title, png_path, mmd_path))
        if not rendered:
            warn("{0} 没有可用图片，跳过该分册".format(level))
            continue
        out_pdf = dist / "pdf" / "{0}.pdf".format(level)
        pages = builder(level, rendered, out_pdf, generated)
        log("  -> {0}（{1} 页）".format(out_pdf.relative_to(dist), pages))
        summary.append((level, len(rendered), len(rendered), pages))
        detail[level] = [title for title, _, _ in rendered]

    if summary:
        out_index = dist / "pdf" / "index-toc.pdf"
        pages = build_index_pdf(summary, detail, out_index, generated)
        log("  -> {0}（{1} 页）".format(out_index.relative_to(dist), pages))

    log("完成：{0}/pdf —— 该目录已在 .gitignore 中，请手动上传 GitHub Releases".format(dist.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
