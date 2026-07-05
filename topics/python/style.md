# Style

## Rules

- Never use bare functions. Only methods are allowed.
- Prefer list comprehension over loops. Use `next`, `map`, `filter`, `reduce` where appropriate.
- Use `defaultdict` instead of `dict.setdefault`.
- Use `@staticmethod` when a method does not use `self`.
- Use `@classmethod` when a method calls another class or static method of its own class.
- Staticmethods are preferred over staticmethods where inheritance override is possible.
- No em dashes, curly quotes, or ellipsis characters. ASCII punctuation only.

## Functions vs Methods

There are no standalone functions. Everything lives in a class:

```python
# good
class TextCleaner(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    @staticmethod
    def normalize(text: str) -> str:
        return text.strip().lower()

# bad
def normalize(text: str) -> str:
    return text.strip().lower()
```

## Comprehensions

```python
# good
results = [item.value for item in items if item.active]
total = sum(item.price for item in cart)
first = next((x for x in items if x.id == target_id), None)

# bad
results = []
for item in items:
    if item.active:
        results.append(item.value)
```

## defaultdict

```python
# good
from collections import defaultdict
groups: defaultdict[str, list[int]] = defaultdict(list)
groups[key].append(value)

# bad
groups: dict[str, list[int]] = {}
groups.setdefault(key, []).append(value)
```

## staticmethod vs classmethod

```python
class Parser(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    @staticmethod
    def _clean(text: str) -> str:           # no self, no class refs
        return text.strip()

    @classmethod
    def from_raw(cls, raw: str) -> "Parser":  # calls cls -- classmethod
        return cls(text=cls._clean(raw))
```

## Entry points

Never use `if __name__ == "__main__":` inside package/library files. Move CLI entry
points to `scripts/`. Scripts are excluded from coverage and mypy, so the guard block
disappears from the report entirely rather than needing suppression.

## Dict-completeness guards

Never use a runtime guard after a dict comprehension to verify all enum members are
covered:

```python
# bad
data = {member: ... for member in MyEnum}
if not all(map(data.__contains__, MyEnum)):
    raise ValueError(...)
```

Instead, replace the dict with an exhaustive `match` function. mypy enforces completeness
statically, and `case _ as never: assert_never(never)` is the signal:

```python
# good
def get_thing(key: MyEnum) -> Thing:
    match key:
        case MyEnum.A:
            return ...
        case MyEnum.B:
            return ...
        case _ as never:
            assert_never(never)
```

See `dnd/character/race/subrace_stats/subrace_to_stats.py` for a worked example.

## Related

- [imports.md](imports.md) -- class and module visibility
- [pydantic.md](pydantic.md) -- all classes are pydantic models
