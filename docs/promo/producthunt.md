# Product Hunt — launch draft

- 阶段：Phase 3（草稿，**未发布**）
- 渠道形态：Product Hunt launch（self-hunt 或由他人 hunter）
- 风险等级：**高**（发布日全天在线；素材不完整会直接影响转化；索票会违规）
- 最后核对：2026-11-08

## 链接清单

| 用途 | 值 | 状态 |
| --- | --- | --- |
| 官网 / 首链 | <https://auding1900.github.io/es-raiz-vocab/> | 2026-11-08 实测可访问 |
| GitHub | <https://github.com/auding1900/es-raiz-vocab> | 已确认存在 |
| PDF Release | <https://github.com/auding1900/es-raiz-vocab/releases/tag/v0.29.1> | 已发布（2026-11-08）；PH 页面与 Maker comment 仍不必提“下载 PDF” |
| Social preview | `assets/root_tree.png` | 图片存在；**是否已上传到 GitHub 未核实** |
| Demo asset | `assets/demo.gif` | 真实 10 秒录屏（640 × 640，23 帧，≈2.3 fps）；不是 2 分钟 demo video |

## 前置阻塞项（发布前必须解决）

1. **没有 2 分钟 demo video。** 已有真实 10 秒 GIF（`assets/demo.gif`）；PH 若要 video，仍需另录 < 2 分钟版本，或只用 gallery 截图。
2. **Social preview 未核实。** GitHub 仓库卡片可能仍是默认图，影响 PH 页面外的分享效果。

已解决：Release 已发布（`v0.29.1`）；PDF 不是 PH 的主打内容。

## 目标受众

- PH 上关注教育、语言学习、开源工具、开发者效率的早期用户和 maker。
- 他们每天看到大量“AI language app”，所以第一眼必须看出**设计差异**，而不是功能数量。
- 不是西语初学者；PH 文案不需要教西语，只需要说清楚“这是什么、为什么不一样”。

## 定位一句话

> Not another language learning app. A Spanish vocabulary **map** whose repository stores structure only — no definitions, no example sentences — and hands the meaning lookup to any LLM at query time.

## 标题备选 / Tagline（3 个，≤ 60 字符）

| # | Tagline | 字符数 |
| --- | --- | ---: |
| 1 | `A navigable Spanish root map. Structure only.` | 45 |
| 2 | `232 Latin roots, 1,423 words, zero definitions.` | 47 |
| 3 | `Spanish vocabulary as a map, not a word list.` | 45 |

选择建议：

- 备选 1 最完整，`Structure only` 是差异点，但需要 short description 解释。
- 备选 2 数字最具体，适合 PH 列表页快速扫读；但“zero definitions”可能被误读为未完成。
- 备选 3 最顺口，但最像普通语言产品，curation 辨识度略低。
- 不要把 “AI-powered” 放进 tagline：这个项目不调用模型，AI 只是用户的查询端。

## Short description（≤ 260 字符，实测 238）

```text
A navigable Spanish vocabulary map: 232 Latin/Greek roots, 1,423 words, A1–C2 tags. Structure only, no definitions or example sentences. Pick a word, send a prepared prompt to any LLM. MIT, YAML plus Mermaid, deployed with GitHub Actions.
```

## 正文 / Maker comment 草稿（英文）

> 这是结构草稿。发布前请用**你自己的话**改写第一段，加入你真实的动机；不要编造学习成果、用户反馈或使用数据。

```text
Hi PH — maker here.

I started this because my Spanish vocabulary notebook had turned into a list of words I could translate individually but could not connect. I could recognize elocuente in a text and still fail to link it to locución or coloquio. Alphabetical lists were not helping, because the thing I was missing was the relation, not another definition.

So I built the project around relations and deliberately left the content out.

The repository stores only structure: root, word form, relation type (derivation, association, easily-confused), CEFR level, and Latin origin. There is no definition field and no example sentence field — the validator rejects them. When you pick a word, the site gives you a prepared prompt; you can send it to Doubao, ChatGPT, Claude, Gemini, or anything else. The repo never calls a model and never stores an answer.

Two consequences worth being upfront about:
- You cannot read a meaning offline. The map works offline; the meaning does not.
- The map is only as good as the YAML, and 232 roots is a seed, not a complete syllabus.

What I would like feedback on: is “level on the relation edge” the right data model? Are three relation types enough for vocabulary learning? And does the structure-only boundary make sense, or does it make the product too incomplete to be useful?

Thanks for looking.
```

