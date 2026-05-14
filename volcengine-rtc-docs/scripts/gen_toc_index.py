"""Regenerate references/toc-index.md from the source PDF.

Run with:  uvx --from pymupdf python scripts/gen_toc_index.py

Override the source PDF path via env var:  VERTC_SRC_PDF=/abs/path.pdf uvx ...
"""
import os
import re
import sys
import pymupdf

# Source PDF — exported from volcengine.com/docs/6348 ("下载文档 PDF" on the doc-hub homepage).
SRC = os.path.expanduser(os.environ.get("VERTC_SRC_PDF", "~/Downloads/实时音视频_文档指南.pdf"))
SKIP_TITLES = {"法律声明", "目录"}
SPLIT_LEVEL = 3


def sanitize(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|\r\n\t]", "_", name).strip()
    return re.sub(r"\s+", " ", name)[:120] or "untitled"


def strip_numeric_prefix(title: str) -> str:
    return re.sub(r"^[\d.]+\s*", "", title).strip()


def build_index():
    doc = pymupdf.open(SRC)
    toc = doc.get_toc()
    total = doc.page_count
    n = len(toc)

    ends = [total] * n
    for i in range(n):
        lvl_i = toc[i][0]
        for j in range(i + 1, n):
            if toc[j][0] <= lvl_i:
                ends[i] = toc[j][2] - 1
                break

    real_l1 = [t for t in toc if t[0] == 1 and strip_numeric_prefix(t[1]) not in SKIP_TITLES]
    l1_index_map = {id(t): i + 1 for i, t in enumerate(real_l1)}

    lines = ["# 火山引擎 RTC 文档 TOC 索引",
             "",
             "本索引列出 ~248 份切分 PDF 的相对路径（相对本文件位置）与页数。",
             "PDF 实体存放于本 skill 的 `references/pdfs/` 子目录。",
             ""]
    cur_l1_path = None
    cur_l2_path = None
    l1_idx = 0
    l2_idx = 0
    l3_idx = 0
    skipping_l1 = False

    for i, (level, title, page) in enumerate(toc):
        clean = strip_numeric_prefix(title)
        if level == 1:
            l2_idx = 0
            l3_idx = 0
            if clean in SKIP_TITLES:
                skipping_l1 = True
                continue
            skipping_l1 = False
            l1_idx = l1_index_map[id(toc[i])]
            cur_l1_path = f"{l1_idx:02d}-{sanitize(clean)}"
            lines.append(f"\n## {l1_idx}. {clean}\n")
            has_child = any(toc[j][0] > 1 for j in range(i + 1, n) if toc[j][2] <= ends[i])
            if not has_child:
                fname = f"00-{sanitize(clean)}.pdf"
                rel = os.path.join("pdfs", cur_l1_path, fname)
                lines.append(f"- [{title}]({rel}) ({ends[i]-page+1}p)")
            continue
        if skipping_l1:
            continue
        if level == 2:
            l3_idx = 0
            l2_idx += 1
            cur_l2_path = f"{l2_idx:02d}-{sanitize(clean)}"
            lines.append(f"\n### {l1_idx}.{l2_idx} {clean}")
            has_child = any(toc[j][0] >= 3 for j in range(i + 1, n) if toc[j][2] <= ends[i])
            if not has_child:
                fname = f"{l2_idx:02d}-{sanitize(clean)}.pdf"
                rel = os.path.join("pdfs", cur_l1_path, fname)
                lines.append(f"- [{title}]({rel}) ({ends[i]-page+1}p)")
            continue
        if level == SPLIT_LEVEL:
            l3_idx += 1
            fname = f"{l3_idx:02d}-{sanitize(clean)}.pdf"
            rel = os.path.join("pdfs", cur_l1_path, cur_l2_path, fname)
            lines.append(f"- [{title}]({rel}) ({ends[i]-page+1}p)")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "references/toc-index.md"
    content = build_index()
    os.makedirs(os.path.dirname(out_path), exist_ok=True) if os.path.dirname(out_path) else None
    with open(out_path, "w") as f:
        f.write(content)
    print(f"wrote {out_path} ({len(content)} bytes)")
