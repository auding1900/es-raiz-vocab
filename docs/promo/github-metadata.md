# GitHub metadata（人工执行）

- 阶段：Phase 4（**仅文档，未执行任何 `gh` 命令**）
- 适用仓库：`auding1900/es-raiz-vocab`
- 最后核对：2026-11-08

> 本文件只提供建议值与命令。所有命令必须由人工在已登录、有写权限的环境执行。
> `gh repo edit` **不会**设置 Social preview，也不会改变 Release 状态。

## 1. Description（≤ 350 字符）

建议值（英文为主，260 字符）：

```text
A navigable Spanish root map: 232 Latin/Greek roots, 1,423 words, 1,513 typed relations, A1–C2 tags. Structure-only repository — no definitions or example sentences; meanings are generated on demand via any LLM. MIT, YAML + Mermaid, static GitHub Pages site.
```

要点：

- 一句话说清三件事：**navigable root map**、**structure-only repo**、**content generated on demand via any LLM**。
- 不写 “best / most effective / covers the full DELE syllabus”。
- 不写 “PDF available in Releases”：Release 已发布，但仓库描述的重点应是在线站点与结构数据，不是 PDF 下载。
- 不写 star 数、用户数、使用量。
- 字符数按 ASCII 计约 258；使用 `–` / `—` 后约 260，仍低于 350 上限。

可选中文对照（**不要**直接填进 GitHub Description，除非决定用中文面向国内搜索）：

```text
一张可导航的西语词根地图：232 个拉丁/希腊词根、1,423 个单词、1,513 条带类型的关系、A1–C2 分级。仓库只存结构，不存释义与例句；内容在查询时由任意 LLM 生成。MIT，YAML + Mermaid，GitHub Pages 静态站。
```

## 2. Topics（8 个）

建议添加：

```text
spanish-learning
etymology
mermaid
vocabulary-builder
dele
open-source-education
language-learning
static-site
```

### 杠杆分类

| Topic | 类型 | 说明 |
| --- | --- | --- |
| `spanish-learning` | **高杠杆（精准意图）** | 最贴目标用户；搜索“spanish learning”时相关度高，竞争也高，但转化意图明确。 |
| `language-learning` | **高杠杆（大流量）** | 发现面最广，但非常拥挤；适合作为大类曝光，不指望靠它排到前面。 |
| `mermaid` | **高杠杆（开发者发现）** | 吸引来看实现的人；与 “Mermaid 图 + 静态站” 的技术角度直接相关。 |
| `static-site` | **高杠杆（开发者发现）** | 与 GitHub Pages / 静态生成角度相关；带来维护者和工具向访客。 |
| `vocabulary-builder` | 中杠杆 | 意图明确，量小于 `language-learning`；适合被“怎么背单词/扩词”类搜索命中。 |
| `open-source-education` | 中杠杆 | 使命匹配，适合教育类聚合与 awesome list 交叉发现；量不大但相关度高。 |
| `etymology` | **长尾（高相关、低量）** | 词源爱好者会主动搜；人数少，但点进来的人理解成本低。 |
| `dele` | **长尾（考试意图）** | 搜索量集中在考试季，波动大；意图很强，但要注意 README 已声明“不是官方 DELE 词表”。 |

补充说明：

- GitHub topic 页的排序不完全由 topic 决定，star / 更新时间 / 描述匹配都会影响；不要期待加完 topic 立刻出现在前排。
- Topic 必须小写、用连字符；最多 20 个。不要添加 `awesome`、`hacktoberfest` 等与项目无关的热门词。
- 如果未来增加 “AI / LLM” 相关 topic，先想清楚：本项目**不调用模型**，只是把 prompt 交给用户；加 `artificial-intelligence` 容易引发错误预期。

## 3. 人工执行命令

### 3.1 先看当前状态（只读）

```bash
gh repo view auding1900/es-raiz-vocab --json description,homepageUrl,repositoryTopics
```

### 3.2 设置 Description + Website + Topics

```bash
gh repo edit auding1900/es-raiz-vocab \
  --description "A navigable Spanish root map: 232 Latin/Greek roots, 1,423 words, 1,513 typed relations, A1–C2 tags. Structure-only repository — no definitions or example sentences; meanings are generated on demand via any LLM. MIT, YAML + Mermaid, static GitHub Pages site." \
  --homepage "https://auding1900.github.io/es-raiz-vocab/" \
  --add-topic spanish-learning,etymology,mermaid,vocabulary-builder,dele,open-source-education,language-learning,static-site
```

