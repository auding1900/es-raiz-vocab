#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成附属文档 no-raiz-vocab.md：只收录无法用拉丁词根拆解的高频词。

用法：
    python scripts/build_no_raiz.py            # 生成并写盘
    python scripts/build_no_raiz.py --dry-run   # 只打印统计
    python scripts/build_no_raiz.py --blacklist extra.txt  # 追加黑名单（每行一个词）

约束：
- 不输出释义、例句、链接、mermaid；
- 自动黑名单：data/relations.yaml 中出现过的所有单词与词根 id 一律剔除；
- 只按 CEFR 等级分段，条目格式为 `- palabra (pos.)`。
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("缺少依赖 PyYAML，请先执行：pip install pyyaml\n")
    raise

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "no-raiz-vocab.md"
LEVELS: Tuple[str, ...] = ("A1", "A2", "B1", "B2", "C1", "C2")

# level -> [("palabra", "pos.")]
# 入选依据（仅四类）：① 西语原生词 ② 功能词 ③ 阿拉伯 / 日耳曼借词 ④ 词根失效的高频不规则动词
CANDIDATES: Dict[str, List[Tuple[str, str]]] = {
    "A1": [
        # 人称代词
        ("yo", "pron."), ("tú", "pron."), ("él", "pron."), ("ella", "pron."),
        ("nosotros", "pron."), ("vosotros", "pron."), ("ellos", "pron."),
        ("me", "pron."), ("te", "pron."), ("se", "pron."), ("nos", "pron."),
        ("os", "pron."), ("le", "pron."), ("les", "pron."), ("mi", "pron."),
        ("tu", "pron."), ("su", "pron."), ("nuestro", "pron."), ("vuestro", "pron."),
        # 介词
        ("de", "prep."), ("en", "prep."), ("con", "prep."), ("por", "prep."),
        ("para", "prep."), ("sin", "prep."), ("sobre", "prep."), ("entre", "prep."),
        ("hasta", "prep."), ("desde", "prep."), ("contra", "prep."),
        ("según", "prep."), ("hacia", "prep."),
        # 连词
        ("y", "conj."), ("o", "conj."), ("pero", "conj."), ("sino", "conj."),
        ("porque", "conj."), ("cuando", "conj."), ("donde", "conj."),
        ("como", "conj."), ("si", "conj."), ("que", "conj."), ("ni", "conj."),
        ("aunque", "conj."), ("pues", "conj."),
        # 基础副词
        ("no", "adv."), ("muy", "adv."), ("más", "adv."), ("menos", "adv."),
        ("también", "adv."), ("tampoco", "adv."), ("aquí", "adv."),
        ("allí", "adv."), ("ahora", "adv."), ("hoy", "adv."), ("ayer", "adv."),
        ("siempre", "adv."), ("nunca", "adv."), ("ya", "adv."),
        ("todavía", "adv."), ("después", "adv."), ("antes", "adv."),
        ("bien", "adv."), ("mal", "adv."), ("así", "adv."), ("casi", "adv."),
        ("tan", "adv."), ("tanto", "adv."), ("bastante", "adv."),
        ("demasiado", "adv."), ("quizá", "adv."), ("entonces", "adv."),
        ("luego", "adv."), ("además", "adv."), ("solo", "adv."),
        # 原生词 / 借词
        ("agua", "s.f."), ("perro", "s.m."), ("barro", "s.m."),
        ("cerveza", "s.f."), ("camisa", "s.f."), ("lanza", "s.f."),
        ("conejo", "s.m."), ("sapo", "s.m."), ("vega", "s.f."),
        ("izquierda", "s.f."), ("guante", "s.m."), ("falda", "s.f."),
        ("saco", "s.m."), ("ropa", "s.f."), ("aceite", "s.m."),
        ("azúcar", "s.m."), ("naranja", "s.f."), ("limón", "s.m."),
        ("arroz", "s.m."), ("aceituna", "s.f."), ("aldea", "s.f."),
        ("almohada", "s.f."), ("alfombra", "s.f."), ("barrio", "s.m."),
        ("zanahoria", "s.f."), ("aduana", "s.f."), ("tarifa", "s.f."),
        ("almacén", "s.m."), ("alquiler", "s.m."), ("albañil", "s.m."),
        ("alcohol", "s.m."), ("ajedrez", "s.m."),
        ("blanco", "adj."), ("gris", "adj."), ("azul", "adj."),
        ("ojalá", "interj."),
        # 词根失效的高频不规则动词
        ("ser", "v."), ("ir", "v."), ("haber", "v."), ("saber", "v."),
        ("andar", "v."), ("jugar", "v."), ("dormir", "v."), ("pedir", "v."),
        ("morir", "v."), ("nacer", "v."), ("caer", "v."), ("reír", "v."),
        ("cubrir", "v."), ("subir", "v."), ("vivir", "v."), ("beber", "v."),
        ("comer", "v."), ("mentir", "v."), ("servir", "v."), ("vestir", "v."),
        ("seguir", "v."), ("conocer", "v."), ("parecer", "v."), ("ofrecer", "v."),
        ("romper", "v."), ("volver", "v."), ("llover", "v."), ("encender", "v."),
        ("perder", "v."), ("entender", "v."), ("defender", "v."),
        ("responder", "v."), ("esconder", "v."), ("deber", "v."),
        ("oler", "v."), ("salir", "v."),
    ],
    "A2": [
        # 基础副词 / 介词
        ("acaso", "adv."), ("apenas", "adv."), ("enseguida", "adv."),
        ("despacio", "adv."), ("arriba", "adv."), ("abajo", "adv."),
        ("dentro", "adv."), ("fuera", "adv."), ("delante", "adv."),
        ("detrás", "adv."), ("cerca", "adv."), ("lejos", "adv."),
        ("encima", "adv."), ("debajo", "adv."), ("junto", "adv."),
        ("quizás", "adv."), ("aun", "adv."), ("tal", "adv."),
        ("demás", "adv."), ("tras", "prep."),
        # 代词 / 限定词
        ("quien", "pron."), ("cual", "pron."), ("cuyo", "pron."),
        ("nada", "pron."), ("alguien", "pron."), ("nadie", "pron."),
        ("algo", "pron."), ("otro", "pron."), ("cada", "pron."),
        ("todo", "pron."), ("mismo", "pron."),
        # 阿拉伯借词
        ("alcalde", "s.m."), ("azotea", "s.f."), ("algodón", "s.m."),
        ("berenjena", "s.f."), ("azafrán", "s.m."), ("azulejo", "s.m."),
        ("acequia", "s.f."), ("aljibe", "s.m."), ("tarea", "s.f."),
        ("marfil", "s.m."), ("alcachofa", "s.f."), ("albaricoque", "s.m."),
        ("alubia", "s.f."), ("acelga", "s.f."), ("alacena", "s.f."),
        # 日耳曼借词
        ("rincón", "s.m."), ("jardín", "s.m."), ("banco", "s.m."),
        ("sala", "s.f."), ("banda", "s.f."),
        ("marrón", "adj."), ("fresco", "adj."), ("rico", "adj."),
        # 词根失效的不规则 / 高频动词
        ("guardar", "v."), ("guiar", "v."), ("robar", "v."),
        ("ganar", "v."), ("gastar", "v."), ("tocar", "v."),
        ("despertar", "v."), ("acostar", "v."), ("escoger", "v."),
        ("arrancar", "v."), ("aguantar", "v."), ("quejarse", "v."),
        ("sonreír", "v."), ("morder", "v."), ("nevar", "v."),
        ("toser", "v."), ("tener", "v."),
    ],
    "B1": [
        # 阿拉伯借词
        ("álgebra", "s.f."), ("algoritmo", "s.m."), ("alquimia", "s.f."),
        ("almanaque", "s.m."), ("arancel", "s.m."), ("jarabe", "s.m."),
        ("elixir", "s.m."), ("azahar", "s.m."), ("alcázar", "s.m."),
        ("alcoba", "s.f."), ("alfarero", "s.m."), ("tahona", "s.f."),
        ("alhaja", "s.f."), ("almoneda", "s.f."), ("almena", "s.f."),
        ("almirante", "s.m."), ("albarán", "s.m."), ("alféizar", "s.m."),
        ("albóndiga", "s.f."), ("azucena", "s.f."), ("albahaca", "s.f."),
        ("alhelí", "s.m."), ("jarra", "s.f."), ("taza", "s.f."),
        ("alarde", "s.m."),
        # 日耳曼借词
        ("espía", "s.m."), ("guardia", "s.f."), ("ganso", "s.m."),
        ("orgullo", "s.m."), ("esgrima", "s.f."), ("tregua", "s.f."),
        ("brindis", "s.m."), ("arpa", "s.f."), ("danza", "s.f."),
        ("galope", "s.m."), ("esquí", "s.m."), ("mariscal", "s.m."),
        ("banquete", "s.m."),
        # 伊比利亚 / 巴斯克底层词
        ("pizarra", "s.f."), ("boina", "s.f."), ("garra", "s.f."),
        ("cencerro", "s.m."),
        # 词根失效的动词
        ("ahorrar", "v."),
    ],
    "B2": [
        # 阿拉伯借词
        ("alarido", "s.m."), ("albricias", "s.f."), ("algazara", "s.f."),
        ("alambique", "s.m."), ("alcancía", "s.f."), ("alcaparra", "s.f."),
        ("azar", "s.m."), ("alfiler", "s.m."), ("alicates", "s.m."),
        ("alcatraz", "s.m."), ("albornoz", "s.m."), ("azogue", "s.m."),
        ("mezquino", "adj."), ("fulano", "s.m."), ("quiosco", "s.m."),
        ("rehén", "s.m."), ("zaguán", "s.m."), ("argamasa", "s.f."),
        ("jarana", "s.f."), ("alardear", "v."), ("zaherir", "v."),
        # 日耳曼 / 法兰克借词
        ("escarnio", "s.m."), ("galardón", "s.m."), ("espuela", "s.f."),
        ("estribo", "s.m."), ("grima", "s.f."), ("guisa", "s.f."),
        ("hucha", "s.f."), ("lozano", "adj."), ("toldo", "s.m."),
        ("toalla", "s.f."), ("guarecer", "v."),
        # 法兰西 / 伊比利亚底层词
        ("heráldica", "s.f."), ("zamarra", "s.f."), ("chaparro", "s.m."),
    ],
    "C1": [
        # 阿拉伯借词
        ("abolengo", "s.m."), ("alcurnia", "s.f."), ("aguinaldo", "s.m."),
        ("atalaya", "s.f."), ("alcaide", "s.m."), ("alguacil", "s.m."),
        ("alférez", "s.m."), ("alfanje", "s.m."), ("adarga", "s.f."),
        ("ajuar", "s.m."), ("aceña", "s.f."), ("alminar", "s.m."),
        ("aljófar", "s.m."), ("almuédano", "s.m."), ("aljama", "s.f."),
        ("azabache", "s.m."), ("aduar", "s.m."), ("arrayán", "s.m."),
        ("zurrón", "s.m."), ("alquería", "s.f."), ("algarada", "s.f."),
        ("algarabía", "s.f."), ("añil", "s.m."), ("maravedí", "s.m."),
        ("fanega", "s.f."), ("almogávar", "s.m."), ("adarve", "s.m."),
        # 日耳曼 / 法兰克借词
        ("yelmo", "s.m."), ("heraldo", "s.m."), ("hidalgo", "s.m."),
        ("gótico", "adj."), ("saya", "s.f."), ("randa", "s.f."),
        ("brío", "s.m."), ("esguince", "s.m."), ("hueste", "s.f."),
        ("arenga", "s.f."), ("feudo", "s.m."), ("vasallo", "s.m."),
        ("mesnada", "s.f."),
        # 巴斯克底层词
        ("aquelarre", "s.m."), ("chabacano", "adj."),
    ],
    "C2": [
        ("antaño", "adv."), ("otrora", "adv."), ("hogaño", "adv."),
        ("allende", "adv."), ("asaz", "adv."), ("empero", "conj."),
        ("maguer", "conj."),
        ("alfeñique", "s.m."), ("almíbar", "s.m."), ("badulaque", "s.m."),
        ("botarate", "s.m."), ("cenutrio", "s.m."), ("zopenco", "s.m."),
        ("hidalguía", "s.f."), ("aljaba", "s.f."), ("alcayata", "s.f."),
        ("rufián", "s.m."), ("baldío", "adj."),
    ],
}


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def repo_blacklist() -> set:
    """词根 id + 关系文件里出现过的所有单词。"""
    blocked = set()
    raices_path = REPO_ROOT / "data" / "raices.yaml"
    relations_path = REPO_ROOT / "data" / "relations.yaml"
    if raices_path.exists():
        data = yaml.safe_load(raices_path.read_text(encoding="utf-8")) or {}
        for item in data.get("raices", []) or []:
            for key in ("id", "root_name"):
                if item.get(key):
                    blocked.add(nfc(str(item[key]).strip().lower()))
    if relations_path.exists():
        data = yaml.safe_load(relations_path.read_text(encoding="utf-8")) or {}
        for item in data.get("relations", []) or []:
            for key in ("source", "target"):
                if item.get(key):
                    blocked.add(nfc(str(item[key]).strip().lower()))
    return blocked


