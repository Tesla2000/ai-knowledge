from abc import ABC
from abc import abstractmethod
from typing import Protocol

from collections.abc import Callable

from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
    _WideBlueprint,
)
from dnd.character.blueprint.sentinels import (
    AnyClassLevel,
    AnyMetamagicChoices,
    AnyNonZeroSorcererLevel,
    AnyNonZeroWizardLevel,
    AnySorcererLevel,
    AnyStatChoices,
    AnyWizardLevel,
    MaybeCharacterData,
)
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.sorcerer.base import SorcererBlueprint
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardInfo
from dnd.character.race.race import Race
from dnd.character.stats import Stats
from pydantic import PositiveInt
from dnd.character.spells import ClassSpellLevel
from dnd.character.spells import get_class_spells_set
from dnd.character.spells import SpellLevel
from dnd.character.spells import Spell
from dnd.character.spells.max_spell_levels import SpellSlots
from dnd.character.spells.spells import Spells
from dnd.choices.class_creation.character_class import Class

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
        self, spell_level: SpellLevel, count: int, available: list[Spell]
    ) -> tuple[Spell, ...]: ...


def _get_available_spells(query: ClassSpellLevel) -> frozenset[Spell]:
    return get_class_spells_set(query)


def _wizard_query(spell_level: SpellLevel) -> ClassSpellLevel:
    return (Class.WIZARD, spell_level)


def _sorcerer_query(spell_level: SpellLevel) -> ClassSpellLevel:
    return (Class.SORCERER, spell_level)


def _apply_spells(
    spells: Spells,
    to_learn: dict[SpellLevel, int],
    make_query: Callable[[SpellLevel], ClassSpellLevel],
    selector: SpellSelector,
) -> Spells:
    for spell_level, count in to_learn.items():
        available = list(_get_available_spells(make_query(spell_level)))
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

    @abstractmethod
    def select_spells(
        self,
        spell_level: SpellLevel,
        count: int,
        available_spells: list[Spell],
        state: _WideBlueprint,
    ) -> tuple[Spell, ...]: ...

    def _get_spells_to_learn(
        self,
        class_level: int,
        spell_slots: SpellSlots,
    ) -> dict[SpellLevel, int]:
        if class_level == 1:
            return {0: 3, 1: 6}
        max_spell_level = spell_slots.max_level()
        n_cantrips_increase_levels = (4, 10)
        return {
            max_spell_level: 2,
            0: int(class_level in n_cantrips_increase_levels),
        }

    def apply[
        _WZK_: AnyNonZeroWizardLevel,
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _SOK_: AnySorcererLevel,
        _FGK_: AnyClassLevel,
        _BAK_: AnyClassLevel,
        _ROK_: AnyClassLevel,
        _CLK_: AnyClassLevel,
        _DRK_: AnyClassLevel,
        _PAK_: AnyClassLevel,
        _RAK_: AnyClassLevel,
        _MOK_: AnyClassLevel,
        _BDK_: AnyClassLevel,
        _WAK_: AnyClassLevel,
        _ARK_: AnyClassLevel,
        _CDK_: MaybeCharacterData,
    ](
        self,
        blueprint: Blueprint[
            Race,
            Stats,
            PositiveInt,
            _StCK_,
            _SkCK_,
            WizardInfo[_WZK_],
            CasterInfo,
            _SOK_,
            _FGK_,
            _BAK_,
            _ROK_,
            _CLK_,
            _DRK_,
            _PAK_,
            _RAK_,
            _MOK_,
            _BDK_,
            _WAK_,
            _ARK_,
            _CDK_,
        ],
    ) -> Blueprint[
        Race,
        Stats,
        PositiveInt,
        _StCK_,
        _SkCK_,
        WizardInfo[_WZK_],
        CasterInfo,
        _SOK_,
        _FGK_,
        _BAK_,
        _ROK_,
        _CLK_,
        _DRK_,
        _PAK_,
        _RAK_,
        _MOK_,
        _BDK_,
        _WAK_,
        _ARK_,
        _CDK_,
    ]:
        spells_to_learn = self._get_spells_to_learn(
            blueprint.classes.get_level(Class.WIZARD),
            blueprint.caster.spell_slots,
        )
        if not spells_to_learn:
            return blueprint

        assigner = self
        wizard_state = blueprint

        class _Selector:
            def select(
                self, spell_level: SpellLevel, count: int, available: list[Spell]
            ) -> tuple[Spell, ...]:
                return assigner.select_spells(
                    spell_level, count, available, wizard_state
                )

        spells = _apply_spells(
            blueprint.spells, spells_to_learn, _wizard_query, _Selector()
        )
        return blueprint.model_copy(update={"spells": spells})


