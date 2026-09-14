#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把目录下的文本文件重新读写一遍，统一成 UTF-8 编码 + LF 换行。

原理：
    以二进制方式读入 -> 用 UTF-8 解码 -> 把 CRLF(\r\n) 和单独的 CR(\r)
    归一成 LF(\n) -> 再以 UTF-8 编码写回。
    等价于“用文本模式打开再原样保存”，但更可控、更安全。

用法：
    python3 normalize_text.py /path/to/dir
    python3 normalize_text.py /path/to/dir -r -e txt,md,py
    python3 normalize_text.py /path/to/dir -r -n      # 只预览，不写入
"""

import argparse
import sys
from pathlib import Path


def convert_file(path: Path, *, dry_run: bool = False) -> tuple[str, str]:
    """处理单个文件。

    返回 (状态, 说明)，状态取值：
        converted / clean / binary / not-utf8 / error
    """
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return "error", str(exc)

    # 含 NUL 字节的基本可以认定是二进制文件，跳过
    if b"\x00" in raw:
        return "binary", "疑似二进制文件"

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return "not-utf8", f"不是合法 UTF-8（{exc.reason}，偏移 {exc.start}）"

    # 模拟 universal newlines：\r\n 和孤立的 \r 都归一成 \n
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    new_raw = normalized.encode("utf-8")

    if new_raw == raw:
        return "clean", "已经是 UTF-8 + LF"

    if dry_run:
        return "converted", "需要转换（dry-run，未写入）"

    try:
        # 文本模式写回；newline="\n" 表示不做任何换行翻译
        with path.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(normalized)
    except OSError as exc:
        return "error", str(exc)

    return "converted", "已转换为 UTF-8 + LF"


def iter_targets(root: Path, recursive: bool, extensions: set[str] | None):
    """遍历 root 下待处理的文件。"""
    pattern = "**/*" if recursive else "*"
    for path in sorted(root.glob(pattern)):
        if not path.is_file() or path.is_symlink():
            continue
        if extensions is not None and path.suffix.lower() not in extensions:
            continue
        yield path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="把文本文件重新读写一遍，统一为 UTF-8 + LF 换行（去掉 Windows 的 \\r\\n）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", type=Path, help="要处理的目录或单个文件")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="递归处理子目录")
    parser.add_argument("-e", "--extensions", metavar="EXT",
                        help="只处理指定扩展名，逗号分隔，例如 txt,md,py")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="只列出会被改动的文件，不实际写入")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="不逐个打印文件名，只输出汇总")

    args = parser.parse_args(argv)

    root: Path = args.path
    if not root.exists():
        print(f"路径不存在：{root}", file=sys.stderr)
        return 2

    extensions: set[str] | None = None
    if args.extensions:
        extensions = set()
        for item in args.extensions.split(","):
            item = item.strip().lower()
            if item:
                extensions.add(item if item.startswith(".") else "." + item)
        if not extensions:
            extensions = None

    if root.is_file():
        targets = [root]
    else:
        targets = list(iter_targets(root, args.recursive, extensions))

    counts = {"converted": 0, "clean": 0, "binary": 0, "not-utf8": 0, "error": 0}

    for path in targets:
        status, detail = convert_file(path, dry_run=args.dry_run)
        counts[status] += 1

        if args.quiet:
            continue
        if status == "converted":
            prefix = "[dry-run] " if args.dry_run else ""
            print(f"{prefix}转换: {path}")
        elif status in ("error", "not-utf8"):
            print(f"跳过: {path} —— {detail}", file=sys.stderr)

    verb = "待转换" if args.dry_run else "已转换"
    print(
        f"\n扫描 {len(targets)} 个文件 | {verb} {counts['converted']} | "
        f"无需改动 {counts['clean']} | 二进制 {counts['binary']} | "
        f"非 UTF-8 {counts['not-utf8']} | 出错 {counts['error']}"
    )
    return 1 if counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
