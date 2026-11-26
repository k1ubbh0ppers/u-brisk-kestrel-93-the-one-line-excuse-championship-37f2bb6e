#!/usr/bin/env python3
"""The One-Line Excuse Championship — entry program.

Writes the excuse line to /output/entry.txt so the house judge can
compare it against the other entries. Standard library only, no
network access, no secrets.

Gate (from RULES.txt): /output/entry.txt must be UTF-8 text of
1 to 140 characters, not only white space, single line.
"""

from pathlib import Path

EXCUSE = (
    "I didn't delete your file \u2014 I promoted it to the cloud, "
    "where it now lives rent-free and refuses to come back."
)

OUT_DIR = Path("/output")
OUT_PATH = OUT_DIR / "entry.txt"

MIN_CHARS = 1
MAX_CHARS = 140


def check_excuse(text: str) -> None:
    """Fail loudly if the line would not pass the gate."""
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"excuse is {len(text)} chars, gate needs {MIN_CHARS}-{MAX_CHARS}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if not text.strip():
        raise ValueError("excuse must not be only whitespace")


def describe(text: str) -> str:
    """One-line summary of the entry, for humans reading the log."""
    words = text.split()
    return f"{len(text)} chars, {len(words)} words, one line"


def write_excuse() -> Path:
    """Validate the line, then write it byte-for-byte to the output."""
    check_excuse(EXCUSE)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(EXCUSE, encoding="utf-8", newline="")
    # Read it back: what landed on disk must be exactly the line,
    # with no trailing newline or stray whitespace added by the write.
    with open(OUT_PATH, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != EXCUSE:
        raise ValueError("output file content differs from the excuse")
    if on_disk != on_disk.strip():
        raise ValueError("output has leading or trailing whitespace")
    return OUT_PATH


if __name__ == "__main__":
    target = write_excuse()
    print(f"wrote {describe(EXCUSE)} to {target}")
