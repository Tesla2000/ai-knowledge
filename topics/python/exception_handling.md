# Exception Handling

## Core principle

Raised exceptions are invisible to the type system -- callers have no static guarantee
an exception won't surface. The fewer `raise` expressions, the better.
Prefer making invalid states unrepresentable through strict types, or surface errors
as explicit return values.

## Internal logic

If a function can only be called incorrectly due to a type violation, fix the types.
A `raise` inside internal logic is a signal that the type contract is too loose.

```python
# bad -- raise used to guard against a type the signature already allows
def process(value: int | None) -> str:
    if value is None:
        raise ValueError("value must not be None")
    return str(value)

# good -- tighten the type so the invalid call is impossible
def process(value: int) -> str:
    return str(value)
```

## External APIs and IO

When an external call can legitimately fail (network, parsing, missing resource),
return `None` for simple cases or a typed error object for richer context.
Do not raise.

```python
# good -- None signals absence
def fetch_price(url: str) -> float | None:
    try:
        response = requests.get(url, timeout=5)
        return float(response.json()["price"])
    except (RequestException, KeyError, ValueError):
        return None

# good -- typed error object for richer context
class FetchResult(NamedTuple):
    price: float | None
    error: str | None

def fetch_price(url: str) -> FetchResult:
    try:
        response = requests.get(url, timeout=5)
        return FetchResult(price=float(response.json()["price"]), error=None)
    except RequestException as exc:
        return FetchResult(price=None, error=str(exc))
```

## When raising is still acceptable

Only raise when the call site has already violated an invariant that cannot be
expressed in the type system (e.g., a validated-data dict missing a field that
should have been set by earlier pydantic validation). This is rare.

```python
def _make_conn(data: dict[str, object]) -> Connection:
    dsn = data.get("dsn")
    if not isinstance(dsn, str):
        raise ValueError("dsn missing -- prior pydantic validation must have failed")
    return connect(dsn)
```

## Catching external exceptions (EAFP)

When an external library raises on an expected absence, catch it and return a fallback.
Do not re-raise.

```python
# good
try:
    return soup.select_one(".price").text
except AttributeError:
    return None
```

## Logging rule (web services only)

In web-service request handlers, log the exception before returning an error response
so it appears in the service log. Does not apply to library or CLI code.

## Related

- [typing.md](typing.md) -- NamedTuple for typed error objects
- [testing.md](testing.md) -- testing None-returning paths
