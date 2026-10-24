#!/usr/bin/env python3
"""Fetch the pinned 9bie upstream.

The upstream repository has no explicit license, so its source is not vendored
and no patch file is redistributed. This script only clones the pinned commit.
The toolkit applies the SNI fix and the heap-parameter overrides in place at
runtime; the same changes are documented in docs/upstream-changes.md for manual
use.

Usage:
    python3 tools/bootstrap_upstream.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "vendor" / "php2shell-upstream"
URL = "https://github.com/9bie/php2shell-bypass-aslr-exp.git"
PIN = "4586f5c"


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def main() -> int:
    if VENDOR.exists() and not (VENDOR / ".git").is_dir():
        print(f"{VENDOR} exists but is not a git checkout; remove it and retry", file=sys.stderr)
        return 2
    if not (VENDOR / "exploit.py").is_file():
        VENDOR.parent.mkdir(parents=True, exist_ok=True)
        print(f"cloning {URL}")
        result = run(["git", "clone", URL, str(VENDOR)], check=False)
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            return result.returncode
    result = run(["git", "-C", str(VENDOR), "checkout", PIN], check=False)
    if result.returncode != 0:
        print(f"cannot checkout {PIN}: {result.stderr.strip()}", file=sys.stderr)
        return result.returncode
    print(f"upstream ready: {VENDOR}")
    print("runtime changes: docs/upstream-changes.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
