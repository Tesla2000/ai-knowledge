from typing import Literal

from dnd.character.blueprint.building_blocks.building_block_type import (
    BuildingBlockType,
)
from dnd.character.health_modifier import DwarfHealthModifier
from dnd.character.blueprint.building_blocks.feat_choice_resolver import (
    AnyFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.feat_choice_resolver.random import (
    RandomFeatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver import (
    AnyLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.language_choice_resolver.random import (
    RandomLanguageChoiceResolver,
)
from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    BaseRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceSubracePair,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver import (
    AnySkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.skill_choice_resolver.random import (
    RandomSkillChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver import (
    AnyStatChoiceResolver,
)
from dnd.character.blueprint.building_blocks.stat_choice_resolver.random import (
    RandomStatChoiceResolver,
)
from typing import TypeVar

from dnd.character.blueprint.sentinels import (
    _ARK,
    _BAK,
    _BDK,
    _CDK,
    _CLK,
    _DRK,
    _FGK,
    _HeK,
    _MOK,
    _PAK,
    _RAK,
    _ROK,
    _SkCK,
    _SOK,
    _WAK,
    AnyWizardLevel,
)
from dnd.character.blueprint.states._caster_info import CasterInfo
from dnd.character.blueprint.states.state import Blueprint
from dnd.character.blueprint.states.wizard._info import WizardInfo

_WIK = TypeVar("_WIK", bound=WizardInfo[AnyWizardLevel] | None)
_CK = TypeVar("_CK", bound=CasterInfo | None)
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName
from dnd.character.stats import Stats
from pydantic import Field


class HumanRaceAssigner(BaseRaceAssigner):
    """Assigns Human race and the specified Human subrace to the character."""

    type: Literal[BuildingBlockType.HUMAN_RACE_ASSIGNER] = (
        BuildingBlockType.HUMAN_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.HUMAN_MARK_OF_FINDING_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.HUMAN_MARK_OF_HANDLING_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.HUMAN_MARK_OF_MAKING_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.HUMAN_MARK_OF_PASSAGE_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.HUMAN_MARK_OF_SENTINEL_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.HUMAN_KELDON_PLANESHIFTDOMINARIA,
        SubraceName.HUMAN_GAVONY_PLANESHIFTINNISTRAD,
        SubraceName.HUMAN_KESSIG_PLANESHIFTINNISTRAD,
        SubraceName.HUMAN_NEPHALIA_PLANESHIFTINNISTRAD,
        SubraceName.HUMAN_STENSIA_PLANESHIFTINNISTRAD,
        SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
        SubraceName.HUMAN_VARIANT_HUMAN_PLAYERSHANDBOOK,
    ] = Field(description="Human subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )
    feat_choice_resolver: AnyFeatChoiceResolver = Field(
        default_factory=RandomFeatChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HUMAN, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        r4 = self.language_choice_resolver.apply(r3)
        r5 = self.feat_choice_resolver.apply(r4)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r5))


class ElfRaceAssigner(BaseRaceAssigner):
    """Assigns Elf race and the specified Elf subrace to the character."""

    type: Literal[BuildingBlockType.ELF_RACE_ASSIGNER] = (
        BuildingBlockType.ELF_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.ELF_MARK_OF_SHADOW_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.ELF_PALLID_ELF_EXPLORERSGUIDETOWILDEMOUNT,
        SubraceName.ELF_BISHTAHAR_ELF_PLANESHIFTKALADESH,
        SubraceName.ELF_TIRAHAR_ELF_PLANESHIFTKALADESH,
        SubraceName.ELF_VAHADAR_ELF_PLANESHIFTKALADESH,
        SubraceName.ELF_JURAGA_PLANESHIFTZENDIKAR,
        SubraceName.ELF_MUL_DAYA_PLANESHIFTZENDIKAR,
        SubraceName.ELF_TAJURU_PLANESHIFTZENDIKAR,
        SubraceName.ELF_DARK_ELF_PLAYERSHANDBOOK,
        SubraceName.ELF_HIGH_ELF_PLAYERSHANDBOOK,
        SubraceName.ELF_WOOD_ELF_PLAYERSHANDBOOK,
        SubraceName.ELF_ASTRAL_ELF_SPELLJAMMERADVENTURESINSPACE,
    ] = Field(description="Elf subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.ELF, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        r4 = self.language_choice_resolver.apply(r3)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r4))


class DwarfRaceAssigner(BaseRaceAssigner):
    """Assigns Dwarf race and the specified Dwarf subrace to the character."""

    type: Literal[BuildingBlockType.DWARF_RACE_ASSIGNER] = (
        BuildingBlockType.DWARF_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.DWARF_HILL_DWARF_PLAYERSHANDBOOK,
        SubraceName.DWARF_MOUNTAIN_DWARF_PLAYERSHANDBOOK,
    ] = Field(description="Dwarf subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.DWARF, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        result = super().apply(blueprint)
        return result.model_copy(
            update={
                "health_modifiers": (
                    *result.health_modifiers,
                    DwarfHealthModifier(),
                )
            }
        )


class HalflingRaceAssigner(BaseRaceAssigner):
    """Assigns Halfling race and the specified Halfling subrace to the character."""

    type: Literal[BuildingBlockType.HALFLING_RACE_ASSIGNER] = (
        BuildingBlockType.HALFLING_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.HALFLING_MARK_OF_HEALING_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.HALFLING_MARK_OF_HOSPITALITY_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.HALFLING_LOTUSDEN_HALFLING_EXPLORERSGUIDETOWILDEMOUNT,
        SubraceName.HALFLING_LIGHTFOOT_PLAYERSHANDBOOK,
        SubraceName.HALFLING_STOUT_PLAYERSHANDBOOK,
        SubraceName.HALFLING_GHOSTWISE_SWORDCOASTADVENTURERSGUIDE,
    ] = Field(description="Halfling subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HALFLING, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r3))


class HalfElfRaceAssigner(BaseRaceAssigner):
    """Assigns Half-Elf race and the specified Half-Elf subrace to the character."""

    type: Literal[BuildingBlockType.HALF_ELF_RACE_ASSIGNER] = (
        BuildingBlockType.HALF_ELF_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.HALF_ELF_AQUATIC_ELF_HERITAGE_PLAYERSHANDBOOK,
        SubraceName.HALF_ELF_DARK_ELF_HERITAGE_PLAYERSHANDBOOK,
        SubraceName.HALF_ELF_HIGH_ELF_HERITAGE_PLAYERSHANDBOOK,
        SubraceName.HALF_ELF_WOOD_ELF_HERITAGE_PLAYERSHANDBOOK,
    ] = Field(description="Half-Elf subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HALF_ELF, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.language_choice_resolver.apply(r2)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r3))


class HalfOrcRaceAssigner(BaseRaceAssigner):
    """Assigns Half-Orc race and the specified Half-Orc subrace to the character."""

    type: Literal[BuildingBlockType.HALF_ORC_RACE_ASSIGNER] = (
        BuildingBlockType.HALF_ORC_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.HALF_ORC_MARK_OF_FINDING_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.HALF_ORC_HALF_ORC_PLAYERSHANDBOOK,
    ] = Field(description="Half-Orc subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HALF_ORC, subrace=self.subrace)


class TieflingRaceAssigner(BaseRaceAssigner):
    """Assigns Tiefling race and the specified Tiefling subrace to the character."""

    type: Literal[BuildingBlockType.TIEFLING_RACE_ASSIGNER] = (
        BuildingBlockType.TIEFLING_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.TIEFLING_BLOODLINE_OF_BAALZEBUL_MORDENKAINENSTOMEOFFOES,
        SubraceName.TIEFLING_BLOODLINE_OF_DISPATER_MORDENKAINENSTOMEOFFOES,
        SubraceName.TIEFLING_BLOODLINE_OF_FIERNA_MORDENKAINENSTOMEOFFOES,
        SubraceName.TIEFLING_BLOODLINE_OF_GLASYA_MORDENKAINENSTOMEOFFOES,
        SubraceName.TIEFLING_BLOODLINE_OF_LEVISTUS_MORDENKAINENSTOMEOFFOES,
        SubraceName.TIEFLING_BLOODLINE_OF_MAMMON_MORDENKAINENSTOMEOFFOES,
        SubraceName.TIEFLING_BLOODLINE_OF_MEPHISTOPHELES_MORDENKAINENSTOMEOFFOES,
        SubraceName.TIEFLING_BLOODLINE_OF_ZARIEL_MORDENKAINENSTOMEOFFOES,
        SubraceName.TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK,
        SubraceName.TIEFLING_DEVILS_TONGUE_SWORDCOASTADVENTURERSGUIDE,
        SubraceName.TIEFLING_FERAL_SWORDCOASTADVENTURERSGUIDE,
        SubraceName.TIEFLING_HELLFIRE_SWORDCOASTADVENTURERSGUIDE,
        SubraceName.TIEFLING_WINGED_SWORDCOASTADVENTURERSGUIDE,
        SubraceName.TIEFLING_ABYSSAL_TIEFLING_UNEARTHEDARCANA,
    ] = Field(description="Tiefling subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.TIEFLING, subrace=self.subrace)


class DragonbornRaceAssigner(BaseRaceAssigner):
    """Assigns Dragonborn race and the specified Dragonborn subrace to the character."""

    type: Literal[BuildingBlockType.DRAGONBORN_RACE_ASSIGNER] = (
        BuildingBlockType.DRAGONBORN_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.DRAGONBORN_DRACONBLOOD_EXPLORERSGUIDETOWILDEMOUNT,
        SubraceName.DRAGONBORN_RAVENITE_EXPLORERSGUIDETOWILDEMOUNT,
        SubraceName.DRAGONBORN_CHROMATIC_FIZBANSTREASURYOFDRAGONS,
        SubraceName.DRAGONBORN_GEM_FIZBANSTREASURYOFDRAGONS,
        SubraceName.DRAGONBORN_METALLIC_FIZBANSTREASURYOFDRAGONS,
        SubraceName.DRAGONBORN_DRAGONBORN_PLAYERSHANDBOOK,
        SubraceName.DRAGONBORN_CHROMATIC_UNEARTHEDARCANA,
        SubraceName.DRAGONBORN_GEM_UNEARTHEDARCANA,
        SubraceName.DRAGONBORN_METALLIC_UNEARTHEDARCANA,
    ] = Field(description="Dragonborn subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.DRAGONBORN, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.language_choice_resolver.apply(r2)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r3))


class GnomeRaceAssigner(BaseRaceAssigner):
    """Assigns Gnome race and the specified Gnome subrace to the character."""

    type: Literal[BuildingBlockType.GNOME_RACE_ASSIGNER] = (
        BuildingBlockType.GNOME_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.GNOME_MARK_OF_SCRIBING_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.GNOME_FOREST_GNOME_PLAYERSHANDBOOK,
        SubraceName.GNOME_ROCK_GNOME_PLAYERSHANDBOOK,
    ] = Field(description="Gnome subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GNOME, subrace=self.subrace)


class AasimarRaceAssigner(BaseRaceAssigner):
    """Assigns Aasimar race and the specified Aasimar subrace to the character."""

    type: Literal[BuildingBlockType.AASIMAR_RACE_ASSIGNER] = (
        BuildingBlockType.AASIMAR_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.AASIMAR_FALLEN_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.AASIMAR_PROTECTOR_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.AASIMAR_SCOURGE_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.AASIMAR_FALLEN_AASIMAR_VOLOSGUIDETOMONSTERS,
        SubraceName.AASIMAR_PROTECTOR_AASIMAR_VOLOSGUIDETOMONSTERS,
        SubraceName.AASIMAR_SCOURGE_AASIMAR_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Aasimar subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.AASIMAR, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r3))


def _apply_stat_lang(
    race_assigner: "BaseRaceAssigner",
    blueprint: Blueprint[
        None,
        Stats,
        _HeK,
        Literal[0],
        _SkCK,
        _WIK,
        _CK,
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
    stat_choice_resolver: AnyStatChoiceResolver,
    language_choice_resolver: AnyLanguageChoiceResolver,
) -> Blueprint[
    Race,
    Stats,
    _HeK,
    Literal[0],
    Literal[0],
    _WIK,
    _CK,
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
    race_bp = race_assigner._build_race_blueprint(blueprint)
    r2 = stat_choice_resolver.apply(race_bp)
    r3 = language_choice_resolver.apply(r2)
    return Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
    ].model_validate(dict(r3))


class GenasiAirRaceAssigner(BaseRaceAssigner):
    """Assigns Air Genasi race and the specified Air Genasi subrace to the character."""

    type: Literal[BuildingBlockType.GENASI_AIR_RACE_ASSIGNER] = (
        BuildingBlockType.GENASI_AIR_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.GENASI_AIR_AIR_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        SubraceName.GENASI_AIR_AIR_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Air Genasi subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GENASI_AIR, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class GenasiWaterRaceAssigner(BaseRaceAssigner):
    """Assigns Water Genasi race and the specified Water Genasi subrace to the character."""

    type: Literal[BuildingBlockType.GENASI_WATER_RACE_ASSIGNER] = (
        BuildingBlockType.GENASI_WATER_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.GENASI_WATER_WATER_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        SubraceName.GENASI_WATER_WATER_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Water Genasi subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GENASI_WATER, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class GenasiFireRaceAssigner(BaseRaceAssigner):
    """Assigns Fire Genasi race and the specified Fire Genasi subrace to the character."""

    type: Literal[BuildingBlockType.GENASI_FIRE_RACE_ASSIGNER] = (
        BuildingBlockType.GENASI_FIRE_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.GENASI_FIRE_FIRE_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        SubraceName.GENASI_FIRE_FIRE_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Fire Genasi subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GENASI_FIRE, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class GenasiEarthRaceAssigner(BaseRaceAssigner):
    """Assigns Earth Genasi race and the specified Earth Genasi subrace to the character."""

    type: Literal[BuildingBlockType.GENASI_EARTH_RACE_ASSIGNER] = (
        BuildingBlockType.GENASI_EARTH_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.GENASI_EARTH_EARTH_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        SubraceName.GENASI_EARTH_EARTH_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Earth Genasi subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GENASI_EARTH, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class GoliathRaceAssigner(BaseRaceAssigner):
    """Assigns Goliath race and the specified Goliath subrace to the character."""

    type: Literal[BuildingBlockType.GOLIATH_RACE_ASSIGNER] = (
        BuildingBlockType.GOLIATH_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.GOLIATH_GOLIATH_ELEMENTALEVILPLAYERSGUIDE,
        SubraceName.GOLIATH_GOLIATH_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Goliath subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GOLIATH, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class FirbolgRaceAssigner(BaseRaceAssigner):
    """Assigns Firbolg race and the specified Firbolg subrace to the character."""

    type: Literal[BuildingBlockType.FIRBOLG_RACE_ASSIGNER] = (
        BuildingBlockType.FIRBOLG_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.FIRBOLG_FIRBOLG_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.FIRBOLG_FIRBOLG_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Firbolg subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.FIRBOLG, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class TabaxiRaceAssigner(BaseRaceAssigner):
    """Assigns Tabaxi race and the specified Tabaxi subrace to the character."""

    type: Literal[BuildingBlockType.TABAXI_RACE_ASSIGNER] = (
        BuildingBlockType.TABAXI_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.TABAXI_TABAXI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.TABAXI_TABAXI_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Tabaxi subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.TABAXI, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class LizardfolkRaceAssigner(BaseRaceAssigner):
    """Assigns Lizardfolk race and the specified Lizardfolk subrace to the character."""

    type: Literal[BuildingBlockType.LIZARDFOLK_RACE_ASSIGNER] = (
        BuildingBlockType.LIZARDFOLK_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.LIZARDFOLK_LIZARDFOLK_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.LIZARDFOLK_LIZARDFOLK_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Lizardfolk subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.LIZARDFOLK, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class KenkuRaceAssigner(BaseRaceAssigner):
    """Assigns Kenku race and the specified Kenku subrace to the character."""

    type: Literal[BuildingBlockType.KENKU_RACE_ASSIGNER] = (
        BuildingBlockType.KENKU_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.KENKU_KENKU_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
    ] = Field(description="Kenku subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.KENKU, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        r4 = self.language_choice_resolver.apply(r3)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r4))


class TortleRaceAssigner(BaseRaceAssigner):
    """Assigns Tortle race and the specified Tortle subrace to the character."""

    type: Literal[BuildingBlockType.TORTLE_RACE_ASSIGNER] = (
        BuildingBlockType.TORTLE_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.TORTLE_TORTLE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
    ] = Field(description="Tortle subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.TORTLE, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class AarakocraRaceAssigner(BaseRaceAssigner):
    """Assigns Aarakocra race and the specified Aarakocra subrace to the character."""

    type: Literal[BuildingBlockType.AARAKOCRA_RACE_ASSIGNER] = (
        BuildingBlockType.AARAKOCRA_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.AARAKOCRA_AARAKOCRA_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
    ] = Field(description="Aarakocra subrace selection")

    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.AARAKOCRA, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        result = super().apply(blueprint)
        return self.language_choice_resolver.apply(result)


class BugbearRaceAssigner(BaseRaceAssigner):
    """Assigns Bugbear race and the specified Bugbear subrace to the character."""

    type: Literal[BuildingBlockType.BUGBEAR_RACE_ASSIGNER] = (
        BuildingBlockType.BUGBEAR_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.BUGBEAR_BUGBEAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.BUGBEAR_BUGBEAR_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Bugbear subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.BUGBEAR, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        r4 = self.language_choice_resolver.apply(r3)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r4))


class GoblinRaceAssigner(BaseRaceAssigner):
    """Assigns Goblin race and the specified Goblin subrace to the character."""

    type: Literal[BuildingBlockType.GOBLIN_RACE_ASSIGNER] = (
        BuildingBlockType.GOBLIN_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.GOBLIN_DANKWOOD_GOBLIN_ADVENTURESWITHMUKDANKWOOD,
        SubraceName.GOBLIN_GOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.GOBLIN_GOBLIN_PLANESHIFTIXALAN,
        SubraceName.GOBLIN_GOBLIN_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Goblin subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GOBLIN, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        r4 = self.language_choice_resolver.apply(r3)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r4))


class HobgoblinRaceAssigner(BaseRaceAssigner):
    """Assigns Hobgoblin race and the specified Hobgoblin subrace to the character."""

    type: Literal[BuildingBlockType.HOBGOBLIN_RACE_ASSIGNER] = (
        BuildingBlockType.HOBGOBLIN_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.HOBGOBLIN_HOBGOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.HOBGOBLIN_HOBGOBLIN_UNEARTHEDARCANA,
        SubraceName.HOBGOBLIN_HOBGOBLIN_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Hobgoblin subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HOBGOBLIN, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r3))


class KoboldRaceAssigner(BaseRaceAssigner):
    """Assigns Kobold race and the specified Kobold subrace to the character."""

    type: Literal[BuildingBlockType.KOBOLD_RACE_ASSIGNER] = (
        BuildingBlockType.KOBOLD_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.KOBOLD_KOBOLD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.KOBOLD_KOBOLD_UNEARTHEDARCANA,
        SubraceName.KOBOLD_KOBOLD_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Kobold subrace selection")

    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.KOBOLD, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        result = super().apply(blueprint)
        return self.language_choice_resolver.apply(result)


class OrcRaceAssigner(BaseRaceAssigner):
    """Assigns Orc race and the specified Orc subrace to the character."""

    type: Literal[BuildingBlockType.ORC_RACE_ASSIGNER] = (
        BuildingBlockType.ORC_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.ORC_ORC_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.ORC_ORC_EXPLORERSGUIDETOWILDEMOUNT,
        SubraceName.ORC_ORC_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.ORC_ORC_PLANESHIFTIXALAN,
        SubraceName.ORC_ORC_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Orc subrace selection")

    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.ORC, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        result = super().apply(blueprint)
        return self.language_choice_resolver.apply(result)


class WarforgedRaceAssigner(BaseRaceAssigner):
    """Assigns Warforged race and the specified Warforged subrace to the character."""

    type: Literal[BuildingBlockType.WARFORGED_RACE_ASSIGNER] = (
        BuildingBlockType.WARFORGED_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.WARFORGED_WARFORGED_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.WARFORGED_ENVOY_UNEARTHEDARCANA,
        SubraceName.WARFORGED_JUGGERNAUT_UNEARTHEDARCANA,
        SubraceName.WARFORGED_SKIRMISHER_UNEARTHEDARCANA,
    ] = Field(description="Warforged subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.WARFORGED, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        r4 = self.language_choice_resolver.apply(r3)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r4))


class ChangelingRaceAssigner(BaseRaceAssigner):
    """Assigns Changeling race and the specified Changeling subrace to the character."""

    type: Literal[BuildingBlockType.CHANGELING_RACE_ASSIGNER] = (
        BuildingBlockType.CHANGELING_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.CHANGELING_CHANGELING_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.CHANGELING_CHANGELING_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.CHANGELING_CHANGELING_UNEARTHEDARCANA,
    ] = Field(description="Changeling subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.CHANGELING, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        r4 = self.language_choice_resolver.apply(r3)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r4))


class ShifterRaceAssigner(BaseRaceAssigner):
    """Assigns Shifter race and the specified Shifter subrace to the character."""

    type: Literal[BuildingBlockType.SHIFTER_RACE_ASSIGNER] = (
        BuildingBlockType.SHIFTER_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.SHIFTER_BEASTHIDE_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.SHIFTER_LONGTOOTH_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.SHIFTER_SWIFTSTRIDE_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.SHIFTER_WILDHUNT_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.SHIFTER_BEASTHIDE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.SHIFTER_LONGTOOTH_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.SHIFTER_SWIFTSTRIDE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.SHIFTER_WILDHUNT_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.SHIFTER_CLIFFWALK_UNEARTHEDARCANA,
        SubraceName.SHIFTER_RAZORCLAW_UNEARTHEDARCANA,
    ] = Field(description="Shifter subrace selection")

    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.SHIFTER, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        result = super().apply(blueprint)
        return self.language_choice_resolver.apply(result)


class MinotaurRaceAssigner(BaseRaceAssigner):
    """Assigns Minotaur race and the specified Minotaur subrace to the character."""

    type: Literal[BuildingBlockType.MINOTAUR_RACE_ASSIGNER] = (
        BuildingBlockType.MINOTAUR_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.MINOTAUR_MINOTAUR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
    ] = Field(description="Minotaur subrace selection")

    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.MINOTAUR, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        result = super().apply(blueprint)
        return self.language_choice_resolver.apply(result)


class CentaurRaceAssigner(BaseRaceAssigner):
    """Assigns Centaur race and the specified Centaur subrace to the character."""

    type: Literal[BuildingBlockType.CENTAUR_RACE_ASSIGNER] = (
        BuildingBlockType.CENTAUR_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.CENTAUR_GRUUL_CENTAUR_GUILDMASTERSGUIDETORAVNICA,
        SubraceName.CENTAUR_SELESNYA_CENTAUR_GUILDMASTERSGUIDETORAVNICA,
        SubraceName.CENTAUR_CENTAURS_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.CENTAUR_LAGONNA_MYTHICODYSSEYSOFTHEROS,
        SubraceName.CENTAUR_PHERES_MYTHICODYSSEYSOFTHEROS,
    ] = Field(description="Centaur subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.CENTAUR, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        r4 = self.language_choice_resolver.apply(r3)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r4))


class SatyrRaceAssigner(BaseRaceAssigner):
    """Assigns Satyr race and the specified Satyr subrace to the character."""

    type: Literal[BuildingBlockType.SATYR_RACE_ASSIGNER] = (
        BuildingBlockType.SATYR_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.SATYR_SATYR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.SATYR_SATYR_MYTHICODYSSEYSOFTHEROS,
    ] = Field(description="Satyr subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.SATYR, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class LeoninRaceAssigner(BaseRaceAssigner):
    """Assigns Leonin race and the specified Leonin subrace to the character."""

    type: Literal[BuildingBlockType.LEONIN_RACE_ASSIGNER] = (
        BuildingBlockType.LEONIN_RACE_ASSIGNER
    )
    subrace: Literal[SubraceName.LEONIN_LEONIN_LEONINFEATURES] = Field(
        description="Leonin subrace selection"
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.LEONIN, subrace=self.subrace)


class VerdanRaceAssigner(BaseRaceAssigner):
    """Assigns Verdan race and the specified Verdan subrace to the character."""

    type: Literal[BuildingBlockType.VERDAN_RACE_ASSIGNER] = (
        BuildingBlockType.VERDAN_RACE_ASSIGNER
    )
    subrace: Literal[SubraceName.VERDAN_VERDAN_PLAYERSHANDBOOK] = Field(
        description="Verdan subrace selection"
    )

    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.VERDAN, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        result = super().apply(blueprint)
        return self.language_choice_resolver.apply(result)


class GrungRaceAssigner(BaseRaceAssigner):
    """Assigns Grung race and the specified Grung subrace to the character."""

    type: Literal[BuildingBlockType.GRUNG_RACE_ASSIGNER] = (
        BuildingBlockType.GRUNG_RACE_ASSIGNER
    )
    subrace: Literal[SubraceName.GRUNG_GRUNG_PLAYERSHANDBOOK] = Field(
        description="Grung subrace selection"
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GRUNG, subrace=self.subrace)


class KalashtarRaceAssigner(BaseRaceAssigner):
    """Assigns Kalashtar race and the specified Kalashtar subrace to the character."""

    type: Literal[BuildingBlockType.KALASHTAR_RACE_ASSIGNER] = (
        BuildingBlockType.KALASHTAR_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.KALASHTAR_KALASHTAR_EBERRONRISINGFROMTHELASTWAR,
        SubraceName.KALASHTAR_KALASHTAR_UNEARTHEDARCANA,
    ] = Field(description="Kalashtar subrace selection")

    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.KALASHTAR, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        result = super().apply(blueprint)
        return self.language_choice_resolver.apply(result)


class YuanTiPurebloodRaceAssigner(BaseRaceAssigner):
    """Assigns Yuan-Ti Pureblood race and the specified Yuan-Ti subrace to the character."""

    type: Literal[BuildingBlockType.YUAN_TI_PUREBLOOD_RACE_ASSIGNER] = (
        BuildingBlockType.YUAN_TI_PUREBLOOD_RACE_ASSIGNER
    )
    subrace: Literal[
        SubraceName.YUAN_TI_PUREBLOOD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        SubraceName.YUAN_TI_PUREBLOOD_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Yuan-Ti Pureblood subrace selection")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.YUAN_TI_PUREBLOOD, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        return _apply_stat_lang(
            self, blueprint, self.stat_choice_resolver, self.language_choice_resolver
        )


class RaceAssigner(BaseRaceAssigner):
    """Assigns any race and subrace combination to the character."""

    type: Literal[BuildingBlockType.RACE_ASSIGNER] = BuildingBlockType.RACE_ASSIGNER
    race: Race = Field(description="The race to assign")
    subrace: SubraceName = Field(description="The subrace to assign")

    stat_choice_resolver: AnyStatChoiceResolver = Field(
        default_factory=RandomStatChoiceResolver
    )
    skill_choice_resolver: AnySkillChoiceResolver = Field(
        default_factory=RandomSkillChoiceResolver
    )
    language_choice_resolver: AnyLanguageChoiceResolver = Field(
        default_factory=RandomLanguageChoiceResolver
    )
    feat_choice_resolver: AnyFeatChoiceResolver = Field(
        default_factory=RandomFeatChoiceResolver
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=self.race, subrace=self.subrace)

    def apply(
        self,
        blueprint: Blueprint[
            None,
            Stats,
            _HeK,
            Literal[0],
            _SkCK,
            _WIK,
            _CK,
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
    ) -> Blueprint[
        Race,
        Stats,
        _HeK,
        Literal[0],
        Literal[0],
        _WIK,
        _CK,
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
        race_bp = self._build_race_blueprint(blueprint)
        r2 = self.stat_choice_resolver.apply(race_bp)
        r3 = self.skill_choice_resolver.apply(r2)
        r4 = self.language_choice_resolver.apply(r3)
        r5 = self.feat_choice_resolver.apply(r4)
        return Blueprint[
            Race,
            Stats,
            _HeK,
            Literal[0],
            Literal[0],
            _WIK,
            _CK,
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
        ].model_validate(dict(r5))
