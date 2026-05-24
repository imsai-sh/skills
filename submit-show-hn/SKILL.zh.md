---
name: submit-show-hn
description: Use when the user is preparing or troubleshooting a Hacker News Show HN submission. Covers the silent new-account throttle (showlim redirect), community karma thresholds, account-warming timeline, what to do if a post got shadowbanned, and how to write a Show HN that doesn't get flagged. Also covers when Show HN is the wrong format vs. a regular submission.
---

# Submit Show HN

## 什么时候用这个 skill

用户准备发(或刚发完)一个 Show HN, 或者在 troubleshoot 为什么自己的
帖子不显示出来。

常见触发场景:
- "我想把这个项目发到 Hacker News"
- "我提交了 Show HN 但首页看不到"
- "为啥 HN 把我重定向到 /showlim"
- "怎么让我的 Show HN 上首页"
- "我的 HN 账号 ready 发 Show HN 了吗"

## 最重要的一件事

**HN 会对新账号 / 低 karma 账号的 Show HN 静默限流。** 没做账号 warmup 就直接发, 结果就是被重定向到 `/showlim`, 帖子被 silent shadowban (你自己能看到, 别人看不到)。

这是头号失败模式。几乎每个人第一次发 Show HN 都会撞上。

→ 详细解释见 `references/showlim-page.md`。

## 发帖前 checklist

让用户在 submit 前过一遍这几条:

### 1. Show HN 是合适的格式吗

参考: `references/showhn.txt` (pg 写的官方规则)。

Show HN **只**适合:
- 用户自己亲手做的东西
- 别人能**试用**的(能跑、能装、能点、能拿)
- 非琐碎(不是"我让 LLM 一把生成的")
- 提交人会在评论区答疑

不适合 Show HN(走普通 submission):
- 博客文章, 哪怕技术含量高
- newsletter 注册、landing page、众筹页
- 列表(`awesome-X`)
- 版本号更新公告("Foo 1.3.1 发布了")
- AI 一键生成的 one-off

### 2. 账号够 warm 吗

用 HN 公开 API 自助查(不需要 auth):

```bash
curl -s "https://hacker-news.firebaseio.com/v0/user/<HN_USERNAME>.json" | python3 -m json.tool
```

看几个字段:
- `created` (unix timestamp) → 算账号年龄
- `karma` → 社区经验值: 低风险地板 ~50–100, 200+ 比较安全。低于 10 几乎肯定被 throttle。
- `submitted` 数组长度 → 看最近活跃度

如果 karma < 50 或账号年龄 < 30 天, **预期会被 throttle**。建议用户先做下面的"账号 warming plan"再发。

### 3. 帖子本身写得对吗

- 标题以字面 `Show HN:` 开头(大小写敏感, 带冒号)
- 标题 ≤ 80 字符, 不要 hype 词("revolutionary"、"powerful"、"amazing")
- 提交时填上 URL field(指向 GitHub repo / 在线 demo 等) — HN 会自动显示 domain, GitHub repo 还会显示 star 数
- 正文: 解释*为什么*做(个人 motivation), 不只是*做了什么*
- 不要 emoji、不要 markdown bold / header (HN 不渲染)
- 主动写明限制 / caveat — HN 尊重坦诚, 惩罚 hype

→ 完整规则见 `references/showhn.txt` 和 `references/newsguidelines.txt`。

## 如果帖子被 throttle 了 (撞到 `/showlim`)

应对 playbook:

1. **先确认是真被 throttle**: 打开
   `https://news.ycombinator.com/threads?id=<USERNAME>` → 如果你的帖子在那, 但用一个 incognito 浏览器去 `/show` 或 `/shownew` 看不到, 就是 throttle 了。

2. **不要**:
   - 立刻重新提交同一个项目 (HN dedup 会标记你)
   - 注册新账号重发 (HN sockpuppet 检测严, 可能永封)
   - 找朋友 upvote (voting ring 检测, 两个账号一起 shadowban)
   - 删掉帖子 (改变不了 throttle 状态, 还浪费一个 URL)

