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
    center_position: tuple[float, float]
    targeted_positions: frozenset[tuple[int, int]]
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

        radius = 4
        all_positions: list[tuple[int, int]] = []
        for slot in battlemap.all_slots():
            match battlemap.get_combatant(slot):
                case FightCharacter() as c:
                    all_positions.append(c.position)
                case _:
                    pass

        if not all_positions:
            return ()

        xs: list[float] = sorted(
            {float(tx + dx) for tx, _ in all_positions for dx in (-radius, radius)}
        )
        ys: list[float] = sorted(
            {float(ty + dy) for _, ty in all_positions for dy in (-radius, radius)}
        )
        x_candidates = xs + [(xs[i] + xs[i + 1]) / 2 for i in range(len(xs) - 1)]
        y_candidates = ys + [(ys[i] + ys[i + 1]) / 2 for i in range(len(ys) - 1)]

        seen: set[frozenset[tuple[int, int]]] = set()
        results: list[CastFireball[SlotT]] = []
        for cx in x_candidates:
            for cy in y_candidates:
                hit_set: frozenset[tuple[int, int]] = frozenset(
                    (tx, ty)
                    for tx, ty in all_positions
                    if max(abs(tx - cx), abs(ty - cy)) <= radius
                )
                if not hit_set or hit_set in seen:
                    continue
                seen.add(hit_set)
                center_f: tuple[float, float] = (cx, cy)
                results.append(
                    cls(
                        actor_slot=actor_slot,
                        center_position=center_f,
                        targeted_positions=hit_set,
                        spell_save_dc=spell_save_dc,
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
            self.actor_slot, fighter.spend_action().spend_level_3_slot()
        )
        damage = sum(randint(1, 6) for _ in range(8))
        for slot in battlemap.all_slots():
            match battlemap.get_combatant(slot):
                case FightCharacter() as combatant:
                    if combatant.position not in self.targeted_positions:
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
