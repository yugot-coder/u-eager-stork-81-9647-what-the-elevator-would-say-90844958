"""What the Elevator Would Say — entry program (make.fun, program/v1).

Writes the funniest one line a talking elevator could say to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

Standard library only: the grader installs nothing.
"""

import hashlib
import os
import sys

# The line, chosen from CANDIDATES.md (candidate 6). 79 characters.
LINE = "The music in here isn't for you. It's so I don't have to listen to you breathe."

MAX_CHARS = 120


def output_path() -> str:
    """Where the entry text goes."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def check() -> int:
    """Re-read the written entry and verify it byte-for-byte.

    Checks the gate the sealed scorer applies: UTF-8 text, 1-120
    characters, not only whitespace, and identical to LINE.
    """
    path = output_path()
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except FileNotFoundError:
        print(f"check failed: {path} does not exist", file=sys.stderr)
        return 1
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("check failed: entry.txt is not valid UTF-8", file=sys.stderr)
        return 1
    if not (1 <= len(text) <= MAX_CHARS):
        print(f"check failed: {len(text)} chars, must be 1-{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("check failed: entry is only whitespace", file=sys.stderr)
        return 1
    digest = hashlib.sha256(raw).hexdigest()
    expected = hashlib.sha256(LINE.encode("utf-8")).hexdigest()
    if digest != expected:
        print(f"check failed: sha256 {digest} != expected {expected}",
              file=sys.stderr)
        return 1
    print(f"check OK: {path} ({len(text)} chars, sha256 {digest})")
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return check()
    text = LINE
    if not (1 <= len(text) <= MAX_CHARS):
        print(f"entry is {len(text)} chars, must be 1-{MAX_CHARS}", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(f"wrote {path} ({len(text)} chars, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
