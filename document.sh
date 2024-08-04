#!/bin/bash

while [[ $# -gt 0 ]]; do
    case $1 in
        --markdown-docs-path)
            MARKDOWN_DOCS_PATH="$2"
            shift 2
            ;;
        --language)
            LANGUAGE="$2"
            shift 2
            ;;
        --target-repo-path)
            TARGET_REPO_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

MARKDOWN_DOCS_PATH="${MARKDOWN_DOCS_PATH:-docs}"
LANGUAGE="${LANGUAGE:-English}"
TARGET_REPO_PATH="${TARGET_REPO_PATH:-$(pwd)}"

cd /home/tesla2000/PassionProjects/RepoAgent
.venv/bin/python repo_agent/main.py run --markdown-docs-path "$MARKDOWN_DOCS_PATH" --language "$LANGUAGE" --target-repo-path "$TARGET_REPO_PATH"
