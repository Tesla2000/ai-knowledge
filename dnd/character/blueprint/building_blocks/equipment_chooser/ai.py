"""AI-powered equipment chooser for intelligent equipment selection."""

from __future__ import annotations

from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.blueprint import Blueprint
from dnd.character.blueprint.blueprint_formatter import (
    BlueprintFormatter,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.base import (
    EquipmentChooser,
)
from dnd.choices.equipment_creation.weapons import WeaponName
from langchain_openai import ChatOpenAI  # type: ignore[import-not-found]
from pydantic import BaseModel
from pydantic import Field


class EquipmentChoiceSelection(BaseModel):
    """Schema for AI to select equipment from choices."""

    selected_indices: tuple[int, ...] = Field(
        description="Index of selected item from each equipment choice (0-indexed)"
    )


class AIEquipmentChooser(EquipmentChooser):
    """AI-powered equipment chooser that selects equipment based on character context.

    Uses an LLM to make intelligent equipment choices based on the character's
    class, background, stats, and overall concept. The AI receives a formatted
    description of the character and selects the most appropriate equipment
    from available options.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> chooser = AIEquipmentChooser(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        ... )
        >>> builder = Builder().add(chooser)
    """

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _build_equipment_choices_section(self, blueprint: Blueprint) -> str:
        """Build the equipment choices section of the prompt.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Formatted equipment choices section.
        """
        lines = [
            "\n## Equipment Choices",
            "Select ONE option from each choice below:\n",
        ]

        for i, options in enumerate(blueprint.equipment_choices):
            lines.append(f"Choice {i}:")
            for j, item in enumerate(options):
                item_desc = self._format_equipment_item(item)
                lines.append(f"  Option {j}: {item_desc}")
            lines.append("")  # Blank line between choices

        return "\n".join(lines)

    def _format_equipment_item(self, item: ArmorName | WeaponName | str) -> str:
        """Format an equipment item for display in the prompt.

        Args:
            item: Equipment item to format.

        Returns:
            Formatted string describing the item.
        """
        if isinstance(item, WeaponName):
            return f"{item.value} (Weapon)"
        elif isinstance(item, ArmorName):
            return f"{item.value} (Armor)"
        else:
            return f"{item} (Equipment)"

    def _build_prompt(self, blueprint: Blueprint) -> str:
        """Build a complete prompt for AI equipment selection.

        Args:
            blueprint: Current character blueprint.

        Returns:
            Formatted prompt string for the AI.
        """
        parts = [
            "You are selecting equipment for a D&D 5e character.",
            "Choose the most thematically appropriate and mechanically sound equipment "
            "based on the character's class, background, stats, and concept.",
        ]

        # Use formatter to add character details
        character_description = self.formatter.format(blueprint)
        if character_description:
            parts.append(character_description)

        # Add equipment choices section
        if blueprint.equipment_choices:
            parts.append(self._build_equipment_choices_section(blueprint))

            # Add selection instructions
            parts.append("\n## Selection Instructions")
            parts.append(
                f"Return exactly {len(blueprint.equipment_choices)} numbers "
                "(0-indexed) representing your selection for each choice in order."
            )
            parts.append(
                "Consider the character's class, stats, and playstyle when making selections."
            )

        return "\n".join(parts)

    def get_change(self, blueprint: Blueprint) -> Blueprint:
        """Use AI to select equipment from available choices.

        Args:
            blueprint: Current character blueprint with equipment_choices populated.

        Returns:
            Blueprint with equipment choices resolved and added to appropriate fields.
        """
        if not blueprint.equipment_choices:
            # No choices to make
            return Blueprint(equipment_choices=())

        # Build prompt and get AI selection
        prompt = self._build_prompt(blueprint)
        structured_llm = self.llm.with_structured_output(EquipmentChoiceSelection)
        selection = structured_llm.invoke(prompt)

        # Validate selection
        if len(selection.selected_indices) != len(blueprint.equipment_choices):
            raise ValueError(
                f"AI returned {len(selection.selected_indices)} selections "
                f"but expected {len(blueprint.equipment_choices)}"
            )

        # Process selections
        weapons, armors, others = [], [], []
        for choice_idx, selected_idx in enumerate(selection.selected_indices):
            options = blueprint.equipment_choices[choice_idx]

            if selected_idx >= len(options):
                raise ValueError(
                    f"AI selected index {selected_idx} but choice {choice_idx} "
                    f"only has {len(options)} options"
                )

            choice = options[selected_idx]

            if isinstance(choice, WeaponName):
                weapons.append(choice)
            elif isinstance(choice, ArmorName):
                armors.append(choice)
            else:
                others.append(choice)

        # Return blueprint with resolved equipment
        # Note: armor is a single field, so we take the last armor selection
        return Blueprint(  # type: ignore[call-arg]
            equipment_choices=(),
            weapons=blueprint.weapons + tuple(weapons),
            armor=armors[-1] if armors else blueprint.armor,  # type: ignore[attr-defined]
            other_equipment=blueprint.other_equipment + tuple(others),
        )
