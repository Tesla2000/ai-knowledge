from pathlib import Path
from typing import Literal

from src.files._base import FileBase
from src.files._types import FileType


class ClaudeReviewWorkflow(FileBase):
    type: Literal[FileType.CLAUDE_REVIEW_WORKFLOW] = (
        FileType.CLAUDE_REVIEW_WORKFLOW
    )
    relative_path: Path = Path(".github/workflows/claude.yml")
    content: str = """\
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]
  issue_comment:
    types: [created]

jobs:
  claude-review:
    if: |
      github.event_name == 'pull_request' ||
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude'))
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: anthropics/claude-code-action@v1

"""
