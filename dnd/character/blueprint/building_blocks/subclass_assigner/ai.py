"""AI-powered subclass assigner for intelligent subclass selection."""

from __future__ import annotations

from collections.abc import Generator
from typing import Never
from typing import overload

from typing_extensions import deprecated
from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    SubclassDelta,
    _SubclassT,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.base import (
    _check_can_assign,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasSubclasses
from dnd.character.delta.delta import Delta
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
    """AI-powered subclass assigner that selects subclasses based on character context.

    Uses an LLM to make intelligent subclass selections based on the character's
    background, stats, personality, and overall concept.

    Example:
        >>> from dnd.choices.class_creation.character_class import Class
        >>> from langchain_openai import ChatOpenAI
        >>> assigner = AISubclassAssigner(
        ...     class_=Class.WIZARD,
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
        ... )
        >>> builder = Builder().add(assigner)
    """

    type: Literal[BuildingBlockType.AI_SUBCLASS_ASSIGNER] = (
        BuildingBlockType.AI_SUBCLASS_ASSIGNER
    )

    class_: Class = Field(
        description="The character class for which to assign a subclass"
    )
    llm: RaisingService = Field(
        default_factory=lambda: RaisingService(service=OpenAIService()),
        description="Language model for making AI-powered decisions",
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _build_prompt(self, state: _SubclassT) -> str:
        system_prompt = (
            f"You are selecting a subclass for a D&D 5e {self.class_.value}.\n"
            "Choose the subclass that best fits the character's:\n"
            "  - Background and backstory\n"
            "  - Personality and ideals\n"
            "  - Ability score distribution\n"
            "  - Overall character concept and theme\n"
            "\nThe subclass should feel like a natural extension of who this character is.\n"
        )

        character_description = self.formatter.format(
            state, system_prompt=system_prompt
        )

        available_subclasses = tuple(SUBCLASSES[self.class_])
        subclass_instructions = [
            f"\n## Available {self.class_.value} Subclasses",
            "Select ONE subclass from the following options:\n",
        ]

        for subclass_option in available_subclasses:
            subclass_instructions.append(f"  - {subclass_option.value}")

        subclass_instructions.append(
            "\n## Selection Instructions\n"
            "Return exactly one subclass from the list above.\n"
            "Consider which subclass:\n"
            "  - Aligns with the character's backstory and motivations\n"
            "  - Complements their ability scores and playstyle\n"
            "  - Fits their personality and moral alignment\n"
            "  - Makes thematic sense for their background"
        )

        return character_description + "\n".join(subclass_instructions)

    @overload
    def get_change[T: _SubclassT](
        self, state: T
    ) -> Generator[SubclassDelta, None, ProtocolIntersection[T, HasSubclasses]]: ...

    @overload
    @deprecated(
        "Pass a state satisfying HasClasses and HasSubclasses for precise return typing"
    )
    def get_change[T: BlueprintProtocol](self, state: T) -> Never: ...

    def get_change[T: BlueprintProtocol](
        self, state: T
    ) -> Generator[Delta, None, BlueprintProtocol]:
        if not isinstance(state, _SubclassT):
            raise TypeError(
                f"{type(self).__name__} requires HasClasses and HasSubclasses, got {type(state).__name__}"
            )
        _check_can_assign(self.class_, state)
        subclass_enum = SUBCLASSES[self.class_]
        for existing in state.subclasses:
            if isinstance(existing, subclass_enum):
                delta = SubclassDelta(subclasses=state.subclasses)
                yield delta
                return delta.apply(state)

        prompt = self._build_prompt(state)

        class _SubclassSelectionBase(BaseModel):
            subclass: AnySubclass

        SubclassSelection = create_model(
            f"{self.class_.value}SubclassSelection",
            __base__=_SubclassSelectionBase,
            subclass=(subclass_enum, ...),
        )

        result = self.llm.create_structured_output(prompt, SubclassSelection)
        selected: AnySubclass = result.subclass
        delta = SubclassDelta(subclasses=state.subclasses + (selected,))
        yield delta
        return delta.apply(state)
