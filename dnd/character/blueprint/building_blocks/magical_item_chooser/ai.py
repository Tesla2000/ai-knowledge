"""AI-powered holistic magical item selection."""

from __future__ import annotations

from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.magical_item_chooser.base_chooser import (
    MagicalItemChooserBase,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.magical_item.item import MagicalItem
from dnd.character.magical_item.items import MAGICAL_ITEMS
from dnd.character.magical_item.level import Level
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class MagicalItemSelection(BaseModel):
    """Package of magical item selections."""

    selected_items: list[str] = Field(
        default_factory=list,
        description="List of selected magical item names",
    )


class AIMagicalItemChooser(MagicalItemChooserBase):
    """AI-powered magical item chooser that makes all selections holistically.

    Unlike the standard MagicalItemChooser which selects items per rarity level,
    this chooser uses a single LLM call to select all items simultaneously.

    Example:
        >>> llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        >>> chooser = AIMagicalItemChooser(
        ...     llm=llm,
        ...     n_uncommon=2,
        ...     n_rare=1,
        ... )
        >>> builder = Builder().add(chooser)
    """

    type: Literal[BuildingBlockType.AI_MAGICAL_ITEM_CHOOSER] = (
        BuildingBlockType.AI_MAGICAL_ITEM_CHOOSER
    )

    model_config = ConfigDict(frozen=True)

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _build_prompt(self, state: BlueprintProtocol) -> str:
        system_prompt = (
            "You are selecting magical items for a D&D 5e character in a "
            "single, holistic decision.\n"
            "Consider the character's class, race, stats, and overall "
            "concept when making ALL selections.\n"
            "Your choices should be coherent and synergistic - items should "
            "complement each other and the character's build.\n"
        )

        character_description = self.formatter.format(
            state, system_prompt=system_prompt
        )

        counts = []
        if self.n_common > 0:
            counts.append(f"- {self.n_common} Common item(s)")
        if self.n_uncommon > 0:
            counts.append(f"- {self.n_uncommon} Uncommon item(s)")
        if self.n_rare > 0:
            counts.append(f"- {self.n_rare} Rare item(s)")
        if self.n_very_rare > 0:
            counts.append(f"- {self.n_very_rare} Very Rare item(s)")
        if self.n_legendary > 0:
            counts.append(f"- {self.n_legendary} Legendary item(s)")
        if self.n_artifact > 0:
            counts.append(f"- {self.n_artifact} Artifact item(s)")
        if self.n_unique > 0:
            counts.append(f"- {self.n_unique} Unique item(s)")
        if self.n_mistery > 0:
            counts.append(f"- {self.n_mistery} Mystery item(s)")

        if not counts:
            return ""

        instructions = [
            "\n## Magical Item Selection\n",
            "You must select the following magical items:\n",
            *counts,
            "\n## Available Items by Rarity\n",
        ]

        for level in Level:
            items = [item for item in MAGICAL_ITEMS if item.level == level]
            if items:
                instructions.append(f"\n### {level.value.title()}\n")
                instructions.append(", ".join(f"'{item.name}'" for item in items))

        instructions.extend(
            [
                "\n## Selection Guidelines",
                "1. Select items that synergize with the character's class and abilities",
                "2. Consider the character's stat priorities and weaknesses",
                "3. Balance offensive, defensive, and utility items",
                "4. Duplicates are allowed if strategically valuable",
                "5. Choose items that enhance the character's role/concept",
                "6. Return EXACTLY the item names as they appear in the available lists",
                "7. Avoid items that set a stat to a fixed value the character already meets or"
                " exceeds (e.g. skip Headband of Intellect if the character's Intelligence is"
                " already at or above the value it would provide)",
                "8. Return EXACTLY"
                f" {self.n_common + self.n_uncommon + self.n_rare + self.n_very_rare + self.n_legendary + self.n_artifact + self.n_unique + self.n_mistery}"
                " item(s) in total — no more, no less",
            ]
        )

        return character_description + "\n".join(instructions)

    def _select_items(self, state: BlueprintProtocol) -> tuple[MagicalItem, ...]:
        total_requested = (
            self.n_common
            + self.n_uncommon
            + self.n_rare
            + self.n_very_rare
            + self.n_legendary
            + self.n_artifact
            + self.n_unique
            + self.n_mistery
        )
        if not total_requested:
            return ()

        prompt = self._build_prompt(state)
        structured_llm = self.llm.with_structured_output(MagicalItemSelection)
        _result = structured_llm.invoke(prompt)
        if not isinstance(_result, MagicalItemSelection):
            raise TypeError(f"Expected MagicalItemSelection, got {type(_result)}")
        selection = _result

        item_map = {item.name: item for item in MAGICAL_ITEMS}
        selected_items = tuple(map(item_map.__getitem__, selection.selected_items))

        if len(selected_items) != total_requested:
            raise ValueError(
                f"AI selected {len(selected_items)} items but "
                f"{total_requested} were requested"
            )

        return selected_items
