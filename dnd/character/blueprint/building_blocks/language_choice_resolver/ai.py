"""AI-powered language choice resolver."""

from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.blueprint_formatter import (
    BlueprintFormatter,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.base import (
    LanguageChoiceResolver,
)
from dnd.choices.language import Language
from langchain_openai import ChatOpenAI  # type: ignore[import-not-found]
from pydantic import BaseModel
from pydantic import Field


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

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _select_from_available(
        self, available: list[Language], blueprint: Blueprint
    ) -> Language:
        """Not used in AI implementation - overrides _get_change instead."""
        raise NotImplementedError(
            "AILanguageChoiceResolver overrides _get_change directly"
        )

    def _build_prompt(self, blueprint: Blueprint) -> str:
        """Build a prompt for AI language selection.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Formatted prompt string.
        """
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

        # Count language placeholders
        count = list(blueprint.languages).count(Language.ANY_OF_YOUR_CHOICE)
        if count == 0:
            return ""  # No placeholders to resolve

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

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Replace Language.ANY_OF_YOUR_CHOICE placeholders using AI.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with language placeholders replaced by AI selections.
        """
        # Check if there are any placeholders
        if Language.ANY_OF_YOUR_CHOICE not in blueprint.languages:
            return Blueprint()

        # Build prompt and get AI selection
        prompt = self._build_prompt(blueprint)
        if not prompt:
            return Blueprint()

        structured_llm = self.llm.with_structured_output(LanguageSelection)
        selection = structured_llm.invoke(prompt)

        # Validate selection count
        count = list(blueprint.languages).count(Language.ANY_OF_YOUR_CHOICE)
        if len(selection.languages) != count:
            raise ValueError(
                f"AI returned {len(selection.languages)} languages but expected {count}"
            )

        # Replace placeholders
        new_languages = set(blueprint.languages)
        new_languages.discard(Language.ANY_OF_YOUR_CHOICE)
        new_languages.update(selection.languages)

        return Blueprint(languages=new_languages)  # type: ignore[arg-type]
