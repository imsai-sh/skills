---
name: volcengine-rtc-docs
description: Local searchable copy of VolcEngine RTC (火山引擎实时音视频 / veRTC) documentation, split into 248 PDFs by table of contents. Covers 实时音视频核心 SDK, AI 音视频互动方案, 硬件对话智能体, 实时信令 RTS, 互动白板, 即时通讯 IM. Use this skill whenever the user mentions 火山 RTC, VolcEngine RTC, veRTC, 声纹/voiceprint registration, 字幕/subtitles, AI 对话智能体 / 端到端语音大模型 / 豆包语音, 房间(Room) / 用户(User) / 流(Stream), 转推直播, 云端录制, 抽帧截图, RTS 实时信令, 互动白板, references a volcengine.com/docs/6348/* URL, asks about RTC SDK method or parameter names, error codes, or platform-specific (iOS / Android / macOS / Windows / Linux / Web / Unity / Electron) integration. Prefer this skill over WebFetch when the topic is VolcEngine RTC — the local PDFs match volcengine.com/docs/6348 content and are faster to read.
---

# 火山引擎 RTC 文档（本地切分版）

The full documentation ships with this skill — **248 PDFs split by TOC**, stored at:

```
volcengine-rtc-docs/references/pdfs/
```

The PDFs are tracked with **git LFS** (the directory totals ~128MB). Make sure `git lfs install` has been run once on the machine, then `git clone` / `git lfs pull` will materialise the binaries.

The TOC index in [`references/toc-index.md`](references/toc-index.md) maps every section heading to a PDF file path (relative to the index file, so paths look like `pdfs/<L1>/<L2>/<L3>.pdf`). Read the index first to locate the right file, then read the PDF.

## How to use

1. **Find a topic** — open `references/toc-index.md` and browse by L1 section or grep for a keyword (Chinese or English). Each entry is `[标题](pdfs/relative/path.pdf) (Np)`.
2. **Read the PDF** — most chunks are under 1MB. The Read tool handles them in one shot. For the handful of chunks over 5MB (a few API reference files), Read with `pages: "1-20"` (1-based, max 20 pages per call) and continue with `"21-40"` etc.
3. **Search across all docs** — when you don't know which file holds the answer, use `pdftotext` with `find` (works in any shell, no globstar needed). Run from the skill root:

   ```bash
   ROOT=volcengine-rtc-docs/references/pdfs
   find "$ROOT" -name '*.pdf' | while read f; do
     hit=$(pdftotext "$f" - 2>/dev/null | grep -in "<keyword>" | head -3)
     [ -n "$hit" ] && printf "\n=== %s ===\n%s\n" "${f#$ROOT/}" "$hit"
   done
   ```

## Top-level structure

| L1 | Folder | What's inside |
|----|--------|---------------|
| 1 | `01-实时音视频/` | Core RTC SDK — 发版说明, 产品简介, 产品计费, SDK 和 Demo, 快速入门, 场景方案, 开发指南, 最佳实践, 升级指南, 客户端 API 参考, 服务端 API 参考, 常见问题 |
| 2 | `02-AI 音视频互动方案/` | AI voice agents — ASR + LLM + TTS pipeline, 端到端豆包语音大模型, AIGCRoom |
| 3 | `03-硬件对话智能体/` | Hardware-side voice agents (IoT devices) |
| 4 | `04-实时信令/` | RTS — low-latency messaging SDK |
| 5 | `05-互动白板/` | Interactive whiteboard |
| 6 | `06-即时通讯 IM（文档停止维护）/` | Legacy IM, no longer maintained — reference only |

## Quick lookups

High-frequency entry points (skip the TOC search for these):

Paths below are relative to `references/pdfs/`:

- **Voiceprint server API (注册/更新/查询/删除)**: `02-AI 音视频互动方案/05-API 参考/04-声纹管理.pdf` — `RegisterVoicePrint` / `UpdateVoicePrint` / `QueryVoicePrint` / `DeleteVoicePrint`.
- **Voiceprint hardware/IoT API**: `03-硬件对话智能体/08-服务端 API/03-声纹.pdf` — `IotVoicePrintRegister` etc.
- **Voiceprint client integration**: `01-实时音视频/07-开发指南/` and `01-实时音视频/10-客户端 API 参考/`.
- **Subtitle / ASR / 字幕**: `02-AI 音视频互动方案/03-开发指南/` and `01-实时音视频/07-开发指南/`.
- **Client SDK API reference (per platform)**: `01-实时音视频/10-客户端 API 参考/`.
- **Server OpenAPI**: `01-实时音视频/11-服务端 API 参考/`.
- **Error codes / 错误码**: `01-实时音视频/12-常见问题/`.
- **Billing / 计费**: `01-实时音视频/03-产品计费/`.

## Maintaining the skill

The 248 PDFs are bundled inside `references/pdfs/` (~128MB, tracked via git LFS). To refresh:

1. Re-export the source PDF from [volcengine.com/docs/6348](https://www.volcengine.com/docs/6348) (right-click → "下载文档 PDF" on the doc-hub homepage). Save it to `~/Downloads/实时音视频_文档指南.pdf` or set `VERTC_SRC_PDF` to its path.
2. Regenerate everything:

   ```bash
   cd volcengine-rtc-docs

   # Optional: VERTC_SRC_PDF=/abs/path.pdf
   uvx --from pymupdf python scripts/split_pdf.py             # rewrites references/pdfs/
   uvx --from pymupdf python scripts/gen_toc_index.py references/toc-index.md
   ```

`scripts/split_pdf.py` uses `subset_fonts()` so each chunk stays small (~0.5MB avg, vs 62MB without subsetting). Don't drop that call — without it the 248 PDFs balloon to 15GB.

## Notes

- The original PDF was generated via WeasyPrint from the HTML docs — directly converting it to Markdown produces broken layout (tables shredded, columnar bullets misaligned). Reading the PDFs is more reliable than converting them. If you need Markdown for a specific page, scrape the live URL instead via firecrawl-cli with `--wait-for 5000`.
- The 25 pages skipped vs the original 10304 are 法律声明 + the auto-generated 目录, intentionally excluded.
