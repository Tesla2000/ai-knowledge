import random
from typing import Literal

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.signature_spell_choice_resolver.base import (
    SignatureSpellChoiceResolver,
)
from dnd.character.blueprint.states.wizard.level20 import AnyWizardLevel20Blueprint
from dnd.character.spells.spell_slots import Spell


class RandomSignatureSpellChoiceResolver(SignatureSpellChoiceResolver):
    """Randomly selects signature spells from the wizard's known 3rd-level spells."""

    type: Literal[BuildingBlockType.RANDOM_SIGNATURE_SPELL_CHOICE_RESOLVER] = (
        BuildingBlockType.RANDOM_SIGNATURE_SPELL_CHOICE_RESOLVER
    )

    seed: int | None = Field(default=None)

    def _select_signature_spells(
        self, state: AnyWizardLevel20Blueprint, n: int
    ) -> tuple[Spell, ...]:
        random.seed(self.seed)
        available = [
            s
            for s in state.spells.third_level_spells
            if s not in state.signature_spells
        ]
        return tuple(random.sample(available, min(n, len(available))))