class SorcererSpellAssigner(BuildingBlock, ABC):
    """Abstract base for sorcerer spell assignment strategies."""

    @abstractmethod
    def select_spells(
        self,
        spell_level: SpellLevel,
        count: int,
        available_spells: list[Spell],
        state: _WideBlueprint,
    ) -> tuple[Spell, ...]: ...

    def _get_spells_to_learn(
        self,
        class_level: int,
        spell_slots: SpellSlots,
    ) -> dict[SpellLevel, int]:
        if class_level == 1:
            return {0: 4, 1: 2}
        max_spell_level = spell_slots.max_level()
        n_cantrips_increase_levels = (4, 10)
        return {
            max_spell_level: 1,
            0: int(class_level in n_cantrips_increase_levels),
        }

    def apply[
        _StCK_: AnyStatChoices,
        _SkCK_: AnyStatChoices,
        _WIK_: WizardInfo[AnyWizardLevel] | None,
        _CK_: CasterInfo | None,
        _SOK_: AnyNonZeroSorcererLevel,
        _FGK_: AnyClassLevel,
        _BAK_: AnyClassLevel,
        _ROK_: AnyClassLevel,
        _CLK_: AnyClassLevel,
        _DRK_: AnyClassLevel,
        _PAK_: AnyClassLevel,
        _RAK_: AnyClassLevel,
        _MOK_: AnyClassLevel,
        _BDK_: AnyClassLevel,
        _WAK_: AnyClassLevel,
        _ARK_: AnyClassLevel,
        _CDK_: MaybeCharacterData,
        _McK_: AnyMetamagicChoices,
    ](
        self,
        blueprint: SorcererBlueprint[
            _StCK_,
            _SkCK_,
            _WIK_,
            _CK_,
            _SOK_,
            _FGK_,
            _BAK_,
            _ROK_,
            _CLK_,
            _DRK_,
            _PAK_,
            _RAK_,
            _MOK_,
            _BDK_,
            _WAK_,
            _ARK_,
            _CDK_,
            _McK_,
        ],
    ) -> SorcererBlueprint[
        _StCK_,
        _SkCK_,
        _WIK_,
        _CK_,
        _SOK_,
        _FGK_,
        _BAK_,
        _ROK_,
        _CLK_,
        _DRK_,
        _PAK_,
        _RAK_,
        _MOK_,
        _BDK_,
        _WAK_,
        _ARK_,
        _CDK_,
        _McK_,
    ]:
        spells_to_learn = self._get_spells_to_learn(
            blueprint.classes.get_level(Class.SORCERER),
            blueprint.spell_slots,
        )
        if not spells_to_learn:
            return blueprint

        assigner = self
        sorcerer_state = blueprint

        class _Selector:
            def select(
                self, spell_level: SpellLevel, count: int, available: list[Spell]
            ) -> tuple[Spell, ...]:
                return assigner.select_spells(
                    spell_level, count, available, sorcerer_state
                )

        spells = _apply_spells(
            blueprint.spells, spells_to_learn, _sorcerer_query, _Selector()
        )
        return blueprint.model_copy(update={"spells": spells})
