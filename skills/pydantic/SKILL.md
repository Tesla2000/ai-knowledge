---
name: pydantic
description: Pydantic model rules: frozen, Annotated validators, cross-field defaults, InstanceOf for non-pydantic fields
---

# Pydantic

- All models must be frozen: ConfigDict(frozen=True).
- allow_arbitrary_types is never allowed.
- Never use dataclasses or plain pydantic class -- use BaseModel or NamedTuple.
- Never instantiate services directly -- they are always fields of a parent model.

## Field validators

Use Annotated with AfterValidator/BeforeValidator. @field_validator only when:
1. Validation uses classmethods of the same class.
2. Must apply to all fields with *.
3. Many subclasses expected (confirm with user first).

```python
ValidatedEmail = Annotated[str, AfterValidator(lambda v: v.lower())]

class User(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    email: ValidatedEmail
```

## Cross-field defaults

```python
def _default_slug(data: dict[str, object]) -> str:
    return str(data["name"]).lower().replace(" ", "-")

class Article(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    name: str
    slug: str = Field(default_factory=_default_slug)
```

Pydantic v2 passes previously-validated fields as data. Prefer over @model_validator.

## Non-pydantic fields (DB connections, clients)

```python
# good
class EmbeddingService(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)
    model: str = "voyage-multilingual-2"
    client: InstanceOf[voyageai.Client] = Field(exclude=True, default_factory=voyageai.Client)

# bad
class EmbeddingService(BaseModel):
    _client: voyageai.Client = PrivateAttr()
    def model_post_init(self, _: object, /) -> None:
        object.__setattr__(self, "_client", voyageai.Client())
```

## Mapping validation

Use Model.model_validate(data) for Mapping[str, object].
Use validation_alias and alias_generators for field name mismatches.
