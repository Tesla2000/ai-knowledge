---
name: testing
description: pytest rules: patch.object format, autospec, coverage expectations, save output before reading
---

# Testing

- Use pytest exclusively.
- Never rewrite implementation code in tests. Tests only supply inputs and clean up.
- Never skip tests -- fail them if values are unavailable.
- Never use # pragma: no cover unless explicitly allowed by user. YOU DO THIS FREQUENTLY.
- 100% coverage means 100%. Flag impossible branches to the user instead of suppressing.
- Save test output to a file and read it to analyse results. Never re-run with a different
  config just to see additional lines -- run once, read the saved output.

## Markers

```python
@pytest.mark.skipif(not os.getenv("RUN_MANUAL"), reason="Manual test")
@pytest.mark.skipif(not os.getenv("RUN_INTEGRATION"), reason="Integration test")
```

## patch.object format

Always patch.object(ClassName, method.__name__) with autospec=True on the class:

```python
# good
with patch.object(
    QuantitiesExtractor,
    QuantitiesExtractor.extract_quantities.__name__,
    autospec=True,
    return_value=(quantity,),
): ...

# bad
with patch.object(scraper.quantities_extractor, "extract_quantities", ...): ...
```

## Flat context managers

```python
# good
with patch.object(Foo, "bar"), patch.object(Baz, "qux"): ...

# bad
with patch.object(Foo, "bar"):
    with patch.object(Baz, "qux"): ...
```

## Pydantic model mocking

Use .model_construct to bypass frozen validation:
```python
service = MyService.model_construct(field=mock_value)
```

## Unreachable code

Extract to a private method and mock it. Do not use pragma.

## Smoke tests

One test per external service call (database, LLM, web).

## Branch coverage notation

| Notation | Meaning |
|----------|---------|
| A->B | Conditional on line A never branched to B |
| N | Line N never executed |
| N-M | Lines N through M never executed |
| A->exit | Line A never exited normally |
