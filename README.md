# es-raiz-vocab

> **西班牙语词根词族 & 联想思维导图｜A1–C2 分级标记，仅存储词语关联关系，点击单词跳转豆包查询释义、搭配、近义词辨析以及公版来源例句。**

仓库里没有词条正文，只有一张可扩展的**关系图**：词根、单词、派生 / 联想 / 易混关系、CEFR 级别标签，以及词根的拉丁本源。所有释义、搭配、例句与辨析都由豆包在点击后实时生成。

```bash
# 三条命令跑起来（Python 3.9+）
python3 -m venv .env && source .env/bin/activate     # Windows: .env\Scripts\activate
pip install pyyaml
python3 scripts/generate_mermaid.py                   # 产物写入 mindmaps/ 与 levels/
```

---

## 1. 项目原理

### 1.1 为什么仓库不内置释义和例句

- **规避版权风险**：词典释义、例句、译文通常属于受版权保护的汇编内容，仓库不复制、不转述、不缓存。
- **避免数据过期**：词义与用法会随语料、教学标准变化，静态副本很快失真；实时查询永远是最新的一次生成结果。
- **边界清晰**：本仓库只负责「结构与关系」这一层，内容由豆包按统一模板产出，责任边界一目了然。

### 1.2 点击之后发生了什么

1. 每个单词节点的链接里内嵌一段固定 prompt，形如 `https://www.doubao.com/chat?q=<URL 编码后的 prompt>`；
2. prompt 中的 `{word}` 替换为单词词形、`{root}` 替换为该词所属词根；
3. 豆包按模板返回：词义、DELE 等级、语体、常用搭配、近义词辨析；
4. 例句**优先取自 Wikisource、古登堡计划等公版西语文本**；现代标准西班牙语优先，古体表达会标注【arcaísmo】；
5. 仓库不保存、不缓存、不复述任何返回内容。

### 1.3 三条硬约束（脚本会校验）

| 约束 | 说明 |
| --- | --- |
| 不存释义 | 数据文件里出现 `definition` / `translation` 等字段或中文值 → 校验报错 |
| 不存例句 | 例句只在豆包侧生成，仓库里没有一句西语例句 |
| 只存结构 | 词根、单词词形、关系类型、CEFR 级别、词根拉丁本源 |

---

## 2. 使用教程

### 2.1 本地 VSCode 预览导图

1. 用 VSCode 打开本文件夹；
2. 安装 Markdown 的 Mermaid 预览支持（扩展市场搜索 `Markdown Preview Mermaid Support`；较新的 VS Code 版本 Markdown 预览可能已内置 Mermaid 渲染）；
3. 打开 [`mindmaps/root_tree.md`](mindmaps/root_tree.md)，按 `Cmd/Ctrl + Shift + V` 打开预览；
4. 联想 / 易混关系看 [`mindmaps/associate_graph.md`](mindmaps/associate_graph.md)，分级清单看 [`levels/`](levels)。

也可以直接在 GitHub 上浏览，GitHub 原生渲染 Mermaid。

### 2.2 点击单词跳转豆包

- 在支持 `click` 交互的渲染器里，**直接点单词节点**即可打开豆包网页版，问题已经带好；
- GitHub 以及部分编辑器预览出于安全策略会忽略 mermaid 的 `click`：此时用同页底部的**「单词链接表」**，或打开 [`levels/A1.md`](levels/A1.md) … [`levels/C2.md`](levels/C2.md) 点每行的「豆包」；
- 节点配色代表级别（A1 绿 → C2 红），灰底表示尚未标注级别。

### 2.3 断网时能做什么

| 能看 | 不能看 |
| --- | --- |
| 词根树、派生链、联想与易混关系、级别标签、链接地址本身 | 词义、语体、搭配、近义词辨析、例句 |

结构完全静态（Mermaid 文本 + Markdown 表格），断网照常渲染；只有跳转豆包那一步需要网络。

---

## 3. 目录结构

```
es-raiz-vocab/
├── README.md
├── LICENSE
├── data/
│   ├── raices.yaml      # 词根节点：id / root_name / latin_origin
│   ├── afijos.yaml      # 词缀节点：id / affix / meaning / type
│   └── relations.yaml   # 关系边：source / target / rel_type / cefr_level / prompt_template
├── scripts/
│   └── generate_mermaid.py   # 读取 yaml，渲染 mindmaps/ 与 levels/ 下的静态 md
├── mindmaps/            # 产物：root_tree.md（词根树） + associate_graph.md（联想网状图）
└── levels/              # 产物：A1.md ~ C2.md 分级清单
```

