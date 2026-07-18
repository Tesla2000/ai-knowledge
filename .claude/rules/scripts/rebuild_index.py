"""Rebuild index.md from topics/ directory."""

import re
import sys
from pathlib import Path


class IndexRebuilder:
    """Rebuilds index.md by scanning all markdown files under topics/."""

    _ROOT = Path(__file__).parent.parent
    _TOPICS_DIR = _ROOT / "topics"
    _INDEX_FILE = _ROOT / "index.md"

    @staticmethod
    def _extract_title(text: str) -> str:
        match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        return match.group(1).strip() if match else "Untitled"

    @staticmethod
    def _extract_summary(text: str) -> str:
        lines = text.splitlines()
        in_body = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#"):
                in_body = True
                continue
            if in_body and stripped and not stripped.startswith("#"):
                return stripped
        return ""

    @classmethod
    def _collect_entries(cls) -> list[tuple[str, str, str]]:
        files = sorted(cls._TOPICS_DIR.rglob("*.md"))
        entries = []
        for path in files:
            text = path.read_text(encoding="utf-8")
            title = cls._extract_title(text)
            summary = cls._extract_summary(text)
            rel = path.relative_to(cls._ROOT).as_posix()
            entries.append((title, rel, summary))
        return entries

    @classmethod
    def rebuild(cls) -> None:
        entries = cls._collect_entries()
        rows = "\n".join(
            f"| [{title}]({rel}) | {summary} |" for title, rel, summary in entries
        )
        content = f"# Knowledge Base Index\n\n| File | Summary |\n|------|---------|\n{rows}\n"
        cls._INDEX_FILE.write_text(content, encoding="utf-8")
        sys.stdout.write(f"index.md updated with {len(entries)} entries.")


if __name__ == "__main__":
    IndexRebuilder.rebuild()
