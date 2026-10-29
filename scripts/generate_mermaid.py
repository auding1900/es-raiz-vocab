#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""es-raiz-vocab 静态产物生成器。

依赖安装：
    pip install pyyaml
    # 或（在项目虚拟环境中）
    python3 -m pip install pyyaml

读取：
    data/raices.yaml     词根节点   id / root_name / latin_origin
    data/relations.yaml  关系边     source / target / rel_type / cefr_level / prompt_template
    data/afijos.yaml     词缀节点   （仅参与校验与统计，暂不渲染）

生成（纯静态 markdown，不启动任何 web 服务）：
    mindmaps/root_tree.md        词根树导图（mermaid graph LR，单词节点带豆包 click）
    mindmaps/associate_graph.md  联想网状图（仅 asociar + confundir）
    levels/A1.md … C2.md         分级清单（每个单词带豆包链接）

用法：
    python3 scripts/generate_mermaid.py            # 清理旧产物后重新生成
    python3 scripts/generate_mermaid.py --check    # 只校验 data/*.yaml，不写文件
    python3 scripts/generate_mermaid.py --dry-run  # 渲染并打印统计，不写文件

说明：
    * 链接形如 https://www.doubao.com/chat?q=<URL 编码后的 prompt>，
      prompt 内的 {word} = 单词，{root} = 词根 id（未绑定词根时为空字符串）。
    * URL 编码使用 UTF-8（quote(..., safe="")），ñ á é í ó ú 等西语字符会正确转义。
    * 本仓库只保存关系，不保存释义与例句；页面上的词义/例句一律跳转豆包。
