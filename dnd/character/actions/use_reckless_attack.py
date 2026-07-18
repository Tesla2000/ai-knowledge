from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from uuid_string import UUIDString

from dnd.character._ability_name import AbilityName
from dnd.character.actions._base_action import FreeAction
from dnd.character.actions.advantage_modifier import (
    RecklessAdvantageModifier,
    RecklessTargetAdvantageModifier,
)
from dnd.fight.fight_character import FightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


class UseRecklessAttack(FreeAction):
    name: Literal[AbilityName.RECKLESS_ATTACK] = AbilityName.RECKLESS_ATTACK
    range_tails: Literal[0] = 0
    fighter_id: UUIDString

    @classmethod
    def create(cls, fighter: FightCharacter) -> tuple[UseRecklessAttack, ...]:
        if AbilityName.RECKLESS_ATTACK not in fighter.character.actions:
            return ()
        if not fighter.has_free_action:
            return ()
        already_reckless = any(
            isinstance(m, RecklessAdvantageModifier)
            for m in fighter.advantage_modifiers
        )
        if already_reckless:
            return ()
        return (cls(fighter_id=fighter.id),)

    def perform(self, battlemap: Battlemap) -> Battlemap:
        fighter = next(
            c
            for c in battlemap.combatants
            if isinstance(c, FightCharacter) and c.id == self.fighter_id
        )
        reckless_mod = RecklessAdvantageModifier()
        updated_fighter = fighter.model_copy(
            update={
                "has_free_action": False,
                "advantage_modifiers": (*fighter.advantage_modifiers, reckless_mod),
            }
        )
        updated = battlemap.replace_combatant(fighter.position, updated_fighter)
        target_mod = RecklessTargetAdvantageModifier(target_id=fighter.id)
        for combatant in updated.combatants:
            if not isinstance(combatant, FightCharacter):
                continue
            if combatant.id == fighter.id:
                continue
            updated_other = combatant.model_copy(
                update={
                    "advantage_modifiers": (*combatant.advantage_modifiers, target_mod),
                }
            )
            updated = updated.replace_combatant(combatant.position, updated_other)
        return updated
