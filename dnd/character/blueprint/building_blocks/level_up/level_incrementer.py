from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import cast
from typing import ClassVar
from typing import TYPE_CHECKING
from typing import TypedDict

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasClasses
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasLevel
from dnd.character.blueprint.state import HasSorcererLevel
from dnd.character.blueprint.state import HasWizardLevel
from dnd.character.class_levels import ClassLevels
from dnd.character.delta.delta import Delta
from dnd.character.feature.feats import FeatName
from dnd.choices.class_creation.character_class import Class
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.stats_creation.statistic import Statistic
from dnd.other_profficiencies import WeaponProficiency
from dnd.skill_proficiency import Skill
from pydantic import PositiveInt


class _LevelIncrementExtra(TypedDict, total=False):
    feats: tuple[FeatName, ...]
    weapon_proficiencies: frozenset[WeaponProficiency]
    n_skill_choices: int
    skills_to_choose_from: frozenset[Skill]
    saving_throw_proficiencies: tuple[Statistic, ...]
    equipment_choices: tuple[tuple[str | WeaponName, ...], ...]
    other_equipment: tuple[str | WeaponName, ...]


class LevelIncrementDeltaBase(Delta, ABC):
    """Shared typed fields for all per-class level increment deltas.

    Blueprint-compatible fields are declared here; only fields explicitly
    provided in the constructor end up in model_fields_set and get
    propagated to the blueprint in apply().
    """

    class_level: PositiveInt
    feats: tuple[FeatName, ...] = ()
    weapon_proficiencies: frozenset[WeaponProficiency] = frozenset()
    n_skill_choices: int = 0
    skills_to_choose_from: frozenset[Skill] = frozenset()
    saving_throw_proficiencies: tuple[Statistic, ...] = ()
    equipment_choices: tuple[tuple[str | WeaponName, ...], ...] = ()
    other_equipment: tuple[str | WeaponName, ...] = ()

    def _extra(self, state: BlueprintProtocol) -> _LevelIncrementExtra:
        state_fields = {k for k, _ in state}
        return cast(
            _LevelIncrementExtra,
            {f: v for f, v in self if f in self.model_fields_set and f in state_fields},
        )

    @abstractmethod
    def apply[T: BlueprintProtocol](self, state: T) -> BlueprintProtocol: ...


class WizardLevelIncrementDelta(LevelIncrementDeltaBase):
    """Delta produced when WizardLevelIncrementer increments wizard class level."""

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasWizardLevel]:
        existing = state.classes if isinstance(state, HasClasses) else ClassLevels()

        if TYPE_CHECKING:

            class _WizardClassLevels(ClassLevels):
                wizard: PositiveInt

                def get_wizard_level(self) -> PositiveInt:
                    return self.wizard

            class _NewBlueprint(Blueprint):
                classes: _WizardClassLevels

                def get_wizard_level(self) -> PositiveInt:
                    return self.classes.get_wizard_level()

        else:

            class _WizardClassLevels(type(existing)):
                wizard: PositiveInt

                def get_wizard_level(self) -> PositiveInt:
                    return self.wizard

            class _NewBlueprint(type(state)):
                classes: _WizardClassLevels

                def get_wizard_level(self) -> PositiveInt:
                    return self.classes.get_wizard_level()

        new_classes = _WizardClassLevels.model_validate(
            {**dict(existing), "wizard": self.class_level}
        )
        result = _NewBlueprint.model_validate(
            {**dict(state), "classes": new_classes, **self._extra(state)}
        )
        return cast(ProtocolIntersection[T, HasWizardLevel], result)


class SorcererLevelIncrementDelta(LevelIncrementDeltaBase):
    """Delta produced when SorcererLevelIncrementer increments sorcerer class level."""

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[T, HasSorcererLevel]:
        existing = state.classes if isinstance(state, HasClasses) else ClassLevels()

        if TYPE_CHECKING:

            class _SorcererClassLevels(ClassLevels):
                sorcerer: PositiveInt

                def get_sorcerer_level(self) -> PositiveInt:
                    return self.sorcerer

            class _NewBlueprint(Blueprint):
                classes: _SorcererClassLevels

                def get_sorcerer_level(self) -> PositiveInt:
                    return self.classes.get_sorcerer_level()

        else:

            class _SorcererClassLevels(type(existing)):
                sorcerer: PositiveInt

                def get_sorcerer_level(self) -> PositiveInt:
                    return self.sorcerer

            class _NewBlueprint(type(state)):
                classes: _SorcererClassLevels

                def get_sorcerer_level(self) -> PositiveInt:
                    return self.classes.get_sorcerer_level()

        new_classes = _SorcererClassLevels.model_validate(
            {**dict(existing), "sorcerer": self.class_level}
        )
        result = _NewBlueprint.model_validate(
            {**dict(state), "classes": new_classes, **self._extra(state)}
        )
        return cast(ProtocolIntersection[T, HasSorcererLevel], result)


