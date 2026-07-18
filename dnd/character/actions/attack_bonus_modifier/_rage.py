from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from typing import Self
from uuid_string import UUIDString

from dnd.character._ability_name import AbilityName
from dnd.character.actions.attack_bonus_modifier._base import _AttackBonusModifier
from dnd.character.actions.attack_bonus_modifier._type import AttackBonusModifierType
from dnd._combat_event import AnyCombatEvent, RageEndsEvent

if TYPE_CHECKING:
    from dnd.fight.battlemap import Battlemap
    from dnd.fight.fight_character import FightCharacter


class _RageAttackBonusModifier(_AttackBonusModifier):
    type: Literal[AttackBonusModifierType.RAGE] = AttackBonusModifierType.RAGE
    owner_id: UUIDString

    def apply(
        self,
        battlemap: Battlemap,
        attacker: FightCharacter,
        defender: FightCharacter,
    ) -> int:
        return 2 if AbilityName.RAGE in attacker.active_features else 0

    def on_event(
        self, event: AnyCombatEvent
    ) -> tuple[Self | None, tuple[AnyCombatEvent, ...]]:
        match event:
            case RageEndsEvent() if event.target_id == self.owner_id:
                return None, ()
            case _:
                return self, ()
