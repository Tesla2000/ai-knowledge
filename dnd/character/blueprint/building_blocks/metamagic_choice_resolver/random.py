import random
from typing import Literal

from pydantic import Field

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.metamagic_choice_resolver.base import (
    MetamagicChoiceResolver,
)
from dnd.character.blueprint.states.sorcerer.base import AnySorcererBlueprint
from dnd.choices.abilities.metamagic import MetamagicOption


class RandomMetamagicChoiceResolver(MetamagicChoiceResolver):
    """Randomly selects metamagic options from those not already chosen."""

    type: Literal[BuildingBlockType.RANDOM_METAMAGIC_CHOICE_RESOLVER] = (
        BuildingBlockType.RANDOM_METAMAGIC_CHOICE_RESOLVER
    )

    seed: int | None = Field(default=None)

    def _select_metamagic(
        self, state: AnySorcererBlueprint, n: int
    ) -> tuple[MetamagicOption, ...]:
        random.seed(self.seed)
        available = [o for o in MetamagicOption if o not in state.metamagic_options]
        return tuple(random.sample(available, min(n, len(available))))