`mindmaps/`、`levels/` 下的 `.md` 全部由脚本生成，**请勿手工编辑**；每次生成都会先清空这两个目录下的旧 `.md`。

---

## 4. 数据格式

三份 yaml 字段名固定，脚本按白名单校验：**多写、少写、拼错都会报错**。

### 4.1 `data/raices.yaml` —— 词根节点

```yaml
version: 2

raices:
  - id: duc
    root_name: duc
    latin_origin: "ducere (to lead)"
```

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `id` | 是 | 词根唯一标识，同时用于节点 id |
| `root_name` | 是 | 词根书写形式（不含连字符） |
| `latin_origin` | 是 | 拉丁本源：拉丁词形 + 本义（英文短注），**不是单词释义** |

本文件不列单词——单词统一在关系文件的 `target` 处声明。

### 4.2 `data/afijos.yaml` —— 词缀节点

```yaml
afijos:
  - id: "re-"
    affix: "re-"
    meaning: "again; back"
    type: prefix
```

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `id` | 是 | 唯一标识 |
| `affix` | 是 | 词缀写法：前缀以 `-` 结尾，后缀以 `-` 开头 |
| `meaning` | 是 | 词缀自身的构词功能（英文短注），**不是单词释义** |
| `type` | 是 | `prefix` / `suffix` |

### 4.3 `data/relations.yaml` —— 关系边（兼单词声明处）

```yaml
relations:
  - source: duc
    target: conducir
    rel_type: derivar
    cefr_level: A1
    prompt_template: null

  - source: reducir
    target: mermar
    rel_type: asociar
    cefr_level: null
    prompt_template: null
```

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `source` | 是 | 起点：词根 `id`，或已在本文件出现过的单词 |
| `target` | 是 | 终点：单词词形（不能是词根 id） |
| `rel_type` | 是 | `derivar` / `asociar` / `confundir` |
| `cefr_level` | 否 | `A1`–`C2`，未标注写 `null` |
| `prompt_template` | 否 | 单条关系覆盖模板，变量 `{word}` `{root}`；`null` = 用默认模板 |

单词节点在 `target` 处声明，级别挂在派生边上，同一份数据不需要两处维护。

---

## 5. 生成产物与图例

| 产物 | 内容 |
| --- | --- |
| [`mindmaps/root_tree.md`](mindmaps/root_tree.md) | `graph LR` 词根树：词根节点显示 `root_name` + `latin_origin`，单词节点显示 `单词` + 级别，全部单词节点带豆包 `click` |
| [`mindmaps/associate_graph.md`](mindmaps/associate_graph.md) | 只含 `asociar` + `confundir` 的联想网状图 |
| [`levels/A1.md`](levels/A1.md) … [`levels/C2.md`](levels/C2.md) | 分级清单，每行 `单词 \| 词根 \| 豆包` |

关系类型与线型：

| 关系 | 含义 | 线型 |
| --- | --- | --- |
| `derivar` | 词根派生 | 实线黑色 `-->` |
| `asociar` | 同义 / 语义联想（可跨词族） | 虚线 `#4488bb` `-.->` |
| `confundir` | 形近易混（可跨词族） | 虚线 `#dd4444` `-.->` |

节点配色：A1 `#e8f5e9` → A2 `#c8e6c9` → B1 `#fff8e1` → B2 `#ffe0b2` → C1 `#ffccbc` → C2 `#ffcdd2`；未标注级别为灰色 `#f5f5f5`；词根为蓝色 `#bbdefb`。

---

## 6. 本地部署与生成

### 6.1 安装依赖

```bash
python3 -m venv .env
source .env/bin/activate          # Windows: .env\Scripts\activate
python3 -m pip install pyyaml
```

唯一第三方依赖是 `pyyaml`；脚本只读写本地文件，不启动 web 服务、不联网。

### 6.2 生成命令

```bash
# 只校验数据源（不写任何文件）
python3 scripts/generate_mermaid.py --check

# 渲染并写盘（先清空 mindmaps/、levels/ 下的旧 md）
python3 scripts/generate_mermaid.py

# 只看会输出哪些文件
python3 scripts/generate_mermaid.py --dry-run

# 静默
python3 scripts/generate_mermaid.py --quiet
```

其他参数：`--data <目录>` 指定数据目录，`--repo <目录>` 指定产物根目录（默认当前仓库）。

---

## 7. 不想点链接？复制模板手动查询

把下面这段整体复制到豆包对话框，按需替换 `{word}` 与 `{root}` 即可得到与点链接完全一致的回答：

