"""Split big PDF by TOC outline into many smaller PDFs.

Folder layout:  <out>/<L1_idx>-<L1_name>/<L2_idx>-<L2_name>/<L3_idx>-<L3_name>.pdf
Skips L1 entries listed in SKIP_TITLES (legal notice, generated TOC).
For TOC entries with no SPLIT_LEVEL descendant, they become a leaf PDF
under their parent folder.
"""

import os
import re
import time
import pymupdf

# Source PDF — exported from volcengine.com/docs/6348 ("下载文档 PDF" on the doc-hub homepage).
# Override via env var when the file lives elsewhere: VERTC_SRC_PDF=/abs/path.pdf uvx ...
SRC = os.path.expanduser(os.environ.get("VERTC_SRC_PDF", "~/Downloads/实时音视频_文档指南.pdf"))
# Output goes inside this skill so PDFs and the TOC index ship together.
# Run from the skill root: `cd volcengine-rtc-docs && uvx --from pymupdf python scripts/split_pdf.py`
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "pdfs")
SKIP_TITLES = {"法律声明", "目录"}
SPLIT_LEVEL = 3


def sanitize(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|\r\n\t]", "_", name).strip()
    return re.sub(r"\s+", " ", name)[:120] or "untitled"


def strip_numeric_prefix(title: str) -> str:
    return re.sub(r"^[\d.]+\s*", "", title).strip()


def main():
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

    chunks = []  # (rel_path, start, end, title)
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
            has_child = any(toc[j][0] > 1 for j in range(i + 1, n) if toc[j][2] <= ends[i])
            if not has_child:
                fname = f"00-{sanitize(clean)}.pdf"
                chunks.append((os.path.join(cur_l1_path, fname), page, ends[i], title))
            continue
        if skipping_l1:
            continue
        if level == 2:
            l3_idx = 0
            l2_idx += 1
            cur_l2_path = f"{l2_idx:02d}-{sanitize(clean)}"
            has_child = any(toc[j][0] >= 3 for j in range(i + 1, n) if toc[j][2] <= ends[i])
            if not has_child:
                fname = f"{l2_idx:02d}-{sanitize(clean)}.pdf"
                chunks.append((os.path.join(cur_l1_path, fname), page, ends[i], title))
            continue
        if level == SPLIT_LEVEL:
            l3_idx += 1
            fname = f"{l3_idx:02d}-{sanitize(clean)}.pdf"
            chunks.append((os.path.join(cur_l1_path, cur_l2_path, fname), page, ends[i], title))
            continue

    print(f"Planned {len(chunks)} PDFs covering {sum(c[2]-c[1]+1 for c in chunks)} pages")
    os.makedirs(OUT, exist_ok=True)

    t0 = time.time()
    for idx, (rel, start, end, title) in enumerate(chunks, 1):
        out_path = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        sub = pymupdf.open()
        sub.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
        # Set the chunk's own metadata title for nicer reader display
        sub.set_metadata({"title": title})
        sub.subset_fonts()
        sub.save(out_path, garbage=4, deflate=True, clean=True)
        sub.close()
        if idx % 25 == 0 or idx == len(chunks):
            print(f"[{idx}/{len(chunks)}] {rel}")

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s. Output: {OUT}")


if __name__ == "__main__":
    main()
