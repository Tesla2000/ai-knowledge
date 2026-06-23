"""AI-powered language choice resolver."""

from __future__ import annotations

from collections.abc import Generator

from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.language_choice_resolver.base import (
    LanguageChoiceResolver,
    LanguagesDelta,
)
from dnd.character.blueprint.state import HasLanguages
from dnd.choices.language import Language
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import Field
from typing_protocol_intersection import ProtocolIntersection


class LanguageSelection(BaseModel):
    """Schema for AI to select language replacements."""

    languages: set[Language] = Field(default_factory=set)


class AILanguageChoiceResolver[T: HasLanguages](LanguageChoiceResolver[T]):
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

    def _select_from_available(self, available: list[Language], state: T) -> Language:
        """Not used — this class overrides get_change directly."""
        raise NotImplementedError("AILanguageChoiceResolver overrides get_change")

    def _build_prompt(self, state: T) -> str:
        system_prompt = (
            "You are resolving Language.ANY_OF_YOUR_CHOICE placeholders "
            "for a D&D 5e character.\n"
            "Replace each placeholder with the most appropriate language "
            "based on the character's race, class, background, and concept.\n"
        )

        character_description = self.formatter.format(
            state, system_prompt=system_prompt
        )

        instructions = ["\n## Placeholders to Resolve\n"]

        count = list(state.languages).count(Language.ANY_OF_YOUR_CHOICE)
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

    def get_change(
        self, state: T
    ) -> Generator[LanguagesDelta, None, ProtocolIntersection[T, HasLanguages]]:
        if Language.ANY_OF_YOUR_CHOICE not in state.languages:
            delta = LanguagesDelta(languages=frozenset(state.languages))
            yield delta
            return delta.apply(state)

        prompt = self._build_prompt(state)
        if not prompt:
            delta = LanguagesDelta(languages=frozenset(state.languages))
            yield delta
            return delta.apply(state)

        structured_llm = self.llm.with_structured_output(LanguageSelection)
        _result = structured_llm.invoke(prompt)
        if not isinstance(_result, LanguageSelection):
            raise TypeError(f"Expected LanguageSelection, got {type(_result)}")
        selection = _result

        count = list(state.languages).count(Language.ANY_OF_YOUR_CHOICE)
        if len(selection.languages) != count:
            raise ValueError(
                f"AI returned {len(selection.languages)} languages but expected {count}"
            )

        new_languages = set(state.languages)
        new_languages.discard(Language.ANY_OF_YOUR_CHOICE)
        new_languages.update(selection.languages)

        delta = LanguagesDelta(languages=frozenset(new_languages))
        yield delta
        return delta.apply(state)
