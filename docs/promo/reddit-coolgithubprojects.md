# Reddit — r/coolgithubprojects

- 阶段：Phase 3（草稿，**未发布**）
- 渠道形态：link post（该 sub 只接受链接帖）
- 风险等级：**中**（账号门槛不公开；9:1 规则仍适用）
- 最后核对：2026-11-08

## 链接清单

| 用途 | 值 | 状态 |
| --- | --- | --- |
| 仓库（link post 的 URL 字段） | <https://github.com/auding1900/es-raiz-vocab> | 已确认存在 |
| 在线站点 | <https://auding1900.github.io/es-raiz-vocab/> | 2026-11-08 实测可访问 |
| PDF Release | <https://github.com/auding1900/es-raiz-vocab/releases/tag/v0.29.1> | 已发布（2026-11-08）；正文仍不必放 Release 链接 |

> 本渠道草稿不需要 Release 链接。Release 已发布，但正文仍只保留仓库链接。

## 目标受众

- 逛 r/coolgithubprojects 的开发者、维护者、技术选型爱好者。
- 关心数据建模、静态站点生成、Mermaid 渲染、GitHub Actions 的人。
- **不是**西语学习帖受众。正文不教西语，不讲“如何背单词”。

## 标题备选（3）

1. `[Project] A Spanish vocabulary repo that stores structure only — 232 roots, 1,423 words, meanings generated at query time`
2. `Show r/coolgithubprojects: I built a Spanish root map as YAML + Mermaid, and deliberately left all definitions out`
3. `[Project] 232 Latin roots, 1,423 Spanish words, zero definitions: a structure-only vocabulary repo`

选择建议：

- 备选 1 信息密度最高，适合开发者快速判断“这是个数据/架构项目”。
- 备选 2 更像 maker 自述，但 “I built” 会提高 self-promo 观感，需确认 sub 允许第一人称。
- 备选 3 最像 r/coolgithubprojects 的常见句式，但 “zero definitions” 可能被误读为“没做完”，正文第一段要立刻解释这是设计选择。

## 正文（英文，可直接复制）

> 说明：这是 link post 的正文。链接已经在 URL 字段里，正文不再重复贴裸链接。

```text
I kept running into the same problem with Spanish vocabulary lists: they are either alphabetical, or they are dictionary dumps. Neither tells you how words relate.

So I built the repository around relations instead of entries.

**The data is three YAML files.**
- `data/raices.yaml`: root id, root name, Latin origin, batch.
- `data/relations.yaml`: source, target, relation type (`derivar`, `asociar`, `confundir`), CEFR level, optional prompt override.
- `data/afijos.yaml`: affixes, validated and counted today, not rendered as graph nodes yet.

There is no separate word table. A word exists because an edge points at it, and its CEFR level lives on the derivation edge. That removes the classic two-tables-drift problem: you cannot add a word without also deciding how it connects.

**Why no definitions or examples.** Two reasons. Dictionary definitions and example sentences are usually copyrighted compilations, and I did not want to redistribute them. A static copy also goes stale. So the repo owns the map and an LLM produces the content at query time. The cost is real: you cannot read a meaning offline. The benefit is that the repository stays small, diffable, and legally boring.

**The pipeline.**
1. `scripts/generate_mermaid.py` validates the YAML — field whitelist, relation integrity, CEFR enum, duplicate edges, self-loops, and a leakage check that rejects definition/Chinese-explanation fields — then writes one Markdown page per root plus six level lists.
2. `scripts/build_site.py` reads those generated Markdown files, extracts the fenced Mermaid block from each family page, and inlines everything into a single `index.html`. No frontend framework, no bundler. Mermaid is pinned and loaded from a CDN.
3. A GitHub Actions workflow regenerates the artifacts, rebuilds the site, and deploys it to Pages. `site/` is a build artifact and is git-ignored.

**The AI boundary.** Each word row carries a URL-encoded prompt. The default target is Doubao because the prompt template is Chinese, but nothing in the repo calls a model. Copy the prompt into ChatGPT, Claude, Gemini, or whatever you use. No API keys, no stored answers, no telemetry.

**Current scale:** 232 roots, 1,423 words, 1,513 typed relations, 1,419 words with a CEFR tag. Graphs are generated per family, not as one giant graph, because Mermaid gets unhappy fast.

**Known trade-offs:** the map is only as good as the YAML; CEFR tags are teaching-oriented, not an official DELE list; 364 frequent words — native words, Arabic/Germanic loans, function words, irregular verbs — cannot be decomposed by Latin roots and live in a separate list; the web view needs a CDN on first load, while the repository view is plain text.

I would rather get criticism of the data model than praise. Is “level on the edge” the right call, or should levels live on words? Are three relation types enough? Is there a better way to render 232 Mermaid graphs without shipping a JS framework?
```

