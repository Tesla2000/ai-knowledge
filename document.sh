#!/bin/bash

# Default values if arguments are not provided
MARKDOWN_DOCS_PATH="${MARKDOWN_DOCS_PATH:-docs}"
LANGUAGE="${LANGUAGE:-English}"
TARGET_REPO_PATH="${TARGET_REPO_PATH:-$(pwd)}"

cd /home/tesla2000/PassionProjects/RepoAgent
.venv/bin/python repo_agent/main.py run --markdown-docs-path "$MARKDOWN_DOCS_PATH" --language "$LANGUAGE" --target-repo-path "$TARGET_REPO_PATH"
