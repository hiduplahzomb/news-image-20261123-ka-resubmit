#!/usr/bin/env python3
"""Entrypoint for the news-image-20261123 make.fun entry.

Copies the pre-rendered dashboard image (entry.png, drawn by
draw_dashboard.py) to the grader's output directory. Standard
library only; deterministic: the same bytes are written on every run.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The grader runs the program twice and both runs must write the
    # same bytes, so confirm the copy is complete.
    assert os.path.getsize(dst) == os.path.getsize(src), "short copy"


if __name__ == "__main__":
    main()
