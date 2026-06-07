from __future__ import annotations


class LatexString(str):
    def replace(self, old, new, count=-1):
        return LatexString(
            str.replace(self, old, new.replace("_", " "), count)
        )
