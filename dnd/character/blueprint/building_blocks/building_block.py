from __future__ import annotations


from collections.abc import Generator
from typing import Self
from typing import TYPE_CHECKING
from typing import TypeAlias
from typing import Union

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.delta.delta import Delta
from pydantic import BaseModel
from pydantic import computed_field
from pydantic import ConfigDict
from pydantic import Field

BLOCK_TYPE_FIELD_NAME = "block_type"

if TYPE_CHECKING:
    AnyBlocks: TypeAlias = tuple["SerializableBlock", ...]


class SerializableBlock(BaseModel):
    """Base model for serializable building blocks with polymorphic type discrimination.

    Provides functionality for serializing building blocks to JSON/dict format
    with a computed 'block_type' field for polymorphic deserialization.
    """

    model_config = ConfigDict(frozen=True)

    if TYPE_CHECKING:

        @property
        def block_type(self) -> str:
            """Return the class name as the block type for polymorphic serialization."""
            return self.get_block_type()

    else:

        @computed_field(alias=BLOCK_TYPE_FIELD_NAME)
        @property
        def block_type(self) -> str:
            """Return the class name as the block type for polymorphic serialization."""
            return self.get_block_type()

    @classmethod
    def get_block_type(cls) -> str:
        return cls.__name__


class BuildingBlock[T: BlueprintProtocol, DeltaT: Delta, Added: BlueprintProtocol](
    SerializableBlock
):
    """Abstract base for a single pipeline step that yields deltas and returns new state."""

    def get_change(
        self, state: T
    ) -> Generator[DeltaT, None, ProtocolIntersection[T, Added]]:
        """Yield deltas and return the new state."""
        raise NotImplementedError(f"{type(self).__name__} must implement get_change")

    def __add__(
        self,
        other: BuildingBlock[BlueprintProtocol, Delta, BlueprintProtocol]
        | CombinedBlock,
    ) -> CombinedBlock:
        return CombinedBlock(blocks=(self, other))


Blocks = tuple[
    Union[
        "BuildingBlock[BlueprintProtocol, Delta, BlueprintProtocol]", "CombinedBlock"
    ],
    ...,
]


class CombinedBlock(SerializableBlock):
    """Combines multiple building blocks to apply sequentially."""

    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)
    blocks: AnyBlocks = Field(description="Tuple of building blocks to apply in order")  # noqa: F821

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

    def get_change(
        self, state: BlueprintProtocol
    ) -> Generator[Delta, None, BlueprintProtocol]:
        current: BlueprintProtocol = state
        for block in self.flatten():
            current = yield from block.get_change(current)
        return current

    def flatten(
        self,
    ) -> Generator[BuildingBlock[BlueprintProtocol, Delta, BlueprintProtocol]]:
        for block in self.blocks:
            if isinstance(block, BuildingBlock):
                yield block
            elif isinstance(block, CombinedBlock):
                yield from block.flatten()
