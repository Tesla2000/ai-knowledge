# Imports

## Rules

- Never use local (inline) imports unless explicitly allowed by the supervisor.
- Never import private members from outside their module.
- Import public members from a module's `__init__.py`, not from the private submodule directly.
- Never alias a public name as a private name to avoid collisions -- use a `_` suffix instead.
- Do not modify import order manually. The linter handles it.
- Do not remove unused imports unless they risk a circular import.
- Never use `# type: ignore[import-not-found]`. Add the package to dependencies or create stub files.

## Module visibility

Classes and files should be private by default. Export publicly only through `__init__.py`
using `import as` and `__all__`:

```python
# module/_my_service.py
class _MyService(BaseModel):
    ...

# module/__init__.py
from module._my_service import _MyService as MyService

__all__: list[str] = ["MyService"]
```

## Name collision

When a public name collides with a local name, use a `_` suffix on the local:

```python
# good
from mylib import Config as Config_

config_ = Config_()

# bad
from mylib import Config as _Config   # do not alias public as private
```

## Circular imports

If removing an unused import would break a circular import boundary, leave it in place.
Otherwise, defer to the linter.

## Related

- [style.md](style.md) -- no standalone functions
- [architecture/services.md](../architecture/services.md) -- __init__.py export pattern for services
