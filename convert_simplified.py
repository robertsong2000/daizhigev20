#!/usr/bin/env python3
"""殆知阁全库繁→简转换: daizhige/ → daizhige-simplified/（保留目录结构，仅处理 .txt）"""
import os
import sys
from multiprocessing import Pool
from pathlib import Path

from opencc import OpenCC

SRC = Path("/home/robertsong/workspace/claude/daizhige")
DST = Path("/home/robertsong/workspace/claude/daizhige-simplified")
CC = OpenCC("t2s")


def convert(src: Path):
    dst = DST / src.relative_to(SRC)
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        try:
            text = src.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = src.read_text(encoding="gb18030")  # ponytail: 个别文件非 UTF-8，按 GBK 家族兜底
        dst.write_text(CC.convert(text), encoding="utf-8")
        return None
    except Exception as e:
        return f"{src.relative_to(SRC)}: {e}"


def main():
    files = sorted(p for p in SRC.rglob("*.txt") if ".venv" not in p.parts)
    total = len(files)
    print(f"共 {total} 个 txt，{os.cpu_count()} 进程启动", flush=True)
    errors = []
    done = 0
    with Pool(os.cpu_count()) as pool:
        for err in pool.imap_unordered(convert, files, chunksize=20):
            done += 1
            if err:
                errors.append(err)
            if done % 500 == 0 or done == total:
                print(f"[{done}/{total}]", flush=True)
    if errors:
        print(f"\n{len(errors)} 个失败:")
        for e in errors:
            print(" ", e)
    else:
        print("\n全部成功")


if __name__ == "__main__":
    sys.exit(main())
