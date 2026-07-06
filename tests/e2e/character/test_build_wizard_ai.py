from __future__ import annotations

import sys

import pytest
from dnd.character.blueprint.building_blocks import (
    AIMagicalItemChooser,
)
from dnd.character.blueprint.building_blocks import (
    AIPartialBuilderAssigner,
)
from dnd.character.blueprint.building_blocks import (
    PriorityStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver import (
    AIAllChoicesResolver,
)
from dnd.character.blueprint.building_blocks.all_choices_resolver.ai import (
    AIAllNonStatChoicesResolver,
)
from dnd.character.blueprint.building_blocks.equipment_chooser.random import (
    RandomEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.max_if_not_maxed import (
    MaxIfNotMaxedResolver,
)
from dnd.character.blueprint.building_blocks.level_up.spell_assignment import (
    WizardLLMSpellAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    AISubclassAssigner,
)
from dnd.character.builder import SuccessBuiltResult
from dnd.character.character import Character
from dotenv import load_dotenv
from structured_output_creator import OpenAIService, RaisingService
from tests.integration.character.test_build_wizard import TestBuildWizard

load_dotenv()


@pytest.mark.e2e
class TestBuildWizardAI(TestBuildWizard):
    def test_build_wizard_with_ai(self) -> None:
        llm = RaisingService(service=OpenAIService(model="gpt-5.4", temperature=0.7))
        spells_llm = RaisingService(
            service=OpenAIService(model="gpt-5.4-mini", temperature=0.3)
        )

        all_choices_resolver = AIAllChoicesResolver(
            stat_choice_resolver=PriorityStatChoiceResolver(
                priority=self.STATS_PRIORITY
            ),
            equipment_chooser=RandomEquipmentChooser(),
            feat_choice_resolver=MaxIfNotMaxedResolver(priority=self.STATS_PRIORITY),
            all_non_stat_choices_resolver=AIAllNonStatChoicesResolver(llm=llm),
        )

        magical_item_chooser = AIMagicalItemChooser(
            llm=llm,
            n_uncommon=0,
            n_rare=2,
            n_very_rare=1,
            n_legendary=1,
        )
        previous_result = ""
        for character_description in (
            "Mistress of evil, summer of friends, mighty and prepared with deadly spells for combat. Has Robe of archmagi in equipment",
        ):
            character_description += previous_result
            result = self._build_wizard(
                magical_item_chooser,
                all_choices_resolver,
                AIPartialBuilderAssigner(
                    description=character_description,
                    llm=llm,
                ),
                AISubclassAssigner(
                    class_=self.CLASS,
                    available_subclasses=self.SUBCLASSES,
                    llm=llm,
                ),
                WizardLLMSpellAssigner(
                    llm=spells_llm,
                    character_description=character_description,
                ),
            )
            assert isinstance(result, SuccessBuiltResult), result
            character = result.character
            assert isinstance(character, Character)
            assert character.weapons
            assert character.other_equipment
            assert character.magical_items

            previous_result += (
                "You already constructed this character. Make this one a bit different holding true to the description"
                + character.model_dump_json(
                    exclude_defaults=True,
                )
            )
            sys.stdout.write(
                character.model_dump_json(
                    indent=2,
                    exclude_defaults=True,
                )
            )
