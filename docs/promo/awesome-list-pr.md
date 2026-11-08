# Awesome-list PR（长期 SEO，不是发帖）

- 阶段：Phase 3（草稿，**未提交任何 PR**）
- 渠道形态：向已有 awesome list 提交 1–2 个条目 PR
- 风险等级：**低**（不会触发平台封禁；但群发 PR 会被 maintainer 拉黑）
- 最后核对：2026-11-08

## 链接清单

| 用途 | 值 | 状态 |
| --- | --- | --- |
| 仓库 | <https://github.com/auding1900/es-raiz-vocab> | 已确认存在 |
| 在线 demo | <https://auding1900.github.io/es-raiz-vocab/> | 2026-11-08 实测可访问 |
| PDF Release | `{{RELEASE_URL}}` | **未发布**；条目里不要提 PDF 下载 |

## 目标受众

- awesome list 的 maintainer：他们决定条目是否“属于这个列表”，关心格式、分类、维护成本与是否 spam。
- 列表读者：用搜索找“西语学习工具/开源项目”的学习者和教师；他们点进来是为了找资源，不是看发布公告。
- 搜索引擎：awesome list 权重高，条目会被长期索引；描述必须客观、可验证。

## 目标

- 不是当天流量，而是长期自然搜索与高权重外链。
- awesome list 的读者会主动找“工具/资源”，转化质量高于泛社交平台。
- 一次只投 **1–2 个最匹配**的列表；群发 PR 是最容易被标记为 spam 的做法。

## 候选列表（5 个，按匹配度排序）

### 1. `jqhoogland/awesome-language-learning`

- 地址：<https://github.com/jqhoogland/awesome-language-learning>
- 匹配度：**高**。它的西语页目前是空的，并明确写着 “Please file a PR if you’d like to see this page not empty!”
- 目标文件：`languages/es/README.md`（README 中链接为 `/languages/es`，已确认该文件存在）
- 最近更新：GitHub 搜索页显示 2025-05（PR 前再确认仓库是否仍活跃）
- 建议条目：

```markdown
- [es-raiz-vocab](https://github.com/auding1900/es-raiz-vocab) - Structure-only Spanish root map: 232 Latin/Greek roots, 1,423 words, CEFR tags and Mermaid graphs; meanings are queried on demand instead of stored.
```

- PR 注意事项：
  - 该页几乎没有内容，先保持它的极简风格，不要顺手加标题层级或大段介绍。
  - 只加一行，不要同时改 README 主文件。
  - 该项目强调 “free resources”；本项目 MIT、免费，符合。
  - PR 标题：`Add es-raiz-vocab to Spanish resources`

### 2. `Spanish-teacher/awesome-learning-spanish`

- 地址：<https://github.com/Spanish-teacher/awesome-learning-spanish>
- 匹配度：**高**。专门面向西语学习者，有 `Vocabulary & SRS` 小节，README 明确写 “PRs welcome!”
- 目标小节：`## Vocabulary & SRS`
- 最近更新：GitHub 搜索页显示 2025-09
- 建议条目（严格按 CONTRIBUTING 的 `- **Name** — one sentence.` 格式）：

```markdown
- **es-raiz-vocab** — A structure-only Spanish root map (232 Latin/Greek roots, 1,423 words, A1–C2 tags) for navigating word families; meanings are queried from any LLM rather than stored.
```

- PR 注意事项：
  - `CONTRIBUTING.md` 要求：`- **Name** — one clear, specific sentence about why it helps.`
  - 小节内尽量按字母序；`es-raiz-vocab` 应放在 `ClozeMaster` 之后、`Readlang` 之前。
  - 运行 `awesome-lint`；描述 ≤ 1 句、不加 emoji、句末有句号。
  - PR 描述里写：目标级别 B1–C2、区域不限、免费/MIT、无广告/无追踪。
  - 该列表偏好 LATAM 友好资源；本项目不区分地区，可在 PR 里说明“地区中立”。

### 3. `Vuizur/awesome-language-learning`

