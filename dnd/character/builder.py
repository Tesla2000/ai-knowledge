from __future__ import annotations

import logging
import traceback
import uuid
from collections.abc import Generator
from itertools import islice
from logging import Logger
from typing import NamedTuple
from typing import Self

from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.blueprint.building_blocks.building_block import (
    CombinedBlock,
)
from dnd.character.delta.delta import Delta

from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
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
    character: PresentableCharacter | None = None
    error: Exception | None = None


_logger = logging.getLogger(__name__)


class Builder:
    def __init__(
        self,
        building_blocks: tuple[BuildingBlock | CombinedBlock, ...] = (),
        increment_storage: IncrementStorage | None = None,
        logger: Logger = _logger,
    ):
        self._logger = logger
        self._building_blocks = building_blocks
        self._increment_storage = increment_storage or MemoryStorage()

    def _flatten(
        self,
    ) -> Generator[BuildingBlock[BlueprintProtocol, Delta, BlueprintProtocol]]:
        for block in self._building_blocks:
            if isinstance(block, CombinedBlock):
                yield from block.flatten()
            else:
                yield block

    @staticmethod
    def _init_character() -> Blueprint:
        return Blueprint()

    def build(self, increment_chain: IncrementChain = IncrementChain()) -> BuildResult:
        """Build character with automatic increment tracking.

        Returns:
            BuildResult containing the character and chain_id for accessing increments
        """
        state: BlueprintProtocol = self._init_character()
        for delta in increment_chain.iter_deltas():
            state = delta.apply(state)

        flatten_blocks = tuple(
            islice(
                self._flatten(),
                increment_chain.length(),
                None,
            )
        )

        chain_id = uuid.uuid4()
        try:
            for block in flatten_blocks:
                gen = block.get_change(state)
                try:
                    while True:
                        delta = next(gen)
                        increment_chain = increment_chain.add_increment(delta)
                except StopIteration as exc:
                    state = exc.value
            return BuildResult(
                character=self._make_presentable(state),
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

    def add(self, building_block: BuildingBlock | CombinedBlock) -> Self:
        return type(self)(
            self._building_blocks + (building_block,), self._increment_storage
        )

    @staticmethod
    def _make_presentable(blueprint: BlueprintProtocol) -> PresentableCharacter:
        blueprint_dict = dict(blueprint)
        if any(
            blueprint_dict.get(field)
            for field in (
                "n_stat_choices",
                "n_skill_choices",
                "skills_to_choose_from",
                "equipment_choices",
            )
        ):
            raise ValueError("Blueprint still has corresponding choices")
        return PresentableCharacter.model_validate(
            {
                field_name: field_value
                for field_name, field_value in dict(blueprint).items()
                if field_name in Character.model_fields
            }
        )
