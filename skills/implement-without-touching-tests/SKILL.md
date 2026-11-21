---
name: implement-without-touching-tests
description: implement, production code, make tests pass, red tests, tests/, do not edit tests, test files, assertions, parametrized values
---

# Implement without touching tests

- Never edit, add, rename, or delete files under `tests/`, and never change a test's
  parametrized values, expected results, assertions, or markers, to make it pass.
- If a test fails, the production code is wrong or incomplete. Fix the production code.
- Only touch test files when the user explicitly asks for it in the current request.
- If a test looks wrong, say so and stop. Do not change it yourself.
- Do not patch around a failing test (for example by patching the code under test or
  the test's inputs) to hide the failure. Make the production behavior match what the test asks for.
- Before finishing, run `git status` and confirm no file under `tests/` was changed by you.
