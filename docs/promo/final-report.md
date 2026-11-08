# Final report — es-raiz-vocab

- 日期：2026-11-08
- 仓库：`auding1900/es-raiz-vocab`（本地工作区路径省略，避免把个人路径写入仓库）
- 分支 / 提交：`main`（tag `v0.29.1` → `886a5ec`；发布后的 README/文档回写已推送）
- 范围：Phase 0–4 收尾 + PDF Release `v0.29.1` 发布。**未发帖、未执行 `gh`、未新增推广渠道。**

## 1. 项目一句话定位与当前完成度

> **不是背单词 App，而是一张可导航的西语词根地图。**
> 仓库只存结构（词根、词形、关系类型、CEFR、拉丁本源），释义与例句在查询时由用户选择的任意 LLM 生成。

当前数据规模（本地校验结果）：

- 232 个词根
- 1,423 个单词
- 1,513 条带类型的关系
- 1,419 个词带 CEFR 标签（A1 77 / A2 218 / B1 326 / B2 406 / C1 300 / C2 92）
- 364 个无词根高频词

### Phase 0–3 产出

| 阶段 | 产出 | 状态 |
| --- | --- | --- |
| Phase 0 | `docs/promo/00-audit.md`：README、数据、脚本、仓库元数据审计；风险清单 R1–R10；建议 Description / Topics | 完成 |
| Phase 1 | 英文落地页 `README.md`、中文页 `README.zh-CN.md`、`assets/` 图资产、`demo-script.md`、`release-draft.md`、`pdf-build.md`、`launch-checklist.md`；本地 PDF 导出 | 完成；PDF 已构建并随 `v0.29.1` 发布 |
| Phase 2 | `scripts/build_site.py`、`site/index.html`（git-ignored）、`.github/workflows/pages.yml`、`site-notes.md`；Pages 已上线 | 完成；`https://auding1900.github.io/es-raiz-vocab/` 可访问（待人工最终确认） |
| Phase 3 | 6 份渠道草稿：Reddit ×2、小红书、中文开发者渠道、Product Hunt、Awesome-list PR；`launch-checklist.md` 增加跨渠道时间线与 Never-do | 完成；全部为草稿，未发布 |
| Phase 4 | `github-metadata.md`、本文件；README 条件性检查；最终校验 | 完成；B1 已解决，B2–B4 保留 |

### 当前**没有**完成的事

- `assets/demo.gif` 仍是占位图，不是真实录屏。
- Social preview 未核实。
- Pages URL 机器可访问，但未由人工在桌面/移动端最终确认。

PDF Release 已在 2026-11-08 发布为 `v0.29.1`（8 个附件）。B2–B4 不是 Phase 4 的失败项，而是 Phase 4 之外的人工阻塞项，见第 4 节。

## 2. 改动文件清单

### 根目录

| 文件 | 类型 | 说明 |
| --- | --- | --- |
| `README.md` | 手写 | 英文落地页；重写首屏、三条硬约束、数据模型、贡献规则 |
| `README.zh-CN.md` | 手写 | 中文落地页；与英文页结构、统计、链接一致 |
| `requirements.txt` | 手写 | `PyYAML`、`reportlab`；Pillow / weasyprint 以注释标注为可选 |
| `.gitignore` | 手写 | 新增 `site/`、`.env`、`*.pyc`；保留 `dist/`、`__pycache__/`、`.venv/` |
| `CHANGELOG.md` / `LICENSE` | 既有 | 本次阶段未改；License 仍为 MIT |

### `assets/`

| 文件 | 类型 | 说明 |
| --- | --- | --- |
| `assets/README.md` | 手写 | 资产说明、来源与再生成方式 |
| `assets/root_tree.svg` | 生成 | 由真实词族图/Mermaid 渲染导出，非手绘 |
| `assets/root_tree_family.png` | 生成 | `vid` 词族的真实渲染图（1013 × 1600） |
| `assets/root_tree.png` | 生成 | 1200 × 630 横版卡片，供 README 与 Social preview 使用 |
| `assets/demo.gif` | 生成（占位） | 1200 × 630；**标注过的占位图，不是录屏**，由 `make_demo_placeholder.py` 生成 |

