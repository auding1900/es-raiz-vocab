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
        ("acaso", "adv."), ("apenas", "adv."), ("enseguida", "adv."),
        ("despacio", "adv."), ("arriba", "adv."), ("abajo", "adv."),
        ("dentro", "adv."), ("fuera", "adv."), ("delante", "adv."),
        ("detrás", "adv."), ("cerca", "adv."), ("lejos", "adv."),
        ("encima", "adv."), ("debajo", "adv."), ("junto", "adv."),
        ("quizás", "adv."), ("tras", "prep."),
        ("alcalde", "s.m."), ("azotea", "s.f."), ("algodón", "s.m."),
        ("berenjena", "s.f."), ("azafrán", "s.m."), ("azulejo", "s.m."),
        ("acequia", "s.f."), ("aljibe", "s.m."), ("tarea", "s.f."),
        ("marfil", "s.m."), ("rincón", "s.m."), ("jardín", "s.m."),
        ("banco", "s.m."), ("sala", "s.f."), ("banda", "s.f."),
        ("marrón", "adj."), ("fresco", "adj."), ("rico", "adj."),
        ("guardar", "v."), ("guiar", "v."), ("robar", "v."),
        ("despertar", "v."), ("sentar", "v."), ("acostar", "v."),
        ("escoger", "v."), ("arrancar", "v."), ("aguantar", "v."),
        ("quejarse", "v."), ("sonreír", "v."),
    ],
    "B1": [
        ("álgebra", "s.f."), ("algoritmo", "s.m."), ("alquimia", "s.f."),
        ("almanaque", "s.m."), ("arancel", "s.m."), ("jarabe", "s.m."),
        ("elixir", "s.m."), ("azahar", "s.m."), ("alcázar", "s.m."),
        ("alcoba", "s.f."), ("alfarero", "s.m."), ("tahona", "s.f."),
        ("espía", "s.m."), ("guardia", "s.f."), ("ganso", "s.m."),
        ("orgullo", "s.m."), ("esgrima", "s.f."), ("tregua", "s.f."),
        ("brindis", "s.m."), ("alarde", "s.m."),
        ("averiguar", "v."), ("aprovechar", "v."), ("apretar", "v."),
        ("arrepentirse", "v."), ("atreverse", "v."), ("ahorrar", "v."),
    ],
    "B2": [
        ("alarido", "s.m."), ("albricias", "s.f."), ("algazara", "s.f."),
        ("acecho", "s.m."), ("heráldica", "s.f."), ("jarana", "s.f."),
        ("alambique", "s.m."), ("alcancía", "s.f."), ("alcaparra", "s.f."),
        ("azar", "s.m."), ("alfiler", "s.m."), ("alicates", "s.m."),
        ("argamasa", "s.f."), ("escarnio", "s.m."),
        ("acechar", "v."), ("alardear", "v."), ("zaherir", "v."),
    ],
    "C1": [
        ("abolengo", "s.m."), ("alcurnia", "s.f."), ("aguinaldo", "s.m."),
        ("atalaya", "s.f."), ("alcaide", "s.m."), ("alguacil", "s.m."),
        ("alférez", "s.m."), ("alfanje", "s.m."), ("adarga", "s.f."),
        ("ajuar", "s.m."), ("aceña", "s.f."), ("alminar", "s.m."),
        ("aljófar", "s.m."), ("yelmo", "s.m."), ("heraldo", "s.m."),
        ("hidalgo", "s.m."), ("chabacano", "adj."), ("gótico", "adj."),
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
    words = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        word = nfc(line.strip().lower())
        if word and not word.startswith("#"):
            words.add(word)
    return words


def build(extra: set) -> Dict[str, List[Tuple[str, str]]]:
    blocked = repo_blacklist() | extra
    result: Dict[str, List[Tuple[str, str]]] = {}
    for level in LEVELS:
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


def render(groups: Dict[str, List[Tuple[str, str]]]) -> str:
    lines = [
        "<!-- 由 scripts/build_no_raiz.py 自动生成，请勿手工编辑 -->",
        "",
        "# no-raiz-vocab",
        "",
        "无法用拉丁词根拆解、与词根导图互补的高频词；只保留西语单词与 CEFR 等级，不含释义与例句。",
        "",
    ]
    for level in LEVELS:
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
    parser.add_argument("--blacklist", type=Path, default=None, help="追加黑名单文件（每行一个词）")
    args = parser.parse_args(argv)

    extra = load_extra_blacklist(args.blacklist) if args.blacklist else set()
    groups = build(extra)

    total = 0
    for level in LEVELS:
        total += len(groups[level])
        print("{0}: {1}".format(level, len(groups[level])))
    print("total: {0}".format(total))

    if args.dry_run:
        return 0

    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(render(groups))
    print("written: {0}".format(OUTPUT.relative_to(REPO_ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
