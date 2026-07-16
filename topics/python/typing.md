# Typing

## Rules

- Always type hint both arguments and return type.
- Never use `Any`. Narrow to a specific type, `object`, or a `Union`; the `any-hook`
  pre-commit hook enforces this and its errors must never be ignored.
- Never use plain tuple with a fixed number of arguments. Use `NamedTuple` instead.
- Use `object` in type hints only when the type genuinely cannot be narrowed.
- Never use `from __future__ import annotations`. Type hints must be real types evaluated at
  definition time, not strings deferred to runtime.
- For self-referential return types inside a class (e.g., a classmethod returning its own
  class), use `typing.Self` — never a quoted string like `"MyClass"`.
- Do not define types between imports.

## NamedTuple

Use `NamedTuple` for any fixed-shape internal state or return value.

```python
# good
class Point(NamedTuple):
    x: float
    y: float

def get_origin() -> Point:
    return Point(x=0.0, y=0.0)

# bad
def get_origin() -> tuple[float, float]:
    return 0.0, 0.0
```

## Narrowing `object`

Only use `object` when no narrower type applies (e.g., values in `dict[str, object]`
for heterogeneous mappings). If you know the set of types, use `Union` or a specific type.

## Type aliases (Python 3.12+)

Use the `type` statement (PEP 695) instead of `X: TypeAlias = Y` for all type aliases:

```python
# good (Python 3.12+)
type Spell = Cantrip | FirstLevel | SecondLevel

# bad
from typing import TypeAlias
Spell: TypeAlias = Cantrip | FirstLevel | SecondLevel
```

Advantages: lazily evaluated (no forward-reference issues), cleaner syntax, explicit alias
statement visible to type checkers and IDEs without importing `TypeAlias`.

Use `type X = Y` for union aliases and for giving a stable name to a complex `Literal` type.

## Exhaustive match: `case _ as never`

In exhaustive `match` statements, use `never` as the variable name in the catch-all arm:

```python
case _ as never:
    assert_never(never)
```

Do NOT use `unreachable` or any other name. `never` is excluded from coverage analysis;
other names are NOT — they get flagged as untested branches.

## `cast` and `TYPE_CHECKING`

Use `cast` only when you have absolute certainty that the runtime value matches the cast type.
`cast` is a lie to the type checker — it creates a discrepancy between static types and runtime
behavior that mypy cannot detect. Every `cast` is a potential silent bug if the assumption breaks.

```python
# bad: cast hides the mismatch between int and Literal[0,1,2,...9]
query = cast(ClassSpellLevel, (class_, spell_level))

# good: change the function signature to accept Class + int directly
def get_class_spell_enum(class_: Class, spell_level: int) -> type[StrEnum]:
    ...
```

`TYPE_CHECKING` imports (guarded by `if TYPE_CHECKING:`) are evaluated only by the type checker,
not at runtime. Code that relies on such imports at runtime will raise `NameError`. Only use
`TYPE_CHECKING` for circular-import stubs where the import is referenced purely in annotations
and never at runtime — this is very rare and should be avoided if there is any alternative.

## Related

- [pydantic.md](pydantic.md) -- Annotated validators use these types
- [imports.md](imports.md) -- where to define shared types
