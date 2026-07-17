from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Annotated,
    ClassVar,
    Protocol,
    assert_never,
    runtime_checkable,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    InstanceOf,
    NonNegativeInt,
    PositiveInt,
)
from typing import Self

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap

from dnd.character.blueprint.character_data import CharacterData
from dnd.character.class_levels import ClassLevels
from dnd.character.spells.max_spell_levels import SpellSlots
from dnd.character.actions._ability_name import AbilityName
from dnd.character.actions._damage_type import DamageType
from dnd.choices.abilities.action import AttackAction, AnyAction
from dnd.fight._condition import Condition
from dnd.fight._fight_resource import _FightResource, ResourceName

_KNOWN_ABILITIES: frozenset[str] = frozenset(AbilityName)


@runtime_checkable
class _CombatCharacter(Protocol):
    health: int
    classes: ClassLevels
    actions: tuple[AnyAction, ...]
    character_data: CharacterData


@runtime_checkable
class _SpellcasterCharacter(_CombatCharacter, Protocol):
    spell_slots: SpellSlots[int, int, int, int, int, int, int, int, int]


class _CombatantBase[HealthType: NonNegativeInt](BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    character: InstanceOf[_CombatCharacter]
    initiative: int
    max_health: PositiveInt
    current_health: HealthType
    temporary_health: NonNegativeInt = 0
    conditions: frozenset[Condition] = frozenset()
    resources: tuple[_FightResource, ...] = ()
    position: tuple[int, int] = (0, 0)

    @property
    def name(self) -> str:
        return self.character.character_data.name or "Unknown"

    def add_condition(self, c: Condition) -> Self:
        return self.model_copy(update={"conditions": self.conditions | {c}})

    def remove_condition(self, c: Condition) -> Self:
        return self.model_copy(update={"conditions": self.conditions - {c}})

    def use_resource(self, name: ResourceName) -> Self:
        updated = tuple(
            r.model_copy(update={"remaining_uses": max(0, r.remaining_uses - 1)})
            if r.name == name
            else r
            for r in self.resources
        )
        return self.model_copy(update={"resources": updated})

    def add_temporary_health(self, amount: int) -> Self:
        new_temp = max(self.temporary_health, amount)
        return self.model_copy(update={"temporary_health": new_temp})

    def on_character_turn_start(self) -> Self:
        return self

    def on_character_turn_end(self) -> Self:
        return self

    def on_round_start(self) -> Self:
        return self

    def on_round_end(self) -> Self:
        return self


class FightCharacter(_CombatantBase[PositiveInt]):
    has_action: bool = True
    has_bonus_action: bool = True
    has_reaction: bool = True
    has_free_action: bool = True
    attack_bonus: int = 0
    damage_resistance: frozenset[DamageType] = frozenset()
    active_features: frozenset[AbilityName] = frozenset()

    @classmethod
    def from_presentable(
        cls,
        character: _CombatCharacter,
        initiative: int,
        resources: tuple[_FightResource, ...] = (),
    ) -> FightCharacter:
        return cls(
            character=character,
            initiative=initiative,
            max_health=character.health,
            current_health=character.health,
            resources=resources,
        )

    def on_character_turn_start(self) -> Self:
        return self.model_copy(
            update={
                "has_action": True,
                "has_bonus_action": True,
                "has_reaction": True,
                "has_free_action": True,
            }
        )

    def spend_action(self) -> Self:
        return self.model_copy(update={"has_action": False})

    def spend_bonus_action(self) -> Self:
        return self.model_copy(update={"has_bonus_action": False})

    def spend_reaction(self) -> Self:
        return self.model_copy(update={"has_reaction": False})

    def spend_free_action(self) -> Self:
        return self.model_copy(update={"has_free_action": False})

    def take_damage(self, amount: int) -> FightCharacter | DownedFightCharacter:
        remaining = amount
        new_temp = self.temporary_health
        if new_temp > 0:
            absorbed = min(new_temp, remaining)
            new_temp -= absorbed
            remaining -= absorbed
        new_hp = self.current_health - remaining
        if new_hp <= 0:
            return DownedFightCharacter.from_active(
                self.model_copy(
                    update={"current_health": 1, "temporary_health": new_temp}
                )
            )
        return self.model_copy(
            update={
                "current_health": new_hp,
                "temporary_health": new_temp,
            }
        )

    def heal(self, amount: int) -> Self:
        new_hp = min(self.current_health + amount, self.max_health)
        return self.model_copy(update={"current_health": new_hp})

    def get_actions(
        self, battlemap: Battlemap
    ) -> tuple[tuple[AnyCombatAction, ...], ...]:
        candidates: list[tuple[AnyCombatAction, ...]] = []
        for action in self.character.actions:
            if isinstance(action, AttackAction):
                for attack_cls in (AttackWithAxe,):
                    attack_options = attack_cls.create(self, battlemap)
                    if attack_options:
                        candidates.append(attack_options)
                        break
            elif action.name in _KNOWN_ABILITIES:
                ability = AbilityName(action.name)
                match ability:
                    case AbilityName.RAGE:
                        rage_options = UseRage.create(self)
                        if rage_options:
                            candidates.append(rage_options)
                    case AbilityName.ATTACK_WITH_AXE:
                        pass
                    case _ as unreachable:
                        assert_never(unreachable)
        return tuple(candidates)


class SpellcasterFightCharacter(FightCharacter):
    remaining_spell_slots: SpellSlots[int, int, int, int, int, int, int, int, int]

    @classmethod
    def from_presentable(
        cls,
        character: _SpellcasterCharacter,
        initiative: int,
        resources: tuple[_FightResource, ...] = (),
    ) -> SpellcasterFightCharacter:
        return cls(
            character=character,
            initiative=initiative,
            max_health=character.health,
            current_health=character.health,
            remaining_spell_slots=character.spell_slots,
            resources=resources,
        )


class DownedFightCharacter(_CombatantBase):
    current_health: NonNegativeInt = 0
    death_save_successes: Annotated[int, Field(ge=0, le=3)] = 0
    death_save_failures: Annotated[int, Field(ge=0, le=3)] = 0

    @classmethod
    def from_active(cls, fc: FightCharacter) -> DownedFightCharacter:
        return cls(
            character=fc.character,
            initiative=fc.initiative,
            max_health=fc.max_health,
            current_health=0,
            temporary_health=0,
            conditions=fc.conditions | {Condition.UNCONSCIOUS},
            resources=fc.resources,
        )

    def make_death_save(
        self, success: bool
    ) -> DownedFightCharacter | StabilizedFightCharacter | DeadFightCharacter:
        if success:
            new_successes = self.death_save_successes + 1
            if new_successes >= 3:
                return StabilizedFightCharacter.from_downed(self)
            return self.model_copy(update={"death_save_successes": new_successes})
        new_failures = self.death_save_failures + 1
        if new_failures >= 3:
            return DeadFightCharacter.from_downed(self)
        return self.model_copy(update={"death_save_failures": new_failures})

    def take_damage(self, amount: int) -> Self:
        new_failures = min(3, self.death_save_failures + 1)
        return self.model_copy(update={"death_save_failures": new_failures})

    def heal(self, amount: int) -> FightCharacter:
        new_hp = min(amount, self.max_health)
        return FightCharacter(
            character=self.character,
            initiative=self.initiative,
            max_health=self.max_health,
            current_health=new_hp if new_hp > 0 else 1,
            temporary_health=self.temporary_health,
            conditions=self.conditions - {Condition.UNCONSCIOUS},
            resources=self.resources,
        )


class StabilizedFightCharacter(_CombatantBase):
    current_health: NonNegativeInt = 0

    @classmethod
    def from_downed(cls, fc: DownedFightCharacter) -> StabilizedFightCharacter:
        return cls(
            character=fc.character,
            initiative=fc.initiative,
            max_health=fc.max_health,
            current_health=0,
            temporary_health=fc.temporary_health,
            conditions=fc.conditions,
            resources=fc.resources,
        )

    def heal(self, amount: int) -> FightCharacter:
        new_hp = min(amount, self.max_health)
        return FightCharacter(
            character=self.character,
            initiative=self.initiative,
            max_health=self.max_health,
            current_health=new_hp if new_hp > 0 else 1,
            temporary_health=self.temporary_health,
            conditions=self.conditions - {Condition.UNCONSCIOUS},
            resources=self.resources,
        )


class DeadFightCharacter(_CombatantBase):
    current_health: NonNegativeInt = 0

    @classmethod
    def from_downed(cls, fc: DownedFightCharacter) -> DeadFightCharacter:
        return cls(
            character=fc.character,
            initiative=fc.initiative,
            max_health=fc.max_health,
            current_health=0,
            temporary_health=0,
            conditions=fc.conditions | {Condition.UNCONSCIOUS},
            resources=fc.resources,
        )

    def revive(self, amount: int) -> FightCharacter:
        new_hp = min(max(1, amount), self.max_health)
        return FightCharacter(
            character=self.character,
            initiative=self.initiative,
            max_health=self.max_health,
            current_health=new_hp,
            temporary_health=0,
            conditions=self.conditions - {Condition.UNCONSCIOUS},
            resources=self.resources,
        )


AnyActiveCombatant = (
    FightCharacter
    | SpellcasterFightCharacter
    | DownedFightCharacter
    | StabilizedFightCharacter
    | DeadFightCharacter
)

# Bottom imports after all classes are defined to resolve circular dependency
from dnd.character.actions.combat_action import (  # noqa: E402
    AnyCombatAction,
    AttackWithAxe,
    UseRage,
)