### `docs/promo/`

全部为**手写**文档（不含生成物）：

| 文件 | 阶段 | 说明 |
| --- | --- | --- |
| `00-audit.md` | Phase 0 | 审计报告与风险清单 |
| `demo-script.md` | Phase 1 | 60 秒分镜、录制设置、不可展示内容 |
| `pdf-build.md` | Phase 1 | 本地 PDF 构建步骤 |
| `release-draft.md` | Phase 1 | Release 标题、正文、附件清单 |
| `site-notes.md` | Phase 2 | 站点结构、Mermaid 版本、验证记录 |
| `launch-checklist.md` | Phase 1/3/4 | 人工清单、Phase 3 前置核对、T−14→T+7 时间线、Never-do |
| `reddit-coolgithubprojects.md` | Phase 3 | link post 草稿 |
| `reddit-spanish-learners.md` | Phase 3 | megathread / 评论话术，不主动开帖 |
| `xiaohongshu.md` | Phase 3 | 中文图文笔记与 7 张轮播设计 |
| `forum-zh.md` | Phase 3 | V2EX + 掘金/知乎技术稿 |
| `producthunt.md` | Phase 3 | Tagline、short description、Maker comment、gallery |
| `awesome-list-pr.md` | Phase 3 | 5 个候选 awesome list 与 PR 模板 |
| `github-metadata.md` | Phase 4 | Description、Topics、`gh repo edit` 命令、Social preview 说明 |
| `final-report.md` | Phase 4 | 本文件 |

### `scripts/`

| 文件 | 类型 | 说明 |
| --- | --- | --- |
| `scripts/generate_mermaid.py` | 手写（既有） | 校验 YAML，生成 `mindmaps/`、`levels/` |
| `scripts/build_no_raiz.py` | 手写（既有） | 生成 `no-raiz-vocab.md` 与可选 YAML |
| `scripts/export_pdf.py` | 手写（修改） | 新增 `--reuse-images`，复用已渲染图，避免重复跑 mmdc |
| `scripts/build_site.py` | 手写（新增） | 从生成的 Markdown 构建单页 `site/index.html` |
| `scripts/make_root_tree_card.py` | 手写（新增） | 生成 1200 × 630 横版卡片 |
| `scripts/make_demo_placeholder.py` | 手写（新增） | 生成占位 `assets/demo.gif` |

### `.github/`

| 文件 | 类型 | 说明 |
| --- | --- | --- |
| `.github/workflows/pages.yml` | 手写 | Node 24 版 actions；重新生成产物 → 构建 site → 部署 Pages |
| `.github/workflows/static.yml` | 已删除 | 远程自动生成的重复 Pages 工作流，在 `60f4f4d` 中移除 |

### 生成物（不应手改）

| 路径 | 类型 | 是否入库 |
| --- | --- | --- |
| `mindmaps/`（254 个 Markdown） | 由 `generate_mermaid.py` 生成 | 入库；本次重新生成后无 diff |
| `levels/A1.md` … `C2.md` | 由 `generate_mermaid.py` 生成 | 入库；无 diff |
| `no-raiz-vocab.md`、`no-raiz-vocab*.yaml` | 由 `build_no_raiz.py` 生成 | 入库 |
| `site/index.html` | 由 `build_site.py` 生成 | **不入库**（`.gitignore`） |
| `dist/pdf/*.pdf`、`SHA256SUMS.txt` | 由 `export_pdf.py` 生成 | **不入库**（`.gitignore`） |
| `scripts/__pycache__/` | Python 编译产物 | **不入库** |

## 3. 验证命令与结果

本地统一使用仓库自带解释器 `.env/bin/python`（Python 3.9.2）。以下命令均在 2026-11-08 实际运行。

