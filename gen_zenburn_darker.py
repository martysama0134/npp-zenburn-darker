#!/usr/bin/env python3
# Copyright (c) 2026, martysama0134
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# Neither the name of martysama0134 nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
