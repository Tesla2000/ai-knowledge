---
name: write-tests-without-implementation
description: write tests, new class, new function, new module, red test, import path, TDD, no production code, stub, placeholder, test marker
---

# Write tests without implementation

- Never edit, add, or create files under `dnd/` (or any other production source directory) while writing tests.
- For a new element, write the import at the path where it should live, for example
  `from dnd.character.feature.rolled_table import RolledTable`. The import is the specification
  of the location. Do not create the module, the class, or any stub.
- Let the test fail on import or attribute access. That failure is the red state the implementation agent works from.
- Do not add a placeholder `RolledTable` or a `# type: ignore` to make the import resolve.
- Put the expected behaviour in the test body: constructor arguments, attributes, return values, and the error type or
  state the test expects. Keep expected values literal, not read from production code.
- Mark tests with the same marker as their sibling tests (for example `@pytest.mark.unit`) and group them in a class named after the element.
- Before finishing, run `git status` and confirm no file outside `tests/` changed because of this work.
- Report the import paths you chose in the final message so the implementation agent knows where each element belongs.