| # | 命令 | 结果 | 证据 / 输出摘要 |
| --- | --- | --- | --- |
| 1 | `python scripts/generate_mermaid.py --check` | **PASS** | `词根 232 · 单词 1423 · 词缀 3 · 关系 1513`；A1 77 / A2 218 / B1 326 / B2 406 / C1 300 / C2 92；未写文件 |
| 2 | `python scripts/generate_mermaid.py` | **PASS** | 写入 254 个 Markdown；完成后 `git status` 无生成物 diff，说明幂等 |
| 3 | `python scripts/build_site.py` | **PASS** | `roots: 232`、`words: 1423`、`relations: 1513`、`CEFR-tagged: 1419`、`no-root: 364`；写入 `site/index.html` |
| 4 | `python -m py_compile scripts/*.py` | **PASS** | 无语法错误 |
| 5 | `git diff --check` | **PASS** | 无空白错误、无冲突标记 |
| 6 | `git check-ignore -v site/index.html dist/pdf/A1.pdf .env/bin/python` | **PASS** | 分别命中 `.gitignore:80 site/`、`.gitignore:76 dist/`、`.gitignore:27 .env/` |
| 7 | `git ls-files \| grep -E '^(site\|dist)/\|\.env\|__pycache__'` | **PASS** | 无输出，生成物/环境未被跟踪 |
| 8 | `git grep` token / 私钥模式扫描 | **PASS** | 无 `ghp_`、`github_pat_`、私钥、`api_key`、`password` 命中 |
| 9 | `git status --short --ignored` | **PASS** | `site/`、`dist/`、`.env/`、`__pycache__/`、`.DS_Store`、`.vscode/` 均为 ignored，未出现在普通 status |
| 10 | 占位符检查 | **PASS** | Release 发布后，渠道草稿中的 Release 占位符已全部替换为真实 `v0.29.1` URL；`{{PAGES_URL}}` 未使用（Pages 已验证）；无编造 URL |
| 11 | README 双语一致性 | **PASS** | 顶部互链正确；两版统计数字、A1–C2 表、在线体验 URL、Release 链接一致 |
| 12 | Release 附件校验 | **PASS** | `v0.29.1` 已发布；8 个附件（7 PDF + `SHA256SUMS.txt`）远端大小与 `dist/pdf/` 完全一致；tag 指向 `886a5ec` |

关于占位符的说明：

- Release 占位符在发布前保留；发布后 6 份渠道草稿中的占位符已替换为真实 URL `https://github.com/auding1900/es-raiz-vocab/releases/tag/v0.29.1`。
- `{{PAGES_URL}}` 没有出现在渠道草稿中：Pages 已在 2026-11-08 实测可访问，因此草稿直接使用真实 URL `https://auding1900.github.io/es-raiz-vocab/`；只有 `launch-checklist.md` 在说明中提到 `{{PAGES_URL}}` 不需要使用。
- 后续渠道正文仍不需要 PDF 下载链接；Release URL 只作为记录。

README 条件性检查结论：

- Release 发布前，`README.md` 与 `README.zh-CN.md` 均未提供 Release 下载链接，没有指向空 Release 的绝对化承诺。
- Release 发布后，两版已在 “Offline PDFs / 离线 PDF” 段落加入 `v0.29.1` 链接；没有提前使用未来 URL。
- 两版第 10 行的在线体验链接一致：`https://auding1900.github.io/es-raiz-vocab/`。
- 两版统计数字与 A1–C2 表一致。

## 4. 阻塞项清单（Phase 4 之外）