Maker comment 写作要求：

- 先讲“为什么做”，再讲“做了什么”；不要上来列 10 个功能。
- 明确写出两个限制，PH 评论区对“过度承诺”很敏感。
- 结尾问一个具体问题，而不是 “please support us”。
- 不写 “we are thrilled / humbled / excited to announce” 这类模板句。
- 不放 star 数、用户数、waitlist 人数。
- 如果产品名不是个人项目，改成 “we”；当前是单人维护，用 “I”。

## Gallery 建议（1270 × 760）

| 顺序 | 内容 | 素材来源 | 说明 |
| --- | --- | --- | --- |
| 1 | 主视觉：`mut` 词族卡片 + 一句话定位 | `assets/root_tree.png` | 原图 1280 × 640；加边距到 1270 × 760，不要拉伸变形 |
| 2 | 站点 `#map` 视图：左侧词根列表 + 右侧 Mermaid 图 | 浏览器截图 | 展示“可导航”，不是静态图片 |
| 3 | 站点 `#levels` 视图：A1–C2 切换 + 搜索框 | 浏览器截图 | 展示 1,419 个带级别的词 |
| 4 | 数据模型：YAML 片段 + 三种关系类型 | 代码截图或排版图 | 解释 “structure only” 到底存了什么 |
| 5 | 使用流程三步：选词 → 复制 prompt → 粘贴到任意 LLM | 截图 + 箭头 | 强调 provider-agnostic，不要只露豆包 |
| 6 | 边界说明：不存释义 / 不存例句 / 不是 DELE 官方词表 | 文字卡片 | 提前回答“为什么没有释义” |

要求：

- 全部 1270 × 760，PNG/JPG，文字在移动端也能读。
- 可以使用 `assets/demo.gif` 的真实截帧，但 GIF 只有 640 × 640；1270 × 760 需要重新截屏或高质量重排，不要直接放大。
- 不要用模糊放大图；`root_tree.png` 放大到 1270 宽会略软，建议重新用原始 SVG 导出，而不是直接放大 PNG。
- 截图里隐藏浏览器书签、账号头像、通知、其他标签页。
- 不放二维码、公众号、微信群。
- 目前只有 10 秒 GIF；如果要上传 PH video，需另录 < 2 分钟版本。

## Demo asset（已录制，非完整 video）

- PH 允许上传 demo video，建议 < 2 分钟。
- 当前有真实 10 秒 GIF：`assets/demo.gif`（640 × 640，23 帧，≈2.3 fps）。
- 它不是 2 分钟 video；若 PH 页面需要视频，另录 < 2 分钟版本，或只用 gallery 截图。
- gallery 截帧见 [`demo-script.md`](demo-script.md)；注意 1270 × 760 的可读性。

## Topic tags（选 3 个，最多准备 5 个）

1. `Education`
2. `Open Source`
3. `Language Learning`
4. `Productivity`
5. `Developer Tools`

选择建议：

- 首选 `Education` + `Open Source` + `Language Learning`：最贴产品本身。
- 如果 PH 当天同赛道产品很多，可把 `Language Learning` 换成 `Developer Tools`，吸引来看实现的人。
- 不要选 `Artificial Intelligence`：项目不调用模型，选了会引发“AI 在哪里”的质疑。

## 链接放置方式

- PH 的 “Website” 字段填在线站点：`https://auding1900.github.io/es-raiz-vocab/`。
- Maker comment 里放 GitHub 链接一次；不要在每条评论里重复。
- 不在 tagline、short description 里放 URL。
- PH 页面不需要 Release 链接；Release 已发布，但 PDF 不是本次发布重点，避免把 PH 页面变成下载页。

