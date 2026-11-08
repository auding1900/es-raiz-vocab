# Phase 0 审计报告

- 审计日期：2026-11-08
- 分支 / 提交：`main` @ `f2d01f8`
- 审计前工作区：干净（`nothing to commit, working tree clean`）
- 审计范围：README、LICENSE、`data/*.yaml`、`scripts/*.py`、`mindmaps/`、`levels/`、`no-raiz-vocab.md`、GitHub 仓库 About 区
- 本阶段只新增本文件，未修改任何源码、数据或生成物

---

## 1. 项目一句话定位

> **不是背单词 App，而是一张可导航的西语词根地图。**

数据侧：232 个拉丁 / 希腊词根、1,423 个单词、1,513 条关系；`levels/` 中 1,419 个词带 CEFR 标签（A1 77 / A2 218 / B1 326 / B2 406 / C1 300 / C2 92），其余 4 个词未定级。
产品侧：仓库只存**结构**（词根、词形、关系类型、CEFR 级别、拉丁本源），不存释义与例句；点击词形跳转豆包，按固定 prompt 实时生成内容。

---

## 2. 当前 README 首屏问题

| # | 问题 | 证据 / 位置 | 影响 |
| --- | --- | --- | --- |
| 1 | 首屏没有视觉锚点 | 第 1–18 行只有标题、超长引用块和一段正文 | 3 秒内看不出“这是一张图”，不像可体验产品 |
| 2 | 首屏信息过密 | 引用块约 100 字，同时讲分级、B2/C1/C2、no-raiz、豆包、版权边界 | 移动端首屏被文字占满 |
| 3 | 没有在线体验入口 | 全文无 Demo / Pages / 截图链接 | 访客必须先 clone 才能理解产物 |
| 4 | 没有截图或 GIF | 仓库无 `assets/`，无 PNG / SVG / GIF | GitHub 搜索结果与社交分享没有缩略图 |
| 5 | 标题层级错误 | 第 12 行 `# 三条命令跑起来（Python 3.9+）` 是第二个 H1 | GitHub 目录结构断裂；语义上应降为 H2 |
| 6 | 快速开始不够“复制即用” | 首屏用 `pip install pyyaml`，未先跑 `--check` | 新贡献者容易先生成、后报错 |
| 7 | 豆包依赖藏在正文 | 第 1 行末尾才出现“豆包”，未说明可用性边界 | 非中国区用户点开才发现无法使用 |
| 8 | README 过长且与生成物重复 | 621 行；5.1 节把每个批次的词表复制进 README | 数据更新时 README 容易与 `root_tree.md` 漂移 |
| 9 | 缺少英文摘要 | 全文中文，无 `README.en.md` 或英文 TL;DR | Reddit / Product Hunt / GitHub 搜索发现率低 |
| 10 | GitHub 元数据为空 | About 区显示 “No description, website, or topics provided.” | 搜索引擎与 GitHub topic 页无法收录 |
| 11 | 没有 Release / 徽章 | Releases 为空；README 已写 PDF 下载说明但无实际发布 | “离线 PDF”承诺暂时不可兑现 |
| 12 | 未说明如何重新生成 no-raiz YAML 片段 | `build_no_raiz.py` 默认只写 `no-raiz-vocab.md`；6 个 `.yaml` 片段与总 YAML 的生成参数未写入 README | 维护者无法一键复现 |

### 首屏建议结构（Phase 1 执行）

1. 一句定位 + 3 个数字（232 词根 / 1,423 词 / A1–C2）
2. `assets/root_tree.svg` 或 `assets/root_tree.png`
3. 三个按钮式链接：在线体验 / 分级清单 / 60 秒演示
4. 三条硬约束（不存释义、不存例句、只存结构）
5. 快速开始（`--check` → 生成）
6. 贡献入口与“生成物不要手改”警告

---

## 3. 缺失的截图 / GIF / 在线 Demo

