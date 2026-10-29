# Changelog

> 本文件记录项目所有值得注意的变更。版本号遵循 [SemVer](https://semver.org/lang/zh-CN/) 的 MAJOR.MINOR.PATCH，格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。
>
> 提醒：仓库只保存**关系结构**（词根、单词、关系、CEFR 级别、拉丁本源），任何版本都不会收录释义、例句、译文等词典内容。

## [Unreleased]

暂无。

## [0.25.0] - 2026-10-29

数据规模：**189 个词根 / 1223 个单词 / 1306 条关系**。

### Added

- 新增 8 个词根（C 批次 8）：`script`、`liter`、`verb`、`or`、`rhet`、`gram`、`dial`、`gloss`。
- 新增 34 条 `derivar` 关系：script 6、liter 6、verb 4、or 5、rhet 2、gram 6、dial 2、gloss 3。
- 新增 1 条 `asociar`（`verbo ↔ palabra`）与 1 条 `confundir`（`literal ↔ literario`）。
- 数据集达到 1223 个单词 / 1306 条关系。
- 级别分布 A1 72 / A2 192 / B1 294 / B2 364 / C1 250 / C2 48，另有 2 个未标注。

### Notes

- `escribir` / `escritor` / `escritura` / `describir` / `manuscrito` 已在 `scrib` 词族，`script` 不重复声明。

## [0.24.0] - 2026-10-29

数据规模：**181 个词根 / 1191 个单词 / 1270 条关系**。

### Added

- 新增 7 个词根（C 批次 7）：`ard`、`cal`、`ferv`、`torr`、`frig`、`alg`、`gel`。
- 新增 30 条 `derivar` 关系：ard 4、cal 6、ferv 3、torr 3、frig 5、alg 2、gel 7。
- 新增 1 条 `asociar`（`arder ↔ helar`）与 1 条 `confundir`（`álgido ↔ gélido`）。
- 数据集达到 1191 个单词 / 1270 条关系。
- 级别分布 A1 71 / A2 189 / B1 289 / B2 356 / C1 240 / C2 44，另有 2 个未标注。

### Notes

- `ign`（ignis 火焰）已在 v0 历史批次，本批次不重复。

## [0.23.0] - 2026-10-29

数据规模：**174 个词根 / 1161 个单词 / 1238 条关系**。

### Added

- 新增 8 个词根（C 批次 6）：`flu`、`flux`、`riv`、`torren`、`und`、`lav`、`rig`、`irrig`。
- 新增 33 条 `derivar` 关系：flu 6、flux 3、riv 4、torren 2、und 8、lav 5、rig 3、irrig 2。
- 新增 1 条 `asociar`（`regar ↔ irrigar`）与 1 条 `confundir`（`abundar ↔ inundar`）。
- 数据集达到 1161 个单词 / 1238 条关系。
- 级别分布 A1 69 / A2 184 / B1 282 / B2 350 / C1 236 / C2 38，另有 2 个未标注。

### Notes

- C 批次清单中 `torr` 出现两次（torrens 激流 / torrere 烤），分别使用 `torren` 与 `torr`。

## [0.22.0] - 2026-10-29

数据规模：**166 个词根 / 1128 个单词 / 1203 条关系**。

### Added

- 新增 7 个词根（C 批次 5）：`cern`、`discrim`、`select`、`elect`、`opt`、`arbit`、`scrut`。
- 新增 26 条 `derivar` 关系：cern 4、discrim 3、select 4、elect 4、opt 4、arbit 5、scrut 2。
- 新增 1 条 `asociar`（`opción ↔ elección`）与 1 条 `confundir`（`selección ↔ elección`）。
- 数据集达到 1128 个单词 / 1203 条关系（1129 条 `derivar` + 48 条 `asociar` + 26 条 `confundir`）。
- 级别分布 A1 68 / A2 183 / B1 273 / B2 339 / C1 228 / C2 35，另有 2 个未标注（`mermar`、`muerte`）。

### Notes

- `judic` 已存在（v0 历史批次）；`seleccionar` / `elegir` 已属 `leg` 词族，本批次不重复声明。

## [0.21.0] - 2026-10-29

数据规模：**159 个词根 / 1103 个单词 / 1175 条关系**。

### Added

- 新增 8 个词根（C 批次 4）：`struct`、`fabric`、`constru`、`mol`、`aed`、`tect`、`mur`、`pont`。
- 新增 42 条 `derivar` 关系：struct 7、fabric 5、constru 6、mol 5、aed 4、tect 7、mur 4、pont 4。
- 新增 1 条 `asociar`（`construir ↔ destruir`）与 1 条 `confundir`（`techo ↔ teja`）。
- 数据集达到 1103 个单词 / 1175 条关系（1103 条 `derivar` + 47 条 `asociar` + 25 条 `confundir`）。
- 级别分布 A1 68 / A2 181 / B1 270 / B2 332 / C1 219 / C2 31，另有 2 个未标注（`mermar`、`muerte`）。

### Notes

- `fabricar` 原先仅出现在 `asociar` 示例边上，本批次归入 `fabric` 词族。

## [0.20.0] - 2026-10-29

数据规模：**151 个词根 / 1063 个单词 / 1131 条关系**。

### Added

- 新增 8 个词根（C 批次 3）：`cent`、`mill`、`dec`、`sept`、`nov`、`vet`、`prim`、`ult`。
- 新增 42 条 `derivar` 关系：cent 6、mill 6、dec 6、sept 3、nov 7、vet 5、prim 6、ult 3。
- 新增 1 条 `asociar`（`viejo ↔ nuevo`）与 1 条 `confundir`（`decimal ↔ décimo`）。
- 数据集达到 1063 个单词 / 1131 条关系（1061 条 `derivar` + 46 条 `asociar` + 24 条 `confundir`）。
- 级别分布 A1 67 / A2 175 / B1 260 / B2 322 / C1 211 / C2 26，另有 2 个未标注（`mermar`、`muerte`）。

### Notes

- `milenio` 已在 `ann`（annus）词族，本批次不重复声明。

## [0.19.0] - 2026-10-29

数据规模：**143 个词根 / 1021 个单词 / 1087 条关系**。

### Added

- 新增 7 个词根（C 批次 2）：`aequ`、`equ`、`par`、`sim`、`id`、`homo`、`heter`。
- 新增 34 条 `derivar` 关系：aequ 4、equ 3、par 6、sim 7、id 5、homo 5、heter 4。
- 新增 1 条 `asociar`（`igual ↔ idéntico`）与 1 条 `confundir`（`similar ↔ semejante`）。
- 数据集达到 1021 个单词 / 1087 条关系（1019 条 `derivar` + 45 条 `asociar` + 23 条 `confundir`）。
- 级别分布 A1 54 / A2 172 / B1 249 / B2 314 / C1 207 / C2 23，另有 2 个未标注（`mermar`、`muerte`）。

### Notes

- `vari` 已在 B 批次 12 建档，本批次不重复。
- `equivalente` / `equivaler` 已归属 `val`（valere），本批次不重复声明。
- `par` 词根与单词 par 同名，该词不单独声明节点。

## [0.18.0] - 2026-10-29

数据规模：**136 个词根 / 987 个单词 / 1051 条关系**。

### Added

- 新增 8 个希腊语词根（C 批次 1）：`arch`、`crac`、`polis`、`anthrop`、`geo`、`bio`、`psych`、`log`（`latin_origin` 字段在本批次记录希腊本源）。
- 新增 50 条 `derivar` 关系：arch 7、crac 6、polis 6、anthrop 5、geo 6、bio 7、psych 6、log 7。
- 新增 1 条 `asociar`（`vida ↔ muerte`）与 1 条 `confundir`（`catálogo ↔ monólogo`）。
- 数据集达到 987 个单词 / 1051 条关系（985 条 `derivar` + 44 条 `asociar` + 22 条 `confundir`）。
- 级别分布 A1 54 / A2 168 / B1 243 / B2 305 / C1 200 / C2 15，另有 2 个未标注（`mermar`、`muerte`）。

## [0.17.0] - 2026-10-29

数据规模：**128 个词根 / 936 个单词 / 999 条关系**。

### Added

- 新增 9 个词根（B 批次 13）：`clar`、`lumin`、`luc`、`splendor`、`teneb`、`obscur`、`umbr`、`pur`、`mund`。
- 新增 44 条 `derivar` 关系：clar 7、lumin 5、luc 6、splendor 5、teneb 2、obscur 5、umbr 5、pur 5、mund 4。
- 新增 1 条 `asociar`（`luz ↔ sombra`）与 1 条 `confundir`（`claridad ↔ caridad`）。
- 数据集达到 936 个单词 / 999 条关系（935 条 `derivar` + 43 条 `asociar` + 21 条 `confundir`）。
- 级别分布 A1 53 / A2 165 / B1 234 / B2 288 / C1 184 / C2 11，另有 1 个未标注（`mermar`）。

## [0.16.0] - 2026-10-29

数据规模：**119 个词根 / 892 个单词 / 953 条关系**。

### Added

- 新增 7 个词根（B 批次 12）：`mov`（movere）、`mot`（motus）、`vers`（vertere）、`vert`（versus）、`mut`（mutare）、`commut`（commutare）、`vari`（varius）。
- 新增 45 条 `derivar` 关系：mov 8、mot 6、vers 7、vert 7、mut 5、commut 4、vari 8。
- 新增 1 条 `asociar`（`movimiento ↔ variación`）与 1 条 `confundir`（`convertir ↔ advertir`）。
- 数据集达到 892 个单词 / 953 条关系（891 条 `derivar` + 42 条 `asociar` + 20 条 `confundir`）。
- 级别分布 A1 50 / A2 163 / B1 225 / B2 279 / C1 166 / C2 8，另有 1 个未标注（`mermar`）。

### Notes

- `vari` 同时出现在 B 批次 12 与 C 批次 2，只建一次（B12）。
- `vers` / `vert` 同出 `vertere`，按「名词性（versión / diversión）」与「动词性（convertir / invertir）」分工，避免派生词跨族重复。

## [0.15.0] - 2026-10-29

数据规模：**112 个词根 / 847 个单词 / 906 条关系**。

### Added

- 新增 7 个词根（B 批次 11）：`car`（carus）、`am`（amare）、`dilect`（diligere）、`od`（odisse）、`invid`（invidere）、`cup`（cupere）、`appet`（appetere）。
- 新增 36 条 `derivar` 关系：car 6、am 9、dilect 5、od 3、invid 4、cup 4、appet 5。
- 新增 2 条 `asociar` 关系：`amor ↔ odio`、`amable ↔ cariñoso`。
- 新导图页：`mindmaps/raiz_b11_*.md`（7 个）。
- 数据集达到 847 个单词 / 906 条关系（846 条 `derivar` + 41 条 `asociar` + 19 条 `confundir`）。
- 级别分布 A1 49 / A2 158 / B1 211 / B2 269 / C1 152 / C2 7，另有 1 个未标注（`mermar`）。

## [0.14.0] - 2026-10-29

数据规模：**105 个词根 / 811 个单词 / 868 条关系**。

### Added

- 新增 6 个词根（B 批次 10）：`col`（colere）、`habit`（habitare）、`domic`（domus）、`urb`（urbs）、`rural`（ruralis）、`incol`（incola）。
- 新增 32 条 `derivar` 关系：col 9、habit 6、domic 5、urb 7、rural 2、incol 3。
- 新增 2 条 `asociar` 关系：`habitante ↔ población`、`colono ↔ habitante`。
- 新导图页：`mindmaps/raiz_b10_*.md`（6 个，一词根一文件）。
- 数据集达到 811 个单词 / 868 条关系（810 条 `derivar` + 39 条 `asociar` + 19 条 `confundir`）。
- 级别分布 A1 46 / A2 155 / B1 203 / B2 258 / C1 144 / C2 4，另有 1 个未标注（`mermar`）。

### Notes

- `civ`（城邦）已在 v0 历史批次中，本批次不重复建词根。
- 词根 `rural` 与单词 `rural` 同名，该词不单独声明节点（同 `flor`、`don`、`arma`）。

## [0.13.0] - 2026-10-29

数据规模：**99 个词根 / 779 个单词 / 834 条关系**。

### Changed

- `mindmaps/` 产物改为**一个词根一个文件、一张图**：`raiz_<批次>_<词根>.md`（历史词根统一批次 `v0`），彻底避免单图 / 单文件过大。
- `mindmaps/root_tree.md` 改为词根索引（按批次分组，含单词数 / 关系数 / 导图链接），不再嵌图。
- 联想网状图按分块拆文件：`associate_graph.md` 仅保留分块导航与关系清单，图分别落在 `asociar_*.md` / `confundir_*.md`；未归属词根的联想关系单独成页 `raiz_sin_raiz.md`。
- `data/raices.yaml` 新增可选字段 `batch`（`b9`、`c10` …），决定文件名与索引分组；省略时归入 `v0`。
- 渲染实测：107 张图全部通过浏览器渲染（failed=0），最大单图 21,937 字符，最大单文件约 41KB。

### Added

- 新增 7 个词根（B 批次 9）：`pac`（pax）、`plac`（placere）、`tranqu`（tranquillus）、`seren`（serenus）、`quies`（quies）、`paus`（pausa）、`sedat`（sedare）。
- 新增 35 条 `derivar` 关系：pac 6、plac 6、tranqu 5、seren 4、quies 6、paus 4、sedat 4。
- 新增 2 条跨词根关系：`paz ↔ guerra`、`quieto ↔ tranquilo`（均为 `asociar`）。
- 数据集达到 779 个单词 / 834 条关系（778 条 `derivar` + 37 条 `asociar` + 19 条 `confundir`）。
- 级别分布 A1 46 / A2 153 / B1 196 / B2 248 / C1 133 / C2 2，另有 1 个未标注（`mermar`）。`levels/C2.md` 首次非空（`serenar`、`aquietar`）。

### Notes

- 词根 `sedare`（安抚）使用 id `sedat`：`sed` 已被 `sedere`（坐）占用。
- 词根 `serenus`（晴朗）使用 id `seren` 而非 `ser`，避免与助动词 `ser` 混淆。

## [0.12.0] - 2026-10-29

数据规模：**92 个词根 / 744 个单词 / 797 条关系**。

### Added

- 新增 7 个词根：`bell`（bellum）、`pugn`（pugnare）、`host`（hostis）、`arma`（arma）、`milit`（miles）、`vict`（vincere）、`fug`（fugere）。
- 新增 45 条 `derivar` 关系：bell 6、pugn 6、host 3、arma 8、milit 6、vict 8、fug 8。
- 新增 3 条跨词根关系：`victoria ↔ guerra`（asociar）、`militar ↔ guerra`（asociar）、`vencer ↔ convencer`（confundir）。
- 数据集达到 744 个单词 / 797 条关系（743 条 `derivar` + 35 条 `asociar` + 19 条 `confundir`）。
- 级别分布 A1 46 / A2 150 / B1 191 / B2 239 / C1 117，另有 1 个未标注（`mermar`）。

### Notes

- 词根 `arma` 与单词 `arma` 同名，该词不单独声明节点（同 `flor`、`don`）。
- `vict` 家族包含 `convencer`、`convicción`、`convincente`（拉丁 `convincere` ← `vincere`），并与 `vencer` 建立 `confundir` 关系。

## [0.11.0] - 2026-10-29

数据规模：**85 个词根 / 699 个单词 / 749 条关系**。

### Added

- 新增 7 个词根：`don`、`dare`、`tribut`、`larg`、`mun`、`commod`、`grat`。
- 数据集达到 699 个单词 / 749 条关系（698 条 `derivar` + 33 条 `asociar` + 18 条 `confundir`）。
- 级别分布 A1 45 / A2 146 / B1 185 / B2 216 / C1 106，另有 1 个未标注（`mermar`）。

### Fixed

- 联想图分块增加第二层兜底：按词根首字母分桶后若单桶仍超过 25,000 字符，则按 8 条关系切片。`associate_graph.md` 现为 6 张图，最大单图 24,386 字符，后续增加关系只会增加图数量。

### Notes

- 词根 `don` 与单词 `don` 同名，该词不单独声明节点（同 `flor`）。

## [0.10.0] - 2026-10-29

数据规模：**78 个词根 / 647 个单词 / 693 条关系**。

### Added

- 新增 7 个词根：`mensur`、`calcul`、`ponder`、`estim`、`preti`、`lib`、`tax`。
- 数据集达到 647 个单词 / 693 条关系（646 条 `derivar` + 31 条 `asociar` + 16 条 `confundir`）。
- 级别分布 A1 42 / A2 142 / B1 169 / B2 195 / C1 98，另有 1 个未标注（`mermar`）。

### Notes

- `metiri`（测量）词根使用 id `mensur`：`mens` 已被 `mens, mentis`（头脑）占用。

## [0.9.0] - 2026-10-29

数据规模：**71 个词根 / 601 个单词 / 644 条关系**。

### Added

- 新增 7 个词根：`ordin`、`reg`、`gubern`、`domin`、`imper`、`mand`、`rect`。
- 数据集达到 601 个单词 / 644 条关系（600 条 `derivar` + 28 条 `asociar` + 16 条 `confundir`）。
- 级别分布 A1 42 / A2 135 / B1 161 / B2 176 / C1 86，另有 1 个未标注（`mermar`）。

### Fixed

- 联想图单图超过 25,000 字符时自动按词根首字母（A–L / M–Z）拆分：`asociar` 由 42,109 字符的整图改为两张（26,097 / 18,156），`confundir` 同步拆为 11k / 16k，重新拉开与 mermaid `maxTextSize` 的安全距离。

## [0.8.0] - 2026-10-29

数据规模：**64 个词根 / 545 个单词 / 584 条关系**。

### Added

- 新增 7 个词根：`cred`、`fid`、`cert`、`prob`、`test`、`judic`、`sentent`。
- 数据集达到 545 个单词 / 584 条关系（544 条 `derivar` + 25 条 `asociar` + 15 条 `confundir`）。
- 级别分布 A1 41 / A2 118 / B1 148 / B2 161 / C1 76，另有 1 个未标注（`mermar`）。

### Notes

- `sententia` 词根使用 id `sentent`：id `sent` 已被 `sentire`（感知）占用，两个词族分开维护。

## [0.7.0] - 2026-10-29

数据规模：**57 个词根 / 490 个单词 / 526 条关系**。

### Added

- 新增 7 个词根：`val`、`firm`、`fort`、`pot`、`vir`、`rob`、`dur`。
- 数据集达到 490 个单词 / 526 条关系（489 条 `derivar` + 23 条 `asociar` + 14 条 `confundir`）。
- 级别分布 A1 40 / A2 106 / B1 137 / B2 143 / C1 63，另有 1 个未标注（`mermar`）。

## [0.6.0] - 2026-10-29

数据规模：**50 个词根 / 433 个单词 / 465 条关系**。

### Added

- 新增 7 个词根：`cresc`、`al`、`nutr`、`flor`、`germ`、`rad`、`fol`。
- 数据集达到 433 个单词 / 465 条关系（432 条 `derivar` + 20 条 `asociar` + 13 条 `confundir`）。
- 级别分布 A1 37 / A2 97 / B1 122 / B2 121 / C1 55，另有 1 个未标注（`mermar`）。

### Notes

- 词根 `flor` 与单词 `flor` 同名，而 `target` 不允许是词根 id，故该词不单独声明词节点（词根节点已展示 `florere`），`flor` 词族为 7 个词。

## [0.5.0] - 2026-10-29

数据规模：**43 个词根 / 385 个单词 / 413 条关系**。

### Added

- 新增 7 个词根：`ced`、`quer`、`prehend`、`tract`、`traj`、`jac`、`surg`。
- 数据集达到 385 个单词 / 413 条关系（384 条 `derivar` + 17 条 `asociar` + 12 条 `confundir`）。
- 级别分布 A1 36 / A2 93 / B1 115 / B2 98 / C1 42，另有 1 个未标注（`mermar`）。

## [0.4.0] - 2026-10-29

数据规模：**36 个词根 / 324 个单词 / 348 条关系**。

### Added

- 新增 15 个词根：`ped`、`man`、`cor`、`anim`、`pop`、`civ`、`terra`、`aqu`、`ign`、`aer`、`temp`、`dies`、`ann`、`mens`、`numer`。
- 数据集达到 324 个单词 / 348 条关系（323 条 `derivar` + 15 条 `asociar` + 10 条 `confundir`）。
- 级别分布 A1 33 / A2 78 / B1 94 / B2 82 / C1 36，另有 1 个未标注（`mermar`）。

### Fixed

- `associate_graph.md` 按关系类型拆成两张图（`asociar` 约 25k / `confundir` 约 17k），不再随联想关系增加而撞 mermaid `maxTextSize` 上限。

## [0.3.0] - 2026-10-29

### Added

- 新增 7 个词根：`sed`、`sol`、`clus`、`apert`、`aud`、`sent`、`curr`。
- 数据集达到 21 个词根 / 198 个单词 / 214 条关系（197 条 `derivar` + 10 条 `asociar` + 7 条 `confundir`）。

## [0.2.0] - 2026-10-29

### Added

- 新增 7 个词根：`dic`、`leg`、`scrib`、`port`、`ven`、`ire`、`sta`。
- 数据集达到 14 个词根 / 134 个单词 / 145 条关系（133 条 `derivar` + 8 条 `asociar` + 4 条 `confundir`）。

## [0.1.0] - 2026-10-28

**初始原型版本**：以词根 `duc`（拉丁 `ducere`）作演示词族，跑通「yaml 数据源 → 静态 markdown」的完整链路。

### Added

- **YAML 数据源**：`data/raices.yaml`（`id` / `root_name` / `latin_origin`）、`data/afijos.yaml`（`id` / `affix` / `meaning` / `type`）、`data/relations.yaml`（`source` / `target` / `rel_type` / `cefr_level` / `prompt_template`）。字段按白名单校验，多写、少写、拼错都会报错。
- **关系模型**：`derivar`（词根派生）、`asociar`（语义联想）、`confundir`（形近易混）；单词节点在 `target` 处声明，CEFR 级别挂在派生边上。
- **词根导图**：`mindmaps/root_tree.md`，Mermaid `graph LR`。词根节点显示词根 + 拉丁本源，单词节点显示单词 + 级别；三种关系用不同线型区分（实线黑 / 虚线 `#4488bb` / 虚线 `#dd4444`），节点按级别配色。
- **联想网状图**：`mindmaps/associate_graph.md`，只保留 `asociar` 与 `confundir` 的跨词族视图，便于单独查看易混 / 近义网络。
- **A1–C2 分级索引**：`levels/A1.md` … `levels/C2.md`，每级一张「单词 / 词根 / 豆包」清单；未标注级别的词只出现在导图中，不进分级页。
- **豆包跳转**：每个单词节点内嵌查询链接，自动填充 `{word}` 与 `{root}`（无词根时自动去掉「词根」分句，不留残句）。一次点击即请求词义、DELE 等级、语体、常用搭配、近义词辨析，并要求返回 Wikisource / 古登堡计划等公版西语文本的自然例句（现代标准西班牙语优先，古体表达标注【arcaísmo】）。
- **编码处理**：URL 全量 UTF-8 编码并做 NFC 归一，`ñ á é í ó ú` 等字符不会乱码。
- **CLI**：`--check`（只校验不写盘）、`--dry-run`、`--quiet`、`--data`、`--repo`；默认流程先清空 `mindmaps/`、`levels/` 下的旧产物再渲染。
- **文档**：README（项目原理、使用教程、数据格式、贡献指南与自查清单、定级声明）、MIT 协议、`.gitignore`。

### Fixed

- 导图超过 mermaid `maxTextSize`（50000 字符）时 GitHub 只显示报错：`root_tree.md` 改为**每个词根一张图**（单图 <12k），并加入 45000 字符的单图大小告警。

### 本版数据

| 项目 | 数量 | 内容 |
| --- | --- | --- |
| 词根 | 1 | `duc` |
| 单词 | 5 | conducir (A1) · deducir (B2) · reducir (B2) · inducir (C1) · mermar（未标注） |
| 词缀 | 3 | `re-` · `de-` · `-ción` |
| 关系边 | 5 | 4 条 `derivar` + 1 条 `asociar` |

### Known Limitations

- **Mermaid 大图会卡顿**：所有词根目前渲染在同一张 `root_tree.md` 中，词族变多后图会变大、GitHub 渲染变慢。建议届时按词根分组拆分成多张图（`--data` / `--repo` 已支持指定目录，拆分逻辑计划在后续版本提供）。
- **仅支持网页版豆包跳转**：链接指向豆包网页版，不支持唤起豆包 APP，移动端需在浏览器中打开。
- **例句由豆包实时生成**：仓库不存储、不缓存任何例句文本，因此跳转需要联网；返回内容的准确性与来源请在豆包侧自行核对。
- **GitHub 会忽略 mermaid 的 `click`**：受其安全策略限制。导图页底部提供了「单词链接表」，`levels/` 页每行也有「豆包」链接，均可直接点击。

### Contributing

欢迎 PR 补充**词根**与**单词关系**（含 CEFR 级别标签）。提交前请只修改 `data/*.yaml`、不提交任何释义 / 例句 / 译文，并运行 `python3 scripts/generate_mermaid.py --check` 确认数据合法。详见 [README 第 8 节](README.md#8-贡献指南)。

## [0.1.0] 之前

正式发布前经历过骨架搭建、yaml 字段规范化、渲染器实现、编码与空词根修复、文档重写等若干轮本地迭代，全部合并进 `0.1.0`，不单独发布。
