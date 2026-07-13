from abc import abstractmethod

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import _BPT
from dnd.choices.language import Language
from pydantic import ConfigDict


class LanguageChoiceResolver(BuildingBlock):
    """Resolves Language.ANY_OF_YOUR_CHOICE placeholders.

    This resolver replaces ANY_OF_YOUR_CHOICE placeholders in the
    blueprint's languages set with concrete Language choices.
    """

    model_config = ConfigDict(frozen=True)

    @abstractmethod
    def _select_from_available(
        self, available: list[Language], languages: tuple[Language, ...]
    ) -> Language: ...

    def apply(self, blueprint: _BPT) -> _BPT:
        resolved = list(blueprint.languages)
        for i, lang in enumerate(resolved):
            if lang == Language.ANY_OF_YOUR_CHOICE:
                available: list[Language] = [
                    option
                    for option in Language
                    if option != Language.ANY_OF_YOUR_CHOICE
                ]
                resolved[i] = self._select_from_available(
                    available, blueprint.languages
                )
        return blueprint.model_copy(update={"languages": tuple(resolved)})
