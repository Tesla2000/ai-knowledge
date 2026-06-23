from __future__ import annotations

from typing import Literal

from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SorcererSpellAssigner,
    WizardSpellAssigner,
)
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasAlignment
from dnd.character.blueprint.state import HasBackground
from dnd.character.blueprint.state import HasInitialData
from dnd.character.blueprint.state import HasLevel
from dnd.character.blueprint.state import HasName
from dnd.character.blueprint.state import HasRace
from dnd.character.blueprint.state import HasSorcererLevel
from dnd.character.blueprint.state import HasWizardLevel
from dnd.character.spells import Spell
from dnd.choices.class_creation.character_class import Class
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import create_model
from pydantic import Field


def _build_llm_prompt(
    class_name: str,
    character_description: str | None,
    spell_level: int,
    count: int,
    available_spells: list[Spell],
    state: BlueprintProtocol,
) -> str:
    spell_level_name = "cantrips" if spell_level == 0 else f"level {spell_level} spells"
    name = state.name if isinstance(state, HasName) else "Unknown"
    level = state.level if isinstance(state, HasLevel) else 1
    race = state.race if isinstance(state, HasRace) else None
    background = state.background if isinstance(state, HasBackground) else None
    backstory = (
        state.backstory if isinstance(state, HasInitialData) else "Generic adventurer"
    )
    alignment = state.alignment if isinstance(state, HasAlignment) else None
    return (
        f"You are selecting {count} {spell_level_name} for a D&D 5e character.\n\n"
        "Character Details:\n"
        f"- Name: {name}\n"
        f"- Class: {class_name}\n"
        f"- Level: {level}\n"
        f"- Race: {race.value if race else 'Unknown'}\n"
        f"- Background: {background.value if background else 'Unknown'}\n"
        f"- Backstory: {backstory}\n"
        f"- Description: {character_description or 'Standard character'}\n"
        f"- Alignment: {alignment.value if alignment else 'Unknown'}\n\n"
        "Available spells to choose from:\n"
        + "\n".join(f"- {s.value}" for s in available_spells)
        + f"\n\nSelect exactly {count} spell(s) that:\n"
        "1. Fit the character's theme, personality, and backstory\n"
        "2. Complement their role and combat style\n"
        "3. Provide tactical variety and utility\n"
        "4. Match their alignment and values\n"
        "5. Would make sense for their background and experience\n\n"
        "Choose spells that tell a story about who this character is."
    )


def _llm_select(
    llm: ChatOpenAI,
    class_name: str,
    character_description: str | None,
    spell_level: int,
    count: int,
    available_spells: list[Spell],
    state: BlueprintProtocol,
) -> tuple[Spell, ...]:
    context = _build_llm_prompt(
        class_name, character_description, spell_level, count, available_spells, state
    )

    class _SpellSelectionBase(BaseModel):
        spells: tuple[Spell, ...]

    SpellSelection = create_model(
        f"Level{spell_level}SpellSelection",
        __base__=_SpellSelectionBase,
        spells=(tuple[Spell, ...], ...),
    )

    structured = llm.with_structured_output(SpellSelection)
    try:
        _result = structured.invoke(context)
    except Exception as e:
        raise ValueError(
            f"LLM failed to select spells for level {spell_level}: {e}"
        ) from e
    if not isinstance(_result, _SpellSelectionBase):
        raise TypeError(f"Expected SpellSelection, got {type(_result)}")
    return tuple(_result.spells[:count])


class WizardLLMSpellAssigner[T: HasWizardLevel](WizardSpellAssigner[T]):
    """Uses LLM to select thematically appropriate wizard spells.

    Selects spells based on character background, personality, and theme
    using an LLM to make intelligent choices that fit the character concept.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> assigner = WizardLLMSpellAssigner(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.7),
        ...     character_description="Fire-focused evocation specialist",
        ... )
    """

    model_config = ConfigDict(frozen=True)

    class_: Literal[Class.WIZARD] = Field(
        default=Class.WIZARD, description="Character class this assigner handles"
    )
    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )
    character_description: str | None = Field(
        default=None,
        description="Additional character context for AI spell selection",
    )

    def _select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        state: T,
    ) -> tuple[Spell, ...]:
        return _llm_select(
            self.llm,
            Class.WIZARD.value,
            self.character_description,
            spell_level,
            count,
            available_spells,
            state,
        )


class SorcererLLMSpellAssigner[T: HasSorcererLevel](SorcererSpellAssigner[T]):
    """Uses LLM to select thematically appropriate sorcerer spells.

    Selects spells based on character background, personality, and theme
    using an LLM to make intelligent choices that fit the character concept.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> assigner = SorcererLLMSpellAssigner(
        ...     llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.7),
        ...     character_description="Draconic sorcerer with fire affinity",
        ... )
    """

    model_config = ConfigDict(frozen=True)

    class_: Literal[Class.SORCERER] = Field(
        default=Class.SORCERER, description="Character class this assigner handles"
    )
    llm: ChatOpenAI = Field(
        description="Language model for making AI-powered decisions"
    )
    character_description: str | None = Field(
        default=None,
        description="Additional character context for AI spell selection",
    )

    def _select_spells(
        self,
        spell_level: int,
        count: int,
        available_spells: list[Spell],
        state: T,
    ) -> tuple[Spell, ...]:
        return _llm_select(
            self.llm,
            Class.SORCERER.value,
            self.character_description,
            spell_level,
            count,
            available_spells,
            state,
        )
