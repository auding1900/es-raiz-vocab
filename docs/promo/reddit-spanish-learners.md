# Reddit — r/Spanish / r/learnspanish

- 阶段：Phase 3（草稿，**未发布**）
- 渠道形态：**不是主动开帖**。A = self-promotion megathread 简短介绍；B = 未来回答“如何按词根整理 B2/C1 词汇”时的评论话术
- 风险等级：**高**（两个 sub 对 self-promotion 都敏感；r/Spanish 通常只允许 megathread 或 mod 批准）
- 最后核对：2026-11-08

## 链接清单

| 用途 | 值 | 状态 |
| --- | --- | --- |
| 仓库 | <https://github.com/auding1900/es-raiz-vocab> | 已确认存在 |
| 在线站点 | <https://auding1900.github.io/es-raiz-vocab/> | 2026-11-08 实测可访问 |
| PDF Release | <https://github.com/auding1900/es-raiz-vocab/releases/tag/v0.29.1> | 已发布（2026-11-08） |

> 本渠道草稿优先使用仓库链接。Release 已发布，但正文不需要 PDF 链接。

## 目标受众

- r/Spanish：中高级学习者、教师、西语母语者；对“学习方法帖”容忍度取决于是否真诚、是否重复。
- r/learnspanish：A1–B2 为主，也有 B2/C1 备考者；sidebar 规则更细，需逐条读。
- 共同点：他们来问“怎么学”，不是来看产品发布。

## 标题备选（3）

> 仅用于“经 mod 批准后开帖”或 megathread 允许带标题的情况。默认形态是 megathread 内的一段文字，不需要标题。

1. `[Resource] Organizing B2/C1 vocabulary by Latin roots instead of alphabet`
2. `A root map for upper-level Spanish vocabulary (structure only, no definitions)`
3. `How I stopped losing track of B2/C1 words: group by root first, look up meaning second`

选择建议：

- 备选 1 最中性，先讲方法再讲资源。
- 备选 2 的 “structure only” 对开发者有吸引力，但对学习者可能是减分项，需要正文解释。
- 备选 3 最像真实学习帖，但不要写成“我的成功故事”；本项目没有学习成果数据。

## 形态 A：self-promotion megathread 简短介绍（英文，可直接复制）

> 3–5 句，链接放末尾。默认假设该 sub 的 megathread 允许每个项目发一条。

```text
Something that helped me with B2/C1 reading was grouping words by Latin root instead of alphabetical lists. Once elocuente, elocuencia, locución and coloquio sat on the same branch, they stopped feeling like four unrelated words. I keep a structure-only repo for this: 232 roots, 1,423 words, typed relations and CEFR tags, with no definitions or example sentences stored — you pick a word and send a prepared prompt to any LLM for the meaning. I maintain it, it is MIT-licensed, and the root index is readable without an account: https://github.com/auding1900/es-raiz-vocab
```

改写建议（如果 megathread 明确要求“不要第一人称推销”）：

```text
A root-family index for upper-level Spanish vocabulary: 232 Latin/Greek roots, 1,423 words, typed derivar/asociar/confundir links and A1–C2 tags. The repository stores structure only — no definitions, no example sentences; meanings are queried from any LLM with a prepared prompt. Useful if you already read B2/C1 texts and keep mixing up words that share a root. MIT, maintained by one person: https://github.com/auding1900/es-raiz-vocab
```

## 形态 B：回答“how to organize B2/C1 vocabulary by roots”的评论话术（英文）

> 只在**别人主动问**的时候用。不要主动贴到无关帖子下面。

```text
I would start from words you have already misread, not from a root dictionary.

1. Take 10 words from your last week of reading that felt similar but not identical.
2. Check whether they share a Latin root. Do not look up full definitions yet.
3. Put the root in the middle and sort the words by relation: same family, easily confused, or merely associated.
4. Only then look up meanings, and write down the contrast that actually confused you.
5. Re-read the original sentences and mark which word you would have chosen before.

The point is to make the relation visible before the definition. Definitions are easy to forget in isolation; a contrast between two words is harder to lose.

I maintain a structure-only map that already does step 2–3 for 232 roots, if it is useful as a starting scaffold: https://github.com/auding1900/es-raiz-vocab — no definitions stored, you query the meaning yourself.
```