"""

from __future__ import annotations

import argparse
import dataclasses
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import quote

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("缺少依赖 PyYAML，请先执行：pip install pyyaml\n")
    raise

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

LEVELS: Tuple[str, ...] = ("A1", "A2", "B1", "B2", "C1", "C2")
REL_TYPES: Tuple[str, ...] = ("derivar", "asociar", "confundir")
AFFIX_TYPES: Tuple[str, ...] = ("prefix", "suffix")

# 默认查询模板：{word} = 单词，{root} = 词根 id
PROMPT_TEMPLATE = (
    "西班牙语{word}，词根{root}，解释词义、DELE等级、语体、常用搭配、近义词辨析，"
    "并且给2条来自公版西语文本（Wikisource/古登堡）的自然例句，"
    "例句优先选用现代标准西班牙语，古体例句标注【arcaísmo】"
)

# 豆包网页查询入口（{query} 会被替换为 URL 编码后的 prompt）
DOUBAO_URL = "https://www.doubao.com/chat?q={query}"

# 关系 -> (mermaid 箭头, linkStyle 样式, 边标签)
EDGE_STYLE: Dict[str, Tuple[str, str, str]] = {
    "derivar": ("-->", "stroke:#000000,stroke-width:1.5px", ""),
    "asociar": ("-.->", "stroke:#4488bb,stroke-width:2px,stroke-dasharray:6 4", "asociar"),
    "confundir": ("-.->", "stroke:#dd4444,stroke-width:2px,stroke-dasharray:6 4", "confundir"),
}

# 级别 -> 节点配色（fill, stroke）
LEVEL_STYLE: Dict[str, Tuple[str, str]] = {
    "A1": ("#e8f5e9", "#2e7d32"),
    "A2": ("#c8e6c9", "#2e7d32"),
    "B1": ("#fff8e1", "#f9a825"),
    "B2": ("#ffe0b2", "#ef6c00"),
    "C1": ("#ffccbc", "#d84315"),
    "C2": ("#ffcdd2", "#b71c1c"),
}
UNKNOWN_LEVEL_STYLE: Tuple[str, str] = ("#f5f5f5", "#9e9e9e")
ROOT_NODE_STYLE: Tuple[str, str] = ("#bbdefb", "#1565c0")

GENERATED_MARK = "<!-- 由 scripts/generate_mermaid.py 自动生成，请勿手工编辑 -->"

# Mermaid 默认 maxTextSize = 50000 字符，超过后 GitHub / 浏览器会直接显示
# “Maximum text size in diagram exceeded”。留出余量后按此阈值告警。
MAX_DIAGRAM_CHARS = 45000

# 联想图单图超过该字符数时，自动按词根首字母（A–L / M–Z）拆分
SPLIT_THRESHOLD = 25000

FORBIDDEN_KEYS = frozenset(
    {
        "definition",
        "definitions",
        "meaning_cn",
        "gloss_cn",
        "example",
        "examples",
        "ejemplo",
        "ejemplos",
        "translation",
        "translations",
        "note_cn",
        "explanation_cn",
    }
)

REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_ROOT_KEYS = ("id", "root_name", "latin_origin")
ALLOWED_AFIJO_KEYS = ("id", "affix", "meaning", "type")
ALLOWED_RELATION_KEYS = ("source", "target", "rel_type", "cefr_level", "prompt_template")

_CJK_RE = re.compile(r"[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]")

_QUIET = False


def log(message: str) -> None:
    if not _QUIET:
        print("[generate] {0}".format(message))


def warn(message: str) -> None:
    sys.stderr.write("warning: {0}\n".format(message))


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class Root:
    id: str
    root_name: str
    latin_origin: str


@dataclasses.dataclass(frozen=True)
class Afijo:
    id: str
    affix: str
    meaning: str
    type: str


@dataclasses.dataclass(frozen=True)
class Relation:
    source: str
    target: str
    rel_type: str
    cefr_level: Optional[str] = None
    prompt_template: Optional[str] = None

    def template(self) -> str:
        return self.prompt_template or PROMPT_TEMPLATE

    @property
    def edge(self) -> Tuple[str, str, str]:
        return (self.source, self.target, self.rel_type)


@dataclasses.dataclass(frozen=True)
class Dataset:
    raices: Tuple[Root, ...]
    afijos: Tuple[Afijo, ...]
    relations: Tuple[Relation, ...]

    @property
    def root_ids(self) -> set:
        return {root.id for root in self.raices}


class DataError(Exception):
    """数据源结构错误：缺字段、多字段、类型不符。"""


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------


def nfc(text: str) -> str:
    """统一成 NFC，避免 macOS 上的分解式重音（n + U+0303 vs ñ）。"""
    return unicodedata.normalize("NFC", text)


def slug(text: str) -> str:
    """ASCII 安全的短 id，用作 mermaid 节点 id 与文件名。"""
    folded = unicodedata.normalize("NFKD", text)
    ascii_only = folded.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", ascii_only).strip("_").lower()
    return cleaned or "node"


def sort_key(text: str) -> str:
    """忽略重音与大小写的排序键。"""
    return unicodedata.normalize("NFKD", text).casefold()


def build_prompt(template: str, word: str, root: str) -> str:
    """填充模板；root 为空时清掉「词根」这一段，避免留下“词根，”这种残句。"""
    prompt = template.format(word=word, root=root)
    if not root:
        prompt = _drop_empty_root(prompt)
    return prompt


_EMPTY_ROOT_CLAUSE = re.compile(r"词根\s*[，,：:]?\s*")


def _drop_empty_root(prompt: str) -> str:
    cleaned = _EMPTY_ROOT_CLAUSE.sub("", prompt)
    cleaned = re.sub(r"[，,]{2,}", "，", cleaned)
    cleaned = re.sub(r"[，,]\s*([。；;])", r"\1", cleaned)
    cleaned = re.sub(r"^[，,：:；;]\s*", "", cleaned)
    return cleaned.strip()


def doubao_url(word: str, root: str, template: Optional[str] = None) -> str:
    """拼接豆包查询链接；query 全量 URL 编码（含 ñ á é í ó ú 等字符）。"""
    prompt = build_prompt(template or PROMPT_TEMPLATE, word, root or "")
    return DOUBAO_URL.format(query=quote(nfc(prompt), safe=""))


def esc_label(text: str) -> str:
    """mermaid 引号标签转义：保留 <br/>，去掉会打断解析的括号。"""
    cleaned = nfc(text).replace('"', "#quot;").replace("\n", " ")
    for char in "[]{}":
        cleaned = cleaned.replace(char, "")
    return re.sub(r"\s+", " ", cleaned).strip()


def level_class(level: Optional[str]) -> str:
    return "lvl{0}".format(level) if level in LEVELS else "lvlNA"


def md_cell(value: Any) -> str:
    text = str(value).replace("|", "\\|").replace("\n", " ").strip()
    return text or "—"


def md_table(headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(cell) for cell in row) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 读取
# ---------------------------------------------------------------------------


def read_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _section(path: Path, key: str) -> List[Any]:
    raw = read_yaml(path)
    if raw is None:
        return []
    if not isinstance(raw, dict):
        raise DataError("{0}: 顶层必须是映射".format(path.name))
    unknown = sorted(set(raw) - {"version", key})
    if unknown:
        raise DataError("{0}: 顶层未知字段 {1}（允许 version / {2}）".format(path.name, unknown, key))
    items = raw.get(key)
    if items is None:
        return []
    if not isinstance(items, list):
        raise DataError("{0}: {1} 必须是列表".format(path.name, key))
    return items


def _expect_mapping(value: Any, where: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise DataError("{0}: 期望映射，实际是 {1}".format(where, type(value).__name__))
    return value


def _reject_unknown(mapping: Dict[str, Any], allowed: Sequence[str], where: str) -> None:
    unknown = sorted(set(mapping) - set(allowed))
    if unknown:
        raise DataError("{0}: 未知字段 {1}；允许的字段为 {2}".format(where, unknown, list(allowed)))


def _require_str(mapping: Dict[str, Any], key: str, where: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DataError("{0}: 字段 {1} 必须是非空字符串".format(where, key))
    return nfc(value.strip())


def _optional_str(mapping: Dict[str, Any], key: str, where: str) -> Optional[str]:
    value = mapping.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise DataError("{0}: 字段 {1} 必须是字符串或 null".format(where, key))
    stripped = nfc(value.strip())
    return stripped or None


def load_dataset(data_dir: Path) -> Dataset:
    raices: List[Root] = []
    for index, item in enumerate(_section(data_dir / "raices.yaml", "raices")):
        where = "raices[{0}]".format(index)
        mapping = _expect_mapping(item, where)
        _reject_unknown(mapping, ALLOWED_ROOT_KEYS, where)
        raices.append(
            Root(
                id=_require_str(mapping, "id", where),
                root_name=_require_str(mapping, "root_name", where),
                latin_origin=_require_str(mapping, "latin_origin", where),
            )
        )

    afijos: List[Afijo] = []
    for index, item in enumerate(_section(data_dir / "afijos.yaml", "afijos")):
        where = "afijos[{0}]".format(index)
        mapping = _expect_mapping(item, where)
        _reject_unknown(mapping, ALLOWED_AFIJO_KEYS, where)
        afijos.append(
            Afijo(
                id=_require_str(mapping, "id", where),
                affix=_require_str(mapping, "affix", where),
                meaning=_require_str(mapping, "meaning", where),
                type=_require_str(mapping, "type", where).lower(),
            )
        )

    relations: List[Relation] = []
    for index, item in enumerate(_section(data_dir / "relations.yaml", "relations")):
        where = "relations[{0}]".format(index)
        mapping = _expect_mapping(item, where)
        _reject_unknown(mapping, ALLOWED_RELATION_KEYS, where)
        level = _optional_str(mapping, "cefr_level", where)
        relations.append(
            Relation(
                source=_require_str(mapping, "source", where),
                target=_require_str(mapping, "target", where),
                rel_type=_require_str(mapping, "rel_type", where).lower(),
                cefr_level=level.upper() if level else None,
                prompt_template=_optional_str(mapping, "prompt_template", where),
            )
        )

    return Dataset(raices=tuple(raices), afijos=tuple(afijos), relations=tuple(relations))


# ---------------------------------------------------------------------------
# 校验
# ---------------------------------------------------------------------------


def scan_raw(data_dir: Path, errors: List[str]) -> None:
    """检查禁用字段与中文值（中文仅允许出现在 prompt_template）。"""
    for name in ("raices", "afijos", "relations"):
        _scan(read_yaml(data_dir / (name + ".yaml")) or {}, name, errors)


def _scan(node: Any, where: str, errors: List[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(key, str) and key in FORBIDDEN_KEYS:
                errors.append("{0}: 禁用字段 {1!r}（仓库不存放释义/例句/翻译）".format(where, key))
            _scan(value, "{0}.{1}".format(where, key), errors)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            _scan(value, "{0}[{1}]".format(where, index), errors)
    elif isinstance(node, str):
        if _CJK_RE.search(node) and not where.endswith("prompt_template"):
            errors.append(
                "{0}: 值 {1!r} 含中文；单词节点不得带中文释义（中文仅允许出现在 prompt_template）".format(
                    where, node
                )
            )


def validate(dataset: Dataset) -> List[str]:
    errors: List[str] = []

    roots: Dict[str, Root] = {}
    for root in dataset.raices:
        if root.id in roots:
            errors.append("raices: 词根 id 重复：{0!r}".format(root.id))
        if not re.match(r"^[a-z0-9][a-z0-9_-]*$", root.id):
            errors.append("raices: 词根 id {0!r} 只能包含小写字母/数字/下划线/连字符".format(root.id))
        roots[root.id] = root

    afijo_ids: set = set()
    for afijo in dataset.afijos:
        if afijo.type not in AFFIX_TYPES:
            errors.append("afijos[{0}]: type 非法 {1!r}（应为 prefix / suffix）".format(afijo.id, afijo.type))
        if afijo.id in afijo_ids:
            errors.append("afijos: 词缀 id 重复：{0!r}".format(afijo.id))
        afijo_ids.add(afijo.id)

    targets = {relation.target for relation in dataset.relations}
    seen_edges: set = set()

    for index, relation in enumerate(dataset.relations):
        where = "relations[{0}]".format(index)

        if relation.rel_type not in REL_TYPES:
            errors.append("{0}: rel_type 非法 {1!r}（应为 derivar / asociar / confundir）".format(where, relation.rel_type))
        if relation.cefr_level is not None and relation.cefr_level not in LEVELS:
            errors.append("{0}: cefr_level 非法 {1!r}".format(where, relation.cefr_level))
        if relation.source == relation.target:
            errors.append("{0}: source 与 target 相同（自环）：{1!r}".format(where, relation.source))
        if relation.source not in roots and relation.source not in targets:
            errors.append(
                "{0}: source {1!r} 既不是词根 id，也不是已声明的单词（需先作为某条边的 target 出现）".format(
                    where, relation.source
                )
            )
        if relation.target in roots:
            errors.append("{0}: target {1!r} 是词根 id；target 必须是单词".format(where, relation.target))
        if relation.edge in seen_edges:
            errors.append(
                "{0}: 重复边 {1} -{2}-> {3}".format(where, relation.source, relation.rel_type, relation.target)
            )
        seen_edges.add(relation.edge)

        template = relation.template()
        for placeholder in ("{word}", "{root}"):
            if placeholder not in template:
                errors.append("{0}: prompt_template 缺少占位符 {1}".format(where, placeholder))
        try:
            build_prompt(template, "muestra", "demo")
        except (KeyError, IndexError, ValueError) as exc:
            errors.append("{0}: prompt_template 无法格式化：{1}".format(where, exc))

    # 不同词形折叠成同一节点 id 时，图里会悄悄合并成两个同名节点
    word_names = {relation.target for relation in dataset.relations}
    word_names |= {relation.source for relation in dataset.relations if relation.source not in roots}
    node_ids: Dict[str, str] = {}
    for name in sorted(word_names):
        node_id = slug(name)
        if node_id in node_ids:
            errors.append(
                "relations: 单词 {0!r} 与 {1!r} 的 mermaid 节点 id 相同（{2}）".format(node_ids[node_id], name, node_id)
            )
        node_ids[node_id] = name

    return errors


def collect_warnings(dataset: Dataset) -> List[str]:
    warnings: List[str] = []
    derived = {relation.source for relation in dataset.relations if relation.rel_type == "derivar"}
    for root in dataset.raices:
        if root.id not in derived:
            warnings.append("词根 {0!r} 没有任何 derivar 边".format(root.id))
    return warnings


# ---------------------------------------------------------------------------
# 派生视图
# ---------------------------------------------------------------------------


def word_levels(dataset: Dataset) -> Dict[str, Optional[str]]:
    """单词 -> CEFR 级别（级别挂在边上，取首条非空值）。"""
    root_ids = dataset.root_ids
    levels: Dict[str, Optional[str]] = {}
    for relation in dataset.relations:
        if relation.target in root_ids:
            continue
        current = levels.get(relation.target)
        if current is None and relation.cefr_level:
            levels[relation.target] = relation.cefr_level
        else:
            levels.setdefault(relation.target, relation.cefr_level)
    for relation in dataset.relations:
        if relation.source not in root_ids:
            levels.setdefault(relation.source, relation.cefr_level)
    return levels


def root_of_word(dataset: Dataset, word: str) -> Optional[str]:
    """沿 derivar 边回溯到词根 id；未绑定时返回 None。"""
    root_ids = dataset.root_ids
    parents: Dict[str, str] = {}
    for relation in dataset.relations:
        if relation.rel_type == "derivar":
            parents.setdefault(relation.target, relation.source)
    current = word
    for _ in range(len(parents) + 1):
        parent = parents.get(current)
        if parent is None:
            return None
        if parent in root_ids:
            return parent
        current = parent
    return None


def prompt_for_word(dataset: Dataset, word: str) -> str:
    """取该单词所在边的 prompt_template；都没有则用默认模板。"""
    candidates = [rel for rel in dataset.relations if rel.target == word]
    candidates += [rel for rel in dataset.relations if rel.source == word]
    for relation in candidates:
        if relation.prompt_template:
            return relation.prompt_template
    return PROMPT_TEMPLATE


def word_link(dataset: Dataset, word: str) -> str:
    root = root_of_word(dataset, word) or ""
    return doubao_url(word, root, prompt_for_word(dataset, word))


# ---------------------------------------------------------------------------
# 渲染：mermaid 片段
# ---------------------------------------------------------------------------


def _root_node_id(root_id: str) -> str:
    return "R_{0}".format(slug(root_id))


def _word_node_id(word: str) -> str:
    return "W_{0}".format(slug(word))


def _node_id(name: str, roots: Dict[str, Root]) -> str:
    return _root_node_id(name) if name in roots else _word_node_id(name)


def _declare_nodes(dataset: Dataset, names: Iterable[str], levels: Dict[str, Optional[str]]) -> List[str]:
    """生成节点声明（词根用根节点样式，单词带级别标签与级别配色）。"""
    roots = {root.id: root for root in dataset.raices}
    lines: List[str] = []

    for name in sorted((n for n in names if n in roots), key=sort_key):
        root = roots[name]
        label = "{0}<br/>{1}".format(root.root_name, root.latin_origin) if root.latin_origin else root.root_name
        lines.append('  {0}["{1}"]:::root'.format(_root_node_id(name), esc_label(label)))

    for name in sorted((n for n in names if n not in roots), key=sort_key):
        level = levels.get(name)
        label = "{0}<br/>{1}".format(name, level) if level else name
        lines.append('  {0}["{1}"]:::{2}'.format(_word_node_id(name), esc_label(label), level_class(level)))

    return lines


def _class_defs() -> List[str]:
    lines = [
        "  classDef root fill:{0},stroke:{1},stroke-width:2px,color:#0d47a1".format(*ROOT_NODE_STYLE)
    ]
    for level in LEVELS:
        fill, stroke = LEVEL_STYLE[level]
        lines.append("  classDef {0} fill:{1},stroke:{2},color:#1a1a1a".format(level_class(level), fill, stroke))
    lines.append(
        "  classDef {0} fill:{1},stroke:{2},color:#424242".format(level_class(None), *UNKNOWN_LEVEL_STYLE)
    )
    return lines


def _click_lines(dataset: Dataset, names: Iterable[str]) -> List[str]:
    root_ids = dataset.root_ids
    lines = []
    for name in sorted(set(names), key=sort_key):
        if name in root_ids:
            continue
        lines.append(
            '  click {0} "{1}" "豆包查询：{2}" _blank'.format(_word_node_id(name), word_link(dataset, name), name)
        )
    return lines


def _edge_block(dataset: Dataset, relations: Sequence[Relation], roots: Dict[str, Root]) -> Tuple[List[str], List[str]]:
    """返回 (边声明, linkStyle)，链接顺序与 relations 顺序一致。"""
    edges: List[str] = []
    styles: List[str] = []
    for index, relation in enumerate(relations):
        arrow, style, label = EDGE_STYLE[relation.rel_type]
        source = _node_id(relation.source, roots)
        target = _node_id(relation.target, roots)
        if label:
            edges.append("  {0} {1}|{2}| {3}".format(source, arrow, label, target))
        else:
            edges.append("  {0} {1} {2}".format(source, arrow, target))
        styles.append("  linkStyle {0} {1}".format(index, style))
    return edges, styles


def _mermaid(diagram: Sequence[str]) -> str:
    return "\n".join(["```mermaid"] + list(diagram) + ["```"])


def _diagram(
    dataset: Dataset, names: Iterable[str], relations: Sequence[Relation], levels: Dict[str, Optional[str]]
) -> List[str]:
    """拼一张完整的 graph LR 图（节点 + 边 + 样式 + click）。"""
    roots = {root.id: root for root in dataset.raices}
    names = list(names)
    lines: List[str] = ["graph LR"]
    lines.extend(_declare_nodes(dataset, names, levels))
    edges, styles = _edge_block(dataset, relations, roots)
    lines.extend(edges)
    lines.extend(styles)
    lines.extend(_class_defs())
    lines.extend(_click_lines(dataset, [name for name in names if name not in roots]))
    return lines


def _size_guard(label: str, diagram: Sequence[str]) -> None:
    """单张图超过 mermaid 上限时告警（不阻断生成）。"""
    size = len("\n".join(diagram))
    if size > MAX_DIAGRAM_CHARS:
        warn(
            "图「{0}」{1} 字符，超过阈值 {2}；mermaid 默认 maxTextSize=50000，需要继续拆分".format(
                label, size, MAX_DIAGRAM_CHARS
            )
        )


# ---------------------------------------------------------------------------
# 渲染：页面
# ---------------------------------------------------------------------------


def _link_table(dataset: Dataset, words: Sequence[str]) -> str:
    levels = word_levels(dataset)
    rows = []
    for word in words:
        root = root_of_word(dataset, word)
        rows.append((word, levels.get(word) or "—", root or "—", "[豆包]({0})".format(word_link(dataset, word))))
    return md_table(["单词", "级别", "词根", "豆包"], rows)


def render_root_tree_page(dataset: Dataset) -> str:
    """每个词根一张 mermaid 图：单图过大时浏览器 / GitHub 会拒绝渲染。"""
    levels = word_levels(dataset)
    roots = {root.id: root for root in dataset.raices}
    grouped, orphan = _blocks_by_root(dataset)
    all_words = sorted(
        {rel.target for rel in dataset.relations}
        | {rel.source for rel in dataset.relations if rel.source not in roots},
        key=sort_key,
    )

    lines = [
        GENERATED_MARK,
        "",
        "# 词根树导图",
        "",
        "- 词根 {0} 个 · 单词 {1} 个 · 关系 {2} 条".format(
            len(dataset.raices), len(all_words), len(dataset.relations)
        ),
        "- 每个词根一张图，避免单图超过 mermaid 的 `maxTextSize` 上限",
        "- 线型：`derivar` 实线黑 · `asociar` 虚线 `#4488bb` · `confundir` 虚线 `#dd4444`",
        "- 节点可点击跳转豆包查询（GitHub 会忽略 mermaid 的 click，可用文末链接表）",
        "",
    ]

    for root in sorted(dataset.raices, key=lambda item: sort_key(item.id)):
        relations = grouped.get(root.id, [])
        names = {root.id} | {rel.source for rel in relations} | {rel.target for rel in relations}
        words = sorted((name for name in names if name not in roots), key=sort_key)
        lines.append("## `{0}` — {1}".format(root.root_name, root.latin_origin))
        lines.append("")
        if words:
            lines.append("单词 {0} 个 · 关系 {1} 条".format(len(words), len(relations)))
            lines.append("")
        diagram = _diagram(dataset, names, relations, levels)
        _size_guard(root.id, diagram)
        lines.append(_mermaid(diagram))
        lines.append("")

    if orphan:
        names = {rel.source for rel in orphan} | {rel.target for rel in orphan}
        lines.extend(
            [
                "## 未绑定词根",
                "",
                "以下单词只出现在联想 / 易混关系中，尚未归入任何词根。",
                "",
            ]
        )
        diagram = _diagram(dataset, names, orphan, levels)
        _size_guard("orphan", diagram)
        lines.append(_mermaid(diagram))
        lines.append("")

    lines.extend(["## 单词链接表", "", _link_table(dataset, all_words), ""])
    return "\n".join(lines)


def _blocks_by_root(dataset: Dataset) -> Tuple[Dict[str, List[Relation]], List[Relation]]:
    """把关系按词根分组；无法归属词根的边进入 orphan 列表。"""
    root_ids = dataset.root_ids
    grouped: Dict[str, List[Relation]] = {root.id: [] for root in dataset.raices}
    orphan: List[Relation] = []
    for relation in dataset.relations:
        if relation.rel_type == "derivar":
            owner = root_of_word(dataset, relation.target)
            if owner is None and relation.source in root_ids:
                owner = relation.source
        else:
            owner = root_of_word(dataset, relation.source) or root_of_word(dataset, relation.target)
        if owner in grouped:
            grouped[owner].append(relation)
        else:
            orphan.append(relation)
    return grouped, orphan


def _bucket_label(dataset: Dataset, relation: Relation) -> str:
    """按所属词根 id 的首字母分桶，用于超长联想图自动拆分。"""
    owner = root_of_word(dataset, relation.source) or root_of_word(dataset, relation.target)
    if not owner:
        return "未归属"
    return "A–L" if owner[0].lower() <= "l" else "M–Z"


def _associate_diagrams(
    dataset: Dataset, relations: Sequence[Relation], levels: Dict[str, Optional[str]]
) -> List[Tuple[str, Sequence[Relation], List[str]]]:
    """返回 [(分块标签, 关系子集, 图代码)]；单图不超过阈值就不拆。"""
    names = {rel.source for rel in relations} | {rel.target for rel in relations}
    diagram = _diagram(dataset, names, relations, levels)
    if len("\n".join(diagram)) <= SPLIT_THRESHOLD:
        return [("", relations, diagram)]

    buckets: Dict[str, List[Relation]] = {}
    for relation in relations:
        buckets.setdefault(_bucket_label(dataset, relation), []).append(relation)

    parts: List[Tuple[str, Sequence[Relation], List[str]]] = []
    for label in ("A–L", "M–Z", "未归属"):
        subset = buckets.get(label)
        if not subset:
            continue
        subset_names = {rel.source for rel in subset} | {rel.target for rel in subset}
        parts.append((label, subset, _diagram(dataset, subset_names, subset, levels)))
    return parts


def render_associate_page(dataset: Dataset) -> str:
    """联想网状图：asociar 与 confundir 分开；单图过长时再按词根首字母拆分。"""
    levels = word_levels(dataset)
    sections: List[str] = []
    rows: List[Tuple[str, str, str, str, str]] = []
    total_edges = 0

    for rel_type in ("asociar", "confundir"):
        relations = [rel for rel in dataset.relations if rel.rel_type == rel_type]
        color = EDGE_STYLE[rel_type][1].split(",")[0].replace("stroke:", "")
        title = "语义联想（`asociar`）" if rel_type == "asociar" else "形近易混（`confundir`）"

        if not relations:
            sections.extend(["## {0} — 虚线 `{1}`".format(title, color), "", "（暂无此类关系）", ""])
            continue

        for label, subset, diagram in _associate_diagrams(dataset, relations, levels):
            heading = "## {0} — 虚线 `{1}`".format(title, color)
            if label:
                heading += " · 词根 {0}".format(label)
            names = {rel.source for rel in subset} | {rel.target for rel in subset}
            sections.append(heading)
            sections.append("")
            sections.append("关系 {0} 条 · 涉及单词 {1} 个".format(len(subset), len(names)))
            sections.append("")
            _size_guard("associate_graph_{0}{1}".format(rel_type, "_" + label if label else ""), diagram)
            sections.append(_mermaid(diagram))
            sections.append("")

        total_edges += len(relations)
        for rel in relations:
            rows.append(
                (
                    rel.rel_type,
                    rel.source,
                    rel.target,
                    "[豆包]({0})".format(word_link(dataset, rel.source)),
                    "[豆包]({0})".format(word_link(dataset, rel.target)),
                )
            )

    lines = [
        GENERATED_MARK,
        "",
        "# 联想网状图（asociar + confundir）",
        "",
        "- 只包含 `asociar`（虚线 `#4488bb`）与 `confundir`（虚线 `#dd4444`），不含 `derivar`",
        "- 两类关系分开渲染；单图超过 {0} 字符时再按词根首字母（A–L / M–Z）拆分".format(SPLIT_THRESHOLD),
        "- 关系 {0} 条".format(total_edges),
        "",
    ]
    lines.extend(sections)
    if rows:
        lines.extend(["## 关系清单", "", md_table(["关系", "起点", "终点", "起点查询", "终点查询"], rows), ""])
    return "\n".join(lines)


def _level_nav(current: str) -> str:
    parts = []
    for level in LEVELS:
        parts.append("**{0}**".format(level) if level == current else "[{0}]({0}.md)".format(level))
    return " · ".join(parts)


def render_level_page(level: str, dataset: Dataset) -> str:
    levels = word_levels(dataset)
    words = sorted((word for word, lv in levels.items() if lv == level), key=sort_key)

    rows = []
    for word in words:
        root = root_of_word(dataset, word)
        rows.append((word, root or "—", "[豆包]({0})".format(word_link(dataset, word))))

    body = md_table(["单词", "词根", "豆包"], rows) if rows else "（本级别暂无单词）"

    lines = [
        GENERATED_MARK,
        "",
        "# {0} 单词清单".format(level),
        "",
        "共 {0} 个单词 · [词根树导图](../mindmaps/root_tree.md) · [联想网状图](../mindmaps/associate_graph.md)".format(
            len(words)
        ),
        "",
        _level_nav(level),
        "",
        body,
        "",
        "> 本页只列出单词与关系，不含释义与例句；词义、语体、搭配、例句请点击「豆包」。",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 写盘
# ---------------------------------------------------------------------------


def render_outputs(dataset: Dataset) -> Dict[str, str]:
    """返回 {相对仓库根的路径: 内容}。"""
    outputs: Dict[str, str] = {
        "mindmaps/root_tree.md": render_root_tree_page(dataset),
        "mindmaps/associate_graph.md": render_associate_page(dataset),
    }
    for level in LEVELS:
        outputs["levels/{0}.md".format(level)] = render_level_page(level, dataset)
    return outputs


def clear_generated(directory: Path) -> int:
    """清空目录下旧的生成文件（保留 .gitkeep 等非 md 文件）。"""
    if not directory.is_dir():
        return 0
    removed = 0
    for path in sorted(directory.glob("*.md")):
        path.unlink()
        removed += 1
    return removed


def write_outputs(outputs: Dict[str, str], repo_root: Path) -> List[Path]:
    written: List[Path] = []
    for relative, text in sorted(outputs.items()):
        path = repo_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        written.append(path)
    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    global _QUIET

    parser = argparse.ArgumentParser(description="生成 es-raiz-vocab 静态 markdown 产物（不启动 web 服务）")
    parser.add_argument("--check", action="store_true", help="只校验 data/*.yaml，不写任何文件")
    parser.add_argument("--dry-run", action="store_true", help="渲染并打印统计，但不写文件、不清理旧产物")
    parser.add_argument("--data", type=Path, default=REPO_ROOT / "data", help="数据目录")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT, help="仓库根目录（产物写到这里）")
    parser.add_argument("--quiet", action="store_true", help="不打印处理日志")
    args = parser.parse_args(argv)

    _QUIET = args.quiet

    log("读取数据：{0}".format(args.data))
    errors: List[str] = []
    scan_raw(args.data, errors)

    dataset: Optional[Dataset] = None
    try:
        dataset = load_dataset(args.data)
    except DataError as exc:
        errors.append(str(exc))

    if dataset is not None:
        errors.extend(validate(dataset))

    if errors:
        sys.stderr.write("数据校验失败：\n")
        for error in errors:
            sys.stderr.write("  - {0}\n".format(error))
        return 2

    assert dataset is not None
    for message in collect_warnings(dataset):
        warn(message)

    levels = word_levels(dataset)
    log(
        "词根 {0} · 单词 {1} · 词缀 {2} · 关系 {3}".format(
            len(dataset.raices), len(levels), len(dataset.afijos), len(dataset.relations)
        )
    )
    for level in LEVELS:
        count = sum(1 for value in levels.values() if value == level)
        log("  {0}: {1} 个".format(level, count))

    if args.check:
        log("--check：校验通过，未写文件")
        return 0

    outputs = render_outputs(dataset)

    if args.dry_run:
        for relative, text in sorted(outputs.items()):
            log("dry-run：{0}（{1} 字符）".format(relative, len(text)))
        log("--dry-run：未写文件")
        return 0

    repo_root = args.repo.resolve()
    for folder in ("mindmaps", "levels"):
        removed = clear_generated(repo_root / folder)
        log("清理 {0}/：删除 {1} 个旧文件".format(folder, removed))

    for path in write_outputs(outputs, repo_root):
        log("写入 {0}".format(path.relative_to(repo_root)))

    log("完成：共 {0} 个 markdown 文件".format(len(outputs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
