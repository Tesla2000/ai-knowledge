from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING, Generic, Literal

from dnd.character._ability_name import AbilityName
from dnd.character.actions._base_action import Action
from dnd.fight._combatant_slot import SlotT
from dnd.fight.fight_character import FightCharacter, SpellcasterFightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


class CastChromaticOrb(Action[SlotT], Generic[SlotT]):
    name: Literal[AbilityName.CHROMATIC_ORB] = AbilityName.CHROMATIC_ORB
    range_tails: Literal[18] = 18
    actor_slot: SlotT
    target_slot: SlotT
    spell_attack_bonus: int

    @classmethod
    def create(
        cls,
        actor_slot: SlotT,
        fighter: FightCharacter,
        battlemap: Battlemap[SlotT],
    ) -> tuple[CastChromaticOrb[SlotT], ...]:
        if not isinstance(fighter, SpellcasterFightCharacter):
            return ()
        if not fighter.has_action:
            return ()
        if fighter.remaining_spell_slots.level_1 == 0:
            return ()
        if AbilityName.CHROMATIC_ORB not in fighter.character.actions:
            return ()
        spell_attack_bonus = sum(
            m.apply(fighter.character)
            for m in fighter.character.spell_attack_bonus_modifiers
        )
        results: list[CastChromaticOrb[SlotT]] = []
        for target_slot in battlemap.all_slots():
            if target_slot == actor_slot:
                continue
            results.append(
                cls(
                    actor_slot=actor_slot,
                    target_slot=target_slot,
                    spell_attack_bonus=spell_attack_bonus,
                )
            )
        return tuple(results)

    def perform(self, battlemap: Battlemap[SlotT]) -> Battlemap[SlotT]:
        match battlemap.get_combatant(self.actor_slot):
            case SpellcasterFightCharacter() as fighter:
                pass
            case _:
                return battlemap
        battlemap = battlemap.replace_combatant(
            self.actor_slot, fighter.spend_action().spend_level_1_slot()
        )
        match battlemap.get_combatant(self.target_slot):
            case FightCharacter() as target:
                pass
            case _:
                return battlemap
        roll = randint(1, 20) + self.spell_attack_bonus
        if roll < target.ac:
            return battlemap
        damage = sum(randint(1, 8) for _ in range(3))
        return battlemap.replace_combatant(self.target_slot, target.take_damage(damage))
