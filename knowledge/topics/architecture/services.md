# Service Creation Pattern

## Rules

- Services are exclusively pydantic `BaseModel` subclasses, frozen.
- Never instantiate a service directly in business logic. It must be a field of a parent model.
- Entry-point method must be descriptively named. Never use `__call__`.
- Use `PydanticLogger` (from `pydantic_logger`) instead of `logging.Logger`.
- Logger is a field: `logger: PydanticLogger = PydanticLogger(name=__name__)`.
- Forbid extra parameters on all service models.

## When to create a service directory

Create a separate directory (with `types.py` and `__init__.py`) only when there are
2 or more service implementations. A single service lives in a single file.

## Multi-implementation layout

```
services/
    types.py          # StrEnum with auto() values
    _fast_service.py
    _slow_service.py
    __init__.py       # AnyServiceType union + __all__
```

### types.py

```python
from enum import StrEnum, auto

class ServiceType(StrEnum):
    fast = auto()
    slow = auto()
```

### Each service file

```python
from typing import ClassVar, Literal
from pydantic import BaseModel, ConfigDict

class _FastService(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    type: Literal[ServiceType.fast] = ServiceType.fast
    logger: PydanticLogger = PydanticLogger(name=__name__)

    def process(self, data: str) -> str:
        ...
```

### __init__.py

```python
from services._fast_service import _FastService as FastService
from services._slow_service import _SlowService as SlowService
from services.types import ServiceType

AnyService = FastService | SlowService

__all__: list[str] = ["AnyService", "FastService", "SlowService", "ServiceType"]
```

## Abstract base class

Add an ABC only when 3 or more implementations exist. Do not use Protocol.

## Non-pydantic dependencies

Use `InstanceOf` with `Field(default_factory=..., exclude=True)`:

```python
def _make_conn(data: dict[str, object]) -> Connection:
    dsn = data.get("dsn")
    if not isinstance(dsn, str):
        raise ValueError("dsn missing from validated data")
    return connect(dsn)

class _DbService(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    dsn: str
    conn: InstanceOf[Connection] = Field(exclude=True, default_factory=_make_conn)
```

## Related

- [pydantic.md](../python/pydantic.md) -- frozen models, field validators
- [cli.md](cli.md) -- services called from cli_cmd
- [imports.md](../python/imports.md) -- __init__.py export pattern
