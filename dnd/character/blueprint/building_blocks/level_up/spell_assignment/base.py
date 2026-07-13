from abc import ABC
from abc import abstractmethod
from typing import ClassVar
from typing import Protocol

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.states.state import _BPT
from dnd.character.spells import Cantrip
from dnd.character.spells import EighthLevel
from dnd.character.spells import FifthLevel
from dnd.character.spells import filter_accessible
from dnd.character.spells import FirstLevel
from dnd.character.spells import FourthLevel
from dnd.character.spells import NinthLevel
from dnd.character.spells import SecondLevel
from dnd.character.spells import SeventhLevel
from dnd.character.spells import SixthLevel
from dnd.character.spells import Spell
from dnd.character.spells import ThirdLevel
from dnd.character.spells.max_spell_levels import CasterType
from dnd.character.spells.max_spell_levels import MAX_SPELL_LEVELS
from dnd.character.spells.spells import Spells
from dnd.choices.class_creation.character_class import Class


_SPELL_LEVEL_TO_CLASS: list[type[Spell]] = [
    Cantrip,
    FirstLevel,
    SecondLevel,
    ThirdLevel,
    FourthLevel,
    FifthLevel,
    SixthLevel,
    SeventhLevel,
    EighthLevel,
    NinthLevel,
]

_SPELL_LEVEL_TO_ATTR: list[str] = [
    "cantrips",
    "first_level_spells",
    "second_level_spells",
    "third_level_spells",
    "fourth_level_spells",
    "fifth_level_spells",
    "sixth_level_spells",
    "seventh_level_spells",
    "eighth_level_spells",
    "ninth_level_spells",
]


class SpellSelector(Protocol):
    def select(
        self, spell_level: int, count: int, available: list[Spell]
    ) -> tuple[Spell, ...]: ...


def _get_available_spells(class_: Class, spell_level: int) -> frozenset[Spell]:
    return filter_accessible(_SPELL_LEVEL_TO_CLASS[spell_level], class_)


def _apply_spells(
    spells: Spells,
    to_learn: dict[int, int],
    class_: Class,
    selector: SpellSelector,
) -> Spells:
    for spell_level, count in to_learn.items():
        available = list(_get_available_spells(class_, spell_level))
        if not available:
            continue
        existing = set(spells.get_spells_by_level()[spell_level])
        filtered = [s for s in available if s not in existing]
        if not filtered:
            continue
        selected = selector.select(spell_level, count, filtered)
        merged = existing.union(selected)
        attr_name = _SPELL_LEVEL_TO_ATTR[spell_level]
        spells = spells.model_copy(update={attr_name: tuple(merged)})
    return spells


class WizardSpellAssigner(BuildingBlock, ABC):
    """Abstract base for wizard spell assignment strategies."""

    _caster_type: ClassVar[CasterType] = CasterType.FULL

    @abstractmethod
    def select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        state: _BPT,
    ) -> tuple[Spell, ...]: ...

    def _get_spells_to_learn(self, state: _BPT) -> dict[int, int]:
        level = state.classes.get_level(Class.WIZARD)
        if level == 1:
            return {0: 3, 1: 6}
        effective = level
        max_spell_level = MAX_SPELL_LEVELS[self._caster_type][min(effective, 20) - 1]
        n_cantrips_increase_levels = (4, 10)
        return {
            max_spell_level: 2,
            0: int(level in n_cantrips_increase_levels),
        }

    def apply(self, blueprint: _BPT) -> _BPT:
        if blueprint.classes.get_level(Class.WIZARD) == 0:
            return blueprint

        wizard_state = blueprint
        spells_to_learn = self._get_spells_to_learn(wizard_state)
        initial = blueprint.spells

        if not spells_to_learn:
            return blueprint

        assigner = self

        class _Selector:
            def select(
                self, spell_level: int, count: int, available: list[Spell]
            ) -> tuple[Spell, ...]:
                return assigner.select_spells(
                    spell_level, count, available, wizard_state
                )

        spells = _apply_spells(initial, spells_to_learn, Class.WIZARD, _Selector())
        return blueprint.model_copy(update={"spells": spells})


class SorcererSpellAssigner(BuildingBlock, ABC):
    """Abstract base for sorcerer spell assignment strategies."""

    _caster_type: ClassVar[CasterType] = CasterType.FULL

    @abstractmethod
    def select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        state: _BPT,
    ) -> tuple[Spell, ...]: ...

    def _get_spells_to_learn(self, state: _BPT) -> dict[int, int]:
        level = state.classes.get_level(Class.SORCERER)
        if level == 1:
            return {0: 4, 1: 2}
        effective = level
        max_spell_level = MAX_SPELL_LEVELS[self._caster_type][min(effective, 20) - 1]
        n_cantrips_increase_levels = (4, 10)
        return {
            max_spell_level: 1,
            0: int(level in n_cantrips_increase_levels),
        }

    def apply(self, blueprint: _BPT) -> _BPT:
        if blueprint.classes.get_level(Class.SORCERER) == 0:
            return blueprint

        sorcerer_state = blueprint
        spells_to_learn = self._get_spells_to_learn(sorcerer_state)
        initial = blueprint.spells

        if not spells_to_learn:
            return blueprint

        assigner = self

        class _Selector:
            def select(
                self, spell_level: int, count: int, available: list[Spell]
            ) -> tuple[Spell, ...]:
                return assigner.select_spells(
                    spell_level, count, available, sorcerer_state
                )

        spells = _apply_spells(initial, spells_to_learn, Class.SORCERER, _Selector())
        return blueprint.model_copy(update={"spells": spells})
