#!/usr/bin/env python3
"""
Zenburn color remapper:
- Opens Zenburn.xml
- Replaces specified hex colors (case-insensitive)
- Saves as Zenburn_Darker.xml

Notes:
- Only exact hex strings are replaced (e.g., 3F3F3F -> 1F1F1F).
- Preserves the original casing style of each matched hex:
  - if original is lowercase -> replacement becomes lowercase
  - if original is UPPERCASE -> replacement becomes UPPERCASE
  - if mixed -> replacement is written as given in the table
"""

from __future__ import annotations

import re
from pathlib import Path


COLOR_MAP = {
    # general
    "3F3F3F": "1F1F1F",
    "FFCFAF": "FF9980",
    "DFC47D": "FEB183",
    "CEDF99": "E4E792",
    "8CD0D3": "7EE0DE",
    "CC9393": "DC8383",
    "9F9D6D": "808040",
    "C89191": "DC8383",
    "DCA3A3": "DC8383",
    "E3CEAB": "FEB183",
    # diff only
    "CFBFAF": "FF0000",
    "FEB183": "00FF40",
}

HEX_RE = re.compile(r"[0-9A-Fa-f]{6}")


def apply_case_style(original: str, replacement: str) -> str:
    """Match replacement hex casing to original token casing where reasonable."""
    if original.islower():
        return replacement.lower()
    if original.isupper():
        return replacement.upper()
    return replacement  # mixed case -> keep table casing


def remap_colors(xml_text: str) -> str:
    """Replace any 6-digit hex tokens found in COLOR_MAP (case-insensitive)."""

    def repl(match: re.Match) -> str:
        token = match.group(0)
        key = token.upper()
        if key not in COLOR_MAP:
            return token
        return apply_case_style(token, COLOR_MAP[key])

    return HEX_RE.sub(repl, xml_text)


def main() -> None:
    src = Path("Zenburn.xml")
    dst = Path("Zenburn_Darker.xml")

    if not src.exists():
        raise FileNotFoundError(f"Input file not found: {src.resolve()}")

    original = src.read_text(encoding="utf-8")
    updated = remap_colors(original)

    dst.write_text(updated, encoding="utf-8")
    print(f"Saved: {dst.resolve()}")


if __name__ == "__main__":
    main()
