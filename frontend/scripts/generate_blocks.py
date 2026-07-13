#!/usr/bin/env python3
"""
Generate block metadata JSON for the frontend.
Run from /workspace/frontend: python3 scripts/generate_blocks.py
"""

import enum
import json
import sys
import types as builtin_types
import typing
from pathlib import Path
from typing import get_args
from typing import get_origin

from typing import TypedDict

from pydantic import BaseModel
from pydantic.fields import FieldInfo


class _ItemSchema(TypedDict, total=False):
    type: str
    enum: list[str]


class _FieldSchema(TypedDict, total=False):
    type: str
    enum: list[str]
    description: str
    required: bool
    default: str | int | float | bool
    note: str
    items: _ItemSchema


sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dnd.character.blueprint.building_blocks import AnyBuildingBlock  # noqa: E402
from dnd.character.blueprint.building_blocks.building_block_type import (  # noqa: E402
    BuildingBlockType,
)


def _get_category(type_name: str) -> str:
    if type_name.startswith("AI_"):
        return "AI"
    if "SUBCLASS_ASSIGNER" in type_name:
        return "Subclass"
    if "RACE" in type_name:
        return "Race"
    if (
        "LEVEL_UP" in type_name
        or "LEVEL_INCREMENT" in type_name
        or "HEALTH_INCREASE" in type_name
    ):
        return "Level-Up"
    if "LEVEL_ASSIGNER" in type_name:
        return "Identity"
    if "SPELL" in type_name:
        return "Spells"
    if "FEAT" in type_name or "MAX_FIRST" in type_name or "MAX_IF_NOT" in type_name:
        return "Feats"
    if "SKILL" in type_name:
        return "Skills"
    if "STAT" in type_name or type_name == "STANDARD_ARRAY":
        return "Stats"
    if "LANGUAGE" in type_name:
        return "Languages"
    if "EQUIPMENT" in type_name or "WEAPON" in type_name or "MAGICAL_ITEM" in type_name:
        return "Equipment"
    if "TOOL_PROFICIENCY" in type_name:
        return "Tool Proficiencies"
    if (
        "NAME" in type_name
        or "AGE" in type_name
        or "SEX" in type_name
        or "ALIGNMENT" in type_name
        or "BACKGROUND" in type_name
    ):
        return "Identity"
    if "INITIAL" in type_name or "BUILDER" in type_name:
        return "Builders"
    if "ALL_CHOICES" in type_name:
        return "Choices"
    if "NULL" in type_name:
        return "Utility"
    return "Other"


def _field_to_schema(field_name: str, field: FieldInfo) -> _FieldSchema:
    """Simplified field schema extraction without recursive Pydantic schema generation."""
    ann = field.annotation
    ann_str = str(ann)

    schema: _FieldSchema = {}

    if field.description:
        schema["description"] = field.description

    # Check for Literal type (enum-like)
    origin = get_origin(ann)
    if origin is not None:
        if origin is typing.Literal or str(origin) == "typing.Literal":
            args = get_args(ann)
            schema["type"] = "string"
            schema["enum"] = [
                str(a.value) if isinstance(a, enum.Enum) else str(a) for a in args
            ]
            return schema

    # Unwrap Optional (X | None or Union[X, None])
    if origin in (typing.Union,) or isinstance(ann, builtin_types.UnionType):
        inner_args = get_args(ann)
        non_none = [a for a in inner_args if a is not type(None)]
        if len(non_none) == 1:
            fake_field = FieldInfo(
                annotation=non_none[0], description=field.description
            )
            inner = _field_to_schema(field_name, fake_field)
            inner["required"] = False
            return inner
        # Multi-type union — fall through to complex

    # Common type mappings
    if ann is str or ann_str == "<class 'str'>":
        schema["type"] = "string"
    elif ann is int or ann_str == "<class 'int'>":
        schema["type"] = "integer"
    elif ann is float or ann_str == "<class 'float'>":
        schema["type"] = "number"
    elif ann is bool or ann_str == "<class 'bool'>":
        schema["type"] = "boolean"
    else:
        # Try to detect enum types
        if isinstance(ann, type) and issubclass(ann, enum.Enum):
            schema["type"] = "string"
            schema["enum"] = [e.value for e in ann]
            return schema

        # Tuple of enum (e.g. stats_priority: tuple[Statistic, ...])
        if origin in (tuple, list) or str(origin) in (
            "<class 'tuple'>",
            "<class 'list'>",
        ):
            item_args = get_args(ann)
            if item_args:
                item_type = item_args[0]
                if isinstance(item_type, type) and issubclass(item_type, enum.Enum):
                    schema["type"] = "array"
                    schema["items"] = {
                        "type": "string",
                        "enum": [e.value for e in item_type],
                    }
                    return schema
            schema["type"] = "array"
            return schema

        # Union / complex nested types
        if "Union" in ann_str or "Optional" in ann_str or "|" in ann_str:
            schema["type"] = "object"
            schema["note"] = "complex nested type"
        else:
            schema["type"] = "string"
            schema["note"] = f"serialized as: {ann_str[:80]}"

    if field.default is not None and str(field.default) != "PydanticUndefined":
        try:
            json.dumps(field.default)
            schema["default"] = field.default
        except (TypeError, ValueError):
            schema["default"] = str(field.default)

    return schema


def _get_fields(cls: type[BaseModel]) -> dict[str, _FieldSchema]:
    """Get fields for a block class, excluding 'type'."""
    fields: dict[str, _FieldSchema] = {}

    for name, field in cls.model_fields.items():
        if name == "type":
            continue
        try:
            schema = _field_to_schema(name, field)
            required = (
                field.default is None or str(field.default) == "PydanticUndefined"
            )
            schema["required"] = required
            fields[name] = schema
        except Exception as e:
            fields[name] = {
                "type": "string",
                "note": f"parse error: {e}",
                "required": True,
            }

    return fields


def _label(type_name: str) -> str:
    """Convert TYPE_NAME_LIKE_THIS to 'Type Name Like This'."""
    return type_name.replace("_", " ").title()


def main() -> None:
    args = get_args(AnyBuildingBlock)
    union_args = get_args(args[0])

    type_to_class: dict[str, type[BaseModel]] = {}
    for cls in union_args:
        for fname, finfo in cls.model_fields.items():
            if fname == "type":
                ann = finfo.annotation
                type_args = get_args(ann)
                if type_args:
                    enum_val = type_args[0]
                    if isinstance(enum_val, enum.Enum):
                        type_to_class[enum_val.name] = cls
                break

    blocks = []
    for bt in BuildingBlockType:
        cls = type_to_class.get(bt.name)
        if cls is None:
            continue

        is_ai = bt.name.startswith("AI_") or "LLM" in bt.name

        block: dict[str, object] = {
            "type": bt.value,
            "type_name": bt.name,
            "label": _label(bt.name),
            "class_name": cls.__name__,
            "category": _get_category(bt.name),
            "description": (cls.__doc__ or "").strip().split("\n")[0],
            "is_ai": is_ai,
            "fields": _get_fields(cls),
        }
        blocks.append(block)

    output = Path(__file__).parent.parent / "src" / "data" / "blocks-generated.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(blocks, indent=2))
    sys.stdout.write(f"Generated {len(blocks)} blocks -> {output}\n")


if __name__ == "__main__":
    main()
