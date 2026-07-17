from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict

from dnd.fight.fight_character import AnyActiveCombatant


class Battlemap(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    combatants: tuple[AnyActiveCombatant, ...]

    def replace_combatant(
        self, position: tuple[int, int], updated: AnyActiveCombatant
    ) -> Battlemap:
        return self.model_copy(
            update={
                "combatants": tuple(
                    updated if c.position == position else c for c in self.combatants
                )
            }
        )
