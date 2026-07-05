from __future__ import annotations

from abc import abstractmethod
from collections.abc import Generator
from typing import cast
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasLanguages
from dnd.character.delta.delta import Delta
from dnd.choices.language import Language
from pydantic import ConfigDict


class LanguagesDelta(Delta):
    """Delta produced when LanguageChoiceResolver resolves language choices."""

    languages: tuple[Language, ...]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasLanguages]:

        if TYPE_CHECKING:

            class BlueprintWithLanguages(Blueprint):
                languages: tuple[Language, ...]

        else:

            class BlueprintWithLanguages(type(state)):
                languages: tuple[Language, ...]

        return cast(
            ProtocolIntersection[T, HasLanguages],
            BlueprintWithLanguages.model_validate(
                {**dict(state), "languages": self.languages}
            ),
        )


class LanguageChoiceResolver[T: HasLanguages](
    BuildingBlock[T, LanguagesDelta, HasLanguages]
):
    """Resolves Language.ANY_OF_YOUR_CHOICE placeholders.

    This resolver replaces ANY_OF_YOUR_CHOICE placeholders in the
    blueprint's languages set with concrete Language choices.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_from_available(
        self, available: list[Language], state: T
    ) -> Language: ...

    def get_change(
        self, state: T
    ) -> Generator[LanguagesDelta, None, ProtocolIntersection[T, HasLanguages]]:
        resolved = list(state.languages)
        for i, lang in enumerate(resolved):
            if lang == Language.ANY_OF_YOUR_CHOICE:
                available: list[Language] = [
                    option
                    for option in Language
                    if option != Language.ANY_OF_YOUR_CHOICE
                ]
                resolved[i] = self._select_from_available(available, state)
        delta = LanguagesDelta(languages=tuple(resolved))
        yield delta
        return delta.apply(state)
