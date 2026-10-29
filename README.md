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
├── CHANGELOG.md
├── LICENSE
├── data/
│   ├── raices.yaml      # 词根节点：id / root_name / latin_origin / batch
│   ├── afijos.yaml      # 词缀节点：id / affix / meaning / type
│   └── relations.yaml   # 关系边：source / target / rel_type / cefr_level / prompt_template
├── scripts/
│   └── generate_mermaid.py   # 读取 yaml，渲染 mindmaps/ 与 levels/ 下的静态 md
├── mindmaps/            # 产物：root_tree.md（索引）+ raiz_<批次>_<词根>.md（一词根一文件一图）
│                        #       + associate_graph.md（联想索引）+ asociar_*.md / confundir_*.md
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

  - id: pac
    root_name: pac
    latin_origin: "pax, pacis (peace)"
    batch: b9
```

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `id` | 是 | 词根唯一标识，同时用于节点 id 与文件名 |
| `root_name` | 是 | 词根书写形式（不含连字符） |
| `latin_origin` | 是 | 拉丁本源：拉丁词形 + 本义（英文短注），**不是单词释义** |
| `batch` | 否 | 批次号（`b9`、`c1` …），决定文件名 `raiz_<batch>_<id>.md` 与索引分组；省略则归入 `v0` |

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
| [`mindmaps/root_tree.md`](mindmaps/root_tree.md) | 词根索引：按批次分组，列出每个词根的单词数 / 关系数并链接到各自的导图页，**本页不含图** |
| `mindmaps/raiz_<批次>_<词根>.md`（如 [`raiz_b9_pac.md`](mindmaps/raiz_b9_pac.md)） | **一个词根一个文件、一张图**：`graph LR`，词根节点显示 `root_name` + `latin_origin`，单词节点显示 `单词` + 级别，全部单词节点带豆包 `click`，页末附本族单词链接表 |
| [`mindmaps/raiz_sin_raiz.md`](mindmaps/raiz_sin_raiz.md) | 尚未归入任何词根的联想 / 易混单词 |
| [`mindmaps/associate_graph.md`](mindmaps/associate_graph.md) | 联想网状图索引：分块导航 + 全部 `asociar` / `confundir` 关系清单 |
| `mindmaps/asociar_*.md` / `mindmaps/confundir_*.md` | 联想 / 易混的单个分块页，一块一图（超 25000 字符按词根首字母拆，仍超则按 8 条关系切片） |
| [`levels/A1.md`](levels/A1.md) … [`levels/C2.md`](levels/C2.md) | 分级清单，每行 `单词 \| 词根 \| 豆包` |

关系类型与线型：

| 关系 | 含义 | 线型 |
| --- | --- | --- |
| `derivar` | 词根派生 | 实线黑色 `-->` |
| `asociar` | 同义 / 语义联想（可跨词族） | 虚线 `#4488bb` `-.->` |
| `confundir` | 形近易混（可跨词族） | 虚线 `#dd4444` `-.->` |

节点配色：A1 `#e8f5e9` → A2 `#c8e6c9` → B1 `#fff8e1` → B2 `#ffe0b2` → C1 `#ffccbc` → C2 `#ffcdd2`；未标注级别为灰色 `#f5f5f5`；词根为蓝色 `#bbdefb`。

单图上限：mermaid 默认 `maxTextSize` 为 50000 字符，超过后 GitHub 只会显示 `Maximum text size in diagram exceeded`。因此**每个词根独立成页、一页一图**（B 批次 9 起文件名统一为 `raiz_<批次>_<词根>.md`，历史词根为 `raiz_v0_<词根>.md`）；联想图先按关系类型分开，超过 25000 字符时按词根首字母拆分，若单个分桶仍超限则再按 8 条关系切片，每个分块同样独立成文件；脚本对超过 45000 字符的单图会打印告警。

### 5.1 批次导图索引

