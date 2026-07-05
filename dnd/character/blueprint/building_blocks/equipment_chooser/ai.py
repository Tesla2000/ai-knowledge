"""AI-powered equipment chooser for intelligent equipment selection."""

from __future__ import annotations

from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.equipment_chooser.base import (
    EquipmentChooser,
)
from dnd.character.blueprint.state import HasEquipmentChoices
from dnd.choices.equipment_creation.weapons import WeaponName
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from langchain_openai import ChatOpenAI
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
    class, background, stats, and overall concept.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> chooser = AIEquipmentChooser(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        ... )
        >>> builder = Builder().add(chooser)
    """

    type: Literal[BuildingBlockType.AI_EQUIPMENT_CHOOSER] = (
        BuildingBlockType.AI_EQUIPMENT_CHOOSER
    )

    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )

    formatter: BlueprintFormatter = Field(
        default_factory=BlueprintFormatter,
        description="Blueprint formatter for creating AI prompts",
    )

    def _format_equipment_item(self, item: ArmorName | WeaponName | str) -> str:
        if isinstance(item, WeaponName):
            return f"{item.value} (Weapon)"
        elif isinstance(item, ArmorName):
            return f"{item.value} (Armor)"
        return f"{item} (Equipment)"

    def _build_prompt(self, state: HasEquipmentChoices) -> str:
        parts = [
            "You are selecting equipment for a D&D 5e character.",
            "Choose the most thematically appropriate and mechanically sound equipment "
            "based on the character's class, background, stats, and concept.",
        ]

        character_description = self.formatter.format(state)
        if character_description:
            parts.append(character_description)

        equipment_choices = state.equipment_choices
        if equipment_choices:
            lines = [
                "\n## Equipment Choices",
                "Select ONE option from each choice below:\n",
            ]
            for i, options in enumerate(equipment_choices):
                lines.append(f"Choice {i}:")
                for j, item in enumerate(options):
                    lines.append(f"  Option {j}: {self._format_equipment_item(item)}")
                lines.append("")
            parts.append("\n".join(lines))

            parts.append("\n## Selection Instructions")
            parts.append(
                f"Return exactly {len(equipment_choices)} numbers "
                "(0-indexed) representing your selection for each choice in order."
            )
            parts.append(
                "Consider the character's class, stats, and playstyle when making selections."
            )

        return "\n".join(parts)

    def _pick_equipment(
        self, state: HasEquipmentChoices
    ) -> tuple[list[WeaponName], list[ArmorName], list[str]]:
        if not state.equipment_choices:
            return [], [], []

        prompt = self._build_prompt(state)
        structured_llm = self.llm.with_structured_output(EquipmentChoiceSelection)
        _result = structured_llm.invoke(prompt)
        if not isinstance(_result, EquipmentChoiceSelection):
            raise TypeError(f"Expected EquipmentChoiceSelection, got {type(_result)}")
        selection = _result

        if len(selection.selected_indices) != len(state.equipment_choices):
            raise ValueError(
                f"AI returned {len(selection.selected_indices)} selections "
                f"but expected {len(state.equipment_choices)}"
            )

        weapons: list[WeaponName] = []
        armors: list[ArmorName] = []
        others: list[str] = []
        for choice_idx, selected_idx in enumerate(selection.selected_indices):
            options = state.equipment_choices[choice_idx]
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
                others.append(str(choice))

        return weapons, armors, others
