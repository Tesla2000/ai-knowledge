# Exception Handling

## Core principle

Raised exceptions are invisible to the type system -- callers have no static guarantee
an exception won't surface. The fewer `raise` expressions, the better.
Operate on return values. Errors must appear in the return type so the caller is
forced by the type checker to handle them.

## Internal logic

If a raise is needed to guard against bad input, the type signature is too loose.
Make the invalid state unrepresentable through stricter types.

```python
# bad -- raise used to guard a type the signature already allows
def process(value: int | None) -> str:
    if value is None:
        raise ValueError("value must not be None")
    return str(value)

# good -- tighten the type, the invalid call is impossible
def process(value: int) -> str:
    return str(value)
```

## External APIs and IO

Catch the exception inside the function and return it as a value with a specific type,
or wrap success and failure in a typed `NamedTuple` result. The error is then part of
the signature and mypy enforces handling at every call site.
Never use bare `Exception` in the return type -- always name the specific exception class.

```python
# simple -- return specific exception type as value
def fetch_price(url: str) -> float | RequestException:
    try:
        return float(requests.get(url, timeout=5).json()["price"])
    except RequestException as exc:
        return exc

price = fetch_price(url)
if isinstance(price, RequestException):
    ...  # mypy forces this check before using price as float

# richer -- typed result object with specific error type
class PriceResult(NamedTuple):
    value: float | None
    error: RequestException | None

def fetch_price(url: str) -> PriceResult:
    try:
        return PriceResult(value=float(requests.get(url, timeout=5).json()["price"]), error=None)
    except RequestException as exc:
        return PriceResult(value=None, error=exc)
```

## What not to do

```python
# bad -- error is invisible to callers
def fetch_price(url: str) -> float:
    response = requests.get(url, timeout=5)
    if not response.ok:
        raise RuntimeError("fetch failed")
    return float(response.json()["price"])

# bad -- let it propagate is not a valid strategy
result = client.fetch(url)  # raises silently on failure
```

## Logging rule (web services only)

In web-service request handlers, log the exception before returning an error response
so it appears in the service log. Does not apply to library or CLI code.

## Related

- [typing.md](typing.md) -- NamedTuple for typed result objects
- [testing.md](testing.md) -- testing error return paths