新增词根的导图按批次归档，直接点开即可查看，也可在 [`mindmaps/root_tree.md`](mindmaps/root_tree.md) 查看完整索引（含 v0 历史词根）。

**B 批次 9 —— 和平与安宁（7 个词根 / 35 个单词）**

| 词根 | 拉丁本源 | 导图 | 派生单词 |
| --- | --- | --- | --- |
| `pac` | pax, pacis（和平） | [`raiz_b9_pac.md`](mindmaps/raiz_b9_pac.md) | paz, pacífico, pacificar, pacifismo, pacifista, apaciguar |
| `plac` | placere（取悦、平静） | [`raiz_b9_plac.md`](mindmaps/raiz_b9_plac.md) | placer, complacer, complaciente, placentero, plácido, implacable |
| `tranqu` | tranquillus（安宁） | [`raiz_b9_tranqu.md`](mindmaps/raiz_b9_tranqu.md) | tranquilo, tranquilidad, tranquilizar, tranquilizante, tranquilizador |
| `seren` | serenus（晴朗、平静） | [`raiz_b9_seren.md`](mindmaps/raiz_b9_seren.md) | sereno, serenidad, serenata, serenar |
| `quies` | quies, quietis（休息） | [`raiz_b9_quies.md`](mindmaps/raiz_b9_quies.md) | quieto, inquieto, inquietud, inquietante, quietud, aquietar |
| `paus` | pausa（停歇） | [`raiz_b9_paus.md`](mindmaps/raiz_b9_paus.md) | pausa, pausado, pausar, pausadamente |
| `sedat` | sedare（安抚） | [`raiz_b9_sedat.md`](mindmaps/raiz_b9_sedat.md) | sedante, sedar, sedación, sedativo |

**B 批次 10 —— 耕种、居住与城乡（6 个词根 / 32 个单词）**

| 词根 | 拉丁本源 | 导图 | 派生单词 |
| --- | --- | --- | --- |
| `col` | colere（耕种、培育） | [`raiz_b10_col.md`](mindmaps/raiz_b10_col.md) | cultura, cultivo, cultivar, cultural, colonia, colonial, colono, colonizar, inculto |
| `habit` | habitare（居住） | [`raiz_b10_habit.md`](mindmaps/raiz_b10_habit.md) | habitación, habitante, habitar, hábitat, habitable, inhabitable |
| `domic` | domus（家） | [`raiz_b10_domic.md`](mindmaps/raiz_b10_domic.md) | doméstico, domicilio, domesticar, domiciliario, domesticación |
| `urb` | urbs（城市） | [`raiz_b10_urb.md`](mindmaps/raiz_b10_urb.md) | urbano, urbanización, suburbio, urbanizar, urbanismo, urbanidad, interurbano |
| `rural` | ruralis（乡村） | [`raiz_b10_rural.md`](mindmaps/raiz_b10_rural.md) | ruralidad, rurícola |
| `incol` | incola（居民） | [`raiz_b10_incol.md`](mindmaps/raiz_b10_incol.md) | inquilino, inquilinato, íncola |

> 本批次未新增 `civ`（城邦）导图：该词根已在 v0 历史批次中。`rural` 词根与单词 rural 同名，故该词不单独声明节点。

**B 批次 11 —— 爱、憎、欲（7 个词根 / 36 个单词）**

