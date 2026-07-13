"""AI-powered language choice resolver."""

from dnd.character.blueprint.formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.language_choice_resolver.base import (
    LanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.language import Language
from pydantic import BaseModel
from pydantic import Field
from structured_output_creator import OpenAIService, RaisingService
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)


class LanguageSelection(BaseModel):
    """Schema for AI to select language replacements."""

    languages: set[Language] = Field(default_factory=set)


class AILanguageChoiceResolver(LanguageChoiceResolver):
    """AI-powered resolver for Language.ANY_OF_YOUR_CHOICE placeholders.

    Uses an LLM to make intelligent language selections based on
    character context (race, background, class, etc.).

    Example:
        >>> resolver = AILanguageChoiceResolver(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        ...  )
    """

    type: Literal[BuildingBlockType.AI_LANGUAGE_CHOICE_RESOLVER] = (
        BuildingBlockType.AI_LANGUAGE_CHOICE_RESOLVER
    )

    llm: RaisingService = Field(
        default_factory=lambda: RaisingService(service=OpenAIService()),
        description="Language model for making AI-powered decisions",
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _select_from_available(
        self, available: list[Language], languages: tuple[Language, ...]
    ) -> Language:
        """Not used — this class overrides apply directly."""
        raise NotImplementedError("AILanguageChoiceResolver overrides apply")

    def _build_prompt(self, blueprint: _WideBlueprint) -> str:
        system_prompt = (
            "You are resolving Language.ANY_OF_YOUR_CHOICE placeholders "
            "for a D&D 5e character.\n"
            "Replace each placeholder with the most appropriate language "
            "based on the character's race, class, background, and concept.\n"
        )

        character_description = self.formatter.format(
            blueprint, system_prompt=system_prompt
        )

        instructions = ["\n## Placeholders to Resolve\n"]

        count = list(blueprint.languages).count(Language.ANY_OF_YOUR_CHOICE)
        if count == 0:
            return ""

        instructions.append(
            f"Languages: {count} ANY_OF_YOUR_CHOICE placeholder(s) to replace"
        )
        instructions.append(
            f"  Available: {', '.join(language.value for language in Language if language != Language.ANY_OF_YOUR_CHOICE)}"
        )
        instructions.append(
            "\n## Selection Instructions\n"
            "Return the complete language set with placeholders replaced "
            "by specific choices.\n"
            "Choose languages that best fit the character's race, "
            "background, and concept.\n"
            "Avoid duplicates unless the character already has them."
        )

        return character_description + "\n".join(instructions)

    def apply(self, blueprint: _BPT) -> _BPT:
        if Language.ANY_OF_YOUR_CHOICE not in blueprint.languages:
            return blueprint

        prompt = self._build_prompt(blueprint)
        if not prompt:
            return blueprint

        selection = self.llm.create_structured_output(prompt, LanguageSelection)

        count = list(blueprint.languages).count(Language.ANY_OF_YOUR_CHOICE)
        if len(selection.languages) != count:
            raise ValueError(
                f"AI returned {len(selection.languages)} languages but expected {count}"
            )

        new_languages = set(blueprint.languages)
        new_languages.discard(Language.ANY_OF_YOUR_CHOICE)
        new_languages.update(selection.languages)

        return blueprint.model_copy(update={"languages": tuple(new_languages)})
