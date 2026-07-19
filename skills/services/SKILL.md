---
name: services
description: Pydantic service creation pattern: frozen BaseModel, types.py StrEnum, __init__.py exports, PydanticLogger, InstanceOf
---

# Service Creation Pattern

- Services are frozen BaseModel subclasses. Never instantiate directly -- always a field.
- Entry-point method must be descriptively named. Never use __call__.
- Use PydanticLogger (from pydantic_logger): logger: PydanticLogger = PydanticLogger(name=__name__).
- Forbid extra parameters: extra="forbid".
- Create a separate directory with types.py and __init__.py only when 2+ implementations exist.
- Add ABC only when 3+ implementations exist. Do not use Protocol.

## Single service

One file, no types.py needed.

## Multi-implementation layout

```
services/
    types.py
    _fast_service.py
    _slow_service.py
    __init__.py
```

### types.py
```python
from enum import StrEnum, auto
class ServiceType(StrEnum):
    fast = auto()
    slow = auto()
```

### Service file
```python
class _FastService(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")
    type: Literal[ServiceType.fast] = ServiceType.fast
    logger: PydanticLogger = PydanticLogger(name=__name__)

    def process(self, data: str) -> str: ...
```

### __init__.py
```python
from services._fast_service import _FastService as FastService
from services._slow_service import _SlowService as SlowService
from services.types import ServiceType

AnyService = FastService | SlowService
__all__: list[str] = ["AnyService", "FastService", "SlowService", "ServiceType"]
```

## Non-pydantic dependencies

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
