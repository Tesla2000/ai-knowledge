---
name: exception-handling
description: exception, raise, error handling, return error value, third-party call, bare Exception, NamedTuple result, isinstance check
---

# Exception Handling

Code must not raise. Raised exceptions are invisible to the type system -- callers have
no static guarantee an exception won't surface. Operate on return values. Errors from
third-party calls must appear in the return type so the type checker forces the caller
to handle them.

## Internal logic

Methods that do not depend on third-party code never return exceptions and never raise.
The type hints must be enough to determine that the input cannot cause an exception.
If a bad input is possible, the type signature is too loose: make the invalid state
unrepresentable through stricter types (`Annotated` validators, enums, narrower types).

```python
# bad -- raise guards a type the signature already allows
def process(value: int | None) -> str:
    if value is None:
        raise ValueError("value must not be None")
    return str(value)

# good -- tighten the type
def process(value: int) -> str:
    return str(value)
```

## External APIs and IO

Only code that calls third-party code (external services, libraries, IO) catches
exceptions, and it returns the specific exception type as a value, or a typed NamedTuple
result. The exception is handled at the level that can act on it, which is not always
the method that caught it. Never use bare Exception in the return type.

```python
# good
def fetch_price(url: str) -> float | RequestException:
    try:
        return float(requests.get(url, timeout=5).json()["price"])
    except RequestException as exc:
        return exc

price = fetch_price(url)
if isinstance(price, RequestException):
    ...  # mypy forces this check before using price as float

# bad -- too broad
def fetch_price(url: str) -> float | Exception: ...
```

## Logging rule (web services only)

Log the exception before returning an error response. Does not apply to library or CLI code.
