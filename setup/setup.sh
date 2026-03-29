#!/usr/bin/env bash
set -e

git init
git branch -M main

pre-commit autoupdate
uv sync

git add .
git commit -m "Initial commit"

pre-commit install --hook-type pre-commit --hook-type pre-push  # don't run on initial commit due to vulture env issue
