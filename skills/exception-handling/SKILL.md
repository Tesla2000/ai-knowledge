---
name: exception-handling
description: Error handling rules: return specific exception types as values, no raise, no bare Exception
---

# Exception Handling

Raised exceptions are invisible to the type system -- callers have no static guarantee
an exception won't surface. The fewer raise expressions, the better.
Operate on return values. Errors must appear in the return type so the caller is
forced by the type checker to handle them.

## Internal logic

If a raise is needed to guard against bad input, the type signature is too loose.
Make the invalid state unrepresentable through stricter types.

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

Return the specific exception type as a value, or a typed NamedTuple result.
Never use bare Exception in the return type.

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
