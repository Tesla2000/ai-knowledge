"""AI-powered holistic magical item selection."""

from __future__ import annotations

from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.blueprint_formatter import (
    BlueprintFormatter,
)
from dnd.character.blueprint.building_blocks.magical_item_chooser.base_chooser import (
    MagicalItemChooserBase,
)
from dnd.character.magical_item.items import MAGICAL_ITEMS
from dnd.character.magical_item.level import Level
from langchain_openai import ChatOpenAI  # type: ignore[import-not-found]
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
    This allows the AI to consider the full character concept and make
    coherent, synergistic decisions across all item selections.

    Example:
        >>> llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        >>> chooser = AIMagicalItemChooser(
        ...     llm=llm,
        ...     n_uncommon=2,
        ...     n_rare=1,
        ... )
        >>> builder = Builder().add(chooser)
    """

    model_config = ConfigDict(frozen=True)

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _build_prompt(self, blueprint: Blueprint) -> str:
        """Build comprehensive prompt for magical item selection.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Formatted prompt string.
        """
        system_prompt = (
            "You are selecting magical items for a D&D 5e character in a "
            "single, holistic decision.\n"
            "Consider the character's class, race, stats, and overall "
            "concept when making ALL selections.\n"
            "Your choices should be coherent and synergistic - items should "
            "complement each other and the character's build.\n"
        )

        character_description = self.formatter.format(
            blueprint, system_prompt=system_prompt
        )

        # Build item counts by rarity
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
            return ""  # No items to select

        instructions = [
            "\n## Magical Item Selection\n",
            "You must select the following magical items:\n",
            *counts,
            "\n## Available Items by Rarity\n",
        ]

        # Group items by rarity for reference
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
                "7. Make sure to make most of this items. Headband of Intellect sounds good but not for a mage with intelligence higher than one provided by the artifact",
                "8. Make sure that thi number of items is correct",
            ]
        )

        return character_description + "\n".join(instructions)

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Select magical items using AI in a single call.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Blueprint with magical items added.
        """
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
            return Blueprint()
        # Build prompt
        prompt = self._build_prompt(blueprint)
        # Get AI selections
        structured_llm = self.llm.with_structured_output(MagicalItemSelection)
        selection: MagicalItemSelection = structured_llm.invoke(prompt)

        # Map selected names to MagicalItem objects
        item_map = {item.name: item for item in MAGICAL_ITEMS}
        selected_items = tuple(map(item_map.__getitem__, selection.selected_items))

        # Verify counts match requested amounts
        if len(selected_items) != total_requested:
            raise ValueError(
                f"AI selected {len(selected_items)} items but "
                f"{total_requested} were requested"
            )

        return self._add_items(blueprint, selected_items)
