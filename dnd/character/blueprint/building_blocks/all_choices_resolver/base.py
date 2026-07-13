from typing import Literal

from dnd.character.blueprint.building_blocks.all_choices_resolver.base_resolver import (
    AllChoicesResolverBase,
)
from dnd.character.blueprint.building_blocks.building_block import BuildingBlock
from dnd.character.blueprint.building_blocks.equipment_chooser import (
    AnyEquipmentChooser,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver import (
    AnyFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver import (
    AnyLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver import (
    AnySkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver import (
    AnyStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.blueprint.building_blocks.tool_proficiency_choice_resolver import (
    AnyToolProficiencyChoiceResolver,
)
from dnd.character.blueprint.sentinels import (
    _RK,
    _HeK,
    _StCK,
    _SkCK,
    _WZK,
    _SOK,
    _FGK,
    _BAK,
    _ROK,
    _CLK,
    _DRK,
    _PAK,
    _RAK,
    _MOK,
    _BDK,
    _WAK,
    _ARK,
    _CDK,
)
from dnd.character.blueprint.states.basic_presentable import PresentableBasicBlueprint
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.stats import Stats


class AllChoicesResolver(AllChoicesResolverBase, BuildingBlock):
    """Resolves all character choices by chaining individual resolvers sequentially."""

    type: Literal[BuildingBlockType.ALL_CHOICES_RESOLVER] = (
        BuildingBlockType.ALL_CHOICES_RESOLVER
    )

    language_choice_resolver: AnyLanguageChoiceResolver
    skill_choice_resolver: AnySkillChoiceResolver
    feat_choice_resolver: AnyFeatChoiceResolver
    tool_proficiency_choice_resolver: AnyToolProficiencyChoiceResolver
    stat_choice_resolver: AnyStatChoiceResolver
    equipment_chooser: AnyEquipmentChooser

    def apply(
        self,
        blueprint: Blueprint[
            _RK,
            Stats,
            _HeK,
            _StCK,
            _SkCK,
            _WZK,
            _SOK,
            _FGK,
            _BAK,
            _ROK,
            _CLK,
            _DRK,
            _PAK,
            _RAK,
            _MOK,
            _BDK,
            _WAK,
            _ARK,
            _CDK,
        ],
    ) -> PresentableBasicBlueprint[
        _RK,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WZK,
        _SOK,
        _FGK,
        _BAK,
        _ROK,
        _CLK,
        _DRK,
        _PAK,
        _RAK,
        _MOK,
        _BDK,
        _WAK,
        _ARK,
        _CDK,
    ]:
        r1 = self.language_choice_resolver.apply(blueprint)
        r2 = self.skill_choice_resolver.apply(r1)
        r3 = self.feat_choice_resolver.apply(r2)
        r4 = self.tool_proficiency_choice_resolver.apply(r3)
        r5 = self.stat_choice_resolver.apply(r4)
        result = self.equipment_chooser.apply(r5)
        return PresentableBasicBlueprint.model_validate(dict(result))
