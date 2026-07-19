from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Literal

from dnd.character._ability_name import AbilityName
from dnd.character.actions._any_modifier import AnyModifier
from dnd.character.actions._base_action import BonusAction
from dnd.character.actions._fight_resource import ResourceName
from dnd.character.actions.attack_bonus_modifier import RageAttackBonusModifier
from dnd.character.actions.conditional_immunity_modifier import (
    MindlessRageConditionalImmunityModifier,
)
from dnd.character.actions.damage_resistance_modifier import (
    RageDamageResistanceModifier,
)
from dnd.fight._combatant_slot import SlotT
from dnd.fight.fight_character import FightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


class UseRage(BonusAction[SlotT], Generic[SlotT]):
    name: Literal[AbilityName.RAGE] = AbilityName.RAGE
    range_tails: Literal[0] = 0
    radius_tails: Literal[0] = 0
    actor_slot: SlotT

    @classmethod
    def create(
        cls,
        actor_slot: SlotT,
        fighter: FightCharacter,
        battlemap: Battlemap[SlotT],
    ) -> tuple[UseRage[SlotT], ...]:
        if not (
            fighter.has_bonus_action
            and AbilityName.RAGE not in fighter.active_features
            and any(
                r.name == ResourceName.RAGE and r.remaining_uses > 0
                for r in fighter.resources
            )
        ):
            return ()
        return (cls(actor_slot=actor_slot),)

    def perform(self, battlemap: Battlemap[SlotT]) -> Battlemap[SlotT]:
        match battlemap.get_combatant(self.actor_slot):
            case FightCharacter() as fighter:
                pass
            case _:
                return battlemap
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
        return battlemap.replace_combatant(self.actor_slot, updated)