def load_extra_blacklist(path: Path) -> set:
    """支持两种格式：每行一个词，或 yaml 片段的 palabras / nivel 列表。"""
    words = set()
    text = path.read_text(encoding="utf-8")
    if "palabras:" in text:
        data = yaml.safe_load(text) or {}
        items = data.get("palabras") or []
        for item in items:
            if isinstance(item, str) and item.strip():
                words.add(nfc(item.strip().lower()))
        return words
    for line in text.splitlines():
        word = nfc(line.strip().lower())
        if word and not word.startswith("#"):
            words.add(word)
    return words


def build(extra: set, levels: Sequence[str] = LEVELS) -> Dict[str, List[Tuple[str, str]]]:
    blocked = repo_blacklist() | extra
    result: Dict[str, List[Tuple[str, str]]] = {}
    for level in levels:
        kept: List[Tuple[str, str]] = []
        seen = set()
        for word, pos in CANDIDATES.get(level, []):
            key = nfc(word.strip().lower())
            if key in blocked or key in seen:
                continue
            seen.add(key)
            kept.append((word, pos))
        result[level] = kept
    return result


LEVEL_ALIASES = {"a1": "A1", "a2": "A2", "b1": "B1", "b2": "B2", "c1": "C1", "c2": "C2"}


def parse_levels(raw: Optional[str]) -> Sequence[str]:
    if not raw:
        return LEVELS
    picked: List[str] = []
    for token in raw.replace(" ", "").split(","):
        if not token:
            continue
        level = LEVEL_ALIASES.get(token.lower())
        if level is None:
            raise SystemExit("等级非法：{0}（可选 A1/A2/B1/B2/C1/C2）".format(token))
        if level not in picked:
            picked.append(level)
    return tuple(picked) or LEVELS


