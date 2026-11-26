#!/usr/bin/env python3
"""Entrypoint for news-image-20261125.

Copies entry.png (the poster drawn by draw_poster.py, shipped in this
repository) to the output directory, checks the copy is at most 1 MiB,
and verifies the copy is byte-identical to the source via sha256.

Stdlib only. No network. Deterministic: the same input always produces
the same output bytes.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1048576
ENTRY_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_dir, ENTRY_NAME)
    if not os.path.isfile(source):
        print(f"error: {ENTRY_NAME} not found next to main.py", file=sys.stderr)
        return 1
    if os.path.getsize(source) > MAX_BYTES:
        print(f"error: source {ENTRY_NAME} is over the 1 MiB limit",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, ENTRY_NAME)

    shutil.copyfile(source, dest)

    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        print(f"error: {ENTRY_NAME} is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1

    src_hash = sha256_of(source)
    dst_hash = sha256_of(dest)
    if src_hash != dst_hash:
        print("error: output sha256 does not match source", file=sys.stderr)
        return 1

    print(f"wrote {dest} ({size} bytes, sha256 {dst_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
