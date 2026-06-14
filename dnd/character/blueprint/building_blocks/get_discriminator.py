from dnd.character.blueprint.building_blocks.building_block import (
    BLOCK_TYPE_FIELD_NAME,
)
from pydantic import Discriminator


def _get_discriminator_value(data: object) -> str | None:
    if isinstance(data, dict):
        return data.get(BLOCK_TYPE_FIELD_NAME)
    return getattr(data, BLOCK_TYPE_FIELD_NAME, None)


def get_discriminator() -> Discriminator:
    return Discriminator(_get_discriminator_value)
