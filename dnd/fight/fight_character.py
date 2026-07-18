from __future__ import annotations

from random import randint
from typing import (
    TYPE_CHECKING,
    Annotated,
    ClassVar,
)
from uuid import uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    InstanceOf,
    NonNegativeInt,
    PositiveInt,
)
from typing import Self
from uuid_string import UUIDString

if TYPE_CHECKING:
    pass

from dnd.character._ability_name import AbilityName
from dnd.character.actions._any_modifier import AnyModifier
from dnd.character.actions._damage_type import DamageType
from dnd.character.actions.advantage_modifier import (
    AdvantageModifier,
    DisadvantageModifier,
    GrantsAdvantageModifier,
)
from dnd.fight._combat_event import (
    AnyCombatEvent,
    RageEndsEvent,
    TurnStartEvent,
)
from dnd.character.presentable_character import PresentableCharacter
from dnd.character.spells.max_spell_levels import SpellSlots
from dnd.choices.stats_creation.statistic import Statistic
from dnd.fight._condition import Condition
from dnd.fight._fight_resource import _FightResource, ResourceName


class _CombatantBase[HealthType: NonNegativeInt](BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    character: InstanceOf[PresentableCharacter]
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

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self, tuple[AnyCombatEvent, ...]]:
        return self, ()


class FightCharacter(_CombatantBase[PositiveInt]):
    has_action: bool = True
    has_bonus_action: bool = True
    has_reaction: bool = True
    has_free_action: bool = True
    base_ac: int = 10
    modifiers: tuple[AnyModifier, ...] = ()
    damage_resistance: frozenset[DamageType] = frozenset()
    condition_immunities: frozenset[Condition] = frozenset()
    active_features: frozenset[AbilityName] = frozenset()
    id: UUIDString = Field(default_factory=lambda: UUIDString(str(uuid4())))
    number_of_attacks: int = 1
    attacks_remaining: int = 1
    brutal_critical_dice: int = 0
    con_save_bonus: int = 0

    @property
    def ac(self) -> int:
        return self.base_ac

    @classmethod
    def from_presentable(
        cls,
        character: PresentableCharacter,
        initiative: int,
        resources: tuple[_FightResource, ...] = (),
    ) -> FightCharacter:
        number_of_attacks = 2 if AbilityName.EXTRA_ATTACK in character.actions else 1
        brutal_critical_dice = (
            3
            if AbilityName.BRUTAL_CRITICAL_3_DICE in character.actions
            else 2
            if AbilityName.BRUTAL_CRITICAL_2_DICE in character.actions
            else 1
            if AbilityName.BRUTAL_CRITICAL_1_DIE in character.actions
            else 0
        )
        con_save_bonus = character.stats.get_modifier(Statistic.CONSTITUTION)
        return cls(
            character=character,
            initiative=initiative,
            max_health=character.health,
            current_health=character.health,
            base_ac=character.ac,
            resources=resources,
            number_of_attacks=number_of_attacks,
            attacks_remaining=number_of_attacks,
            brutal_critical_dice=brutal_critical_dice,
            con_save_bonus=con_save_bonus,
        )

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self, tuple[AnyCombatEvent, ...]]:
        pending: list[AnyCombatEvent] = []
        surviving: list[AnyModifier] = []
        for m in self.modifiers:
            r, emitted = m.on_event(event)
            pending.extend(emitted)
            if r is not None:
                surviving.append(r)

        update: dict[str, object] = {}

        match event:
            case TurnStartEvent() if event.target_id == self.id:
                update["has_action"] = True
                update["has_bonus_action"] = True
                update["has_reaction"] = True
                update["has_free_action"] = True
                update["attacks_remaining"] = self.number_of_attacks
                surviving = [
                    m for m in surviving
                    if not isinstance(
                        m, (AdvantageModifier, DisadvantageModifier, GrantsAdvantageModifier)
                    )
                ]
            case RageEndsEvent() if event.target_id == self.id:
                update["active_features"] = self.active_features - {AbilityName.RAGE}
            case _:
                pass

        update["modifiers"] = tuple(surviving)
        return self.model_copy(update=update), tuple(pending)

    def spend_attack(self) -> Self:
        return self.model_copy(
            update={
                "attacks_remaining": self.attacks_remaining - 1,
                "has_action": False,
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
            if (
                self.has_reaction
                and AbilityName.RELENTLESS_RAGE in self.character.actions
                and randint(1, 20) + self.con_save_bonus >= 10
            ):
                return self.model_copy(
                    update={
                        "current_health": 1,
                        "temporary_health": new_temp,
                        "has_reaction": False,
                    }
                )
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


class SpellcasterFightCharacter(FightCharacter):
    remaining_spell_slots: SpellSlots

    @classmethod
    def from_presentable(
        cls,
        character: PresentableCharacter,
        initiative: int,
        resources: tuple[_FightResource, ...] = (),
    ) -> SpellcasterFightCharacter:
        number_of_attacks = 2 if AbilityName.EXTRA_ATTACK in character.actions else 1
        brutal_critical_dice = (
            3
            if AbilityName.BRUTAL_CRITICAL_3_DICE in character.actions
            else 2
            if AbilityName.BRUTAL_CRITICAL_2_DICE in character.actions
            else 1
            if AbilityName.BRUTAL_CRITICAL_1_DIE in character.actions
            else 0
        )
        con_save_bonus = character.stats.get_modifier(Statistic.CONSTITUTION)
        return cls(
            character=character,
            initiative=initiative,
            max_health=character.health,
            current_health=character.health,
            base_ac=character.ac,
            remaining_spell_slots=character.spell_slots,
            resources=resources,
            number_of_attacks=number_of_attacks,
            attacks_remaining=number_of_attacks,
            brutal_critical_dice=brutal_critical_dice,
            con_save_bonus=con_save_bonus,
        )

    def spend_level_1_slot(self) -> Self:
        return self.model_copy(
            update={
                "remaining_spell_slots": self.remaining_spell_slots.spend_level_1_slot()
            }
        )

    def spend_level_3_slot(self) -> Self:
        return self.model_copy(
            update={
                "remaining_spell_slots": self.remaining_spell_slots.spend_level_3_slot()
            }
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