def render_yaml(groups: Dict[str, List[Tuple[str, str]]], levels: Sequence[str]) -> str:
    """用于后续批量挂载豆包链接的片段：只有等级与单词，不含任何释义。"""
    lines: List[str] = []
    for level in levels:
        if len(levels) == 1:
            lines.append("nivel: {0}".format(level))
            lines.append("palabras:")
            for word, _ in groups[level]:
                lines.append("  - {0}".format(word))
        else:
            lines.append("{0}:".format(level.lower()))
            for word, _ in groups[level]:
                lines.append("  - {0}".format(word))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render(groups: Dict[str, List[Tuple[str, str]]], levels: Sequence[str] = LEVELS) -> str:
    lines = [
        "<!-- 由 scripts/build_no_raiz.py 自动生成，请勿手工编辑 -->",
        "",
        "# no-raiz-vocab",
        "",
        "无法用拉丁词根拆解、与词根导图互补的高频词；只保留西语单词与 CEFR 等级，不含释义与例句。",
        "",
    ]
    for level in levels:
        lines.append("### {0}".format(level))
        lines.append("")
        for word, pos in groups[level]:
            lines.append("- {0} ({1})".format(word, pos))
        if not groups[level]:
            lines.append("- （暂无）")
        lines.append("")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="生成 no-raiz-vocab.md")
    parser.add_argument("--dry-run", action="store_true", help="只打印统计，不写盘")
    parser.add_argument("--blacklist", type=Path, default=None, help="追加黑名单文件（每行一个词，或 yaml 片段的 palabras）")
    parser.add_argument("--exclude", type=Path, action="append", default=None, help="排除已生成的批次片段（可多次指定）")
    parser.add_argument("--levels", default=None, help="只输出指定等级，逗号分隔，如 A1 或 A1,A2")
    parser.add_argument("--yaml", type=Path, default=None, help="同时输出 YAML 单词片段（不含释义）")
    parser.add_argument("--no-md", action="store_true", help="不写 no-raiz-vocab.md")
    args = parser.parse_args(argv)

    levels = parse_levels(args.levels)
    extra = load_extra_blacklist(args.blacklist) if args.blacklist else set()
    for path in args.exclude or []:
        extra |= load_extra_blacklist(path)
    groups = build(extra, levels)

    total = 0
    for level in levels:
        total += len(groups[level])
        print("{0}: {1}".format(level, len(groups[level])))
    print("total: {0}".format(total))

    if args.dry_run:
        return 0

    if args.yaml:
        with args.yaml.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(render_yaml(groups, levels))
        print("written: {0}".format(args.yaml))

    if args.no_md:
        return 0

    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(render(groups, LEVELS if tuple(LEVELS) == tuple(levels) else levels))
    print("written: {0}".format(OUTPUT.relative_to(REPO_ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
