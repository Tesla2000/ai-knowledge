from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.feature.feats import FeatName
from pydantic import Field


class FeatAdder(BuildingBlock):
    """Adds a feat to the character's feat list.

    Appends to existing feats, allowing incremental feat additions.
    Raises error if feat already exists.

    Example:
        >>> builder = Builder([
        ...     FeatAdder(feat=FeatName.TOUGH),
        ...     FeatAdder(feat=FeatName.ALERT),
        ...     FeatAdder(feat=FeatName.LUCKY),
        ... ])  # Character will have all three feats
    """

    feat: FeatName = Field(description="Feat to add to character's feat list")

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Add the feat to the existing feat tuple.

        Args:
            blueprint: The current blueprint state.

        Yields:
            Blueprint with the feat added.

        Raises:
            ValueError: If feat already exists.
        """
        existing_feats = blueprint.feats

        # Raise if feat already exists
        if self.feat in existing_feats:
            raise ValueError(f"Feat {self.feat} already exists in character feats")

        new_feats = existing_feats + (self.feat,)
        return Blueprint(feats=new_feats)
