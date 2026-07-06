from __future__ import annotations

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pydantic import Field
from pydantic import ValidationError

from dnd.character.armor.names import ArmorName
from dnd.character.blueprint.blueprint_formatter import BlueprintFormatter
from dnd.character.blueprint.building_blocks.all_choices_resolver.ai import (
    AIAllChoicesResolver,
    AIAllNonStatChoicesResolver,
)
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.null_block import NullBlock
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver.ai import (
    AIToolProficiencyChoiceResolver,
    ToolProficiencySelection,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.ai import (
    AILanguageChoiceResolver,
    LanguageSelection,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver.choice_package import (
    ChoicePackage,
)
from dnd.character.blueprint.building_blocks.character_base_template import (
    CharacterBaseTemplate,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.ai import (
    AIEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.ai import (
    AIFeatChoiceResolver,
    FeatSelection,
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
    MagicalItemSelection,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.ai import (
    AISkillChoiceResolver,
    SkillSelection,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.ai import (
    AIStatChoiceResolver,
    StatIncreaseSelection,
)
from dnd.character.blueprint.building_blocks.subclass_assigner.ai import (
    AISubclassAssigner,
)
from dnd.character.blueprint.state import Blueprint
from dnd.character.feature.feats import FeatName
from dnd.character.magical_item.items import MAGICAL_ITEMS
from dnd.character.spells.spell_slots import Cantrip, FirstLevel
from dnd.character.stats import Stats
from dnd.choices.alignment import Alignment
from dnd.choices.background_creatrion.background import Background
from dnd.choices.class_creation.character_class import Class, SUBCLASSES
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.choices.language import Language
from dnd.other_profficiencies import ToolProficiency, GamingSet, MusicalInstrument
from dnd.character.race.race import Race
from dnd.choices.sex import Sex
from dnd.choices.stats_creation.statistic import Statistic
from dnd.skill_proficiency import Skill
from structured_output_creator import LLMRefusalError


def _exhaust(gen: Generator[object, object, object]) -> object:
    try:
        while True:
            next(gen)
    except StopIteration as exc:
        return exc.value


class _MinimalBP:
    """Satisfies BlueprintProtocol (__iter__) but lacks all specific protocol fields."""

    def __iter__(self) -> object:
        return iter([])


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


class _WizardBlueprint(Blueprint):
    """Blueprint subclass with get_wizard_level for spell assigner tests."""

    def get_wizard_level(self) -> int:
        return 1


class _SorcererBlueprint(Blueprint):
    """Blueprint subclass with get_sorcerer_level for spell assigner tests."""

    def get_sorcerer_level(self) -> int:
        return 1


class _Level1ClassLevels(ClassLevels):
    """ClassLevels with exactly 1 wizard level for testing level-1 branches."""

    wizard: int = 1


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
        result = _exhaust(block.get_change(Blueprint()))
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
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIStatChoiceResolver:
    def test_no_stat_choices_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        result = _exhaust(block.get_change(_StatsBP()))
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_stat_choices_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = StatIncreaseSelection(
            stat_increases={Statistic.INTELLIGENCE: 2}
        )

        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = _StatsBP(n_stat_choices=2)
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAISkillChoiceResolver:
    def test_no_skill_choices_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_skill_choices_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = SkillSelection(
            selected_skills=(Skill.ARCANA, Skill.HISTORY)
        )

        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(
            n_skill_choices=2,
            skills_to_choose_from=frozenset(
                {Skill.ARCANA, Skill.HISTORY, Skill.PERCEPTION}
            ),
        )
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIAllNonStatChoicesResolver:
    def test_no_choices_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIAllNonStatChoicesResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_language_choice_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ChoicePackage(
            languages=[Language.COMMON]
        )

        block = AIAllNonStatChoicesResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(languages=(Language.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIMagicalItemChooser:
    def test_no_items_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIMagicalItemChooser.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        result = _exhaust(block.get_change(Blueprint()))
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
            formatter=BlueprintFormatter(),
            n_common=1,
            n_uncommon=0,
            n_rare=0,
            n_very_rare=0,
            n_legendary=0,
            n_artifact=0,
            n_unique=0,
            n_mistery=0,
        )
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIEquipmentChooser:
    def test_no_choices_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIEquipmentChooser.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_equipment_choices_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = lambda prompt, model_class: (
            model_class(choice_0=0, choice_1=0, choice_2=0)
        )

        block = AIEquipmentChooser.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(
            equipment_choices=(
                (WeaponName.DAGGER,),
                (ArmorName.CLOTHES,),
                ("Rope",),
            )
        )
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAIFeatChoiceResolver:
    def test_no_placeholders_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIFeatChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = FeatSelection(
            feats={FeatName.ALERT}
        )

        block = AIFeatChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(feats=(FeatName.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()


@pytest.mark.unit
class TestAISubclassAssigner:
    def test_already_assigned_skips_llm(self) -> None:
        mock_llm = MagicMock()
        wizard_subclass_enum = SUBCLASSES[Class.WIZARD]
        first_subclass = next(iter(wizard_subclass_enum))

        with patch(
            "dnd.character.blueprint.building_blocks.subclass_assigner.ai._check_can_assign"
        ):
            state = Blueprint(subclasses=(first_subclass,))
            block = AISubclassAssigner.model_construct(
                class_=Class.WIZARD, llm=mock_llm, formatter=BlueprintFormatter()
            )
            result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_new_assignment_calls_llm(self) -> None:
        wizard_subclass_enum = SUBCLASSES[Class.WIZARD]
        first_subclass = next(iter(wizard_subclass_enum))

        def subclass_model_side_effect(prompt: object, model_class: object) -> object:
            return model_class(subclass=first_subclass)

        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = subclass_model_side_effect

        with patch(
            "dnd.character.blueprint.building_blocks.subclass_assigner.ai._check_can_assign"
        ):
            state = Blueprint()
            block = AISubclassAssigner.model_construct(
                class_=Class.WIZARD, llm=mock_llm, formatter=BlueprintFormatter()
            )
            result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("LLM failure")

        with patch(
            "dnd.character.blueprint.building_blocks.subclass_assigner.ai._check_can_assign"
        ):
            state = Blueprint()
            block = AISubclassAssigner.model_construct(
                class_=Class.WIZARD, llm=mock_llm, formatter=BlueprintFormatter()
            )
            with pytest.raises(LLMRefusalError):
                _exhaust(block.get_change(state))


@pytest.mark.unit
class TestWizardLLMSpellAssigner:
    def test_get_change_selects_spells(self) -> None:
        call_count: list[int] = [0]

        def spell_model_side_effect(prompt: object, model_class: object) -> object:
            level = call_count[0]
            call_count[0] += 1
            if level == 0:
                return model_class(spells=(Cantrip.FIRE_BOLT,))
            return model_class(spells=(FirstLevel.MAGIC_MISSILE,))

        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = spell_model_side_effect

        block = WizardLLMSpellAssigner.model_construct(
            llm=mock_llm, character_description=None, class_=Class.WIZARD
        )
        state = _WizardBlueprint()
        result = _exhaust(block.get_change(state))
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
                return model_class(spells=(Cantrip.FIRE_BOLT,))
            return model_class(spells=(FirstLevel.MAGIC_MISSILE,))

        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = spell_model_side_effect

        block = SorcererLLMSpellAssigner.model_construct(
            llm=mock_llm, character_description=None, class_=Class.SORCERER
        )
        state = _SorcererBlueprint()
        result = _exhaust(block.get_change(state))
        assert result is not None
        assert mock_llm.create_structured_output.call_count >= 1

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("network error")

        block = SorcererLLMSpellAssigner.model_construct(
            llm=mock_llm, character_description=None, class_=Class.SORCERER
        )
        state = _SorcererBlueprint()
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(state))


@pytest.mark.unit
class TestWizardLLMSpellAssignerErrors:
    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("network error")

        block = WizardLLMSpellAssigner.model_construct(
            llm=mock_llm, character_description=None, class_=Class.WIZARD
        )
        state = _WizardBlueprint()
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(state))


@pytest.mark.unit
class TestAIAllNonStatChoicesResolverExtraBranches:
    def test_skill_proficiency_choice_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ChoicePackage(
            skill_proficiencies=[Skill.PERCEPTION]
        )

        block = AIAllNonStatChoicesResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(skill_proficiencies=(Skill.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_feat_choice_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ChoicePackage(
            feats=[FeatName.ALERT]
        )

        block = AIAllNonStatChoicesResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(feats=(FeatName.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_tool_proficiency_choice_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ChoicePackage(
            tool_proficiencies=[ToolProficiency.ALCHEMISTS_SUPPLIES]
        )

        block = AIAllNonStatChoicesResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(tool_proficiencies=(ToolProficiency.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIAllNonStatChoicesResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(languages=(Language.ANY_OF_YOUR_CHOICE,))
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(state))


@pytest.mark.unit
class TestAILanguageChoiceResolver:
    def test_no_placeholder_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AILanguageChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(languages=(Language.COMMON,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = LanguageSelection(
            languages={Language.ELVISH}
        )

        block = AILanguageChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(languages=(Language.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_wrong_count_raises_value_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = LanguageSelection(
            languages={Language.ELVISH, Language.DWARVISH}
        )

        block = AILanguageChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(languages=(Language.ANY_OF_YOUR_CHOICE,))
        with pytest.raises(ValueError, match="AI returned"):
            _exhaust(block.get_change(state))

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AILanguageChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(languages=(Language.ANY_OF_YOUR_CHOICE,))
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(state))


@pytest.mark.unit
class TestAIToolProficiencyChoiceResolver:
    def test_no_placeholder_skips_llm(self) -> None:
        mock_llm = MagicMock()
        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(tool_proficiencies=(ToolProficiency.ALCHEMISTS_SUPPLIES,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_not_called()

    def test_with_tool_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ToolProficiencySelection(
            tool_proficiencies={ToolProficiency.ALCHEMISTS_SUPPLIES}
        )

        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(tool_proficiencies=(ToolProficiency.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_gaming_set_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ToolProficiencySelection(
            tool_proficiencies={GamingSet.DICE_SET}
        )

        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(tool_proficiencies=(GamingSet.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_musical_instrument_placeholder_calls_llm(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ToolProficiencySelection(
            tool_proficiencies={MusicalInstrument.LUTE}
        )

        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(tool_proficiencies=(MusicalInstrument.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None
        mock_llm.create_structured_output.assert_called_once()

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(tool_proficiencies=(ToolProficiency.ANY_OF_YOUR_CHOICE,))
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(state))


@pytest.mark.unit
class TestAIFeatChoiceResolverExtraBranches:
    def test_wrong_count_raises_value_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = FeatSelection(
            feats={FeatName.ALERT, FeatName.ACTOR}
        )

        block = AIFeatChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(feats=(FeatName.ANY_OF_YOUR_CHOICE,))
        with pytest.raises(ValueError, match="AI returned"):
            _exhaust(block.get_change(state))

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIFeatChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(feats=(FeatName.ANY_OF_YOUR_CHOICE,))
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(state))


@pytest.mark.unit
class TestAISkillChoiceResolverExtraBranches:
    def test_wrong_count_raises_value_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = SkillSelection(
            selected_skills=(Skill.ARCANA, Skill.HISTORY, Skill.PERCEPTION)
        )

        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(
            n_skill_choices=2,
            skills_to_choose_from=frozenset(
                {Skill.ARCANA, Skill.HISTORY, Skill.PERCEPTION}
            ),
        )
        with pytest.raises(ValueError, match="AI returned"):
            _exhaust(block.get_change(state))

    def test_invalid_skill_raises_value_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = SkillSelection(
            selected_skills=(Skill.ATHLETICS, Skill.DECEPTION)
        )

        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(
            n_skill_choices=2,
            skills_to_choose_from=frozenset({Skill.ARCANA, Skill.HISTORY}),
        )
        with pytest.raises(ValueError, match="not in available skills"):
            _exhaust(block.get_change(state))

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AISkillChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(
            n_skill_choices=2,
            skills_to_choose_from=frozenset({Skill.ARCANA, Skill.HISTORY}),
        )
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(state))


@pytest.mark.unit
class TestAIStatChoiceResolverExtraBranches:
    def test_wrong_total_raises_value_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = StatIncreaseSelection(
            stat_increases={Statistic.INTELLIGENCE: 1}
        )

        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = _StatsBP(n_stat_choices=2)
        with pytest.raises(ValueError, match="AI distributed"):
            _exhaust(block.get_change(state))

    def test_negative_increase_raises_value_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = StatIncreaseSelection(
            stat_increases={Statistic.INTELLIGENCE: 3, Statistic.WISDOM: -1}
        )

        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = _StatsBP(n_stat_choices=2)
        with pytest.raises(ValueError, match="negative increase"):
            _exhaust(block.get_change(state))

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIStatChoiceResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = _StatsBP(n_stat_choices=2)
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(state))


@pytest.mark.unit
class TestAIEquipmentChooserExtraBranches:
    def test_missing_choice_raises_validation_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = lambda prompt, model_class: (
            model_class(choice_0=0)  # choice_1 missing
        )

        block = AIEquipmentChooser.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(
            equipment_choices=(
                (WeaponName.DAGGER,),
                (ArmorName.CLOTHES,),
            )
        )
        with pytest.raises(ValidationError):
            _exhaust(block.get_change(state))

    def test_out_of_bounds_index_raises_validation_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = lambda prompt, model_class: (
            model_class(choice_0=5)  # lt=1, so 5 is out of bounds
        )

        block = AIEquipmentChooser.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(equipment_choices=((WeaponName.DAGGER,),))
        with pytest.raises(ValidationError):
            _exhaust(block.get_change(state))

    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIEquipmentChooser.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(equipment_choices=((WeaponName.DAGGER,),))
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(state))


@pytest.mark.unit
class TestAIMagicalItemChooserExtraBranches:
    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIMagicalItemChooser.model_construct(
            llm=mock_llm,
            formatter=BlueprintFormatter(),
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
            _exhaust(block.get_change(Blueprint()))

    def test_wrong_count_raises_value_error(self) -> None:
        first_item = next(iter(MAGICAL_ITEMS))
        second_item = next(
            item for item in MAGICAL_ITEMS if item.name != first_item.name
        )
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = MagicalItemSelection(
            selected_items=[first_item.name, second_item.name]
        )

        block = AIMagicalItemChooser.model_construct(
            llm=mock_llm,
            formatter=BlueprintFormatter(),
            n_common=1,
            n_uncommon=0,
            n_rare=0,
            n_very_rare=0,
            n_legendary=0,
            n_artifact=0,
            n_unique=0,
            n_mistery=0,
        )
        with pytest.raises(ValueError, match="AI selected"):
            _exhaust(block.get_change(Blueprint()))


@pytest.mark.unit
class TestAIBaseBuilderAssignerExtraBranches:
    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        block = AIBaseBuilderAssigner.model_construct(
            description="A wizard", llm=mock_llm
        )
        with pytest.raises(LLMRefusalError):
            _exhaust(block.get_change(Blueprint()))


@pytest.mark.unit
class TestAISubclassAssignerExtraBranches:
    def test_llm_error_raises_llm_error(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.side_effect = LLMRefusalError("bad output")

        with patch(
            "dnd.character.blueprint.building_blocks.subclass_assigner.ai._check_can_assign"
        ):
            state = Blueprint()
            block = AISubclassAssigner.model_construct(
                class_=Class.WIZARD, llm=mock_llm, formatter=BlueprintFormatter()
            )
            with pytest.raises(LLMRefusalError):
                _exhaust(block.get_change(state))


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
            formatter=BlueprintFormatter(),
            n_common=0,
            n_uncommon=1,
            n_rare=1,
            n_very_rare=1,
            n_legendary=1,
            n_artifact=1,
            n_unique=1,
            n_mistery=1,
        )
        result = _exhaust(block.get_change(Blueprint()))
        assert result is not None

    def test_build_prompt_no_items_returns_empty(self) -> None:
        block = AIMagicalItemChooser.model_construct(
            llm=MagicMock(),
            formatter=BlueprintFormatter(),
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
        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        with pytest.raises(NotImplementedError):
            block._select_tool_proficiency([], Blueprint())

    def test_select_gaming_set_not_implemented(self) -> None:
        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        with pytest.raises(NotImplementedError):
            block._select_gaming_set([], Blueprint())

    def test_select_musical_instrument_not_implemented(self) -> None:
        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        with pytest.raises(NotImplementedError):
            block._select_musical_instrument([], Blueprint())

    def test_build_prompt_no_placeholders_returns_empty(self) -> None:
        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        state = Blueprint(tool_proficiencies=(ToolProficiency.ALCHEMISTS_SUPPLIES,))
        assert block._build_prompt(state) == ""

    def test_get_change_empty_prompt_returns_early(self) -> None:
        with patch.object(
            AIToolProficiencyChoiceResolver, "_build_prompt", return_value=""
        ):
            block = AIToolProficiencyChoiceResolver.model_construct(
                llm=MagicMock(), formatter=BlueprintFormatter()
            )
            state = Blueprint(tool_proficiencies=(ToolProficiency.ANY_OF_YOUR_CHOICE,))
            result = _exhaust(block.get_change(state))
        assert result is not None


@pytest.mark.unit
class TestAILanguageChoiceResolverMethods:
    def test_select_from_available_not_implemented(self) -> None:
        block = AILanguageChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        with pytest.raises(NotImplementedError):
            block._select_from_available([], Blueprint())

    def test_build_prompt_no_placeholders_returns_empty(self) -> None:
        block = AILanguageChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        assert block._build_prompt(Blueprint(languages=(Language.COMMON,))) == ""

    def test_get_change_empty_prompt_returns_early(self) -> None:
        with patch.object(AILanguageChoiceResolver, "_build_prompt", return_value=""):
            block = AILanguageChoiceResolver.model_construct(
                llm=MagicMock(), formatter=BlueprintFormatter()
            )
            state = Blueprint(languages=(Language.ANY_OF_YOUR_CHOICE,))
            result = _exhaust(block.get_change(state))
        assert result is not None


@pytest.mark.unit
class TestAIFeatChoiceResolverBuildPrompt:
    def test_build_prompt_no_placeholders_returns_empty(self) -> None:
        block = AIFeatChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        assert block._build_prompt(Blueprint(feats=(FeatName.ALERT,))) == ""

    def test_build_prompt_level_one_adds_asi_note(self) -> None:
        block = AIFeatChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        state = Blueprint(
            feats=(FeatName.ANY_OF_YOUR_CHOICE,), classes=_Level1ClassLevels()
        )
        prompt = block._build_prompt(state)
        assert "ABILITY_SCORE_IMPROVEMENT is not available at level 1" in prompt

    def test_get_change_empty_prompt_returns_early(self) -> None:
        with patch.object(AIFeatChoiceResolver, "_build_prompt", return_value=""):
            block = AIFeatChoiceResolver.model_construct(
                llm=MagicMock(), formatter=BlueprintFormatter()
            )
            state = Blueprint(feats=(FeatName.ANY_OF_YOUR_CHOICE,))
            result = _exhaust(block.get_change(state))
        assert result is not None


@pytest.mark.unit
class TestAIAllNonStatChoicesResolverBuildPrompt:
    def test_feat_level_one_note(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ChoicePackage(
            feats=[FeatName.ALERT]
        )

        block = AIAllNonStatChoicesResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(
            feats=(FeatName.ANY_OF_YOUR_CHOICE,), classes=_Level1ClassLevels()
        )
        result = _exhaust(block.get_change(state))
        assert result is not None

    def test_stat_choices_section_in_prompt(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ChoicePackage(
            languages=[Language.COMMON]
        )

        block = AIAllNonStatChoicesResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        state = Blueprint(n_stat_choices=2, languages=(Language.ANY_OF_YOUR_CHOICE,))
        result = _exhaust(block.get_change(state))
        assert result is not None

    def test_skill_choices_section_in_prompt(self) -> None:
        mock_llm = MagicMock()
        mock_llm.create_structured_output.return_value = ChoicePackage()

        block = AIAllNonStatChoicesResolver.model_construct(
            llm=mock_llm, formatter=BlueprintFormatter()
        )
        result = _exhaust(block.get_change(Blueprint(n_skill_choices=2)))
        assert result is not None

    def test_build_prompt_all_zero_returns_empty(self) -> None:
        block = AIAllNonStatChoicesResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        assert block._build_prompt(Blueprint(), 0, 0, 0, 0) == ""


@pytest.mark.unit
class TestSpellAssignerEmptySpellsToLearn:
    def test_wizard_empty_spells_returns_early(self) -> None:
        with patch.object(WizardSpellAssigner, "_get_spells_to_learn", return_value={}):
            block = WizardLLMSpellAssigner.model_construct(
                llm=MagicMock(), character_description=None, class_=Class.WIZARD
            )
            result = _exhaust(block.get_change(_WizardBlueprint()))
        assert result is not None

    def test_sorcerer_empty_spells_returns_early(self) -> None:
        with patch.object(
            SorcererSpellAssigner, "_get_spells_to_learn", return_value={}
        ):
            block = SorcererLLMSpellAssigner.model_construct(
                llm=MagicMock(), character_description=None, class_=Class.SORCERER
            )
            result = _exhaust(block.get_change(_SorcererBlueprint()))
        assert result is not None


@pytest.mark.unit
class TestEquipmentChooserBasePickEquipment:
    def test_pick_equipment_raises_not_implemented(self) -> None:
        block = _ConcreteEquipmentChooser.model_construct()
        with pytest.raises(NotImplementedError):
            block._pick_equipment(Blueprint())


@pytest.mark.unit
class TestAIBlocksTypeErrors:
    def test_minimal_bp_iter_returns_empty(self) -> None:
        assert list(_MinimalBP()) == []

    def test_ai_feat_resolver_requires_feats_and_classes(self) -> None:
        block = AIFeatChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        with pytest.raises(TypeError):
            next(block.get_change(_MinimalBP()))

    def test_ai_language_resolver_requires_languages(self) -> None:
        block = AILanguageChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        with pytest.raises(TypeError):
            next(block.get_change(_MinimalBP()))

    def test_ai_subclass_assigner_requires_classes_and_subclasses(self) -> None:
        block = AISubclassAssigner.model_construct(
            class_=Class.WIZARD, llm=MagicMock(), formatter=BlueprintFormatter()
        )
        with pytest.raises(TypeError):
            next(block.get_change(_MinimalBP()))

    def test_ai_tool_proficiency_resolver_requires_tool_proficiencies(self) -> None:
        block = AIToolProficiencyChoiceResolver.model_construct(
            llm=MagicMock(), formatter=BlueprintFormatter()
        )
        with pytest.raises(TypeError):
            next(block.get_change(_MinimalBP()))


@pytest.mark.unit
class TestAIAllChoicesResolverGetChange:
    def test_get_change_with_null_blocks(self) -> None:
        resolver = AIAllChoicesResolver.model_construct(
            type=BuildingBlockType.AI_ALL_CHOICES_RESOLVER,
            stat_choice_resolver=NullBlock(),
            equipment_chooser=NullBlock(),
            feat_choice_resolver=NullBlock(),
            all_non_stat_choices_resolver=NullBlock(),
        )
        result = _exhaust(resolver.get_change(Blueprint()))
        assert result is not None
