---
name: subraces-scraper
description: TDD workflow for dnd subraces. Build and fix the subrace scraper, scrape the wiki to a cache, map every subrace class to its scraped section, write red unit tests under tests/unit/subraces, then stop and wait for the user's approval before any implementation. Use when subrace scrapes, subrace classes or their tests change.
---

# Subraces TDD

This skill produces failing tests for the subrace classes. It does not implement them. The handoff is the red suite: the user reviews it, approves, and another agent writes the implementation in `dnd/`.

## Rules

- Never edit `dnd/`. Not to make a test pass, not to fix a darkvision value, not to add a missing class.
- The scraper in `tools/subraces_scraper/` may be changed when the scrape is wrong. Update its README in the same change.
- Tests live under `tests/unit/subraces/` only.
- Never use `xfail`, `skip`, or `# pragma: no cover` to hide a mismatch. A mismatch is a red test.
- A class with no scraped section gets no test. Report it by name. Do not invent a value.
- Only add a manual map entry when the variant text is already in a scraped section. Check the text first.

## Step 1: Build the scraper

- Run the scraper's tests if they exist and keep them passing.
- The scraper is `tools/subraces_scraper`. The README at `tools/subraces_scraper/README.md` describes the output format and scope.

## Step 2: Scrape to cache

From the repo root:

```bash
PYTHONPATH=tools .venv/bin/python -m subraces_scraper --output .scrape_cache/subraces.txt
```

- `.scrape_cache/` is gitignored and `--output` creates the directory.
- Expect 216 sections (`grep -c '^Source: ' .scrape_cache/subraces.txt`). Report any other count.
- Each block is `<name>`, `Source: <url>`, then text. Names are `<Title> (<Source>)`, or `<Race> (<Source>)` for a lineage with no h2 subraces.
- Each h2 subrace's text includes its source's base traits, so darkvision the base states is already in the block.

## Step 3: Map each class to its section

- A class is `<Title><Source>Race` in `dnd.character.subrace`. Match on lowercase alphanumerics of title plus source. Also try `<Race> <Title>`, `<Title> <Race>`, and the reversed qualifier form (`Genasi (Air)` → `Air Genasi`).
- Where the wiki source differs from the code source (for example the code says Mordenkainen Presents and the wiki says Eberron), map by hand and check the text before accepting it.
- Some variants sit inside another section: Devil's Tongue, Feral, Hellfire and Winged are in `Variant Tiefling (Sword Coast Adventurer's Guide)`, and Gruul and Selesnya are in `Centaur (Guildmaster's Guide to Ravnica)`. Map those classes to the section that holds them.
- Expected darkvision is the darkvision in the matched block. If the block states none, use the core race's darkvision from its Player's Handbook lineage page.
- Report every class with no section, by name, and every manual mapping, with the text that justified it.

Expect 138 matched classes: 128 that agree with the code and 10 darkvision mismatches.

## Step 4: Write the tests (red)

- `tests/unit/subraces/_subrace_case.py` holds `SubraceTestCase`. Each subrace gets `tests/unit/subraces/test_<snake_class>.py` with `class Test<Name>(SubraceTestCase)`, `@pytest.mark.unit`, and the attributes `subrace`, `race` and `DARKVISION`. The attributes are required, not defaulted.
- The expected value is the scraped darkvision. Do not change it to match the code.
- Each test file is generated from the map, so the output is repeatable. Format and lint with `uvx ruff format tests/unit/subraces` and `uvx ruff check --fix tests/unit/subraces`.

## Step 5: Verify red

```bash
.venv/bin/python -m pytest tests/unit/subraces -p no:cacheprovider --no-cov -q
```

- Expect the mismatches to fail and everything else to pass. The current run is 10 failed and 404 passed.
- Each failure must be a darkvision assertion. Any other failure is a bug in the tests or the scraper; fix it before stopping.
- Check the failing set matches the mismatches listed in step 3.

## Step 6: Stop for approval

Report to the user, then stop:

- The scrape count and the cache path.
- The matched count, the unmatched classes by name, and the manual mappings.
- The red tests by name, each with its scraped and expected darkvision.

Do not write any implementation. Wait for the user to approve. Once approved, the implementation goes to another agent, not to this skill.
