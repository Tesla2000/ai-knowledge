# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all pre-commit checks (the primary quality gate)
pre-commit run --all-files

# Run a specific hook
pre-commit run mypy --all-files
pre-commit run ruff --all-files

# Run tests (skip integration and API-key tests by default)
pytest -m "not integration and not requires_api_key"

# Run a single test file
pytest tests/character/test_build_wizard.py -m "not integration"

# Run integration tests (requires OpenAI key in .env)
pytest -m integration

# Start the FastAPI server locally
uvicorn dnd.server.app:app --reload
# OR
python -m dnd.server
```

## Pre-commit hooks

All hooks must pass; `any-hook` is the strictest and bans:
- All `# type: ignore[...]` comments (the `comment-detector` modifier)
- `hasattr`, `getattr`, `print` calls (`forbidden-functions`)
- Various Pydantic v1 patterns, leaky mapping types, `len(x) == 0` as bool, etc.

mypy runs with `--strict` and `plugins = ["pydantic.mypy"]`. Tests and `scripts/` are excluded from mypy.

vulture runs from a [fork](https://github.com/Tesla2000/vulture) and will flag unused code. If you add something that must be unused (e.g. a public API surface), add it to `--ignore-names` in `.pre-commit-config.yaml`.

## Architecture

### Character construction pipeline

Characters are built by composing `BuildingBlock` instances into a `Builder`. The pipeline is:

```
BuildingBlock.get_change(blueprint) → (Delta, Blueprint)
```

- **`Blueprint`** (`dnd/character/blueprint/blueprint.py`) — frozen Pydantic model with ~60 optional fields; the accumulating mutable character state during construction.
- **`Delta`** (`dnd/character/delta/delta.py`) — frozen Pydantic base with a `apply(blueprint) -> Blueprint` method; each block returns its own typed `XxxDelta` subclass containing only the fields it changes.
- **`BuildingBlock[StateIn, DeltaT, StateOut]`** (`building_block.py`) — generic abstract base. Concrete blocks inherit `BuildingBlock[Blueprint, XxxDelta, Blueprint]` and implement `get_change`. `CombinedBlock` chains multiple blocks sequentially.
- **`Builder`** (`dnd/character/builder.py`) — iterates `CombinedBlock.flatten()`, calls `block.get_change(blueprint)`, accumulates deltas in `IncrementChain`, and at the end calls `_make_presentable(blueprint)`.
- **`IncrementChain`** (`dnd/character/checkpoint/`) — immutable tuple of `Delta` objects; used to replay partial builds from a checkpoint.

### Block type discrimination

All `BuildingBlock` subclasses have a `block_type` computed field (the class name) used as a Pydantic discriminator. The `AnyBuildingBlock` union type in `building_blocks/__init__.py` is the `TypeAdapter` target for API deserialization. Every concrete block **must have a docstring** (asserted at server startup in `app.py`).

### Typed state wrappers (`state.py`)

`dnd/character/blueprint/state.py` defines generic state wrappers for future typed pipeline stages:
- `Blueprint[T: "None | Blueprint"]` — generic base with `base: T`
- `WithStats[T: Blueprint]` — adds guaranteed `stats: Stats`
- `WithRace[T: Blueprint]` — adds guaranteed `race`, `subrace`, `speed`, `dark_vision_range`

These are used when a block's `StateIn` type must guarantee certain fields are already set (e.g. `StatChoiceResolver` requires stats). The builder loop itself uses `Blueprint` (flat) as the runtime state.

### Block categories

| Directory | Purpose |
|---|---|
| `stats_builder/` | Abstract `StatsBuilder` + `StandardArray` (and future strategies) |
| `race_assigner/` | `BaseRaceAssigner` → `RaceAssigner` / `RandomRaceAssigner` |
| `stat_choice_resolver/` | Resolves `n_stat_choices` from race/ASI grants |
| `skill_choice_resolver/` | Resolves `n_skill_choices` |
| `feat_choice_resolver/` | Resolves `FeatName.ANY_*` placeholders, converts ASI → `n_stat_choices` |
| `level_up/` | `LevelIncrementer`, `HealthIncrease`, `SpellAssigner`, `LevelUp` composite |
| `initial_data_filler/` | Random or AI-generated backstory, name, appearance, etc. |
| `all_choices_resolver/` | `AllChoicesResolver` runs all per-level resolvers in one block |
| `subclass_assigner/` | Assigns subclass at the appropriate level |

`InitialBuilder` is a typed `CombinedBlock` (via `InitialBuilderBlocks` NamedTuple) that enforces a `LevelAssigner → StatsBuilder → RaceAssigner → AllChoicesResolver` order with compile-time type checking.

### Data model

`_CreatureBase` → `Character` → `PresentableCharacter` is the read-only output chain. `PresentableCharacter` computes derived fields (AC, spell slots, abilities, etc.) from the flat `Character` fields. `Blueprint` mirrors `Character`'s fields but makes all required fields optional to allow incremental assembly.

### Server

`dnd/server/app.py` exposes a FastAPI app (`create_app(storage)`). Key endpoints:
- `POST /create_character` — accepts `building_blocks` (JSON-serialized block tree) + optional `increment_chain` for resuming
- `GET /building_blocks` — metadata for all registered block types
- `GET /simplified_templates`, `POST /format_simplified` — `SimplifiedBlocks` high-level API
- `GET /schema/simplified-blocks` — JSON schema for the web editor

`SimplifiedBlocks` (`dnd/character/blueprint/simplified_blocks/`) is a higher-level config model that expands into a full block pipeline automatically.

### Adding a new BuildingBlock

1. Create `XxxDelta(Delta)` with only the fields the block sets; the default `apply()` on `Delta` uses `model_fields_set` + `model_fields` intersection to apply via `model_copy`.
2. Create `class XxxBlock(BuildingBlock[Blueprint, XxxDelta, Blueprint])` implementing `get_change(self, blueprint: Blueprint) -> tuple[XxxDelta, Blueprint]`.
3. Add to `AnyBuildingBlock` union in `building_blocks/__init__.py`.
4. Add a docstring (required by server startup assertion).

### TYPE_CHECKING pattern for `@computed_field` / `@property`

To satisfy mypy's `prop-decorator` check while keeping Pydantic's computed field at runtime:
```python
# Source: https://stackoverflow.com/a/79966495 (Filip Ratajczak, CC BY-SA 4.0)
from typing import TYPE_CHECKING
from pydantic import computed_field

@(property if TYPE_CHECKING else computed_field)(alias="some_field")
def some_field(self) -> str: ...
```
This pattern is used on `Delta.delta_type` and `SerializableBlock.block_type`.
