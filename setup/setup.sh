#!/usr/bin/env bash
set -e

git init
git branch -M main
git add .

uv sync
pre-commit install --hook-type pre-commit --hook-type pre-push
pre-commit autoupdate

git commit -m "Initial commit"