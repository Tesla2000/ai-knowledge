from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import Self
from typing import Union

from dnd.character.blueprint.blueprint import Blueprint
from pydantic import BaseModel
from pydantic import computed_field
from pydantic import ConfigDict
from pydantic import Field

BLOCK_TYPE_FIELD_NAME = "block_type"


class SerializableBlock(BaseModel):
    """Base model for serializable building blocks with polymorphic type discrimination.

    Provides functionality for serializing building blocks to JSON/dict format
    with a computed 'block_type' field for polymorphic deserialization.
    """

    model_config = ConfigDict(frozen=True)

    @computed_field(alias=BLOCK_TYPE_FIELD_NAME)  # type: ignore[prop-decorator]
    @property
    def block_type(self) -> str:
        """Return the class name as the block type for polymorphic serialization."""
        return self.get_block_type()

    @classmethod
    def get_block_type(cls) -> str:
        return cls.__name__


class BuildingBlock(SerializableBlock, ABC):
    @abstractmethod
    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Returns Blueprint differences to apply.

        Receives the current blueprint state from yield returns,
        allowing decisions based on current state.
        """

    def __add__(self, other: BuildingBlock) -> CombinedBlock:
        return CombinedBlock(blocks=(self, other))


Blocks = tuple[Union[BuildingBlock, "CombinedBlock"], ...]


class CombinedBlock(SerializableBlock):
    """Combines multiple building blocks to apply sequentially."""

    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)
    blocks: Blocks = Field(description="Tuple of building blocks to apply in order")

    def __add__(self, other: object) -> Self:
        allowed_types = (BuildingBlock, CombinedBlock)
        if not isinstance(other, allowed_types):
            raise ValueError(
                f"Only instances of {allowed_types} allowed for {type(self).__name__} addition"
            )
        if isinstance(other, CombinedBlock):
            return type(self)(blocks=self.blocks + other.blocks)
        if isinstance(other, BuildingBlock):
            return type(self)(blocks=self.blocks + (other,))
        raise ValueError("What?")

    def flatten(self) -> Generator[BuildingBlock]:
        for block in self.blocks:
            if not isinstance(block, CombinedBlock):
                yield block
            else:
                yield from block.flatten()