如果 sub 规则不允许评论带链接，删掉最后一段，只保留方法。

## 链接放置方式

- r/Spanish：**只在 megathread 内**或获得 mod 明确批准后放链接；否则不发。
- r/learnspanish：发布前逐条读 sidebar / wiki 的 self-promotion 条款；很多规则要求链接放在指定 thread，而不是新帖。
- 形态 B 的链接只在对方明确问“有没有现成资源”时给；对方只是问方法时，不要塞链接。
- 一个帖子里最多一个链接；不要同时贴仓库和 Pages。
- 不私信发送链接，即使对方说“DM me”。

## 该平台的具体合规提醒

- **先参与，后链接**：在目标 sub 至少 2–4 周的真实参与记录（回答问题、参与讨论），再考虑发自己的项目。
- r/Spanish 的 self-promotion 通常只允许在专门的 megathread 或经 mod 批准后发布；不要假设“我有一个免费开源项目”就自动豁免。
- r/learnspanish 的规则需要**人工在发布前逐条读 sidebar**，不同时期规则会变；不要照搬旧帖的做法。
- 必须披露关系：`I maintain it` / `my project`，不要伪装成“偶然发现”。
- 不请求 upvote、不写 “please try”、不写 “would love your feedback” 式的软性拉票。
- 不伪造学习成果、不提分数据、不说“用了这个我 DELE 过了”。
- 不在两个 sub 同一天发同一内容；不要 crosspost 刷曝光。
- 不贬低 Anki、Duolingo、词典 App 或其他学习资源。
- 不贴词典释义或例句截图；本项目不存这些内容，草稿也不要引用。
- 不声称覆盖 DELE 大纲；CEFR 只是参考坐标。

## 预期质疑与回应思路

| 质疑 | 回应思路 |
| --- | --- |
| “词根不是完整的学习方法。” | 同意。它是组织工具，不替代输入、输出和语法练习；适合已经能读 B2 文本、但词汇关系混乱的人。 |
| “西语很多高频词根本不能拆词根。” | 正确。原生词、阿拉伯/日耳曼借词、功能词、不规则动词另有一个 364 词清单，和词根图互补。 |
| “这是自我推广。” | 直接承认 `I maintain it`，说明只发在允许的 megathread / 经批准的位置，不重复发。 |
| “让 LLM 解释词义不可靠。” | 仓库不存答案，也不声称权威；用户可以换任何模型，仍建议用词典核对。这里解决的是“词与词的关系”，不是“权威释义”。 |
| “为什么不直接用词典？” | 词典回答“这个词什么意思”，词根图回答“它和哪些词是一组、容易和谁混”。两者不冲突。 |
| “CEFR 标签准确吗？” | 教学参考，不是官方 DELE 词表；README 已写明。 |
| “为什么默认是豆包？” | 预置 prompt 是中文，所以默认链接指向豆包；prompt 本身与 provider 无关，可粘贴到任意 LLM。 |

## 人工发布前检查清单

- [ ] 已逐条读目标 sub 的 sidebar、wiki、置顶帖和 megathread 规则。
- [ ] 已在该 sub 有 2–4 周真实参与记录，且不是只回复自己的帖子。
- [ ] 确认当前允许 self-promotion 的位置（megathread / mod 批准 / 指定日）。
- [ ] 如不确定，先 modmail 询问，不直接发帖；不私信单个 mod。
- [ ] 文案中包含 `I maintain it` 或等价披露。
- [ ] 没有 “please try / please star / upvote” 等表述。
- [ ] 没有学习成果、提分、通过考试等未经证实的主张。
- [ ] 没有第二个链接；Release 链接未出现。
- [ ] 没有同一天在 r/Spanish 和 r/learnspanish 重复发。
- [ ] 发布后记录 URL；如被移除，先读 removal reason，至少 7 天后再考虑是否重发。
