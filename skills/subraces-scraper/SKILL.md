---
name: subraces-scraper
description: Scrape every D&D 5e subrace page with tools/subraces_scraper, map each dnd subrace class to its scraped section, and write its unit test in tests/unit/subraces. Use when subrace scrapes, subrace classes or their tests change.
---

# Subraces scraper and tests

Every class in `dnd.character.subrace.__all__` must have a scraped section and a test. A class with no section is a gap to fix, not a case to skip.

## Scrape

- Run from the repo root: `PYTHONPATH=tools .venv/bin/python -m subraces_scraper --output <path>`. The default `--section` is `toc2` (Lineages). The tool's README is `tools/subraces_scraper/README.md`.
- Each block is `<name>`, `Source: <url>`, then text. Names are `<Title> (<Source>)`.
- Pages scraped:
  - Every lineage linked from `toc2`, plus `UNLISTED` in `_scraper.py` (Kalashtar, Leonin, Warforged), which the index does not link.
  - A lineage with no h2 subraces is one entry: `<Lineage> (<Source>)`. This covers Orc and Tabaxi.
  - A source with text before its first h2 is also the standard lineage: `Human (Player's Handbook)`.
  - A page with no h1 (Grung, Verdan) is one entry named from its `Source:` line.
- Each h2 subrace's text includes its source's base traits, so darkvision the base states is already in the block.

## Find a class with no section

Look for the class's variant text in the scrape before deciding it has no source. The wiki often puts variants inside another section: Devil's Tongue, Feral, Hellfire and Winged are in `Variant Tiefling (Sword Coast Adventurer's Guide)`, and Gruul and Selesnya are in `Centaur (Guildmaster's Guide to Ravnica)`.

- Search the scraped text with the class's distinctive word, for example `grep -l "Devil" <scrape>`.
- If the variant is in a section, map the class to that section.
- If no page has it, the class has no source. Report it. Do not invent a value.

## Map a class to its section

- A class is `<Title><Source>Race` in `dnd.character.subrace`. Match by lowercase alphanumerics of title+source. Also try `<Race> <Title>`, `<Title> <Race>` and the reversed qualifier form (`Genasi (Air)` → `Air Genasi`).
- Where the wiki's source differs from the code's (e.g. code says Mordenkainen Presents, wiki says Eberron), map by hand. Check the text before accepting the match.
- Expected darkvision is the darkvision in the matched block. If the block states none, use the core race's darkvision from its Player's Handbook lineage page.

## Tests

- `tests/unit/subraces/_subrace_case.py` holds `SubraceTestCase`. Each subrace gets `tests/unit/subraces/test_<snake_class>.py` with `class Test<Name>(SubraceTestCase)`, `@pytest.mark.unit`, and the attributes `subrace`, `race` and `DARKVISION`. Attributes are required, not defaulted.
- A mismatch between the wiki and the code is an xfail, not a code change and not a changed expectation. Override `test_grants_its_darkvision` with `@pytest.mark.xfail(strict=True, reason=...)` and call `super()`. The reason states the scraped value and the code value.
- Do not add `# pragma: no cover`. Coverage is 100% for the full suite, so flag any uncovered branch to the user instead.

## Run

- `.venv/bin/python -m pytest tests/unit/subraces tests/unit/test_subraces.py`
- Format and lint with `uvx ruff format` and `uvx ruff check --fix` on the touched paths (pre-commit uses ruff).
- Check coverage of the full suite before reporting it. Running a subset does not reach 100%.
