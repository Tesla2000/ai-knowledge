import os
import typing
from contextlib import suppress
from typing import Any
from typing import get_args
from typing import get_origin
from typing import Optional

from dnd.character.blueprint.building_blocks import (
    AnyBuildingBlock,
)
from dnd.character.blueprint.building_blocks.building_block import (
    BLOCK_TYPE_FIELD_NAME,
)
from dnd.character.blueprint.building_blocks.building_block import (
    SerializableBlock,
)
from dnd.character.blueprint.building_blocks.stats_priority import (
    StatsPriority,
)
from dnd.character.blueprint.simplified_blocks.simplified_blocks import (
    Classes,
)
from dnd.character.blueprint.simplified_blocks.simplified_blocks import (
    EXCLUDE_FACTORY_DEFAULTS,
)
from dnd.character.blueprint.simplified_blocks.simplified_blocks import (
    SimplifiedBlocks,
)
from dnd.character.builder import Builder
from dnd.character.checkpoint import IncrementChain
from dnd.character.checkpoint import IncrementStorage
from dnd.character.checkpoint import MemoryStorage
from dnd.character.presentable_character import (
    PresentableCharacter,
)
from dnd.choices.class_creation.character_class import Class
from dnd.server.example_generators.example_building_blocks import (
    example_building_blocks,
)
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pydantic import Field
from pydantic import TypeAdapter
from pydantic import ValidationError
from starlette.responses import RedirectResponse
from starlette.responses import Response
from subclass_getter import get_unique_subclasses


class _CreateCharacterResponse(BaseModel):
    character: Optional[PresentableCharacter] = None
    increment_chain: IncrementChain
    error: Optional[str] = None


EXAMPLES = (
    SimplifiedBlocks(
        classes=Classes(class_levels={Class.WIZARD: 1})
    ).model_dump(include={"classes", BLOCK_TYPE_FIELD_NAME}, mode="json"),
    SimplifiedBlocks(
        classes=Classes(class_levels={Class.WIZARD: 1})
    ).model_dump(exclude={"blocks"}, mode="json"),
    example_building_blocks().model_dump(mode="json"),
)


class _CreateCharacterRequestSchema(BaseModel):
    building_blocks: dict[str, Any] = Field(examples=list(EXAMPLES))
    increment_chain: dict[str, Any] = Field(examples=[IncrementChain()])


_building_block_creator = TypeAdapter(AnyBuildingBlock)


def _generate_building_blocks_metadata() -> list[dict[str, Any]]:
    """Generate metadata for all building blocks.

    Returns:
        List of building block metadata dictionaries, sorted alphabetically by name.
    """
    blocks_metadata = []
    for block_class in get_unique_subclasses(SerializableBlock):
        fields = {}
        for field_name, field_info in block_class.model_fields.items():
            if field_name == BLOCK_TYPE_FIELD_NAME:
                continue  # Skip discriminator field

            if hasattr(field_info.annotation, "__name__"):
                field_type = field_info.annotation.__name__
            elif hasattr(field_info.annotation, "_name"):
                field_type = field_info.annotation._name
            else:
                field_type = str(field_info.annotation)

            default_value = None
            if field_info.default is not None:
                with suppress(Exception):
                    if isinstance(
                        field_info.default, (str, int, float, bool, list, dict)
                    ):
                        default_value = field_info.default

            fields[field_name] = {
                "type": field_type,
                "description": field_info.description or "",
                "default": default_value,
            }

        assert (
            block_class.__doc__
        ), f"{block_class.__name__} is missing a docstring"

        blocks_metadata.append(
            {
                "block_type": block_class.get_block_type(),
                "name": block_class.__name__,
                "description": block_class.__doc__.strip(),
                "fields": fields,
            }
        )

    blocks_metadata.sort(key=lambda x: x["name"])

    return blocks_metadata


