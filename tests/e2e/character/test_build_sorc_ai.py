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
    LLMSpellAssigner,
)
from dnd.character.blueprint.building_blocks.subclass_assigner import (
    AISubclassAssigner,
)
from dnd.character.character import Character
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tests.integration.character.test_build_sorc import TestBuildSorcerer

load_dotenv()


@pytest.mark.e2e
class TestBuildSorcererAI(TestBuildSorcerer):
    def test_build_sorcerer_with_ai(self) -> None:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        spells_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

        all_choices_resolver = AIAllChoicesResolver(
            blocks=(
                PriorityStatChoiceResolver(priority=self.STATS_PRIORITY),
                RandomEquipmentChooser(),
                MaxIfNotMaxedResolver(priority=self.STATS_PRIORITY),
                AIAllNonStatChoicesResolver(llm=llm),
            )
        )

        magical_item_chooser = AIMagicalItemChooser(
            llm=llm,
            n_uncommon=1,
            n_rare=2,
            n_very_rare=1,
            n_legendary=1,
        )
        character_description = "Rządna władzy czarodziejka gotowa złamać wszelkie zasady by osiągnąć cel, preferuje manipulację i magię błyskawic"
        sorcerer = self._build_sorc(
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
            lambda class_: LLMSpellAssigner(
                class_=class_,
                llm=spells_llm,
                character_description=character_description,
            ),
        ).character

        assert isinstance(sorcerer, Character)
        assert sorcerer.weapons
        assert sorcerer.other_equipment
        assert sorcerer.magical_items
        sys.stdout.write(
            sorcerer.model_dump_json(
                indent=2,
                exclude_defaults=True,
            )
        )
