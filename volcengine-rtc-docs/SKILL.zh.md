---
name: volcengine-rtc-docs
description: |
  火山引擎实时音视频（VolcEngine RTC / veRTC）官方文档的本地可检索副本，已按目录切成 248 个 PDF。
  涵盖实时音视频核心 SDK、AI 音视频互动方案、硬件对话智能体、实时信令 RTS、互动白板、即时通讯 IM。
  触发场景：用户提到"火山 RTC"、"VolcEngine RTC"、"veRTC"、"声纹注册 / voiceprint"、"字幕 / 实时翻译"、
  "AI 对话智能体 / 端到端语音大模型 / 豆包语音"、"房间(Room) / 用户(User) / 流(Stream)"、
  "转推直播"、"云端录制"、"抽帧截图"、"RTS 实时信令"、"互动白板"，或贴出 volcengine.com/docs/6348/* 链接，
  或追问 RTC SDK 方法名 / 参数名 / 错误码、跨平台（iOS / Android / macOS / Windows / Linux / Web / Unity / Electron）集成细节。
  In English: "VolcEngine RTC", "veRTC", "voiceprint registration", "AI voice agent",
  "AIGCRoom", "RTC SDK method", "RTS signaling".
  当问题落在火山 RTC 范围内时，优先使用本 skill 而非 WebFetch —— 本地 PDF 与 volcengine.com/docs/6348 内容一致，读取更快。
---

# 火山引擎 RTC 文档（本地切分版）

完整官方文档随 skill 一起发布 —— **按目录切分的 248 个 PDF**，存放在：

```
volcengine-rtc-docs/references/pdfs/
```

PDF 通过 **git LFS** 存储（整个目录约 128MB）。新机器先 `git lfs install` 一次，再 `git clone` / `git lfs pull` 就能拉到二进制内容。

目录索引 [`references/toc-index.md`](references/toc-index.md) 把每个章节标题映射到对应的 PDF 路径（路径相对索引文件本身，形如 `pdfs/<L1>/<L2>/<L3>.pdf`）。先读索引定位，再读对应 PDF。

## 使用流程

1. **找主题** —— 打开 `references/toc-index.md`，按 L1 分类浏览，或直接 grep 关键词（中英文皆可）。每条形如 `[标题](pdfs/相对路径.pdf) (Np)`。
2. **读 PDF** —— 大部分切片小于 1MB，Read 工具一次性可读完。少量 API 参考类大于 5MB 的文件，用 `pages: "1-20"`（1-based，每次最多 20 页）分批读，依次 `"21-40"` 继续。
3. **跨文档搜索** —— 不确定答案在哪个文件时，用 `pdftotext` + `find`（任何 shell 都能跑，无需 globstar）。从 skill 根目录运行：

   ```bash
   ROOT=volcengine-rtc-docs/references/pdfs
   find "$ROOT" -name '*.pdf' | while read f; do
     hit=$(pdftotext "$f" - 2>/dev/null | grep -in "<关键词>" | head -3)
     [ -n "$hit" ] && printf "\n=== %s ===\n%s\n" "${f#$ROOT/}" "$hit"
   done
   ```

## 顶层结构

| L1 | 目录 | 内容 |
|----|------|------|
| 1 | `01-实时音视频/` | 核心 RTC SDK —— 发版说明、产品简介、产品计费、SDK 和 Demo、快速入门、场景方案、开发指南、最佳实践、升级指南、客户端 API 参考、服务端 API 参考、常见问题 |
| 2 | `02-AI 音视频互动方案/` | AI 语音 agent —— ASR + LLM + TTS pipeline、端到端豆包语音大模型、AIGCRoom |
| 3 | `03-硬件对话智能体/` | 硬件侧语音 agent（IoT 设备） |
| 4 | `04-实时信令/` | RTS —— 低延迟消息 SDK |
| 5 | `05-互动白板/` | 互动白板 |
| 6 | `06-即时通讯 IM（文档停止维护）/` | 旧版 IM，文档停止维护，仅供参考 |

## 高频入口

下列路径相对 `references/pdfs/`，常用问题可直接定位：

- **声纹服务端 API（注册/更新/查询/删除）**：`02-AI 音视频互动方案/05-API 参考/04-声纹管理.pdf` —— `RegisterVoicePrint` / `UpdateVoicePrint` / `QueryVoicePrint` / `DeleteVoicePrint`
- **声纹硬件 / IoT API**：`03-硬件对话智能体/08-服务端 API/03-声纹.pdf` —— `IotVoicePrintRegister` 等
- **声纹客户端集成**：`01-实时音视频/07-开发指南/` 与 `01-实时音视频/10-客户端 API 参考/`
- **字幕 / ASR / 实时翻译**：`02-AI 音视频互动方案/03-开发指南/` 与 `01-实时音视频/07-开发指南/`
- **客户端 SDK API 参考（分平台）**：`01-实时音视频/10-客户端 API 参考/`
- **服务端 OpenAPI**：`01-实时音视频/11-服务端 API 参考/`
- **错误码**：`01-实时音视频/12-常见问题/`
- **计费**：`01-实时音视频/03-产品计费/`

## 维护 skill

`references/pdfs/` 下的 248 个 PDF（~128MB）通过 git LFS 存储。需要刷新时：

1. 去 [volcengine.com/docs/6348](https://www.volcengine.com/docs/6348) 主页右键"下载文档 PDF"，重新导出源 PDF。默认放到 `~/Downloads/实时音视频_文档指南.pdf`；放别处的话用 `VERTC_SRC_PDF` 指。
2. 重新生成：

   ```bash
   cd volcengine-rtc-docs

   # 可选：VERTC_SRC_PDF=/abs/path.pdf
   uvx --from pymupdf python scripts/split_pdf.py             # 重写 references/pdfs/
   uvx --from pymupdf python scripts/gen_toc_index.py references/toc-index.md
   ```

`scripts/split_pdf.py` 用了 `subset_fonts()` 保证每个切片小（平均 ~0.5MB，不做子集化的话每片 62MB）。**不要删这一行** —— 删了 248 个 PDF 会膨胀到 15GB。

## 备注

- 源 PDF 是 WeasyPrint 从 HTML 文档渲染出来的；直接转 Markdown 会破版（表格散架、栏式列表错位），还是读 PDF 更可靠。如果一定要 Markdown，建议针对单页用 firecrawl-cli `--wait-for 5000` 重新抓在线 URL。
- 相对原 PDF 10304 页跳过的 25 页是法律声明 + 自动生成的目录，故意排除。
