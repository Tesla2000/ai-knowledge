from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from pydantic import InstanceOf
from typing import Self

from dnd.character.actions._ability_name import AbilityName
from dnd.character.actions._base_action import BonusAction
from dnd.character.actions._damage_type import DamageType
from dnd.character.actions._fight_resource import ResourceName

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
                updated = fighter.model_copy(
                    update={
                        "has_bonus_action": False,
                        "attack_bonus": fighter.attack_bonus + 2,
                        "damage_resistance": fighter.damage_resistance
                        | {
                            DamageType.BLUDGEONING,
                            DamageType.PIERCING,
                            DamageType.SLASHING,
                        },
                        "active_features": fighter.active_features | {AbilityName.RAGE},
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