```text
西班牙语{word}，词根{root}，解释词义、DELE等级、语体、常用搭配、近义词辨析，并且给2条来自公版西语文本（Wikisource/古登堡）的自然例句，例句优先选用现代标准西班牙语，古体例句标注【arcaísmo】
```

- `{word}` 填单词词形（重音符号照写，如 `mañana`、`canción`）；
- `{root}` 填该词所属词根 id（如 `duc`）；**若该词没有绑定词根，把「词根{root}，」这一小段整体删掉**，避免出现「词根，」这种残句；
- 生成器里的默认模板与查询入口是 `scripts/generate_mermaid.py` 顶部的 `PROMPT_TEMPLATE`、`DOUBAO_URL` 两个常量，改完重新生成即可。

---

## 8. 贡献指南

### 8.1 PR 只接受这四类改动

| ✅ 可以提交 | 说明 |
| --- | --- |
| 新增词根 | 在 `data/raices.yaml` 加一条 `id` / `root_name` / `latin_origin` |
| 新增单词 | 在 `data/relations.yaml` 里作为 `target` 出现 |
| 新增关联关系 | `derivar` / `asociar` / `confundir` 边 |
| CEFR 级别标签 | `cefr_level` 字段 |

### 8.2 ❌ 明确禁止

- **任何中文释义、词典文本、译文**；
- **任何例句**（包括你自己写的、从教材抄的、从公版书摘的）；
- 近义词辨析文字、语体说明、搭配清单；
- 与「单词」无关的图片、PDF、语料文件。

> 这些内容一律由豆包在查询时生成。PR 里出现上述内容会被直接关闭，不需要讨论。

### 8.3 提交前必须保证 yaml 合法

```bash
# 1. 语法 + 字段白名单 + 关系完整性 + 中文/释义检测
python3 scripts/generate_mermaid.py --check

# 2. 重新生成产物，和 data 一起提交
python3 scripts/generate_mermaid.py
```

`--check` 覆盖：YAML 语法、字段白名单（多写/少写/拼错）、`cefr_level` 枚举、`rel_type` 枚举、关系端点是否存在、`target` 不能是词根 id、重复边、自环、`prompt_template` 占位符、中文值检测、节点 id 冲突。

### 8.4 自查清单

**数据层面**

1. 词根 `id` 唯一、全小写、只含 `a-z0-9_-`；`latin_origin` 写「拉丁词形 + 本义」英文短注；
2. 词缀 `type` 只能是 `prefix` / `suffix`；`meaning` 是词缀功能，不是单词释义；
3. 单词只作为 `target` 出现，重音照写（`ñ á é í ó ú`），不另建单词表；
4. `cefr_level` 取 `A1/A2/B1/B2/C1/C2` 或 `null`；`null` 的词只出现在导图，**不进分级页**；
5. `source` 必须是词根 `id`，或已作为 `target` 出现过的单词；
6. 同一 `(source, target, rel_type)` 不重复；`source == target` 不允许；
7. 中文只允许出现在 `prompt_template`，其他字段一律英文/西语；
8. 两个词形折叠后 id 相同（如 `educación` 与 `educacion`）会报错，需改名或改用别的写法。

**流程层面**

9. 先 `--check` 再正式生成；
10. 产物目录每次清空重建，不要在里面放手工文件；`data/` 与 `mindmaps/`、`levels/` 一起提交；
11. 生成后抽查三点：新词是否出现在 `root_tree.md`、级别是否落入正确的 `levels/<级别>.md`、点开豆包看 query 里的单词与词根是否对应。

---

## 9. 定级声明

- 仓库里的 CEFR 级别（A1–C2）是**基于常见教学经验的参考坐标**，用于给词族分层、安排学习顺序，**不是 DELE 官方词表**；
- 本项目与 Instituto Cervantes / DELE 考试机构**没有任何隶属或授权关系**；
- 同一单词在不同教材、不同地区语料中的级别判定可能不同，请以官方大纲或你所用教材为准；
- 级别只挂在 `relations.yaml` 的派生边上；未标注（`null`）的单词不会出现在 `levels/` 页面。

---

## 10. 开源协议

本项目以 [MIT License](LICENSE) 授权，可自由使用、修改、分发，请保留版权声明。

仓库**仅包含单词关系图谱**（词根、词形、关系、级别、拉丁词源），**不含任何词典内容**：不提供释义、例句、译文或中文解释。释义、例句、辨析请使用页内豆包链接，由豆包实时生成，生成结果与本仓库无关，请自行核对来源。单词词形与拉丁词源属公共语言事实；若你认为某处内容侵权，请开 issue，我们会移除。
