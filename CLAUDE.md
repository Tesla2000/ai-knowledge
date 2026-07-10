# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all pre-commit hooks (lint + type-check)
pre-commit run --all-files

# Run only mypy
pre-commit run mypy --all-files

# Run tests by marker
pytest -m unit
pytest -m integration
pytest -m "unit or integration"   # no API key required
pytest -m smoke                   # requires OPENAI_API_KEY
pytest -m e2e                     # full AI flows

# Run a single test file
pytest tests/unit/path/to/test_file.py

# Run the FastAPI server locally
uvicorn dnd.server.app:app --reload
```

## Architecture

### The Blueprint Pipeline

`Blueprint` (`dnd/character/blueprint/state.py`) is a **19-parameter frozen Pydantic generic** that encodes build state in its type parameters:

```
Blueprint[_RK, _StK, _HeK, _StCK, _SkCK, _WZK, _SOK, _FGK, _BAK, _ROK, _CLK, _DRK, _PAK, _RAK, _MOK, _BDK, _WAK, _ARK, _CDK]
```

- `_RK` — `Race | None` (race assigned)
- `_StK` — `Stats | None` (base stats assigned)
- `_HeK` — `PositiveInt | None` (health pool)
- `_StCK / _SkCK` — `Literal[0] | PositiveInt` (remaining choice counts)
- `_WZK / _SOK / _FGK…_ARK` — phantom class levels (pre/post-subclass per class)
- `_CDK` — `CharacterData | None` (name, age, background, etc.)

The type parameters are **covariant** (Blueprint is frozen/read-only), so `Blueprint[Race, Stats, ...]` is a subtype of `Blueprint[Race|None, Stats|None, ...]`. This makes `_WideBlueprint` and `AnyBluprint` work as proper supertypes.

### Building Blocks

Each step is a `BuildingBlock` — a frozen Pydantic model with a discriminated `type: BuildingBlockType` field and an `apply(blueprint: InType) -> OutType` method. The type signature precisely encodes what changes at each step.

Key type aliases used in `apply` signatures:
- `_WideBlueprint` (`building_block.py`) — accepts any Blueprint as input (all params at max width)
- `AnyBluprint` / `_BPT` (`state.py`) — for type-preserving identity-like blocks (e.g. `NullBlock`)
- `EmptyBlueprint` — the all-None/Literal[0] starting state
- `InitializedBlueprint` (`initial_builder.py`) — output after race+stats+level are set

### Build Pipeline

The `/create_character` endpoint in `dnd/server/app.py` chains blocks in two phases:

1. **`InitialBuilder.apply(EmptyBlueprint)`** — orchestrates: `LevelAssigner → StatsBuilder → RaceAssigner → AllChoicesResolver`, outputs `InitializedBlueprint`
2. **Subsequent blocks** — health, subclass assigners (per class), feat/spell/equipment resolvers, `InitialDataFiller` (assigns `CharacterData`)
3. **`CharacterConverter`** — seals the final Blueprint into `PresentableCharacter`

### Phantom Subclass Types

Different classes gain subclasses at different levels (Sorcerer=1, Wizard=2, most others=3). Each has dedicated enums and phantom generic classes (`WizardPreSubclassLevel`, `SorcererPreSubclassLevel`, `ClassPreSubclassLevel`, etc.) so that level-gated subclass blocks are type-safe — the wrong block on the wrong class fails at pipeline-construction time, not runtime.

## Strict Constraints (enforced by pre-commit hooks)

- **`# type: ignore` is forbidden** — fix the underlying type error instead
- **`arbitrary_types_allowed = True` is forbidden** — use `InstanceOf[T]` from pydantic-frozendict
- **`hasattr`, `getattr`, `print` are forbidden** — use attribute access directly; use logging
- **OOP methods over standalone functions** — the main API surface should be a method on the relevant class
- **`from __future__ import annotations`** — required in all files that use forward references in type hints
- mypy runs with `--strict`; 100% test coverage is required

## Key Invariants

- All Pydantic models must be `frozen=True`
- `apply` methods in building blocks must be fully typed with explicit Blueprint TypeVar signatures — do not use `_WideBlueprint` as both input and output; use the 19-TypeVar form
- `_StK = Stats` must be pinned (not free) in any block that reads `blueprint.stats` for computation (e.g. `FeatChoiceResolver`, `AllChoicesResolver`)
- `model_copy(update={...})` is the mutation pattern; `Blueprint[...].model_validate(dict(bp) | {...})` is used when the type parameter changes