## 链接放置方式

- 使用 **link post**：URL 字段填仓库地址。
- 正文不放第二遍仓库链接，避免被判为 link spam；也不放 Pages 链接。
- 如果 sub 允许 flair，选 `Showcase` / `Project` 一类，不要自己造 flair。
- 不在评论里补链接，除非有人明确问“repo?”；即使补，也只补一次。

## Social preview 与 Reddit 卡片效果

- Reddit 链接帖的缩略图来自页面 Open Graph 图。GitHub 仓库的 OG 图只有在 **Settings → Social preview** 上传后才稳定，否则可能显示通用头像或默认图。
- `assets/root_tree.png` 是 1200 × 630（约 1.91:1），接近 Reddit 卡片的横向比例；但 new Reddit 会裁切，**文字和 `vid` 节点必须留在中间安全区**。
- 上传后分别检查 new Reddit、old.reddit、移动端三处的缩略图；如果缩略图不可读，卡片点击率会明显下降。
- 不要在帖子里说“看我的预览图”，让人自己判断。

## 账号门槛（发布前必须人工确认）

- 该 sub 的 karma / 账号年龄过滤阈值**没有公开**，被自动移除不等于违规。
- 发布前确认：账号有真实历史、近期有非推广评论、没有连续多天只发自己的链接。
- 若帖子被自动移除：
  1. 先读 removal reason；
  2. 不要立刻重发；
  3. 必要时通过 modmail 礼貌询问，不要私信单个 mod。
- Reddit 站级 9:1 规则仍然适用：推广内容不超过总活动的约 10%。这个账号如果平时不参与，先积累 2–4 周再发。

## 该平台的具体合规提醒

- 只发 link post，不发 text post 夹带链接。
- 标题必须带 `[Project]` 或 `Show r/coolgithubprojects:` 前缀（按 sub 当前 sidebar 为准）。
- 不请求 upvote、不写 “please star”、不放 “upvote if”。
- 不伪造 star 数、用户数、使用量、评价。
- 不在同一天把同一链接发到多个 sub。
- 不在正文里贬低其他项目或词典产品。
- 不贴词典释义或例句截图；本项目本身也不存这些内容。
- 发布后如果收到“这是自我推广”的质疑，直接承认并说明已按 sub 规则发布，不要争辩。

## 预期质疑与回应思路

| 质疑 | 回应思路 |
| --- | --- |
| “这不就是一堆没有释义的单词吗？” | 是刻意的。释义和例句属于受版权保护的汇编且会过期；仓库负责关系和导航，内容在查询时生成。 |
| “默认跳豆包，海外用不了。” | 预置 prompt 与 provider 无关；页面上有复制按钮，可粘贴到任意 LLM。豆包只是默认链接目标。 |
| “为什么不直接用 Wikidata / Wiktionary？” | 它们有词源和释义，但没有 CEFR 标记、`asociar`/`confundir` 关系类型，也没有面向学习的单页导航。这个项目的价值在关系层，不在词条层。 |
| “LLM 会编造释义。” | 仓库不保存答案，也不声称生成内容权威；prompt 要求引用公版文本并标注古体。用户仍需自行核对。 |
| “232 个词根太少了。” | 这是可扩展的种子集，不是全量词表；数据在 YAML 里，PR 可以加根、加词、加关系。 |
| “CEFR 标错了。” | CEFR 是教学参考坐标，不是官方 DELE 大纲；README 已写明边界。 |
| “为什么不用数据库 / 前端框架？” | 目标是 diff-friendly、PR-friendly、可离线阅读的纯文本；单页 HTML 足够，且 CI 可复现。 |

## 人工发布前检查清单

- [ ] 已读 r/coolgithubprojects 当前 sidebar 与置顶帖（规则会变）。
- [ ] 账号 karma / 年龄满足该 sub 的（未公开）过滤阈值；近期有真实非推广活动。
- [ ] 距上次发自己链接至少 7 天；本周未在其他 sub 发同一链接。
- [ ] 已在 GitHub 上传 Social preview，并检查三端缩略图可读。
- [ ] 标题使用 `[Project]` 或 `Show r/coolgithubprojects:` 前缀。
- [ ] 正文通读一遍，确认“离开链接也值得读”，且没有中文营销腔。
- [ ] 正文与 URL 字段加起来只有一个仓库链接。
- [ ] 未出现 star / 用户数 / 评价 / “please star” / “upvote”。
- [ ] 正文未出现具体 Release 链接（本渠道只放仓库链接；Release 已发布）。
- [ ] 发布后 2 小时内在线回评论；被自动移除时先读原因，不重发。
- [ ] 记录发布 URL、发布时间、首日评论数与移除状态到 launch 记录。