| 词根 | 拉丁本源 | 导图 | 派生单词 |
| --- | --- | --- | --- |
| `car` | carus（珍贵、喜爱） | [`raiz_b11_car.md`](mindmaps/raiz_b11_car.md) | cariño, cariñoso, caridad, caritativo, carestía, encarecer |
| `am` | amare（爱） | [`raiz_b11_am.md`](mindmaps/raiz_b11_am.md) | amor, amar, amigo, amistad, amable, enamorar, enamorado, amante, amistoso |
| `dilect` | diligere（珍爱） | [`raiz_b11_dilect.md`](mindmaps/raiz_b11_dilect.md) | predilecto, predilección, diligente, diligencia, dilección |
| `od` | odisse（憎恨） | [`raiz_b11_od.md`](mindmaps/raiz_b11_od.md) | odio, odiar, odioso |
| `invid` | invidere（嫉妒） | [`raiz_b11_invid.md`](mindmaps/raiz_b11_invid.md) | envidia, envidiar, envidioso, envidiable |
| `cup` | cupere（渴望） | [`raiz_b11_cup.md`](mindmaps/raiz_b11_cup.md) | codicia, codiciar, codicioso, cupidez |
| `appet` | appetere（渴求） | [`raiz_b11_appet.md`](mindmaps/raiz_b11_appet.md) | apetito, apetecer, apetecible, apetitoso, inapetencia |

**B 批次 12 —— 移动、转向、改变（7 个词根 / 45 个单词）**

| 词根 | 拉丁本源 | 导图 | 单词 |
| --- | --- | --- | --- |
| `mov` | movere（移动） | [`raiz_b12_mov.md`](mindmaps/raiz_b12_mov.md) | 8 |
| `mot` | motus（运动） | [`raiz_b12_mot.md`](mindmaps/raiz_b12_mot.md) | 6 |
| `vers` | vertere（翻转、转向） | [`raiz_b12_vers.md`](mindmaps/raiz_b12_vers.md) | 7 |
| `vert` | versus（转变） | [`raiz_b12_vert.md`](mindmaps/raiz_b12_vert.md) | 7 |
| `mut` | mutare（改变） | [`raiz_b12_mut.md`](mindmaps/raiz_b12_mut.md) | 5 |
| `commut` | commutare（互换） | [`raiz_b12_commut.md`](mindmaps/raiz_b12_commut.md) | 4 |
| `vari` | varius（多样、变化） | [`raiz_b12_vari.md`](mindmaps/raiz_b12_vari.md) | 8 |

> `vari` 在 C 批次 2 中重复出现，统一在 B12 建档；具体词表见各导图页。

**B 批次 13 —— 光、暗与纯净（9 个词根 / 44 个单词）**

| 词根 | 拉丁本源 | 导图 | 单词 |
| --- | --- | --- | --- |
| `clar` | clarus（明亮、清晰） | [`raiz_b13_clar.md`](mindmaps/raiz_b13_clar.md) | 7 |
| `lumin` | lumen（光） | [`raiz_b13_lumin.md`](mindmaps/raiz_b13_lumin.md) | 5 |
| `luc` | lux（光线） | [`raiz_b13_luc.md`](mindmaps/raiz_b13_luc.md) | 6 |
| `splendor` | splendere（发光） | [`raiz_b13_splendor.md`](mindmaps/raiz_b13_splendor.md) | 5 |
| `teneb` | tenebrae（黑暗） | [`raiz_b13_teneb.md`](mindmaps/raiz_b13_teneb.md) | 2 |
| `obscur` | obscurus（昏暗） | [`raiz_b13_obscur.md`](mindmaps/raiz_b13_obscur.md) | 5 |
| `umbr` | umbra（阴影） | [`raiz_b13_umbr.md`](mindmaps/raiz_b13_umbr.md) | 5 |
| `pur` | purus（纯净） | [`raiz_b13_pur.md`](mindmaps/raiz_b13_pur.md) | 5 |
| `mund` | mundus（洁净、世界） | [`raiz_b13_mund.md`](mindmaps/raiz_b13_mund.md) | 4 |

**C 批次 1 —— 权柄、大地、生命（8 个希腊词根 / 50 个单词）**

