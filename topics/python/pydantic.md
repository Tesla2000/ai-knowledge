# Pydantic

## Rules

- All pydantic models must be frozen (`ConfigDict(frozen=True)`).
- `allow_arbitrary_types` is never allowed.
- Never use dataclasses or plain pydantic class. Use `BaseModel` or `NamedTuple`.
- Never instantiate pydantic services directly in code. Services are always fields of another model.

## Field Validators

Prefer `Annotated` with `AfterValidator` / `BeforeValidator` over `@field_validator`.

```python
# good
ValidatedEmail = Annotated[str, AfterValidator(lambda v: v.lower())]

class User(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    email: ValidatedEmail
```

`@field_validator` is only allowed when:
1. Validation uses classmethods of the same class.
2. Validation must be applied to all fields with `*`.
3. Many subclasses are expected (confirm with human overseer first).

## Cross-field Defaults

When a field default depends on another field, use a standalone function:

```python
def _default_slug(data: dict[str, object]) -> str:
    return str(data["name"]).lower().replace(" ", "-")

class Article(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    name: str
    slug: str = Field(default_factory=_default_slug)
```

Pydantic v2 passes previously-validated fields as `data`. Prefer this over `@model_validator`.

A `default_factory` receives validated data, but a child class can override a field's
type annotation. Do NOT assume the factory only ever receives the parent-class type.
Always guard with `isinstance` and raise `TypeError` for unexpected types:

```python
def _default_hp(data: Mapping[str, object]) -> int:
    stats = data.get("stats")
    if isinstance(stats, Stats):
        constitution = stats.constitution
    elif stats is not None:
        raise TypeError(f"stats must be Stats, got {type(stats)}")
    else:
        constitution = 10
    ...
```

## Mapping Validation

When validating `Mapping[str, object]`, use `Model.model_validate(data)` to reduce boilerplate.
Use `validation_alias` and `alias_generators` for field name mismatches.

## Non-pydantic Fields (e.g., DB connections)

Use `InstanceOf` from pydantic with `Field(default_factory=..., exclude=True)`:

```python
def _make_client(data: dict[str, object]) -> voyageai.Client:
    return voyageai.Client()

class EmbeddingService(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    model: str = "voyage-multilingual-2"
    client: InstanceOf[voyageai.Client] = Field(exclude=True, default_factory=_make_client)
```

`default_factory` receives previously-validated fields. If required fields are absent,
raise `ValueError` -- it means earlier validation already failed.

## Related

- [services.md](../architecture/services.md) -- full service creation pattern
- [typing.md](typing.md) -- NamedTuple for internal state