| # | 阻塞项 | 当前证据 | 影响渠道 | 解决动作 | 解决后回写文件 |
| --- | --- | --- | --- | --- | --- |
| B1 | **PDF Release（已解决）** | 2026-11-08 发布 `v0.29.1`，8 个附件大小校验通过 | 已解除；README 与渠道草稿已更新 | 已完成 | `README.md`、`README.zh-CN.md`、`docs/promo/release-draft.md`、`docs/promo/final-report.md`、6 份渠道草稿 |
| B2 | **`assets/demo.gif` 仍是占位图** | 文件内明确标注 placeholder；由 `make_demo_placeholder.py` 生成 | Product Hunt（不能上传为 demo video，gallery 不能用其截帧）；README 的 “See it in motion” 只能显示占位说明 | 按 `demo-script.md` 录制 55–60 秒真实流程，替换 `assets/demo.gif`，验证 GitHub 上可播放、≤ 10 MB | `README.md` / `README.zh-CN.md` 的 alt text（如录屏与分镜不同）、`docs/promo/producthunt.md`、`docs/promo/launch-checklist.md`、本文件 |
| B3 | **Social preview 未核实** | 无 API/CLI 证据；`gh repo edit` 不能设置 | Reddit link post 缩略图、PH 站外分享、任何 Open Graph 卡片 | 人工在 **Settings → Social preview** 上传 `assets/root_tree.png`（1200 × 630），检查 new Reddit / old Reddit / 移动端 | `docs/promo/github-metadata.md`（标记已上传）、`docs/promo/launch-checklist.md`、`docs/promo/reddit-coolgithubprojects.md`（如需要）、本文件 |
| B4 | **Pages URL 未人工最终验证** | 2026-11-08 机器抓取成功并渲染词根图；未由人工在桌面/移动端逐项点验 | README 双语“在线体验”、`github-metadata.md` 的 Website、PH Website、Reddit / awesome-list 链接 | 人工打开桌面 + 移动端，验证 Mermaid、词根搜索、A1–C2 切换、单词搜索、豆包跳转、复制指令、no-root 视图 | `README.md`、`README.zh-CN.md`（可移除“若链接尚未生效”的保守说明）、`docs/promo/github-metadata.md`、`docs/promo/launch-checklist.md`、本文件 |

> 说明：B1 已解决；B2 仍是发布类阻塞，B3/B4 是可信度/体验类阻塞。它们不影响仓库本地可运行，但会影响对外发布质量。

## 5. 条件性待办

### 5.1 Release 发布后（已完成）

- [x] 在 `README.md` 的 “Offline PDFs” 段落加入真实 `v0.29.1` Release 链接。
- [x] 在 `README.zh-CN.md` 的“离线 PDF”段落做同样修改。
- [x] 更新 `docs/promo/release-draft.md`：状态改为 **published**，补发布日期、tag、附件数量、Release URL。
- [x] 将渠道草稿中的 Release 占位符替换为真实 URL（渠道正文仍不需要 PDF 下载链接）。
- [x] 更新本文件第 4 节 B1 状态。
- [x] 发布后才回写 README，未提前使用未来 URL。

回写文件：`README.md`、`README.zh-CN.md`、`docs/promo/release-draft.md`（另含本文件与渠道草稿）。

### 5.2 `demo.gif` 替换后

- [ ] 确认 README 的嵌入路径仍是 `assets/demo.gif`，无需改 Markdown 路径。
- [ ] 如果真实录屏与 `demo-script.md` 分镜不同，更新两版 README 的 alt text。
- [ ] 确认 GitHub 页面上 GIF 能播放，而不只是本地能播。
- [ ] 确认 Product Hunt gallery 可以从真实录屏截帧；在录制完成前不要使用占位图。
- [ ] 更新 `docs/promo/launch-checklist.md` 与 `docs/promo/producthunt.md` 的状态。

### 5.3 Social preview 上传后

- [ ] 在 GitHub 仓库首页检查 About 区右侧卡片。
- [ ] 检查 new Reddit 链接卡片、old Reddit 缩略图、移动端分享预览三处。
- [ ] 如果第三方仍显示旧图，先判断是否为缓存，不要反复替换图片。
- [ ] 在 `docs/promo/github-metadata.md` 勾选“已上传”，并更新 `launch-checklist.md` 与本文 B3。

### 5.4 Pages 验证后

- [ ] 确认 `README.md` 与 `README.zh-CN.md` 的在线体验链接完全一致。
- [ ] 确认 `github-metadata.md` 的 `--homepage` 值与 README 一致。
- [ ] 确认 `docs/promo/producthunt.md` 的 Website 字段使用同一 URL。
- [ ] 如果确认稳定，可移除两版 README 第 12 行“若链接尚未生效”的保守说明；移除前先保留一次可回滚的记录。
- [ ] 更新本文 B4 与 `launch-checklist.md` 的 Pages 行。

