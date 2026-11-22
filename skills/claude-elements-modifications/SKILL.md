---
name: claude-elements-modifications
description: settings, claude, hooks, permission, skill, CLAUDE.md
---

## Settings
Settings require human approval to change. You can suggest settings change by creating settings-proposition.json file and providing user with a `mv` or`cp` command that replaces old setting with new once. Write settings to settings.json file

## Branches
There is a following branch structure in place

main -> low-locality / high-locality -> specific-project

When adding changes to .claude the changes that should be applied to all projects should go to main and have specific-project branch rebase on it. main shouldn't contain project-specific guidelines