- 地址：<https://github.com/Vuizur/awesome-language-learning>
- 匹配度：**中高**。通用语言学习项目列表，接受 PR 或 issue。
- 目标小节：`## Developer Resources` → `### Other Great Projects`（如果 maintainer 认为应放 `Useful Resources`，按对方判断）
- 最近更新：GitHub 搜索页显示 2025-10
- 建议条目（该列表用 `* [name](url) - Description.`）：

```markdown
* [es-raiz-vocab](https://github.com/auding1900/es-raiz-vocab) - A structure-only Spanish root map with 232 Latin/Greek roots, 1,423 words, CEFR tags and Mermaid graphs; definitions and examples are generated on demand instead of stored.
```

- PR 注意事项：
  - 该列表主要收录“帮助学语言的项目”，不是纯词典数据；PR 描述要强调“导航/关系层”，不要只说“词汇数据”。
  - 格式是 `*` 而不是 `-`；保持与相邻条目一致。
  - 没有找到 `CONTRIBUTING.md`；README 末尾写 “send a pull request or open an issue”。开 PR 即可，不要同时开 issue。
  - 不要加到 `Dictionaries` 小节：本项目不存释义，放那里会被认为不符合分类。

### 4. `Areso/Awesome-for-Spanish-learners`

- 地址：<https://github.com/Areso/Awesome-for-Spanish-learners>
- 匹配度：**中**。专门面向西语学习者，但列表较小、更新较旧（搜索页显示 2021-09），PR 可能长时间无人处理。
- 目标小节：`## Applications` 表格
- 建议行（按该表 5 列格式：Name / repo / try / Stack / Comment）：

```markdown
| es-raiz-vocab | [repo](https://github.com/auding1900/es-raiz-vocab) | [demo](https://auding1900.github.io/es-raiz-vocab/) | Python, YAML, Mermaid | Structure-only Spanish root map; no definitions or example sentences stored |
```

- PR 注意事项：
  - 该列表强调 “public repos and useful resources under open licenses”；本项目 MIT，符合。
  - 表格对齐不要求完美，但列数必须一致；不要破坏原有表格。
  - 该仓库活动度低，PR 可能几周无回应；**不要**反复 ping，等 14 天再礼貌问一次，仍无回应就放弃。

### 5. `stackwild/Awesome-Open-Source-Education`（可选，优先级最低）

- 地址：<https://github.com/stackwild/Awesome-Open-Source-Education>
- 匹配度：**中低**。它是“开放教育资源”列表，语言学习属于 `humanities.md` 下的一个小节。
- 目标文件：`humanities.md`（先确认其中是否已有语言学习小节及条目格式）
- 最近更新：搜索页显示 2025-08
- 建议条目（仅在格式匹配时使用）：

```markdown
- [es-raiz-vocab](https://github.com/auding1900/es-raiz-vocab) - A structure-only Spanish root map with 232 Latin/Greek roots, 1,423 words and CEFR tags; meanings are generated on demand.
```

- PR 注意事项：
  - 先读 `humanities.md` 的实际结构；**如果它不是按 `- [Name](url) - Desc.` 组织，按实际格式改写**。
  - 如果该文件没有语言学习小节，不要硬塞；放弃这个目标。
  - 该列表的主题是“开放教育”，PR 描述要强调 MIT、无付费、可用于教学，而不是“产品发布”。

## 推荐提交顺序

1. `jqhoogland/awesome-language-learning`（西语页为空，明确邀请 PR，成功率最高）
2. `Spanish-teacher/awesome-learning-spanish`（规则清晰，维护活跃）
3. `Vuizur/awesome-language-learning`（受众更广，但分类需要解释）
4. `Areso/Awesome-for-Spanish-learners`（匹配但低活动）
5. `stackwild/Awesome-Open-Source-Education`（可选，先确认格式）

**一次只投 1–2 个。** 建议先投 1 和 2；观察 7–14 天，再决定是否投 3。

## 标题备选（3）

1. `Add es-raiz-vocab to Spanish resources`
2. `Add es-raiz-vocab (structure-only Spanish root map) to Vocabulary & SRS`
3. `Add es-raiz-vocab to Other Great Projects`

选择建议：标题里带上目标小节名，maintainer 不用打开 diff 就知道改哪里；不要写 “New open-source project” 这种没有信息量的标题。

