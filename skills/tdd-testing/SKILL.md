---
name: tdd-testing
description: TDD, red tests, scraped data, scrape cache, .scrape_cache, test case base class, expected values, assertion per sentence, class per concept, choice, mixin, rolled table, approval gate
---

# TDD tests from scraped data

## Reference

- Follow the file layout of `tests/unit/backgrounds/`: `_background_case.py`, the helpers `_rolls.py` and `_choices.py`, and one `test_<background>.py` per background.
- For import paths of elements that do not exist yet, follow `write-tests-without-implementation`.

## Order

1. The scraper and its README, in `tools/<domain>_scraper/`, committed on its own. Writing or fixing it is a separate task, not part of writing tests.
2. The scrape, written to `.scrape_cache/`. Read the scraper's README for the output format.
3. The tests (red), committed on their own.
4. The implementation, by another session, after the user approves the tests.

## Map every piece of the scrape

- Go through each element's scraped text sentence by sentence. Every rule, number, choice, table and named thing in it becomes an assertion. Nothing in the text is left without one.
- Give each distinct concept in the text its own class, not a string, dict or flag: each table row, each feature, each item, each choice option. For example, each bond row is its own class with its own test in `tests/unit/bond/`.
- Assert a choice both ways: each allowed pick is granted, and a pick outside the options is rejected.
- Assert a rolled table on every face.
- When the tests are written, re-read each element's scraped text and check that every sentence stating logic has an assertion. Report any sentence you could not turn into one.
``
## Shared test case

- Put one base class in `tests/unit/<domain>/_<domain>_case.py`, holding every test that all elements share.
- A section that only some scraped pages have becomes a mixin class with its own test. Mix it in only for elements whose page has that section.
- Put shared helpers in sibling private modules, for example a patched dice roll in `_rolls.py`.

## One test file per element

- Each scraped element gets `tests/unit/<domain>/test_<element>.py` with `class Test<Element>(<mixins>, <Domain>TestCase)`.
- The expected values in that class come from that element's scraped text, written as literals.
- Tests that only one element needs, such as rejecting an invalid choice, go in that element's class.

## Nested elements

- A value that is an element in its own right, such as one row's text in a rolled table, gets its own test file in its own domain directory, for example `tests/unit/bond/test_<row>.py`.
- A table that many elements have is rolled by a mixin in the shared case, for example `BondsCase`.
- A table that only a few elements offer gets `tests/unit/<table>/test_<table>_table.py`, next to its rows. It is parametrized over the sources that offer it, patches the roll for each face, and checks that the right row comes back.

## Verify and stop

- Run the new tests once and save the output to a file. Read the saved file.
- Report any sentence of the scrape without an assertion, the import path chosen for each new class, and the output file. Then stop and wait for approval.
