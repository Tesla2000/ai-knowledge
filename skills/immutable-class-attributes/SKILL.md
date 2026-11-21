---
name: immutable-class-attributes
description: ClassVar, immutable, reassign, in-place write, dict in ClassVar, class attribute, instance assignment, pytest.raises, description, tables, race, statistic, priority
---

# Immutable class attributes

`ClassVar` is a type hint only. It does not stop runtime assignment, so a `ClassVar` can be
reassigned on the class (`Sample.description = "x"`) even when pydantic blocks it on an instance.
A dict in a `ClassVar` can also be changed in place with `Sample.tables["k"] = ...`, which
changes the shared dict for every subclass that does not override it.

Type checking covers part of this. mypy runs on `dnd/` in pre-commit (tests/ are excluded), and it
rejects a `Literal[...]` reassignment such as `StrengthGetter.statistic = Statistic.WISDOM`. It
does not catch a plain `str` reassignment (any string fits), a dict write (any key and value fit),
`setattr`, or anything in excluded paths. So write runtime tests for fields whose type is wider
than the value they must keep. Rely on mypy for `Literal` fields in production code.

## What to test

For each `ClassVar` field that is meant to be fixed, write tests for:

- reassignment on an instance (`instance.field = ...`)
- for a dict field: in-place write (`Sample.field["k"] = ...`), with the shared base dict checked afterwards

Do not write tests for reassignment on the class (`Sample.field = ...`). Class-level assignment
can only be blocked by a metaclass, and the architecture tests forbid metaclasses in `dnd/`.

## Rules

- Use `pytest.raises(Exception)` and then assert the value is unchanged. Do not require a
  specific exception type. A property, a metaclass guard, or pydantic's own check should all pass.
- Define a local subclass inside each test (for example `class Sample(Flavour): description = "original"`)
  so a failing class-level write cannot leak into other tests.
- Use `pytest.raises` for the write itself. Keep the write outside any helper so the failure is the write, not the setup.
- Don't add `suppress`, and don't add cleanup in `finally` that would error if the implementation is correct.
- Mark tests `@pytest.mark.unit` and group them in a class named after the model, for example `TestFlavourDescriptionIsImmutable`.
- Expect in-place tests to fail on the current code until the implementation guards them. That is the red state.

## Existing examples

- `tests/unit/test_flavour.py`: `description` on instance
- `tests/unit/test_feature.py`: `description` on instance, and `tables` in-place writes
- `tests/unit/test_subrace_immutability.py`: `race` on instance
- `tests/unit/test_backgrounds.py`: `background` and `priority` on `BackgroundSource` instances