## 6. 建议执行顺序

沿用 Phase 3 的顺序，并标注前置阻塞项：

| 顺序 | 动作 | 前置阻塞项 | 现在能否开始 | 备注 |
| --- | --- | --- | --- | --- |
| 1 | Awesome-list PR（先 `jqhoogland/awesome-language-learning`） | 无硬阻塞；建议先完成 B4（Pages 人工确认） | **可以** | 只投 1 个；用仓库链接，不用 Release |
| 2 | 中文开发者渠道（V2EX → 掘金/知乎） | 无硬阻塞；V2EX 账号可能受限 | **可以**（V2EX 无法发帖则跳过） | 技术角度写，不写西语教学；Release 已发布，不影响本渠道 |
| 3 | 小红书 | 需要 7 张 1080 × 1440 截图 | **可以**（先截图） | 不使用 demo.gif；截图来自实时站点 |
| 4 | Reddit megathread | 需要 2–4 周真实参与；B3（Social preview）建议先完成 | **暂缓** | 先参与、后发链接；不要主动开帖 |
| 5 | Product Hunt | **B2 必须先解决**（真实 demo）；gallery 1270 × 760；发布前 2–4 周 PH 参与 | **阻塞** | 占位 GIF 不能提交；Release 已发布，但 PH 不以 PDF 为卖点 |

原则：**先做不依赖 Release 和 demo 的动作**；Product Hunt 放在最后，且必须等真实 demo 与素材齐备。

## 7. 不做什么

- 不发帖、不评论、不私信、不群发。
- 不再执行 `gh` 命令；Release 已通过 GitHub REST API 发布。
- 不刷票、不买 upvote / star / 评论 / 评价。
- 不伪造 star 数、用户数、学习成果、使用数据、社区反馈。
- 不在 Release 不存在时推广 PDF 下载；本次已在发布后才加链接。
- 不在 `assets/demo.gif` 仍是占位图时提交 Product Hunt，也不把它当 demo video。
- 不使用编造的 URL；占位符只在未验证时保留。
- 不新增推广渠道（本阶段只有 Phase 3 已列出的渠道）。
- 不买 V2EX 邀请码或账号。
- 不在禁止 self-promotion 的 sub 硬发，不在 PH 发布日 begging for upvotes。
- 不手改 `mindmaps/`、`levels/`、`no-raiz-vocab*.md` 等生成物。

## 8. 下一步建议（1–2 周内可完成的最小动作）

### 第 1 周

1. **人工验证 Pages**（B4）：桌面 + 移动端各走一遍；记录截图与时间。
2. **上传 Social preview**（B3）：`assets/root_tree.png`；检查三端卡片。
3. **录制并替换 `demo.gif`**（B2）：按 `demo-script.md`，55–60 秒，≤ 10 MB；验证 GitHub 播放。
4. **提交 1 个 awesome-list PR**：`jqhoogland/awesome-language-learning` 的 `languages/es/README.md`；只投 1 个。
5. **准备小红书 7 张图**：从实时站点截 `rad` / `loqu` / `vid`；1080 × 1440；打码个人信息。

### 第 2 周

6. **（已完成）PDF Release**：`v0.29.1`，2026-11-08 发布，8 个附件；两版 README 已回写。
7. **发 1 篇中文技术稿**：先 V2EX（若账号可用），或先掘金/知乎；不要同日多平台群发。
8. **开始 Reddit 真实参与**：只回答问题，不发自己的链接；为 T+2 周的 megathread 做准备。
9. **复查 GitHub Traffic → Referrers**：只记录真实来源，不对外宣称排名或增长。
10. **Product Hunt 仍暂缓**：等 demo、gallery、PH 参与记录齐备后再排期；不要把“准备中”写成“已发布”。

> 最小可交付版本：完成第 1–3 项（Pages 确认 + Social preview + 真实 demo），即可让 Phase 3 的 Reddit / PH 草稿具备基本发布条件。Release 已完成；awesome-list 可以并行，但不要为了赶进度群发 PR。
