from __future__ import annotations

import logging
import traceback
import uuid
from itertools import islice
from logging import Logger
from typing import NamedTuple
from typing import Optional
from typing import Self
from typing import Union

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.blueprint.building_blocks.building_block import (
    CombinedBlock,
)
from dnd.character.character import Character
from dnd.character.checkpoint import IncrementChain
from dnd.character.checkpoint import IncrementStorage
from dnd.character.checkpoint import MemoryStorage
from dnd.character.presentable_character import (
    PresentableCharacter,
)


class BuildResult(NamedTuple):
    """Result of building a character with increment tracking."""

    chain_id: uuid.UUID
    character: Optional[PresentableCharacter] = None
    error: Optional[Exception] = None


_logger = logging.getLogger(__name__)


class Builder:
    def __init__(
        self,
        building_blocks: tuple[Union[BuildingBlock, CombinedBlock], ...] = (),
        increment_storage: Optional[IncrementStorage] = None,
        logger: Logger = _logger,
    ):
        self._logger = logger
        self._building_blocks = building_blocks
        self._increment_storage = increment_storage or MemoryStorage()

    @staticmethod
    def _init_character() -> Blueprint:
        return Blueprint()

    def build(
        self, increment_chain: IncrementChain = IncrementChain()
    ) -> BuildResult:
        """Build character with automatic increment tracking.

        Returns:
            BuildResult containing the character and chain_id for accessing increments
        """
        blueprint = self._init_character()
        flatten_blocks = tuple(
            islice(
                CombinedBlock(blocks=self._building_blocks).flatten(),
                increment_chain.length(),
                None,
            )
        )
        for diff in increment_chain:
            blueprint = blueprint.add_diff(diff)

        chain_id = uuid.uuid4()
        try:
            for block in flatten_blocks:
                diff = block.get_change(blueprint)
                blueprint = blueprint.add_diff(diff)
                increment_chain = increment_chain.add_increment(diff)
            return BuildResult(
                character=self._make_presentable(blueprint),
                chain_id=chain_id,
            )
        except Exception as e:
            self._logger.error(traceback.format_exc())
            return BuildResult(
                chain_id=chain_id,
                error=e,
            )
        finally:
            self._increment_storage.save_chain(chain_id, increment_chain)

    def add(self, building_block: Union[BuildingBlock, CombinedBlock]) -> Self:
        return type(self)(
            self._building_blocks + (building_block,), self._increment_storage
        )

    @staticmethod
    def _make_presentable(blueprint: Blueprint) -> PresentableCharacter:
        if (
            blueprint.n_stat_choices
            or blueprint.n_skill_choices
            or blueprint.skills_to_choose_from
            or blueprint.equipment_choices
        ):
            raise ValueError("Blueprint still has corresponding choices")
        return PresentableCharacter.model_validate(
            {
                field_name: field_value
                for field_name, field_value in iter(blueprint)
                if field_name in Character.model_fields
            }
        )