| 资产 | 当前状态 | Phase 1–2 计划 |
| --- | --- | --- |
| `assets/root_tree.svg` | 不存在 | 用 `mmdc` 渲染 `mindmaps/root_tree.md`；若环境无 `mmdc`，尝试 `npx -y @mermaid-js/mermaid-cli`；仍失败则只写 `assets/README.md` 说明，不伪造 |
| `assets/root_tree.png` | 不存在 | 同上，PNG 作为 GitHub 社交预览候选 |
| `assets/demo.gif` | 不存在 | 先放占位说明，配套 `docs/promo/demo-script.md`；不伪造录屏 |
| `site/index.html` | 不存在 | Phase 2 由 `scripts/build_site.py` 生成 |
| GitHub Pages | 未配置 | Phase 2 加 `.github/workflows/pages.yml`，人工启用 |
| 社交预览图 | 不存在 | 人工在 GitHub Settings 上传，Phase 4 写入检查清单 |

环境检测：

- `mmdc`：**未安装**
- `node` / `npm`：已安装，可用 npx 临时拉取 mermaid-cli（需要网络）
- `gh`：**未安装**，所有 `gh repo edit` 只能写入文档等待人工执行

---

## 4. 脚本与生成物状态

全部命令使用仓库自带 `.env/bin/python`（Python 3.9.2）。

| 检查 | 命令 | 结果 |
| --- | --- | --- |
| 词根图生成 | `.env/bin/python scripts/generate_mermaid.py` | 成功，写入 254 个 Markdown；重新生成后 `git status` 仍干净，**产物可复现** |
| 无词根清单 | `.env/bin/python scripts/build_no_raiz.py` | 成功：A1 142 / A2 71 / B1 43 / B2 35 / C1 42 / C2 31，合计 364；`no-raiz-vocab.md` 无 diff |
| 语法编译 | `.env/bin/python -m py_compile scripts/*.py` | 通过 |
| 空白 / 冲突标记 | `git diff --check` | 通过 |
| PDF 脚本 | `export_pdf.py` | 仅 `py_compile` 通过；未实际导出（缺 `mmdc`，且 `dist/` 被忽略） |

结论：

- `mindmaps/`、`levels/`、`no-raiz-vocab.md` 当前与数据一致，无未提交改动。
- 生成脚本**幂等**，可安全在 CI 中用于“生成后检查 diff”。
- `no-raiz-vocab.yaml` 与 `no-raiz-vocab.<level>.yaml` 的生成命令未文档化，属于维护缺口（见 TODO）。
- `export_pdf.py` 依赖 `mmdc` + Chrome + ReportLab；本机缺 `mmdc`，PDF 流程未验证。

---

## 5. 建议的 GitHub Description 与 Topics

> 以下只是建议，**不要自动执行**；命令见 Phase 4 `github-metadata.md`。

### Description（推荐英文，利于搜索）

```text
A navigable Spanish word-root map: 232 Latin/Greek roots, 1,419 CEFR-tagged words (A1–C2). Structure-only data — no definitions or examples; meanings are generated on demand. Mermaid + Markdown, offline-friendly, MIT.
```

中文备选：

```text
不是背单词 App，而是一张可导航的西语词根地图：232 个词根、1,419 个 A1–C2 分级词形；只存结构与关系，释义和例句按需生成。
```

### Topics（GitHub 最多 20 个，建议全用）

```text
spanish-learning
etymology
mermaid
vocabulary-builder
dele
open-source-education
latin-roots
cefr
language-learning
static-site
github-pages
markdown
yaml
spanish
vscode
mindmap
word-roots
educational-resources
python
mit-license
```

### 不建议写入推广材料的数据

- 不引用 star / fork / 用户评价 / “已有 X 人使用”，除非未来有真实可核查数据。
- 不声称“覆盖 DELE 全词表”；README 已有边界声明，推广文案必须沿用。

---

## 6. 风险清单

