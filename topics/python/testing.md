# Testing

## Rules

- Use pytest exclusively.
- Never rewrite implementation code in tests. Tests only supply mock inputs and clean up.
- Never skip tests. If a value is unavailable, fail the test.
- Never use `# pragma: no cover` unless the user explicitly allows it.
- Do not use local imports in tests.
- 100% coverage means 100%. Flag impossible branches or defensive code to the user instead of suppressing.

## Markers

```python
# manual test
@pytest.mark.skipif(not os.getenv("RUN_MANUAL"), reason="Manual test")

# integration test
@pytest.mark.skipif(not os.getenv("RUN_INTEGRATION"), reason="Integration test")
```

## patch.object format

Always use `patch.object(ClassName, method.__name__)`, not string paths:

```python
# good
with patch.object(
    QuantitiesExtractor,
    QuantitiesExtractor.extract_quantities.__name__,
    autospec=True,
    return_value=(quantity,),
):
    ...

# bad
with patch.object(scraper.quantities_extractor, "extract_quantities", return_value=(quantity,)):
    ...
```

Always pass `autospec=True` with the class (not an instance).

## Flat patch context managers

Prefer one flat `with patch(...), patch(...):` over nested withs:

```python
# good
with patch.object(Foo, "bar"), patch.object(Baz, "qux"):
    ...

# bad
with patch.object(Foo, "bar"):
    with patch.object(Baz, "qux"):
        ...
```

## Pydantic model mocking

To mock fields on a frozen pydantic model, use `.model_construct` to bypass validation:

```python
service = MyService.model_construct(field=mock_value)
```

## Unreachable code

If a branch is unreachable (e.g., inside an infinite loop), extract it to a private method
and mock that method in tests. Do not use pragma suppression.

```python
# extract
def _process(self) -> None:
    ...

# test
with patch.object(MyClass, "_process"):
    ...
```


## Smoke tests

One test per external service call (database, LLM, web). Do not bundle multiple external
calls into one test.

## Branch coverage notation

| Notation | Meaning |
|----------|---------|
| `A->B` | Conditional on line A never branched to line B |
| `N` | Line N was never executed |
| `N-M` | Lines N through M were never executed |
| `A->exit` | Line A never exited the function normally from that point |

## Resource paths

Paths to test resources must be relative to the project root, not the test file path.

## Related

- [pydantic.md](pydantic.md) -- model_construct for frozen models
- [style.md](style.md) -- no functions, only methods