## 该平台的具体合规提醒

- 发布日按**太平洋时间 12:01 AM** 上线；提前确认时区，不要按本地时间算。
- 发布前 2–4 周应在 PH 上真实参与：upvote 你真正用过的产品、写有内容的评论、关注相关 maker。不要发布前一周才注册。
- **不要**在发布日 begging for upvotes：不群发私信、不发邮件列表、不在 Discord/微信群喊“帮点一下”、不承诺回赞。
- 不买 upvote、不买评论、不找水军；PH 会清理异常投票，且会损害账号。
- 不伪造用户评价、不使用他人 testimonial、不写“已有 N 人使用”。
- Maker comment 必须披露你是 maker；不要用第三方口吻写。
- 发布后全天在线回复评论；不要只回复好评，质疑也要回。
- 发布后不要大改 tagline / 主图；小错别字可以修，大改会让页面数据和讨论错位。
- 不在 PH 页面放“请 star”“请转发”等交换条件。
- 若被 PH curation 拒绝，不要重复提交同一产品；先根据反馈改素材，至少间隔一个周期。

## 预期质疑与回应思路

| 质疑 | 回应思路 |
| --- | --- |
| “又一个语言学习 App。” | 不是 App，也不是课程。核心是一张可导航的关系图，仓库不存释义；内容由用户自己的模型生成。差异在“存什么”，不在“功能多少”。 |
| “AI 会编造释义。” | 仓库不存 AI 回答，也不声称权威；prompt 要求引用公版文本并标注古体。用户可以选择自己信任的模型，并自行核对。 |
| “为什么没有释义/例句？” | 版权与过期问题；同时避免仓库变成一份静态词典副本。地图负责关系，词典负责定义。 |
| “232 个词根太少了。” | 这是种子集，可扩展；数据在 YAML 里，PR 可以加根、加词、加关系。不是 DELE 全量词表。 |
| “为什么默认豆包？” | 预置 prompt 是中文，默认链接指向豆包；prompt 本身与 provider 无关。 |
| “有移动端 App 吗？” | 没有原生 App；站点是响应式的，仓库是纯文本。 |
| “怎么盈利？” | 不盈利，MIT 开源，没有付费层。 |
| “和词源词典有什么区别？” | 词源词典解释来源；这里加了 CEFR 标记、三种学习关系、按词族导航和查询 prompt。 |
| “为什么把生成物提交进仓库？” | GitHub 可直接渲染、clone 即可离线读，CI 还能用 diff 检查数据与产物是否同步。 |

## 人工发布前检查清单

- [ ] 已确认 `assets/demo.gif` 为真实录屏；如上传 video，已录 < 2 分钟版本；gallery 截帧已检查。
- [ ] 6 张 gallery 均为 1270 × 760，文字可读，无个人信息。
- [ ] `assets/root_tree.png` 未直接拉伸；如放大，已从 SVG 重新导出。
- [ ] Tagline ≤ 60 字符（当前 45 / 47 / 45），short description ≤ 260 字符（当前 238）。
- [ ] Maker comment 已用第一人称改写，包含真实动机与两个限制。
- [ ] Maker comment 没有功能清单堆砌、没有 star/用户数、没有 “please support”。
- [ ] Topic tags 已选 3 个，未选 `Artificial Intelligence`。
- [ ] Website 字段是在线站点，GitHub 链接只在 Maker comment 出现一次。
- [ ] PH 页面未把 PDF 下载当作重点（Release 已发布，但 PH 仍以在线站点为首链）。
- [ ] 发布前 2–4 周已有真实 PH 参与记录。
- [ ] 发布日日历提醒设在太平洋时间 12:01 AM；全天有人在线回评论。
- [ ] 已准备好首批评论回复模板（技术问题、质疑、竞品对比各一条），但不复制粘贴同一句。
- [ ] 未安排任何“帮点 upvote”的私信、群发、互赞。
- [ ] 发布后记录 PH URL、首日排名、评论数、站点 referrer（只记录真实数据）。
