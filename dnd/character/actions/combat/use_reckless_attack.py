from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from uuid_string import UUIDString

from dnd.character._ability_name import AbilityName
from dnd.character.actions._base_action import FreeAction
from dnd.character.actions.advantage_modifier import (
    RecklessAdvantageModifier,
    RecklessGrantsAdvantageModifier,
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
            isinstance(m, RecklessAdvantageModifier) for m in fighter.modifiers
        )
        if already_reckless:
            return ()
        return (cls(fighter_id=fighter.id),)

    def perform(self, battlemap: Battlemap) -> Battlemap:
        fighter = battlemap.find_fight_character(self.fighter_id)
        if fighter is None:
            return battlemap
        updated_fighter = fighter.model_copy(
            update={
                "has_free_action": False,
                "modifiers": (
                    *fighter.modifiers,
                    RecklessAdvantageModifier(),
                    RecklessGrantsAdvantageModifier(),
                ),
            }
        )
        return battlemap.replace_combatant(fighter.position, updated_fighter)
