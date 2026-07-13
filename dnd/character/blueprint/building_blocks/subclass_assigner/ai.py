"""AI-powered subclass assigner."""

from dnd.character.blueprint.formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    _check_can_assign,
)
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.class_creation.character_class import AnySubclass
from dnd.choices.class_creation.character_class import Class
from dnd.choices.class_creation.character_class import SUBCLASSES
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from pydantic import BaseModel
from pydantic import Field
from pydantic import create_model
from structured_output_creator import OpenAIService, RaisingService


class AISubclassAssigner(BuildingBlock):
    """AI-powered subclass assigner that selects subclasses based on character context."""

    type: Literal[BuildingBlockType.AI_SUBCLASS_ASSIGNER] = (
        BuildingBlockType.AI_SUBCLASS_ASSIGNER
    )

    class_: Class = Field(
        description="The character class for which to assign a subclass"
    )
    llm: RaisingService = Field(
        default_factory=lambda: RaisingService(service=OpenAIService())
    )
    formatter: BlueprintFormatter = Field(default_factory=BlueprintFormatter)

    def _build_prompt(self, blueprint: _WideBlueprint) -> str:
        system_prompt = (
            f"You are selecting a subclass for a D&D 5e {self.class_.value}.\n"
            "Choose the subclass that best fits the character's background, stats, and concept.\n"
        )
        character_description = self.formatter.format(
            blueprint, system_prompt=system_prompt
        )
        available_subclasses = tuple(SUBCLASSES[self.class_])
        options = "\n".join(f"  - {s.value}" for s in available_subclasses)
        return (
            character_description
            + f"\n## Available {self.class_.value} Subclasses\n{options}"
        )

    def apply(self, blueprint: _BPT) -> _BPT:
        _check_can_assign(self.class_, blueprint.classes)
        subclass_enum = SUBCLASSES[self.class_]
        for existing in blueprint.subclasses:
            if isinstance(existing, subclass_enum):
                return blueprint

        prompt = self._build_prompt(blueprint)

        class _SubclassSelectionBase(BaseModel):
            subclass: AnySubclass

        SubclassSelection = create_model(
            f"{self.class_.value}SubclassSelection",
            __base__=_SubclassSelectionBase,
            subclass=(subclass_enum, ...),
        )

        result = self.llm.create_structured_output(prompt, SubclassSelection)
        selected: AnySubclass = result.subclass
        return blueprint.model_copy(
            update={"subclasses": blueprint.subclasses + (selected,)}
        )