class LevelIncrementer[
    T: HasLevel,
    DeltaT: LevelIncrementDeltaBase,
    StateOut: BlueprintProtocol,
](BuildingBlock[T, DeltaT, StateOut], ABC):
    """Abstract base for building blocks that increment a character's level in one class.

    Subclass per class — do not add match statements here. Each concrete subclass
    owns its delta type, current-level retrieval, and first-level grant logic.
    """

    _ASI_LEVELS: ClassVar[frozenset[int]] = frozenset({4, 8, 12, 16, 19})

    def get_change(
        self, state: T
    ) -> Generator[DeltaT, None, ProtocolIntersection[T, StateOut]]:
        existing_classes = (
            state.classes if isinstance(state, HasClasses) else ClassLevels()
        )
        current_level = self._get_current_level(state)
        new_level = current_level + 1
        total_class_levels = existing_classes.total_level() + 1
        if total_class_levels > state.level:
            raise ValueError(
                f"Total class levels ({total_class_levels}) would exceed "
                f"character level ({state.level}). "
                "Set character level first with LevelAssigner."
            )
        if total_class_levels == 1:
            delta = self._first_level_delta(new_level)
        elif new_level in self._ASI_LEVELS:
            feats = (state.feats if isinstance(state, HasFeats) else ()) + (
                FeatName.ANY_EXCEPT_ABILITY_SCORE_IMPROVEMENT,
            )
            delta = self._make_delta(new_level, feats)
        else:
            delta = self._make_delta(new_level)
        yield delta
        return cast(ProtocolIntersection[T, StateOut], delta.apply(state))

    @abstractmethod
    def _get_current_level(self, state: T) -> int: ...

    @abstractmethod
    def _first_level_delta(self, class_level: PositiveInt) -> DeltaT: ...

    @abstractmethod
    def _make_delta(
        self, class_level: int, feats: tuple[FeatName, ...] = ()
    ) -> DeltaT: ...


class WizardLevelIncrementer[T: HasLevel](
    LevelIncrementer[T, WizardLevelIncrementDelta, HasWizardLevel]
):
    """Increments wizard class level; grants proficiencies at level 1 and ASI at 4/8/12/16/19."""

    @property
    def class_(self) -> Class:
        return Class.WIZARD

    def _get_current_level(self, state: T) -> int:
        return state.get_wizard_level() if isinstance(state, HasWizardLevel) else 0

    def _make_delta(
        self, class_level: int, feats: tuple[FeatName, ...] = ()
    ) -> WizardLevelIncrementDelta:
        if feats:
            return WizardLevelIncrementDelta(class_level=class_level, feats=feats)
        return WizardLevelIncrementDelta(class_level=class_level)

    def _first_level_delta(self, class_level: PositiveInt) -> WizardLevelIncrementDelta:
        return WizardLevelIncrementDelta(
            class_level=class_level,
            weapon_proficiencies=frozenset(
                {
                    WeaponProficiency.DAGGER,
                    WeaponProficiency.DART,
                    WeaponProficiency.SLING,
                    WeaponProficiency.QUARTERSTAFF,
                    WeaponProficiency.LIGHT_CROSSBOW,
                }
            ),
            n_skill_choices=2,
            skills_to_choose_from=frozenset(
                {
                    Skill.ARCANA,
                    Skill.HISTORY,
                    Skill.INSIGHT,
                    Skill.INVESTIGATION,
                    Skill.MEDICINE,
                    Skill.RELIGION,
                }
            ),
            saving_throw_proficiencies=(
                Statistic.INTELLIGENCE,
                Statistic.WISDOM,
            ),
            equipment_choices=(
                (WeaponName.QUARTERSTAFF, WeaponName.DAGGER),
                ("component pouch", "arcane focus"),
                ("scholor's pack", "explarer's pack"),
            ),
            other_equipment=("spellbook",),
        )


class SorcererLevelIncrementer[T: HasLevel](
    LevelIncrementer[T, SorcererLevelIncrementDelta, HasSorcererLevel]
):
    """Increments sorcerer class level; grants proficiencies at level 1 and ASI at 4/8/12/16/19."""

    @property
    def class_(self) -> Class:
        return Class.SORCERER

    def _get_current_level(self, state: T) -> int:
        return state.get_sorcerer_level() if isinstance(state, HasSorcererLevel) else 0

    def _make_delta(
        self, class_level: int, feats: tuple[FeatName, ...] = ()
    ) -> SorcererLevelIncrementDelta:
        if feats:
            return SorcererLevelIncrementDelta(class_level=class_level, feats=feats)
        return SorcererLevelIncrementDelta(class_level=class_level)

    def _first_level_delta(
        self, class_level: PositiveInt
    ) -> SorcererLevelIncrementDelta:
        return SorcererLevelIncrementDelta(
            class_level=class_level,
            weapon_proficiencies=frozenset(
                {
                    WeaponProficiency.DAGGER,
                    WeaponProficiency.DART,
                    WeaponProficiency.SLING,
                    WeaponProficiency.QUARTERSTAFF,
                    WeaponProficiency.LIGHT_CROSSBOW,
                }
            ),
            n_skill_choices=2,
            skills_to_choose_from=frozenset(
                {
                    Skill.ARCANA,
                    Skill.DECEPTION,
                    Skill.INSIGHT,
                    Skill.INTIMIDATION,
                    Skill.PERSUASION,
                    Skill.RELIGION,
                }
            ),
            saving_throw_proficiencies=(
                Statistic.CHARISMA,
                Statistic.CONSTITUTION,
            ),
            equipment_choices=(
                (WeaponName.CROSSBOW_LIGHT, WeaponName.DAGGER),
                ("component pouch", "arcane focus"),
                ("dungeoneer's pack", "explarer's pack"),
            ),
            other_equipment=(WeaponName.DAGGER, WeaponName.DAGGER),
        )
