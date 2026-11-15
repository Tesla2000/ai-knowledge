---
name: subraces-scraper
description: Write unit tests for every dnd subrace class from the scraped subrace pages in tests/unit/subraces, mapping each class to its scraped section. Use when subrace scrapes, subrace classes or their tests change.
---

# Subraces tests

This skill adds tests only. The scraper in `tools/subraces_scraper` and the code in `dnd/` are not changed to make a class match. Do not edit either to get a test to pass or to pick up a missing section.

## Scope rules

- Write tests under `tests/unit/subraces/`. Never edit `tools/subraces_scraper/` or `dnd/`.
- A class with no scraped section gets no test. Report it by name. Do not invent a value, do not add a scraper rule, and do not write code to fill the gap. Changing the scraper needs the user's go-ahead.
- Only add a manual map entry when the variant text is already in a scraped section. Check the text first.

## Scrape

- Run from the repo root: `PYTHONPATH=tools .venv/bin/python -m subraces_scraper --output <path>`. The default `--section` is `toc2` (Lineages). The tool's README is `tools/subraces_scraper/README.md`.
- Each block is `<name>`, `Source: <url>`, then text. Names are `<Title> (<Source>)`. A lineage with one entry and no h2 subraces is `<Race> (<Source>)`, for example Orc or Tabaxi.
- Each h2 subrace's text includes its source's base traits, so darkvision the base states is already in the block.

## Map a class to its section

- A class is `<Title><Source>Race` in `dnd.character.subrace`. Match by lowercase alphanumerics of title+source. Also try `<Race> <Title>`, `<Title> <Race>` and the reversed qualifier form (`Genasi (Air)` → `Air Genasi`).
- Where the wiki's source differs from the code's (e.g. code says Mordenkainen Presents, wiki says Eberron), map by hand. Check the text before accepting the match.
- Some variants sit inside another section, not their own: Devil's Tongue, Feral, Hellfire and Winged are in `Variant Tiefling (Sword Coast Adventurer's Guide)`, and Gruul and Selesnya are in `Centaur (Guildmaster's Guide to Ravnica)`. Map those classes to the section that holds them.
- Expected darkvision is the darkvision in the matched block. If the block states none, use the core race's darkvision from its Player's Handbook lineage page.

## Tests

- `tests/unit/subraces/_subrace_case.py` holds `SubraceTestCase`. Each subrace gets `tests/unit/subraces/test_<snake_class>.py` with `class Test<Name>(SubraceTestCase)`, `@pytest.mark.unit`, and the attributes `subrace`, `race` and `DARKVISION`. Attributes are required, not defaulted.
- A mismatch between the wiki and the code is an xfail, not a code change and not a changed expectation. Override `test_grants_its_darkvision` with `@pytest.mark.xfail(strict=True, reason=...)` and call `super()`. The reason states the scraped value and the code value.
- Do not add `# pragma: no cover`. Coverage is 100% for the full suite, so flag any uncovered branch to the user instead.

## Run

- `.venv/bin/python -m pytest tests/unit/subraces tests/unit/test_subraces.py`
- Format and lint the test files with `uvx ruff format` and `uvx ruff check --fix` (pre-commit uses ruff).
- Check coverage of the full suite before reporting it. Running a subset does not reach 100%.
