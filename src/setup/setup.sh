#!/usr/bin/env bash
set -e

git init
git branch -M main

uv sync

uv run pre-commit autoupdate

git add .
git commit -m "Initial commit"

git subtree add --prefix=knowledge git@github.com:Tesla2000/ai-knowledge.git main --squash

uv run pre-commit install --hook-type pre-commit --hook-type pre-push
