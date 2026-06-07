from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.choices.language import Language
from pydantic import ConfigDict


class LanguageChoiceResolver(BuildingBlock, ABC):
    """Resolves Language.ANY_OF_YOUR_CHOICE placeholders.

    This resolver replaces ANY_OF_YOUR_CHOICE placeholders in the
    blueprint's languages set with concrete Language choices.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_from_available(
        self, available: list[Language], blueprint: Blueprint
    ) -> Language:
        """Select a language from available options.

        Args:
            available: List of Language options excluding ANY_OF_YOUR_CHOICE.
            blueprint: Current character blueprint for context.

        Returns:
            Selected Language.
        """

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Replace Language.ANY_OF_YOUR_CHOICE placeholders.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with language placeholders replaced.
        """
        resolved = set()
        for lang in blueprint.languages:
            if lang == Language.ANY_OF_YOUR_CHOICE:
                available = [
                    language
                    for language in Language
                    if language != Language.ANY_OF_YOUR_CHOICE
                ]
                resolved.add(self._select_from_available(available, blueprint))
            else:
                resolved.add(lang)
        return Blueprint(languages=resolved)