3. **应该做**:
   - 让 throttle 的帖子留着不动
   - 开始下一节的"账号 warming plan"
   - 同时把项目推到别的渠道(Reddit、Twitter、Bluesky、awesome-* PR、对口子版块)
   - 计划 2–4 周后再 resubmit, 带一个小的可见改动(新版本、新功能)以避开纯 dedup

## 账号 warming plan (1–2 周)

目标: karma 50+, 看得见的 substantive 参与, 不像 drive-by 自我推广。

日常作息:
- 每天看 HN 首页(`/news`) 和 `/show`
- 找 2–3 个**你真懂**的故事(AI tooling、CLI、TypeScript、devops、你的领域随便)
- 写 **technical, substantive** 的评论:
  - 解释一个非显然的 trade-off
  - 分享亲身经历("我之前做 X 时, Y 发生了")
  - 提替代方案(别只吐槽)
  - 提问要 out of curiosity, 不要 "gotcha" 式 cross-examine
- 避免: "+1" / "this" / "great post" / 一句话评论 — 这些不涨 karma 还像凑数
- 避免: 早期在评论里贴自己项目链接 (HN 标记 self-promo 模式; karma 上来之后偶尔贴是可以接受的)

避雷:
- 政治、意识形态、技术宗教战 — karma 涨得快但 downvote 也快
- contrarian / inflammatory 钓鱼式发言

大约 2 周后(或 karma > 50), Show HN 限流通常自动解除。没有通知, 自己再 submit 试试。

## HN 冷却期可以同步推的备用渠道

项目不需要等。先在其它地方发, 攒 GitHub stars — 将来 resubmit Show HN 时, 帖子里能 humble brag 一句"X 天 Y 个 star", 增加可信度。

| 渠道 | 备注 |
|---|---|
| r/<对口 sub> | 最对口的 subreddit 看项目领域 |
| r/programming | 通用, 流量大但淹没快 |
| Twitter/X | thread 形式: hook + screenshot + code + link |
| Bluesky | 跟 X 同, 但氛围更友好 |
| Mastodon (fosstodon.org) | OSS 友善的 fediverse instance |
| Dev.to / Hashnode | 长文 "how I built X" |
| awesome-* GitHub 列表 | PR 进去; 长尾流量 |
| Product Hunt | 如果项目偏 consumer-facing |
| V2EX / 即刻 / 掘金 | 中文技术社区 |

## Show HN 正文模板 (resubmit 时用)

参考: `references/showhn.txt`、`references/newsguidelines.txt`。

符合 HN 文化的结构模板:

```
Hi HN, I built this because <个人 motivation, 1-2 句>。

<它是啥、怎么工作, 1-2 段。带够技术细节让 HN 读者看出不是玩具。
提一下语言、关键依赖、有意思的设计选择。>

<想主动说的 caveat, 用 bullet list:>
- 已知限制 1
- 没测过的平台 / 场景
- 你做的 trade-off

<安装 / 试用 / 文档链接>

<协议>. Feedback welcome.
```

几个关键习惯:
- "Hi HN" 开头 — 社区友善的称呼
- 用纯文本, 不要用 HN 不渲染的 markdown
- 先讲 motivation (why), 别一上来就讲 features (what)
- 主动说 caveat — HN 尊重诚实, 鄙视 hype
- 发出去后**至少在评论区待 2 小时** — 前 30 分钟决定能不能上首页

## 发帖后在评论区

参考: `references/showhn.txt` 末尾段。

要 respectful:
- 任何人分享作品都是在贡献, 不论多 modest
- 提问要 out of curiosity, 不要 cross-examine
- 不要说"你这做得不对", 要 suggest alternatives
- 不好就是不好, 不必假装好 — 但**别 gratuitously negative**

## 这个 skill 包含的文件

- `references/showhn.txt` — pg 写的 Show HN 官方规则
- `references/newsguidelines.txt` — HN 社区通用规则
- `references/newswelcome.txt` — HN 新人 onboarding 页
- `references/showlim-page.md` — throttle 页面内容 + 社区对这个机制的经验解读
