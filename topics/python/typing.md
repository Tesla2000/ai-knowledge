# Typing

## Rules

- Always type hint both arguments and return type.
- Never use `Any`. Narrow to a specific type, `object`, or a `Union`; the `any-hook`
  pre-commit hook enforces this and its errors must never be ignored.
- Never use plain tuple with a fixed number of arguments. Use `NamedTuple` instead.
- Use `object` in type hints only when the type genuinely cannot be narrowed.
- Never use `from __future__ import annotations`.
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

## Related

- [pydantic.md](pydantic.md) -- Annotated validators use these types
- [imports.md](imports.md) -- where to define shared types
