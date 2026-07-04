#!/usr/bin/env bash
set -e

git init
git branch -M main

uv sync

uv run pre-commit autoupdate

git add .
git commit -m "Initial commit"

uv run pre-commit install --hook-type pre-commit --hook-type pre-push
