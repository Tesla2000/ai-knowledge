from pathlib import Path
from typing import Literal

from src.files._base import FileBase
from src.files._types import FileType


class ClaudeSettings(FileBase):
    type: Literal[FileType.CLAUDE_SETTINGS] = FileType.CLAUDE_SETTINGS
    relative_path: Path = Path(".claude/settings.json")
    content: str = """\
{
  "permissions": {
    "deny": [
      "Write(./.pre-commit-config.yaml)",
      "Edit(./.pre-commit-config.yaml)",
      "Write(./pyproject.toml)",
      "Edit(./pyproject.toml)",
      "Read(./.env)",
      "Bash(cat .env)"
    ]
  },
  "sandbox": {
    "enabled": true,
    "network": {
      "allowedDomains": [
        "api.anthropic.com",
        "github.com",
        "*.github.com",
        "*.githubusercontent.com",
        "pypi.org",
        "files.pythonhosted.org",
        "registry.npmjs.org"
      ]
    }
  }
}
"""