def create_app(storage: IncrementStorage):
    app_ = FastAPI()

    # Generate building blocks metadata once at startup
    blocks_metadata = _generate_building_blocks_metadata()

    @app_.post(
        "/create_character",
        response_model=_CreateCharacterResponse,
        response_model_exclude_unset=True,
    )
    def create_character(
        request: _CreateCharacterRequestSchema, response: Response
    ) -> _CreateCharacterResponse:
        blocks = request.building_blocks

        errors = []
        try:
            if (
                blocks.get(BLOCK_TYPE_FIELD_NAME)
                == SimplifiedBlocks.get_block_type()
            ):
                building_blocks = SimplifiedBlocks.model_validate(blocks)
            else:
                building_blocks = _building_block_creator.validate_python(
                    blocks
                )
        except ValidationError as e:
            errors.append(e)
        try:
            increment_chain = IncrementChain.model_validate(
                request.increment_chain
            )
        except ValidationError as e:
            errors.append(e)
        if errors:
            raise HTTPException(
                status_code=422, detail="\n\n".join(map(str, errors))
            )
        builder = Builder(
            building_blocks=(building_blocks,),
            increment_storage=storage,
        )
        result = builder.build(increment_chain)
        output_increment_chain = storage.load_chain(result.chain_id)
        response.status_code = 422 if result.error else 200
        return _CreateCharacterResponse(
            character=result.character,
            increment_chain=output_increment_chain,
            error=str(result.error) if result.error else None,
        )

    @app_.get("/building_blocks")
    def get_building_blocks():
        """Return metadata about all available building blocks (cached at startup)."""
        return {"building_blocks": blocks_metadata}

    @app_.get("/simplified_templates")
    def get_simplified_templates():
        """Return example SimplifiedBlocks configurations."""

        # Template 1: Level 1 Wizard (minimal config)
        wizard_l1 = SimplifiedBlocks(
            classes=Classes(class_levels={Class.WIZARD: 1})
        )

        # Template 2: Level 3 Wizard
        wizard_l3 = SimplifiedBlocks(
            classes=Classes(class_levels={Class.WIZARD: 3})
        )

        # Template 3: Level 5 Sorcerer
        sorcerer_l5 = SimplifiedBlocks(
            classes=Classes(class_levels={Class.SORCERER: 5})
        )

        return {
            "templates": [
                {
                    "name": "Level 1 Wizard",
                    "description": "Minimal configuration with only class specified",
                    "config": wizard_l1.model_dump(
                        exclude={"blocks"},
                        context={EXCLUDE_FACTORY_DEFAULTS: True},
                        mode="json",
                    ),
                    "config_with_defaults": wizard_l1.model_dump(
                        exclude={"blocks"}, mode="json"
                    ),
                },
                {
                    "name": "Level 3 Wizard",
                    "description": "Mid-level wizard with standard defaults",
                    "config": wizard_l3.model_dump(
                        exclude={"blocks"},
                        context={EXCLUDE_FACTORY_DEFAULTS: True},
                        mode="json",
                    ),
                    "config_with_defaults": wizard_l3.model_dump(
                        exclude={"blocks"}, mode="json"
                    ),
                },
                {
                    "name": "Level 5 Sorcerer",
                    "description": "Mid-level sorcerer caster",
                    "config": sorcerer_l5.model_dump(
                        exclude={"blocks"},
                        context={EXCLUDE_FACTORY_DEFAULTS: True},
                        mode="json",
                    ),
                    "config_with_defaults": sorcerer_l5.model_dump(
                        exclude={"blocks"}, mode="json"
                    ),
                },
            ]
        }

    @app_.post("/format_simplified")
    def format_simplified(request: dict[str, Any], show_defaults: bool = True):
        """Validate and reformat SimplifiedBlocks config with or without defaults.

        This endpoint preserves user changes while toggling default value display.
        """

        try:
            simplified = SimplifiedBlocks.model_validate(request)
            if show_defaults:
                return simplified.model_dump(exclude={"blocks"}, mode="json")
            else:
                return {
                    **simplified.model_dump(
                        exclude={"blocks"},
                        context={EXCLUDE_FACTORY_DEFAULTS: True},
                        mode="json",
                    ),
                    "block_type": SimplifiedBlocks.get_block_type(),
                }
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=str(e))

    @app_.get("/schema/simplified-blocks")
    def get_simplified_blocks_schema():
        """Return JSON schema for SimplifiedBlocks editor validation.

        Recursively generates validation for:
        - classes (Classes model)
        - stats_priority (tuple of Statistic enums)
        - block_type fields within all Union type resolvers/choosers (recursive)
        """

        def get_union_schema(
            annotation: Any, field_name: str, visited: set[Any] | None = None
        ) -> dict[str, Any] | None:
            """Recursively build schema for Union type fields.

            Returns a schema that validates block_type and recursively validates
            nested Union fields within the Union member types.
            """
            if visited is None:
                visited = set()

            if annotation in visited:
                return None
            visited.add(annotation)

            origin = get_origin(annotation)
            if origin is not typing.Union:
                return None

            args = get_args(annotation)

            block_types = []
            nested_properties = {}

            for arg in args:
                # Unwrap Annotated types to get the actual class
                actual_type = arg
                if get_origin(arg) is typing.Annotated:
                    actual_type = get_args(arg)[0]

                # Check if it's a class and is a subclass of SerializableBlock
                if not (
                    isinstance(actual_type, type)
                    and issubclass(actual_type, SerializableBlock)
                ):
                    continue
                block_types.append(actual_type.get_block_type())

                # Recursively process fields of this Union member
                if hasattr(actual_type, "model_fields"):
                    for (
                        nested_field_name,
                        nested_field_info,
                    ) in actual_type.model_fields.items():
                        nested_schema = get_union_schema(
                            nested_field_info.annotation,
                            nested_field_name,
                            visited.copy(),
                        )
                        if nested_schema:
                            if nested_field_name not in nested_properties:
                                nested_properties[nested_field_name] = (
                                    nested_schema
                                )

            if not block_types:
                return None

            return {
                "type": "object",
                "properties": {
                    BLOCK_TYPE_FIELD_NAME: {
                        "type": "string",
                        "enum": sorted(block_types),
                        "description": f"Block type for {field_name}",
                    },
                    **nested_properties,
                },
                "required": [BLOCK_TYPE_FIELD_NAME],
                "additionalProperties": True,
            }

        # Generate schemas for non-Union fields
        classes_adapter = TypeAdapter(Classes)
        stats_priority_adapter = TypeAdapter(StatsPriority)

        classes_schema = classes_adapter.json_schema()
        stats_priority_schema = stats_priority_adapter.json_schema()

        # Extract the actual type definitions (handle $defs if present)
        classes_def = classes_schema.get("$defs", {}).get(
            "Classes", classes_schema
        )

        # Dynamically discover Union fields and build schemas recursively
        union_properties = {}
        for field_name, field_info in SimplifiedBlocks.model_fields.items():
            union_schema = get_union_schema(field_info.annotation, field_name)
            if union_schema:
                union_properties[field_name] = union_schema

        # Build schema
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "SimplifiedBlocks",
            "description": "Schema for SimplifiedBlocks editor with recursive validation for classes, stats_priority, and block_type fields",
            "type": "object",
            "properties": {
                "classes": {
                    **classes_def,
                    "description": 'Character class levels (e.g., {"Wizard": 1})',
                },
                "stats_priority": {
                    **stats_priority_schema,
                    "description": 'Ability score priority: 6 stats in order (e.g., ["intelligence", "constitution", ...])',
                },
                **union_properties,
            },
            "required": ["classes"],
            "additionalProperties": True,  # Allow other fields without validation
        }

        return schema

    @app_.get("/health")
    def health():
        return {"status": "ok"}

    @app_.get("/")
    def redirect_doc():
        return RedirectResponse("/docs")

    # Serve static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app_.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Redirect to building blocks page
    @app_.get("/blocks")
    def blocks_page():
        return RedirectResponse("/static/building_blocks.html")

    # Redirect to builder page
    @app_.get("/builder")
    def builder_page():
        return RedirectResponse("/static/builder.html")

    return app_


app = create_app(MemoryStorage())
