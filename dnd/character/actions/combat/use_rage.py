from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from pydantic import InstanceOf
from typing import Self

from dnd.character._ability_name import AbilityName
from dnd.character.actions._any_modifier import AnyModifier
from dnd.character.actions._base_action import BonusAction
from dnd.character.actions._fight_resource import ResourceName
from dnd.character.actions.attack_bonus_modifier import RageAttackBonusModifier
from dnd.character.actions.conditional_immunity_modifier import (
    MindlessRageConditionalImmunityModifier,
)
from dnd.character.actions.damage_resistance_modifier import RageDamageResistanceModifier

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap
    from dnd.fight.fight_character import FightCharacter


@runtime_checkable
class _UseRagePerformer(Protocol):
    def apply_rage(self, battlemap: Battlemap) -> Battlemap: ...


class UseRage(BonusAction):
    name: Literal[AbilityName.RAGE] = AbilityName.RAGE
    range_tails: Literal[0] = 0
    radius_tails: Literal[0] = 0
    performer: InstanceOf[_UseRagePerformer]

    @classmethod
    def create(cls, fighter: FightCharacter) -> tuple[Self, ...]:
        class _Performer:
            def apply_rage(self, battlemap: Battlemap) -> Battlemap:
                rage_mods: tuple[AnyModifier, ...] = (
                    RageAttackBonusModifier(owner_id=fighter.id),
                    RageDamageResistanceModifier(owner_id=fighter.id),
                )
                if AbilityName.MINDLESS_RAGE in fighter.character.actions:
                    rage_mods = rage_mods + (
                        MindlessRageConditionalImmunityModifier(owner_id=fighter.id),
                    )
                updated = fighter.model_copy(
                    update={
                        "has_bonus_action": False,
                        "active_features": fighter.active_features | {AbilityName.RAGE},
                        "modifiers": fighter.modifiers + rage_mods,
                    }
                ).use_resource(ResourceName.RAGE)
                return battlemap.replace_combatant(fighter.position, updated)

        if (
            fighter.has_bonus_action
            and AbilityName.RAGE not in fighter.active_features
            and any(
                r.name == ResourceName.RAGE and r.remaining_uses > 0
                for r in fighter.resources
            )
        ):
            return (cls(performer=_Performer()),)
        return ()

    def perform(self, battlemap: Battlemap) -> Battlemap:
        return self.performer.apply_rage(battlemap)
