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
- Avoid a generic method whose type parameter isn't reflected in its return type, unless there's a valid reason (e.g. constraining two or more parameters to agree with each other); otherwise use the bound type directly instead of a TypeVar.
- Never use `@dataclass` -- use a frozen Pydantic BaseModel for validated data, or NamedTuple for a plain fixed-arity immutable record.
- When editing a file that's already committed, judge whether the change bolts a field onto an existing class (possible OCP violation) instead of solving it architecturally; enum members, match/case arms, AnyX union members, and genuine bugfixes are normal and fine.
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

## Generic methods must use the type parameter in the return type

```python
# bad -- T only types one input, never comes back out
def from_active[T: IntEnum](cls, fc: FightCharacter[T]) -> DownedFightCharacter: ...

# good -- T flows through to the return type
def on_event[T: IntEnum](self, event: AnyCombatEvent[T]) -> tuple[Self, tuple[AnyCombatEvent[T], ...]]: ...

# good -- valid exception: T constrains two parameters to agree, return is unrelated
def apply[SlotT: IntEnum](self, attacker: FightCharacter[SlotT], defender: FightCharacter[SlotT]) -> bool: ...
```

## No dataclass -- Pydantic or NamedTuple instead

```python
# bad
@dataclass
class Point:
    x: int
    y: int

# good -- validated, has methods, can be frozen
class Point(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    x: int
    y: int

# good -- plain fixed-arity immutable record, no validation needed
class Point(NamedTuple):
    x: int
    y: int
```

## Open/Closed Principle on already-committed files

A class that's already shipped should stay closed to modification. Extending it to
cover a new case is usually a sign the new case needs a different shape, not a
wider one.

```python
# bad -- Character already shipped; bolting on a nullable field for one new case
class Character(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    name: str
    hit_points: int
    wild_shape_form: CreatureStatBlock | None = None  # only druids ever set this

# good -- the new case gets its own type instead of widening the shipped one
class Character(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    name: str
    hit_points: int

class WildShapedCharacter(Character):
    wild_shape_form: CreatureStatBlock
```

Extending an Enum, adding a match/case arm, adding a member to an AnyX union, or a
genuine bugfix is normal maintenance, not an OCP violation -- this only applies to
widening an existing class's shape to absorb a new responsibility.

## Exhaustive enum matching (replaces runtime dict-completeness guards)

```python
def get_thing(key: MyEnum) -> Thing:
    match key:
        case MyEnum.A: return ...
        case MyEnum.B: return ...
        case _ as never: assert_never(never)
```
