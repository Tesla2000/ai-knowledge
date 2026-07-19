from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING, Generic, Literal

from dnd.character._ability_name import AbilityName
from dnd.character.actions._base_action import Action
from dnd.choices.stats_creation.statistic import Statistic
from dnd.fight._combatant_slot import SlotT
from dnd.fight.fight_character import FightCharacter, SpellcasterFightCharacter

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap


class CastFireball(Action[SlotT], Generic[SlotT]):
    name: Literal[AbilityName.FIREBALL] = AbilityName.FIREBALL
    range_tails: Literal[30] = 30
    radius_tails: Literal[4] = 4
    actor_slot: SlotT
    center_position: tuple[int, int]
    spell_save_dc: int

    @classmethod
    def create(
        cls,
        actor_slot: SlotT,
        fighter: FightCharacter,
        battlemap: Battlemap[SlotT],
    ) -> tuple[CastFireball[SlotT], ...]:
        if not isinstance(fighter, SpellcasterFightCharacter):
            return ()
        if not fighter.has_action:
            return ()
        if fighter.remaining_spell_slots.level_3 == 0:
            return ()
        if AbilityName.FIREBALL not in fighter.character.actions:
            return ()
        spell_save_dc = 8 + sum(
            m.apply(fighter.character)
            for m in fighter.character.spell_save_dc_modifiers
        )
        results: list[CastFireball[SlotT]] = []
        for target_slot in battlemap.all_slots():
            if target_slot == actor_slot:
                continue
            match battlemap.get_combatant(target_slot):
                case FightCharacter() as target:
                    results.append(
                        cls(
                            actor_slot=actor_slot,
                            center_position=target.position,
                            spell_save_dc=spell_save_dc,
                        )
                    )
                case _:
                    pass
        return tuple(results)

    def perform(self, battlemap: Battlemap[SlotT]) -> Battlemap[SlotT]:
        match battlemap.get_combatant(self.actor_slot):
            case SpellcasterFightCharacter() as fighter:
                pass
            case _:
                return battlemap
        battlemap = battlemap.replace_combatant(
            self.actor_slot, fighter.spend_action().spend_level_3_slot()
        )
        damage = sum(randint(1, 6) for _ in range(8))
        cx, cy = self.center_position
        for slot in battlemap.all_slots():
            match battlemap.get_combatant(slot):
                case FightCharacter() as combatant:
                    tx, ty = combatant.position
                    if max(abs(tx - cx), abs(ty - cy)) > 4:
                        continue
                    roll = (
                        randint(1, 20)
                        + combatant.character.saving_throw_modifiers[
                            Statistic.DEXTERITY
                        ]
                    )
                    hit_damage = damage if roll < self.spell_save_dc else damage // 2
                    battlemap = battlemap.replace_combatant(
                        slot, combatant.take_damage(hit_damage)
                    )
                case _:
                    pass
        return battlemap