| 词根 | 希腊本源 | 导图 | 单词 |
| --- | --- | --- | --- |
| `arch` | arkhe（统治、开端） | [`raiz_c1_arch.md`](mindmaps/raiz_c1_arch.md) | 7 |
| `crac` | kratos（权力） | [`raiz_c1_crac.md`](mindmaps/raiz_c1_crac.md) | 6 |
| `polis` | polis（城邦） | [`raiz_c1_polis.md`](mindmaps/raiz_c1_polis.md) | 6 |
| `anthrop` | anthropos（人类） | [`raiz_c1_anthrop.md`](mindmaps/raiz_c1_anthrop.md) | 5 |
| `geo` | ge（大地） | [`raiz_c1_geo.md`](mindmaps/raiz_c1_geo.md) | 6 |
| `bio` | bios（生命） | [`raiz_c1_bio.md`](mindmaps/raiz_c1_bio.md) | 7 |
| `psych` | psykhe（灵魂） | [`raiz_c1_psych.md`](mindmaps/raiz_c1_psych.md) | 6 |
| `log` | logos（言语、学科） | [`raiz_c1_log.md`](mindmaps/raiz_c1_log.md) | 7 |

**C 批次 2 —— 平等、相似、相异（7 个词根 / 34 个单词）**

| 词根 | 本源 | 导图 | 单词 |
| --- | --- | --- | --- |
| `aequ` | aequus（平等） | [`raiz_c2_aequ.md`](mindmaps/raiz_c2_aequ.md) | 4 |
| `equ` | aequare（使相等） | [`raiz_c2_equ.md`](mindmaps/raiz_c2_equ.md) | 3 |
| `par` | par（对等） | [`raiz_c2_par.md`](mindmaps/raiz_c2_par.md) | 6 |
| `sim` | similis（相似） | [`raiz_c2_sim.md`](mindmaps/raiz_c2_sim.md) | 7 |
| `id` | idem（同一） | [`raiz_c2_id.md`](mindmaps/raiz_c2_id.md) | 5 |
| `homo` | homos（相同） | [`raiz_c2_homo.md`](mindmaps/raiz_c2_homo.md) | 5 |
| `heter` | heteros（相异） | [`raiz_c2_heter.md`](mindmaps/raiz_c2_heter.md) | 4 |

> `vari` 已在 B 批次 12 建档，本批次不重复。`par` 词根与单词 par 同名，该词不单独声明节点。

**C 批次 3 —— 数量、新旧、首末（8 个词根 / 42 个单词）**

| 词根 | 拉丁本源 | 导图 | 单词 |
| --- | --- | --- | --- |
| `cent` | centum（百） | [`raiz_c3_cent.md`](mindmaps/raiz_c3_cent.md) | 6 |
| `mill` | mille（千） | [`raiz_c3_mill.md`](mindmaps/raiz_c3_mill.md) | 6 |
| `dec` | decem（十） | [`raiz_c3_dec.md`](mindmaps/raiz_c3_dec.md) | 6 |
| `sept` | septem（七） | [`raiz_c3_sept.md`](mindmaps/raiz_c3_sept.md) | 3 |
| `nov` | novus（新） | [`raiz_c3_nov.md`](mindmaps/raiz_c3_nov.md) | 7 |
| `vet` | vetus（旧） | [`raiz_c3_vet.md`](mindmaps/raiz_c3_vet.md) | 5 |
| `prim` | primus（第一） | [`raiz_c3_prim.md`](mindmaps/raiz_c3_prim.md) | 6 |
| `ult` | ultimus（最后） | [`raiz_c3_ult.md`](mindmaps/raiz_c3_ult.md) | 3 |

> `milenio` 已属 `ann`（annus）词族，本批次不重复。

**C 批次 4 —— 搭建、制造、建筑（8 个词根 / 42 个单词）**

