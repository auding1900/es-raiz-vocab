# Changelog

> 本文件记录项目所有值得注意的变更。版本号遵循 [SemVer](https://semver.org/lang/zh-CN/) 的 MAJOR.MINOR.PATCH，格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。
>
> 提醒：仓库只保存**关系结构**（词根、单词、关系、CEFR 级别、拉丁本源），任何版本都不会收录释义、例句、译文等词典内容。

## [Unreleased]

### Added

- 词根扩充至 36 个：`ag`、`pon`、`cap`、`vid`、`mit`、`duc`、`fac`、`dic`、`leg`、`scrib`、`port`、`ven`、`ire`、`sta`、`sed`、`sol`、`clus`、`apert`、`aud`、`sent`、`curr`、`ped`、`man`、`cor`、`anim`、`pop`、`civ`、`terra`、`aqu`、`ign`、`aer`、`temp`、`dies`、`ann`、`mens`、`numer`；数据集达到 324 个单词 / 348 条关系（323 条 `derivar` + 15 条 `asociar` + 10 条 `confundir`）。
- 每个派生单词都标注 CEFR 级别，级别分布 A1 33 / A2 78 / B1 94 / B2 82 / C1 36，另有 1 个未标注（`mermar`）。

### Fixed

- 导图超过 mermaid 的 `maxTextSize`（50000 字符）时，GitHub 只会显示 `Maximum text size in diagram exceeded`：`root_tree.md` 改为**每个词根一张图**，单图均在 11k 字符以内。
- `associate_graph.md` 同样拆分：`asociar` 与 `confundir` 各一张图（最大 25k），不再随联想关系增加而撞上限。
- 生成器新增单图大小告警（超过 45000 字符即提示继续拆分），避免以后再撞上限而无人察觉。

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
