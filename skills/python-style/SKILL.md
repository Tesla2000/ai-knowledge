---
name: python-style
description: Python style rules: comprehensions, defaultdict, staticmethod vs classmethod, no bare functions, imports, typing
---

# Python Style

- No bare functions. Everything is a method on a class.
- Prefer list comprehension over loops. Use next, map, filter, reduce.
- Use defaultdict instead of dict.setdefault.
- Use @staticmethod when method does not use self.
- Use @classmethod when method calls another class or static method of its own class.
- Never use local (inline) imports unless explicitly allowed.
- Never import private members from outside their module.
- Import public members from __init__.py, not private submodules.
- Name collision: use _ suffix on the local name, never alias public as private.
- Classes and files are private by default; export via __init__.py with import-as and __all__.
- Always type hint both arguments and return type.
- Never use plain tuple for fixed-arity returns -- use NamedTuple.
- Use object only when type cannot be narrowed.
- Never use from __future__ import annotations.
- Do not define types between imports.
- Do not remove unused imports unless they risk circular import.
- Never use # type: ignore[import-not-found] -- add the package or create stubs.
- Use only ASCII punctuation. No em dashes, curly quotes, or ellipsis characters.
- When mentioning files always use full path from root with line number: full_path:69

## staticmethod vs classmethod

```python
class Parser(BaseModel):
    @staticmethod
    def _clean(text: str) -> str:           # no self, no class refs
        return text.strip()

    @classmethod
    def from_raw(cls, raw: str) -> "Parser":  # calls cls
        return cls(text=cls._clean(raw))
```

## Comprehensions

```python
results = [item.value for item in items if item.active]
first = next((x for x in items if x.id == target_id), None)
```

## defaultdict

```python
groups: defaultdict[str, list[int]] = defaultdict(list)
groups[key].append(value)
```

## Module exports

```python
# module/_my_service.py  -- private
class _MyService(BaseModel): ...

# module/__init__.py  -- public
from module._my_service import _MyService as MyService
__all__: list[str] = ["MyService"]
```

## Exhaustive enum matching (replaces runtime dict-completeness guards)

```python
def get_thing(key: MyEnum) -> Thing:
    match key:
        case MyEnum.A: return ...
        case MyEnum.B: return ...
        case _ as never: assert_never(never)
```