| # | 风险 | 影响 | 缓解 |
| --- | --- | --- | --- |
| R1 | 内容生成强依赖豆包（中国区服务） | Reddit / Product Hunt 海外用户点开可能不可用 | 在首屏明确“可把同一 prompt 粘贴到任意 LLM”；不擅自改默认 provider，等待人工决定 |
| R2 | 在线站点依赖 Mermaid CDN | 与“离线可用”表述冲突 | 区分：仓库/VSCode 离线可用；网页首次加载需 CDN |
| R3 | Mermaid `click` 在 GitHub 被忽略 | 用户以为链接坏了 | 保留每页“单词链接表”；README 首屏写明 |
| R4 | README 中的批次词表与生成物重复 | 数据更新后文案漂移 | 首屏只放数字与索引链接；明细交给 `mindmaps/root_tree.md` |
| R5 | 全中文内容与海外推广不匹配 | 搜索引擎与社区转化低 | Phase 1 增加英文 5 行摘要；是否做完整 `README.en.md` 需人工确认 |
| R6 | Pages 路径 / 相对链接 | 复制到 `site/` 后 `../mindmaps/` 可能失效 | `build_site.py` 统一重写链接；本地打开 `site/index.html` 验证 |
| R7 | 无 CI | 数据和生成物可能不同步 | 增加 Pages workflow，并在 workflow 中先跑 `--check` 和生成后 diff |
| R8 | 权益与定级争议 | CEFR 非官方大纲 | 沿用 README 第 10 节免责声明；PR 模板要求不提交释义/例句 |
| R9 | 过早提交 Product Hunt / 榜单 | 没有 Demo、Release、英文说明，转化差 | 先完成 Phase 1–2 与一次 Release，再执行 Phase 3 草稿 |
| R10 | 生成物被手改 | 下次生成被覆盖 | README 首屏、贡献指南、workflow 三处重复警告 |

---

## 7. TODO 与需要人工确认的事项

### 需要人工决定

1. **目标受众优先级**：中文西语学习者 vs 海外西语学习者 / 词源爱好者。决定 README 是否双语、Description 用英文还是中文。
2. **豆包是否为唯一查询入口**：是否允许文档中给出“任意 LLM”替代方案；是否未来加 provider 配置。
3. **是否发布 PDF Release**：README 第 9 节已承诺 Releases 下载，但当前 Releases 为空。
4. **GitHub Pages URL**：远端为 `auding1900/es-raiz-vocab`，预计 `https://auding1900.github.io/es-raiz-vocab/`；需确认仓库名是否保持不变。
5. **社交预览图**：是否使用 `assets/root_tree.png` 作为 Open Graph 图。
6. **LICENSE 版权人**：当前为 “es-raiz-vocab contributors”，是否改为个人 / 组织名称。

### 技术 TODO

- [ ] 文档化 `no-raiz-vocab.yaml` 与分等级 YAML 片段的完整生成命令（含 `--exclude` / `--yaml` / `--yaml-pos`）。
- [ ] 在 CI 中校验“生成后无 diff”。
- [ ] 为 `build_site.py` 增加链接重写与 Mermaid `securityLevel` 配置。
- [ ] 为 `export_pdf.py` 补一次真实导出验证（需 `mmdc` + Chrome + ReportLab）。
- [ ] 增加 `CONTRIBUTING.md` 与 PR 模板（可选，Phase 1 之后）。
- [ ] 评估英文 README（至少加英文 TL;DR）。

---

## 8. GitHub Pages 启用的人工步骤（Phase 2 会用到）

1. 推送 `.github/workflows/pages.yml` 到 `main`。
2. 打开仓库 **Settings → Pages**。
3. **Build and deployment → Source** 选择 **GitHub Actions**（不要选 “Deploy from a branch”）。
4. 等待 Actions 中 `pages` workflow 变绿。
5. 访问 `https://auding1900.github.io/es-raiz-vocab/`，确认 Mermaid 图、级别筛选、搜索框、豆包说明链接均可用。
6. 若 404：检查仓库是否 Public、Pages 是否启用、workflow 是否有 `pages: write` 与 `id-token: write` 权限。
7. 启用后把真实 URL 写回 README 与 `docs/promo/github-metadata.md` 的 Website 字段。

---

## 9. 阶段边界

本文件完成后**停止**，不进入 Phase 1。README 重写、资产渲染、`site/`、推广草稿与元数据命令均留待后续阶段，并逐阶段汇报。