| 词根 | 拉丁本源 | 导图 | 单词 |
| --- | --- | --- | --- |
| `struct` | struere（搭建、建造） | [`raiz_c4_struct.md`](mindmaps/raiz_c4_struct.md) | 7 |
| `fabric` | fabrica（制造） | [`raiz_c4_fabric.md`](mindmaps/raiz_c4_fabric.md) | 5 |
| `constru` | construere（构筑） | [`raiz_c4_constru.md`](mindmaps/raiz_c4_constru.md) | 6 |
| `mol` | moles（大块、工程） | [`raiz_c4_mol.md`](mindmaps/raiz_c4_mol.md) | 5 |
| `aed` | aedes（建筑） | [`raiz_c4_aed.md`](mindmaps/raiz_c4_aed.md) | 4 |
| `tect` | tegere（覆盖、屋顶） | [`raiz_c4_tect.md`](mindmaps/raiz_c4_tect.md) | 7 |
| `mur` | murus（墙壁） | [`raiz_c4_mur.md`](mindmaps/raiz_c4_mur.md) | 4 |
| `pont` | pons（桥梁） | [`raiz_c4_pont.md`](mindmaps/raiz_c4_pont.md) | 4 |

**C 批次 5 —— 分辨、挑选、裁决（7 个词根 / 26 个单词）**

| 词根 | 拉丁本源 | 导图 | 单词 |
| --- | --- | --- | --- |
| `cern` | cernere（分辨、筛选） | [`raiz_c5_cern.md`](mindmaps/raiz_c5_cern.md) | 4 |
| `discrim` | discernere（区分） | [`raiz_c5_discrim.md`](mindmaps/raiz_c5_discrim.md) | 3 |
| `select` | seligere（挑选） | [`raiz_c5_select.md`](mindmaps/raiz_c5_select.md) | 4 |
| `elect` | eligere（选出） | [`raiz_c5_elect.md`](mindmaps/raiz_c5_elect.md) | 4 |
| `opt` | optare（选择） | [`raiz_c5_opt.md`](mindmaps/raiz_c5_opt.md) | 4 |
| `arbit` | arbitrari（裁决） | [`raiz_c5_arbit.md`](mindmaps/raiz_c5_arbit.md) | 5 |
| `scrut` | scrutari（细查） | [`raiz_c5_scrut.md`](mindmaps/raiz_c5_scrut.md) | 2 |

> `judic` 已在 v0 历史批次；`seleccionar` / `elegir` 已属 `leg`（legere）词族，本批次不重复。

**C 批次 6 —— 流动、水、冲洗（8 个词根 / 33 个单词）**

| 词根 | 拉丁本源 | 导图 | 单词 |
| --- | --- | --- | --- |
| `flu` | fluere（流淌） | [`raiz_c6_flu.md`](mindmaps/raiz_c6_flu.md) | 6 |
| `flux` | fluxus（流动） | [`raiz_c6_flux.md`](mindmaps/raiz_c6_flux.md) | 3 |
| `riv` | rivus（溪流） | [`raiz_c6_riv.md`](mindmaps/raiz_c6_riv.md) | 4 |
| `torren` | torrens（激流） | [`raiz_c6_torren.md`](mindmaps/raiz_c6_torren.md) | 2 |
| `und` | unda（波浪） | [`raiz_c6_und.md`](mindmaps/raiz_c6_und.md) | 8 |
| `lav` | lavare（冲洗） | [`raiz_c6_lav.md`](mindmaps/raiz_c6_lav.md) | 5 |
| `rig` | rigare（浇灌） | [`raiz_c6_rig.md`](mindmaps/raiz_c6_rig.md) | 3 |
| `irrig` | irrigare（灌溉） | [`raiz_c6_irrig.md`](mindmaps/raiz_c6_irrig.md) | 2 |

> 词根 `torrens`（激流）使用 id `torren`，与 C 批次 7 的 `torr`（torrere 烤）区分。

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
11. 生成后抽查三点：新词是否出现在对应的 `mindmaps/raiz_<批次>_<词根>.md` 且该页只有一个词族、级别是否落入正确的 `levels/<级别>.md`、点开豆包看 query 里的单词与词根是否对应。

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

版本变更记录见 [CHANGELOG.md](CHANGELOG.md)。