说明：

- `--add-topic` 支持逗号分隔，也可以重复写 8 次 `--add-topic`；两种写法等价。
- 如果只想先加 4 个高杠杆 topic：

```bash
gh repo edit auding1900/es-raiz-vocab \
  --add-topic spanish-learning,language-learning,mermaid,static-site
```

- 如果仓库已有旧 topic，`--add-topic` 只追加，不删除；需要清理时先看 `repositoryTopics`，再决定是否用 `--remove-topic`。

### 3.3 Website 字段

About 区右侧 “Website” 填：

```text
https://auding1900.github.io/es-raiz-vocab/
```

对应命令已包含在上面的 `--homepage` 中。也可以单独执行：

```bash
gh repo edit auding1900/es-raiz-vocab --homepage "https://auding1900.github.io/es-raiz-vocab/"
```

注意：

- 该 URL 已在 2026-11-08 实测可访问，但仍需人工在浏览器里最终确认（桌面 + 移动）。
- 如果 Pages 之后绑定自定义域名，再回来改 `--homepage`。
- 不要把 `{{PAGES_URL}}` 占位符填进 GitHub；它不是有效 URL。

## 4. Social preview（命令无法设置）

**`gh repo edit` 不会设置 Social preview。** 必须在网页端手动上传：

1. 打开 `https://github.com/auding1900/es-raiz-vocab`。
2. **Settings → Social preview → Edit → Upload an image**。
3. 上传 `assets/root_tree.png`（1200 × 630）。
4. 保存后刷新仓库首页，检查卡片文字与图是否清晰。
5. 分别检查 new Reddit、old Reddit、移动端三处的链接卡片；GitHub 只保证仓库页的预览，不保证第三方抓取即时更新。

说明：

- Social preview 上传与 metadata 命令**没有先后依赖**：可以在 `gh repo edit` 之前或之后做，但两边都要做。
- 上传后如果 Reddit / X 仍显示旧图，通常是对方缓存；等待或换一个带查询参数的 URL 测试，不要反复改图。
- 不要把 “Social preview 已上传” 写进 README 或推广文案，除非人工确认。

## 5. 修改后的验证（可选）

```bash
gh repo view auding1900/es-raiz-vocab --json description,homepageUrl,repositoryTopics
```

检查：

- `description` 与上面一致，且没有超过 350 字符；
- `homepageUrl` 是 `https://auding1900.github.io/es-raiz-vocab/`；
- `repositoryTopics` 包含 8 个 topic，没有拼写错误。

浏览器检查：

- 仓库首页 About 区显示 Description 与 Website；
- 点击 Website 能打开在线站点；
- 搜索 `repo:auding1900/es-raiz-vocab` 或 topic 页时，描述与 topic 能显示（索引可能延迟）。

## 6. 生效时间与预期

- GitHub 仓库页的 Description / Topics 通常**立即**显示。
- GitHub 站内搜索与 topic 页的排序**不会立即变化**；索引和权重更新可能需要数天到数周。
- 第三方搜索引擎（Google / Bing）抓取更慢，不要因为第二天没有流量就反复改描述。
- 建议在修改后 **7 天**和 **14 天**各看一次 GitHub Traffic → Referrers，只记录真实数据，不对外宣称“搜索排名提升”。

## 7. 执行前检查清单

- [ ] 已确认当前 `description` / `homepageUrl` / `repositoryTopics`（先跑只读命令）。
- [ ] Description ≤ 350 字符，且没有 Release / demo / star 数等未验证承诺。
- [ ] 8 个 topic 均为小写、连字符、无空格。
- [ ] 没有添加 `artificial-intelligence` 等会误导的 topic。
- [ ] 已确认 `https://auding1900.github.io/es-raiz-vocab/` 在桌面和移动端可访问。
- [ ] 已知 `gh repo edit` **不会**设置 Social preview。
- [ ] 已计划手动上传 `assets/root_tree.png` 到 Settings → Social preview。
- [ ] 已接受搜索权重延迟，不把“加 topic”当作即时推广手段。
- [ ] 执行后记录修改时间与执行人，便于 7 / 14 天后复查。