## 正文模板（英文）

```text
Hi — adding a free, MIT-licensed Spanish vocabulary project.

What it is: a structure-only Spanish root map. 232 Latin/Greek roots, 1,423 words, 1,513 typed relations, 1,419 words with A1–C2 tags. Each root has a Mermaid graph showing derivation, association, and easily-confused relations.

Why it fits this list: it is a navigation resource for learners, not a dictionary. The repository intentionally stores no definitions and no example sentences; learners pick a word and send a prepared prompt to any LLM for the meaning. This avoids redistributing copyrighted dictionary content and keeps the data diffable.

- Repo: https://github.com/auding1900/es-raiz-vocab
- Demo: https://auding1900.github.io/es-raiz-vocab/
- License: MIT
- Cost: free, no account, no ads, no tracking

I maintain the project. Happy to adjust the wording, section, or format to match the list's conventions.
```

## 链接放置方式

- 条目只放仓库链接；demo 仅在 PR 正文中出现，避免列表条目变成双链接。
- 不放 Release 链接（`{{RELEASE_URL}}` 尚未发布）。
- 不在条目描述里写 “please star / check it out”。
- 不在 PR 评论里重复贴链接。

## 该平台的具体合规提醒

- **遵循格式**：每个列表的符号（`*` vs `-`）、加粗、标点、字母序都不同；先读相邻 3 条，照抄格式。
- **遵循 contribution guidelines**：有 `CONTRIBUTING.md` 的先读；有 `awesome-lint` 的先本地跑。
- **一次一个 PR**：不要在一个 PR 里加多个不相关项目，也不要 fork 后批量向多个列表提 PR。
- **不要群发**：同一天向 5 个列表提 PR 会被识别为 spam；1–2 个最匹配的即可。
- **披露关系**：PR 正文写 `I maintain the project`，不要伪装成第三方推荐。
- **不要催**：14 天内不 ping；被拒后不要换账号重提。
- **不要买 star**：awesome list 的 maintainer 会看仓库真实活跃度；买 star 只会增加被拒风险。
- **描述客观**：不用 “amazing / best / revolutionary”，不用未经证实的数据。
- **版权**：描述里只讲结构（root、word form、relation type、CEFR、Latin origin），不要贴词典释义或例句。

## 预期质疑与回应思路

| Maintainer 可能问 | 回应思路 |
| --- | --- |
| “这是不是一个词表？我们已经有词典类资源了。” | 不是词表，是关系图；仓库不存释义，定位是导航层。 |
| “为什么没有释义？用户还要跳去 AI。” | 版权与过期问题；用户可以用任何 LLM 或自己的词典，项目不绑定 provider。 |
| “依赖 AI 的项目稳定吗？” | 仓库本身不调用模型、不存 key；即使没有 AI，词根图和分级清单仍可离线阅读。 |
| “数据准确吗？” | 结构数据在 YAML 里，可 review、可提 PR；CEFR 是教学参考，不是官方大纲，README 已写明。 |
| “为什么默认豆包？” | 预置 prompt 是中文；prompt 与 provider 无关，可复制到任意模型。 |
| “项目会不会很快不维护？” | 单人维护，但生成脚本幂等、CI 会校验；欢迎 issue/PR。不要承诺无法保证的更新频率。 |

## 人工发布前检查清单

- [ ] 已确认目标列表仍在维护（最近 6 个月有 commit 或 merge）。
- [ ] 已读 `CONTRIBUTING.md` / `contributing.md` / README 的贡献小节。
- [ ] 已读相邻 3 条的格式，条目符号、标点、字母序一致。
- [ ] 描述只有 1 句，句末有句号，无 emoji，无营销形容词。
- [ ] 条目只含仓库链接，未出现 Release 链接。
- [ ] PR 正文包含 `I maintain the project` 披露。
- [ ] 本地跑过 `awesome-lint`（如果该列表使用）。
- [ ] 本次只提 1 个 PR；未同时向多个列表群发。
- [ ] 未购买 star、未请求朋友点赞。
- [ ] 记录 PR URL 与提交日期；14 天内不催。
- [ ] 被拒后记录原因，不换账号重提。
