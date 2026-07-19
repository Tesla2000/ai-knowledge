from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Literal

from dnd.character._ability_name import AbilityName
from dnd.character.actions._base_action import FreeAction
from dnd.character.actions.advantage_modifier import (
    RecklessAdvantageModifier,
    RecklessGrantsAdvantageModifier,
)
from dnd.fight._combatant_slot import SlotT
from dnd.fight.fight_character import FightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


class UseRecklessAttack(FreeAction[SlotT], Generic[SlotT]):
    name: Literal[AbilityName.RECKLESS_ATTACK] = AbilityName.RECKLESS_ATTACK
    range_tails: Literal[0] = 0
    actor_slot: SlotT

    @classmethod
    def create(
        cls,
        actor_slot: SlotT,
        fighter: FightCharacter,
        battlemap: Battlemap[SlotT],
    ) -> tuple[UseRecklessAttack[SlotT], ...]:
        if AbilityName.RECKLESS_ATTACK not in fighter.character.actions:
            return ()
        if not fighter.has_free_action:
            return ()
        already_reckless = any(
            isinstance(m, RecklessAdvantageModifier) for m in fighter.modifiers
        )
        if already_reckless:
            return ()
        return (cls(actor_slot=actor_slot),)

    def perform(self, battlemap: Battlemap[SlotT]) -> Battlemap[SlotT]:
        match battlemap.get_combatant(self.actor_slot):
            case FightCharacter() as fighter:
                return battlemap.replace_combatant(
                    self.actor_slot,
                    fighter.model_copy(
                        update={
                            "has_free_action": False,
                            "modifiers": (
                                *fighter.modifiers,
                                RecklessAdvantageModifier(),
                                RecklessGrantsAdvantageModifier(),
                            ),
                        }
                    ),
                )
            case _:
                return battlemap
