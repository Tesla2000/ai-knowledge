from __future__ import annotations

from typing import SupportsIndex


class LatexString(str):
    def replace(self, old: str, new: str, count: SupportsIndex = -1) -> LatexString:
        return LatexString(str.replace(self, old, new.replace("_", " "), count))
