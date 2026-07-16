"""AI-powered equipment chooser for intelligent equipment selection."""

import json
from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.building_blocks.equipment_chooser.base import (
    EquipmentChooser,
)
from dnd.character.blueprint.building_blocks.building_block import _WideBlueprint
from dnd.choices.equipment_creation.weapons import WeaponName
from typing import Literal
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from typing import Annotated

from pydantic import BaseModel
from pydantic import Field
from structured_output_creator import OpenAIService, RaisingService


class AIEquipmentChooser(EquipmentChooser):
    """AI-powered equipment chooser that selects equipment based on character context.

    Uses an LLM to make intelligent equipment choices based on the character's
    class, background, stats, and overall concept.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> chooser = AIEquipmentChooser(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        ... )
    """

    type: Literal[BuildingBlockType.AI_EQUIPMENT_CHOOSER] = (
        BuildingBlockType.AI_EQUIPMENT_CHOOSER
    )

    llm: RaisingService[BaseModel] = Field(
        exclude=True,
        default_factory=lambda: RaisingService(service=OpenAIService()),
        description="Language model for making AI-powered decisions",
    )

    @staticmethod
    def _format_equipment_item(item: ArmorName | WeaponName | str) -> str:
        if isinstance(item, WeaponName):
            return f"{item.value} (Weapon)"
        elif isinstance(item, ArmorName):
            return f"{item.value} (Armor)"
        return f"{item} (Equipment)"

    def _build_prompt(self, state: _WideBlueprint) -> str:
        parts = [
            "You are selecting equipment for a D&D 5e character.",
            "Choose the most thematically appropriate and mechanically sound equipment "
            "based on the character's class, background, stats, and concept.",
        ]

        parts.append(
            "Character state (JSON):\n"
            + json.dumps(
                {
                    k: v
                    for k, v in state.model_dump(mode="json").items()
                    if v is not None
                },
                indent=2,
            )
        )

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
        self, state: _WideBlueprint
    ) -> tuple[list[WeaponName], list[ArmorName], list[str]]:
        if not state.equipment_choices:
            return [], [], []

        EquipmentChoiceSelection = type(
            "EquipmentChoiceSelection",
            (BaseModel,),
            {
                "__annotations__": {
                    f"choice_{i}": Annotated[
                        int,
                        Field(
                            ge=0,
                            lt=len(opts),
                            description=", ".join(
                                f"{j}={self._format_equipment_item(item)}"
                                for j, item in enumerate(opts)
                            ),
                        ),
                    ]
                    for i, opts in enumerate(state.equipment_choices)
                }
            },
        )

        prompt = self._build_prompt(state)
        selection: BaseModel = self.llm.create_structured_output(
            prompt, EquipmentChoiceSelection
        )
        selected = selection.model_dump()

        weapons: list[WeaponName] = []
        armors: list[ArmorName] = []
        others: list[str] = []
        for choice_idx, options in enumerate(state.equipment_choices):
            choice = options[selected[f"choice_{choice_idx}"]]
            if isinstance(choice, WeaponName):
                weapons.append(choice)
            elif isinstance(choice, ArmorName):
                armors.append(choice)
            else:
                others.append(str(choice))

        return weapons, armors, others
