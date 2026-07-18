from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pydantic import Field
from pydantic import ValidationError

from pydantic import BaseModel as _BaseModel

from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.ai import (
    AIToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.ai import (
    AILanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.character_base_template import (
    CharacterBaseTemplate,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.ai import (
    AIEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.ai import (
    AIFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.ai_base_builder_assigner import (
    AIBaseBuilderAssigner,
)
from dnd.character.blueprint.building_blocks.initial_data_filler.ai_partial_builder_assigner import (
    AIPartialBuilderAssigner,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.base import (
    EquipmentChooser,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.base import (
    SorcererSpellAssigner,
    WizardSpellAssigner,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment.llm import (
    SorcererLLMSpellAssigner,
    WizardLLMSpellAssigner,
)
from dnd.character.class_levels import ClassLevels
from dnd.character.blueprint.building_blocks.magical_item_chooser.ai import (
    AIMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.ai import (
    AISkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.ai import (
    AIStatChoiceResolver,
    StatIncreaseSelection,
)
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.sorcerer.base import SorcererBlueprint
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard.base import WizardBlueprint
from dnd.character.feature.feats import FeatName
from dnd.character.magical_item.items import MAGICAL_ITEMS
from dnd.character.spells.max_spell_levels import FULL_CASTER_SPELL_SLOTS
from dnd.character.spells.spell_slots import WizardCantrip as Cantrip
from dnd.character.spells.spell_slots import WizardFirstLevel as FirstLevel
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.class_creation.character_class import Class
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.language import Language
from dnd.other_profficiencies import ToolProficiency, GamingSet, MusicalInstrument
from dnd.character.race.race import Race
from dnd.choices.sex import Sex
from dnd.skill_proficiency import Skill
from structured_output_creator import LLMRefusalError


def _exhaust(gen: Generator[object, object, object]) -> object:
    try:
        while True:
            next(gen)
    except StopIteration as exc:
        return exc.value


class SkillSelection(_BaseModel):
    selected_skills: list[Skill]


class MagicalItemSelection(_BaseModel):
    selected_items: list[str]


class FeatSelection(_BaseModel):
    feats: list[FeatName]


class LanguageSelection(_BaseModel):
    languages: list[Language]


class ToolProficiencySelection(_BaseModel):
    tool_proficiencies: list[ToolProficiency | GamingSet | MusicalInstrument]


_DEFAULT_STATS = Stats(
    strength=10,
    dexterity=10,
    constitution=10,
    intelligence=10,
    wisdom=10,
    charisma=10,
)

_MOCK_TEMPLATE = CharacterBaseTemplate(
    name="Alice",
    sex=Sex.FEMALE,
    age=25,
    race=Race.HUMAN,
    background=Background.SAGE,
    alignment=Alignment.CHAOTIC_GOOD,
    backstory="A brilliant mage.",
    height=65,
    weight=130,
    eye_color="blue",
    skin_color="fair",
    hairstyle="long brown",
    appearance="tall and slender",
    character_traits="curious",
    ideals="knowledge",
    bonds="books",
    weaknesses="overconfident",
)


class _StatsBP(Blueprint):
    """Blueprint subclass with stats field for stat-resolver tests."""

    stats: Stats = Field(default=_DEFAULT_STATS)


class _Level1ClassLevels(ClassLevels):
    """ClassLevels with exactly 1 wizard level for testing level-1 branches."""

    wizard: int = 1


class _Level1SorcererClassLevels(ClassLevels):
    """ClassLevels with exactly 1 sorcerer level for testing level-1 branches."""

    sorcerer: int = 1


class _ConcreteEquipmentChooser(EquipmentChooser):
    """Concrete EquipmentChooser that inherits the base _pick_equipment."""


@pytest.mark.unit
class TestAIBaseBuilderAssigner:
    def test_get_change_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = _MOCK_TEMPLATE

        block = AIBaseBuilderAssigner.model_construct(
            description="A wizard", llm=mock_llm
        )
        result = block.apply(Blueprint())
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIPartialBuilderAssigner:
    def test_get_change_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = _MOCK_TEMPLATE

        block = AIPartialBuilderAssigner.model_construct(
            description="A wizard", llm=mock_llm
        )
        result = block.apply(Blueprint())
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIStatChoiceResolver:
    def test_no_stat_choices_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm,
        )
        result = block.apply(_StatsBP())
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_stat_choices_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = StatIncreaseSelection(
            intelligence=2
        )

        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = _StatsBP(n_stat_choices=2)
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAISkillChoiceResolver:
    def test_no_skill_choices_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm,
        )
        result = block.apply(Blueprint())
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_skill_choices_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = SkillSelection(
            selected_skills=(Skill.ARCANA, Skill.HISTORY)
        )

        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(
            n_skill_choices=2,
            skills_to_choose_from=frozenset(
                {Skill.ARCANA, Skill.HISTORY, Skill.PERCEPTION}
            ),
        )
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIMagicalItemChooser:
    def test_no_items_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIMagicalItemChooser.model_construct(
            llm=mock_llm,
        )
        result = block.apply(Blueprint())
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_n_common_calls_llm(self) -> None:
        first_item = next(iter(MAGICAL_ITEMS))
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = MagicalItemSelection(
            selected_items=[first_item.name]
        )

        block = AIMagicalItemChooser.model_construct(
            llm=mock_llm,
            n_common=1,
            n_uncommon=0,
            n_rare=0,
            n_very_rare=0,
            n_legendary=0,
            n_artifact=0,
            n_unique=0,
            n_mistery=0,
        )
        result = block.apply(Blueprint())
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIEquipmentChooser:
    def test_no_choices_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIEquipmentChooser.model_construct(
            llm=mock_llm,
        )
        result = block.apply(Blueprint())
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_equipment_choices_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = lambda prompt, model_class: (
            model_class(choice_0=0, choice_1=0, choice_2=0)
        )

        block = AIEquipmentChooser.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(
            equipment_choices=(
                (WeaponName.DAGGER,),
                (ArmorName.CLOTHES,),
                ("Rope",),
            )
        )
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIFeatChoiceResolver:
    def test_no_placeholders_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIFeatChoiceResolver.model_construct(
            llm=mock_llm,
        )
        result = block.apply(Blueprint())
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = FeatSelection(
            feats={FeatName.ALERT}
        )

        block = AIFeatChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(feats=(FeatName.ANY_OF_YOUR_CHOICE,))
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestWizardLLMSpellAssigner:
    def test_get_change_selects_spells(self) -> None:
        call_count: list[int] = [0]

        def spell_model_side_effect(prompt: object, model_class: object) -> object:
            level = call_count[0]
            call_count[0] += 1
            if level == 0:
                return model_class.model_construct(spells=(Cantrip.FIRE_BOLT,))
            return model_class.model_construct(spells=(FirstLevel.MAGIC_MISSILE,))

        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = spell_model_side_effect

        block = WizardLLMSpellAssigner.model_construct(
            llm=mock_llm, character_description=None, class_=Class.WIZARD
        )
        state = WizardBlueprint(
            classes=_Level1ClassLevels(),
            caster=CasterInfo(spell_slots=FULL_CASTER_SPELL_SLOTS[0]),
        )
        result = block.apply(state)
        assert result is not None
        assert mock_llm.create_structured_output.call_count >= 1


@pytest.mark.unit
class TestSorcererLLMSpellAssigner:
    def test_get_change_selects_spells(self) -> None:
        call_count: list[int] = [0]

        def spell_model_side_effect(prompt: object, model_class: object) -> object:
            level = call_count[0]
            call_count[0] += 1
            if level == 0:
                return model_class.model_construct(spells=(Cantrip.FIRE_BOLT,))
            return model_class.model_construct(spells=(FirstLevel.MAGIC_MISSILE,))

        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = spell_model_side_effect

        block = SorcererLLMSpellAssigner.model_construct(
            llm=mock_llm, character_description=None, class_=Class.SORCERER
        )
        state = SorcererBlueprint(
            classes=_Level1SorcererClassLevels(), spell_slots=FULL_CASTER_SPELL_SLOTS[0]
        )
        result = block.apply(state)
        assert result is not None
        assert mock_llm.create_structured_output.call_count >= 1

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("network error")

        block = SorcererLLMSpellAssigner.model_construct(
            llm=mock_llm, character_description=None, class_=Class.SORCERER
        )
        state = SorcererBlueprint(
            classes=_Level1SorcererClassLevels(), spell_slots=FULL_CASTER_SPELL_SLOTS[0]
        )
        with pytest.raises(LLMRefusalError):
            block.apply(state)


@pytest.mark.unit
class TestWizardLLMSpellAssignerErrors:
    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("network error")

        block = WizardLLMSpellAssigner.model_construct(
            llm=mock_llm, character_description=None, class_=Class.WIZARD
        )
        state = WizardBlueprint(
            classes=_Level1ClassLevels(),
            caster=CasterInfo(spell_slots=FULL_CASTER_SPELL_SLOTS[0]),
        )
        with pytest.raises(LLMRefusalError):
            block.apply(state)


@pytest.mark.unit
class TestAILanguageChoiceResolver:
    def test_no_placeholder_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AILanguageChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(languages=(Language.COMMON,))
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = LanguageSelection(
            languages={Language.ELVISH}
        )

        block = AILanguageChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(languages=(Language.ANY_OF_YOUR_CHOICE,))
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AILanguageChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(languages=(Language.ANY_OF_YOUR_CHOICE,))
        with pytest.raises(LLMRefusalError):
            block.apply(state)


@pytest.mark.unit
class TestAIToolProficiencyChoiceResolver:
    def test_no_placeholder_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(tool_proficiencies=(ToolProficiency.ALCHEMISTS_SUPPLIES,))
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_tool_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ToolProficiencySelection(
            tool_proficiencies={ToolProficiency.ALCHEMISTS_SUPPLIES}
        )

        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(tool_proficiencies=(ToolProficiency.ANY_OF_YOUR_CHOICE,))
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_gaming_set_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ToolProficiencySelection(
            tool_proficiencies={GamingSet.DICE_SET}
        )

        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(tool_proficiencies=(GamingSet.ANY_OF_YOUR_CHOICE,))
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_musical_instrument_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ToolProficiencySelection(
            tool_proficiencies={MusicalInstrument.LUTE}
        )

        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(tool_proficiencies=(MusicalInstrument.ANY_OF_YOUR_CHOICE,))
        result = block.apply(state)
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(tool_proficiencies=(ToolProficiency.ANY_OF_YOUR_CHOICE,))
        with pytest.raises(LLMRefusalError):
            block.apply(state)


@pytest.mark.unit
class TestAIFeatChoiceResolverExtraBranches:
    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIFeatChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(feats=(FeatName.ANY_OF_YOUR_CHOICE,))
        with pytest.raises(LLMRefusalError):
            block.apply(state)


@pytest.mark.unit
class TestAISkillChoiceResolverExtraBranches:
    def test_invalid_skill_raises_value_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = SkillSelection(
            selected_skills=(Skill.ATHLETICS, Skill.DECEPTION)
        )

        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(
            n_skill_choices=2,
            skills_to_choose_from=frozenset({Skill.ARCANA, Skill.HISTORY}),
        )
        with pytest.raises(ValueError, match="not in available skills"):
            block.apply(state)

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(
            n_skill_choices=2,
            skills_to_choose_from=frozenset({Skill.ARCANA, Skill.HISTORY}),
        )
        with pytest.raises(LLMRefusalError):
            block.apply(state)


@pytest.mark.unit
class TestAIStatChoiceResolverExtraBranches:
    def test_wrong_total_raises_value_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = StatIncreaseSelection(
            intelligence=1
        )

        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = _StatsBP(n_stat_choices=2)
        with pytest.raises(ValueError, match="AI distributed"):
            block.apply(state)

    def test_negative_increase_raises_value_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = StatIncreaseSelection(
            intelligence=3, wisdom=-1
        )

        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = _StatsBP(n_stat_choices=2)
        with pytest.raises(ValueError, match="negative increase"):
            block.apply(state)

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm,
        )
        state = _StatsBP(n_stat_choices=2)
        with pytest.raises(LLMRefusalError):
            block.apply(state)


@pytest.mark.unit
class TestAIEquipmentChooserExtraBranches:
    def test_missing_choice_raises_validation_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = lambda prompt, model_class: (
            model_class(choice_0=0)  # choice_1 missing
        )

        block = AIEquipmentChooser.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(
            equipment_choices=(
                (WeaponName.DAGGER,),
                (ArmorName.CLOTHES,),
            )
        )
        with pytest.raises(ValidationError):
            block.apply(state)

    def test_out_of_bounds_index_raises_validation_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = lambda prompt, model_class: (
            model_class(choice_0=5)  # lt=1, so 5 is out of bounds
        )

        block = AIEquipmentChooser.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(equipment_choices=((WeaponName.DAGGER,),))
        with pytest.raises(ValidationError):
            block.apply(state)

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIEquipmentChooser.model_construct(
            llm=mock_llm,
        )
        state = Blueprint(equipment_choices=((WeaponName.DAGGER,),))
        with pytest.raises(LLMRefusalError):
            block.apply(state)


@pytest.mark.unit
class TestAIMagicalItemChooserExtraBranches:
    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIMagicalItemChooser.model_construct(
            llm=mock_llm,
            n_common=1,
            n_uncommon=0,
            n_rare=0,
            n_very_rare=0,
            n_legendary=0,
            n_artifact=0,
            n_unique=0,
            n_mistery=0,
        )
        with pytest.raises(LLMRefusalError):
            block.apply(Blueprint())


@pytest.mark.unit
class TestAIBaseBuilderAssignerExtraBranches:
    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIBaseBuilderAssigner.model_construct(
            description="A wizard", llm=mock_llm
        )
        with pytest.raises(LLMRefusalError):
            block.apply(Blueprint())


@pytest.mark.unit
class TestAIMagicalItemChooserRarityBranches:
    def test_all_non_common_rarities(self) -> None:
        items = list(MAGICAL_ITEMS)
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = MagicalItemSelection(
            selected_items=[items[0].name] * 7
        )

        block = AIMagicalItemChooser.model_construct(
            llm=mock_llm,
            n_common=0,
            n_uncommon=1,
            n_rare=1,
            n_very_rare=1,
            n_legendary=1,
            n_artifact=1,
            n_unique=1,
            n_mistery=1,
        )
        result = block.apply(Blueprint())
        assert result is not None

    def test_build_prompt_no_items_returns_empty(self) -> None:
        block = AIMagicalItemChooser.model_construct(
            llm=MagicMock(),
            n_common=0,
            n_uncommon=0,
            n_rare=0,
            n_very_rare=0,
            n_legendary=0,
            n_artifact=0,
            n_unique=0,
            n_mistery=0,
        )
        assert block._build_prompt(Blueprint()) == ""


@pytest.mark.unit
class TestAIToolProficiencyChoiceResolverMethods:
    def test_select_tool_proficiency_not_implemented(self) -> None:
        block = AIToolProficiencyChoiceResolver.model_construct()
        with pytest.raises(NotImplementedError):
            block.select_tool_proficiency([], Blueprint())

    def test_select_gaming_set_not_implemented(self) -> None:
        block = AIToolProficiencyChoiceResolver.model_construct()
        with pytest.raises(NotImplementedError):
            block.select_gaming_set([], Blueprint())

    def test_select_musical_instrument_not_implemented(self) -> None:
        block = AIToolProficiencyChoiceResolver.model_construct()
        with pytest.raises(NotImplementedError):
            block.select_musical_instrument([], Blueprint())

    def test_build_prompt_no_placeholders_returns_empty(self) -> None:
        block = AIToolProficiencyChoiceResolver.model_construct()
        state = Blueprint(tool_proficiencies=(ToolProficiency.ALCHEMISTS_SUPPLIES,))
        assert block._build_prompt(state) == ""

    def test_get_change_empty_prompt_returns_early(self) -> None:
        with patch.object(
            AIToolProficiencyChoiceResolver, "_build_prompt", return_value=""
        ):
            block = AIToolProficiencyChoiceResolver.model_construct()
            state = Blueprint(tool_proficiencies=(ToolProficiency.ANY_OF_YOUR_CHOICE,))
            result = block.apply(state)
        assert result is not None


@pytest.mark.unit
class TestAILanguageChoiceResolverMethods:
    def test_select_from_available_not_implemented(self) -> None:
        block = AILanguageChoiceResolver.model_construct()
        with pytest.raises(NotImplementedError):
            block._select_from_available([], Blueprint())

    def test_build_prompt_no_placeholders_returns_empty(self) -> None:
        block = AILanguageChoiceResolver.model_construct()
        assert block._build_prompt(Blueprint(languages=(Language.COMMON,))) == ""

    def test_get_change_empty_prompt_returns_early(self) -> None:
        with patch.object(AILanguageChoiceResolver, "_build_prompt", return_value=""):
            block = AILanguageChoiceResolver.model_construct()
            state = Blueprint(languages=(Language.ANY_OF_YOUR_CHOICE,))
            result = block.apply(state)
        assert result is not None


@pytest.mark.unit
class TestAIFeatChoiceResolverBuildPrompt:
    def test_build_prompt_no_placeholders_returns_empty(self) -> None:
        block = AIFeatChoiceResolver.model_construct()
        assert block._build_prompt(Blueprint(feats=(FeatName.ALERT,))) == ""

    def test_build_prompt_level_one_adds_asi_note(self) -> None:
        block = AIFeatChoiceResolver.model_construct()
        state = Blueprint(
            feats=(FeatName.ANY_OF_YOUR_CHOICE,), classes=_Level1ClassLevels()
        )
        prompt = block._build_prompt(state)
        assert "ABILITY_SCORE_IMPROVEMENT is not available at level 1" in prompt

    def test_get_change_empty_prompt_returns_early(self) -> None:
        with patch.object(AIFeatChoiceResolver, "_build_prompt", return_value=""):
            block = AIFeatChoiceResolver.model_construct()
            state = Blueprint(feats=(FeatName.ANY_OF_YOUR_CHOICE,))
            result = block.apply(state)
        assert result is not None


@pytest.mark.unit
class TestSpellAssignerEmptySpellsToLearn:
    def test_wizard_empty_spells_returns_early(self) -> None:
        with patch.object(WizardSpellAssigner, "_get_spells_to_learn", return_value={}):
            block = WizardLLMSpellAssigner.model_construct(
                llm=MagicMock(), character_description=None, class_=Class.WIZARD
            )
            result = block.apply(
                WizardBlueprint(
                    classes=_Level1ClassLevels(),
                    caster=CasterInfo(spell_slots=FULL_CASTER_SPELL_SLOTS[0]),
                )
            )
        assert result is not None

    def test_sorcerer_empty_spells_returns_early(self) -> None:
        with patch.object(
            SorcererSpellAssigner, "_get_spells_to_learn", return_value={}
        ):
            block = SorcererLLMSpellAssigner.model_construct(
                llm=MagicMock(), character_description=None, class_=Class.SORCERER
            )
            result = block.apply(
                SorcererBlueprint(
                    classes=_Level1SorcererClassLevels(),
                    spell_slots=FULL_CASTER_SPELL_SLOTS[0],
                )
            )
        assert result is not None


@pytest.mark.unit
class TestEquipmentChooserBasePickEquipment:
    def test_pick_equipment_raises_not_implemented(self) -> None:
        block = _ConcreteEquipmentChooser.model_construct()
        with pytest.raises(NotImplementedError):
            block._pick_equipment(Blueprint())
