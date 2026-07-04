from __future__ import annotations

from typing import Literal

from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    BaseRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceSubracePair,
)
from dnd.character.blueprint.state import HasStats
from dnd.character.race.race import Race
from dnd.character.race.subraces import Subrace
from pydantic import Field


class HumanRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Human race and the specified Human subrace to the character."""

    subrace: Literal[
        Subrace.HUMAN_MARK_OF_FINDING_EBERRONRISINGFROMTHELASTWAR,
        Subrace.HUMAN_MARK_OF_HANDLING_EBERRONRISINGFROMTHELASTWAR,
        Subrace.HUMAN_MARK_OF_MAKING_EBERRONRISINGFROMTHELASTWAR,
        Subrace.HUMAN_MARK_OF_PASSAGE_EBERRONRISINGFROMTHELASTWAR,
        Subrace.HUMAN_MARK_OF_SENTINEL_EBERRONRISINGFROMTHELASTWAR,
        Subrace.HUMAN_KELDON_PLANESHIFTDOMINARIA,
        Subrace.HUMAN_GAVONY_PLANESHIFTINNISTRAD,
        Subrace.HUMAN_KESSIG_PLANESHIFTINNISTRAD,
        Subrace.HUMAN_NEPHALIA_PLANESHIFTINNISTRAD,
        Subrace.HUMAN_STENSIA_PLANESHIFTINNISTRAD,
        Subrace.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
        Subrace.HUMAN_VARIANT_HUMAN_PLAYERSHANDBOOK,
    ] = Field(description="Human subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HUMAN, subrace=self.subrace)


class ElfRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Elf race and the specified Elf subrace to the character."""

    subrace: Literal[
        Subrace.ELF_MARK_OF_SHADOW_EBERRONRISINGFROMTHELASTWAR,
        Subrace.ELF_PALLID_ELF_EXPLORERSGUIDETOWILDEMOUNT,
        Subrace.ELF_BISHTAHAR_ELF_PLANESHIFTKALADESH,
        Subrace.ELF_TIRAHAR_ELF_PLANESHIFTKALADESH,
        Subrace.ELF_VAHADAR_ELF_PLANESHIFTKALADESH,
        Subrace.ELF_JURAGA_PLANESHIFTZENDIKAR,
        Subrace.ELF_MUL_DAYA_PLANESHIFTZENDIKAR,
        Subrace.ELF_TAJURU_PLANESHIFTZENDIKAR,
        Subrace.ELF_DARK_ELF_PLAYERSHANDBOOK,
        Subrace.ELF_HIGH_ELF_PLAYERSHANDBOOK,
        Subrace.ELF_WOOD_ELF_PLAYERSHANDBOOK,
        Subrace.ELF_ASTRAL_ELF_SPELLJAMMERADVENTURESINSPACE,
    ] = Field(description="Elf subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.ELF, subrace=self.subrace)


class DwarfRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Dwarf race and the specified Dwarf subrace to the character."""

    subrace: Literal[
        Subrace.DWARF_HILL_DWARF_PLAYERSHANDBOOK,
        Subrace.DWARF_MOUNTAIN_DWARF_PLAYERSHANDBOOK,
    ] = Field(description="Dwarf subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.DWARF, subrace=self.subrace)


class HalflingRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Halfling race and the specified Halfling subrace to the character."""

    subrace: Literal[
        Subrace.HALFLING_MARK_OF_HEALING_EBERRONRISINGFROMTHELASTWAR,
        Subrace.HALFLING_MARK_OF_HOSPITALITY_EBERRONRISINGFROMTHELASTWAR,
        Subrace.HALFLING_LOTUSDEN_HALFLING_EXPLORERSGUIDETOWILDEMOUNT,
        Subrace.HALFLING_LIGHTFOOT_PLAYERSHANDBOOK,
        Subrace.HALFLING_STOUT_PLAYERSHANDBOOK,
        Subrace.HALFLING_GHOSTWISE_SWORDCOASTADVENTURERSGUIDE,
    ] = Field(description="Halfling subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HALFLING, subrace=self.subrace)


class HalfElfRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Half-Elf race and the specified Half-Elf subrace to the character."""

    subrace: Literal[
        Subrace.HALF_ELF_AQUATIC_ELF_HERITAGE_PLAYERSHANDBOOK,
        Subrace.HALF_ELF_DARK_ELF_HERITAGE_PLAYERSHANDBOOK,
        Subrace.HALF_ELF_HIGH_ELF_HERITAGE_PLAYERSHANDBOOK,
        Subrace.HALF_ELF_WOOD_ELF_HERITAGE_PLAYERSHANDBOOK,
    ] = Field(description="Half-Elf subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HALF_ELF, subrace=self.subrace)


class HalfOrcRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Half-Orc race and the specified Half-Orc subrace to the character."""

    subrace: Literal[
        Subrace.HALF_ORC_MARK_OF_FINDING_EBERRONRISINGFROMTHELASTWAR,
        Subrace.HALF_ORC_HALF_ORC_PLAYERSHANDBOOK,
    ] = Field(description="Half-Orc subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HALF_ORC, subrace=self.subrace)


class TieflingRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Tiefling race and the specified Tiefling subrace to the character."""

    subrace: Literal[
        Subrace.TIEFLING_BLOODLINE_OF_BAALZEBUL_MORDENKAINENSTOMEOFFOES,
        Subrace.TIEFLING_BLOODLINE_OF_DISPATER_MORDENKAINENSTOMEOFFOES,
        Subrace.TIEFLING_BLOODLINE_OF_FIERNA_MORDENKAINENSTOMEOFFOES,
        Subrace.TIEFLING_BLOODLINE_OF_GLASYA_MORDENKAINENSTOMEOFFOES,
        Subrace.TIEFLING_BLOODLINE_OF_LEVISTUS_MORDENKAINENSTOMEOFFOES,
        Subrace.TIEFLING_BLOODLINE_OF_MAMMON_MORDENKAINENSTOMEOFFOES,
        Subrace.TIEFLING_BLOODLINE_OF_MEPHISTOPHELES_MORDENKAINENSTOMEOFFOES,
        Subrace.TIEFLING_BLOODLINE_OF_ZARIEL_MORDENKAINENSTOMEOFFOES,
        Subrace.TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK,
        Subrace.TIEFLING_DEVILS_TONGUE_SWORDCOASTADVENTURERSGUIDE,
        Subrace.TIEFLING_FERAL_SWORDCOASTADVENTURERSGUIDE,
        Subrace.TIEFLING_HELLFIRE_SWORDCOASTADVENTURERSGUIDE,
        Subrace.TIEFLING_WINGED_SWORDCOASTADVENTURERSGUIDE,
        Subrace.TIEFLING_ABYSSAL_TIEFLING_UNEARTHEDARCANA,
    ] = Field(description="Tiefling subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.TIEFLING, subrace=self.subrace)


class DragonbornRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Dragonborn race and the specified Dragonborn subrace to the character."""

    subrace: Literal[
        Subrace.DRAGONBORN_DRACONBLOOD_EXPLORERSGUIDETOWILDEMOUNT,
        Subrace.DRAGONBORN_RAVENITE_EXPLORERSGUIDETOWILDEMOUNT,
        Subrace.DRAGONBORN_CHROMATIC_FIZBANSTREASURYOFDRAGONS,
        Subrace.DRAGONBORN_GEM_FIZBANSTREASURYOFDRAGONS,
        Subrace.DRAGONBORN_METALLIC_FIZBANSTREASURYOFDRAGONS,
        Subrace.DRAGONBORN_DRAGONBORN_PLAYERSHANDBOOK,
        Subrace.DRAGONBORN_CHROMATIC_UNEARTHEDARCANA,
        Subrace.DRAGONBORN_GEM_UNEARTHEDARCANA,
        Subrace.DRAGONBORN_METALLIC_UNEARTHEDARCANA,
    ] = Field(description="Dragonborn subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.DRAGONBORN, subrace=self.subrace)


class GnomeRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Gnome race and the specified Gnome subrace to the character."""

    subrace: Literal[
        Subrace.GNOME_MARK_OF_SCRIBING_EBERRONRISINGFROMTHELASTWAR,
        Subrace.GNOME_FOREST_GNOME_PLAYERSHANDBOOK,
        Subrace.GNOME_ROCK_GNOME_PLAYERSHANDBOOK,
    ] = Field(description="Gnome subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GNOME, subrace=self.subrace)


class AasimarRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Aasimar race and the specified Aasimar subrace to the character."""

    subrace: Literal[
        Subrace.AASIMAR_FALLEN_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.AASIMAR_PROTECTOR_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.AASIMAR_SCOURGE_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.AASIMAR_FALLEN_AASIMAR_VOLOSGUIDETOMONSTERS,
        Subrace.AASIMAR_PROTECTOR_AASIMAR_VOLOSGUIDETOMONSTERS,
        Subrace.AASIMAR_SCOURGE_AASIMAR_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Aasimar subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.AASIMAR, subrace=self.subrace)


class GenasiAirRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Air Genasi race and the specified Air Genasi subrace to the character."""

    subrace: Literal[
        Subrace.GENASI_AIR_AIR_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        Subrace.GENASI_AIR_AIR_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Air Genasi subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GENASI_AIR, subrace=self.subrace)


class GenasiWaterRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Water Genasi race and the specified Water Genasi subrace to the character."""

    subrace: Literal[
        Subrace.GENASI_WATER_WATER_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        Subrace.GENASI_WATER_WATER_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Water Genasi subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GENASI_WATER, subrace=self.subrace)


class GenasiFireRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Fire Genasi race and the specified Fire Genasi subrace to the character."""

    subrace: Literal[
        Subrace.GENASI_FIRE_FIRE_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        Subrace.GENASI_FIRE_FIRE_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Fire Genasi subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GENASI_FIRE, subrace=self.subrace)


class GenasiEarthRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Earth Genasi race and the specified Earth Genasi subrace to the character."""

    subrace: Literal[
        Subrace.GENASI_EARTH_EARTH_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        Subrace.GENASI_EARTH_EARTH_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Earth Genasi subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GENASI_EARTH, subrace=self.subrace)


class GoliathRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Goliath race and the specified Goliath subrace to the character."""

    subrace: Literal[
        Subrace.GOLIATH_GOLIATH_ELEMENTALEVILPLAYERSGUIDE,
        Subrace.GOLIATH_GOLIATH_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
    ] = Field(description="Goliath subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GOLIATH, subrace=self.subrace)


class FirbolgRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Firbolg race and the specified Firbolg subrace to the character."""

    subrace: Literal[
        Subrace.FIRBOLG_FIRBOLG_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.FIRBOLG_FIRBOLG_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Firbolg subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.FIRBOLG, subrace=self.subrace)


class TabaxiRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Tabaxi race and the specified Tabaxi subrace to the character."""

    subrace: Literal[
        Subrace.TABAXI_TABAXI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.TABAXI_TABAXI_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Tabaxi subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.TABAXI, subrace=self.subrace)


class LizardfolkRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Lizardfolk race and the specified Lizardfolk subrace to the character."""

    subrace: Literal[
        Subrace.LIZARDFOLK_LIZARDFOLK_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.LIZARDFOLK_LIZARDFOLK_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Lizardfolk subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.LIZARDFOLK, subrace=self.subrace)


class KenkuRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Kenku race and the specified Kenku subrace to the character."""

    subrace: Literal[
        Subrace.KENKU_KENKU_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
    ] = Field(description="Kenku subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.KENKU, subrace=self.subrace)


class TortleRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Tortle race and the specified Tortle subrace to the character."""

    subrace: Literal[
        Subrace.TORTLE_TORTLE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
    ] = Field(description="Tortle subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.TORTLE, subrace=self.subrace)


class AarakocraRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Aarakocra race and the specified Aarakocra subrace to the character."""

    subrace: Literal[
        Subrace.AARAKOCRA_AARAKOCRA_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
    ] = Field(description="Aarakocra subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.AARAKOCRA, subrace=self.subrace)


class BugbearRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Bugbear race and the specified Bugbear subrace to the character."""

    subrace: Literal[
        Subrace.BUGBEAR_BUGBEAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.BUGBEAR_BUGBEAR_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Bugbear subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.BUGBEAR, subrace=self.subrace)


class GoblinRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Goblin race and the specified Goblin subrace to the character."""

    subrace: Literal[
        Subrace.GOBLIN_DANKWOOD_GOBLIN_ADVENTURESWITHMUKDANKWOOD,
        Subrace.GOBLIN_GOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.GOBLIN_GOBLIN_PLANESHIFTIXALAN,
        Subrace.GOBLIN_GOBLIN_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Goblin subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GOBLIN, subrace=self.subrace)


class HobgoblinRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Hobgoblin race and the specified Hobgoblin subrace to the character."""

    subrace: Literal[
        Subrace.HOBGOBLIN_HOBGOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.HOBGOBLIN_HOBGOBLIN_UNEARTHEDARCANA,
        Subrace.HOBGOBLIN_HOBGOBLIN_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Hobgoblin subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.HOBGOBLIN, subrace=self.subrace)


class KoboldRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Kobold race and the specified Kobold subrace to the character."""

    subrace: Literal[
        Subrace.KOBOLD_KOBOLD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.KOBOLD_KOBOLD_UNEARTHEDARCANA,
        Subrace.KOBOLD_KOBOLD_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Kobold subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.KOBOLD, subrace=self.subrace)


class OrcRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Orc race and the specified Orc subrace to the character."""

    subrace: Literal[
        Subrace.ORC_ORC_EBERRONRISINGFROMTHELASTWAR,
        Subrace.ORC_ORC_EXPLORERSGUIDETOWILDEMOUNT,
        Subrace.ORC_ORC_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.ORC_ORC_PLANESHIFTIXALAN,
        Subrace.ORC_ORC_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Orc subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.ORC, subrace=self.subrace)


class WarforgedRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Warforged race and the specified Warforged subrace to the character."""

    subrace: Literal[
        Subrace.WARFORGED_WARFORGED_EBERRONRISINGFROMTHELASTWAR,
        Subrace.WARFORGED_ENVOY_UNEARTHEDARCANA,
        Subrace.WARFORGED_JUGGERNAUT_UNEARTHEDARCANA,
        Subrace.WARFORGED_SKIRMISHER_UNEARTHEDARCANA,
    ] = Field(description="Warforged subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.WARFORGED, subrace=self.subrace)


class ChangelingRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Changeling race and the specified Changeling subrace to the character."""

    subrace: Literal[
        Subrace.CHANGELING_CHANGELING_EBERRONRISINGFROMTHELASTWAR,
        Subrace.CHANGELING_CHANGELING_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.CHANGELING_CHANGELING_UNEARTHEDARCANA,
    ] = Field(description="Changeling subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.CHANGELING, subrace=self.subrace)


class ShifterRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Shifter race and the specified Shifter subrace to the character."""

    subrace: Literal[
        Subrace.SHIFTER_BEASTHIDE_EBERRONRISINGFROMTHELASTWAR,
        Subrace.SHIFTER_LONGTOOTH_EBERRONRISINGFROMTHELASTWAR,
        Subrace.SHIFTER_SWIFTSTRIDE_EBERRONRISINGFROMTHELASTWAR,
        Subrace.SHIFTER_WILDHUNT_EBERRONRISINGFROMTHELASTWAR,
        Subrace.SHIFTER_BEASTHIDE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.SHIFTER_LONGTOOTH_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.SHIFTER_SWIFTSTRIDE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.SHIFTER_WILDHUNT_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.SHIFTER_CLIFFWALK_UNEARTHEDARCANA,
        Subrace.SHIFTER_RAZORCLAW_UNEARTHEDARCANA,
    ] = Field(description="Shifter subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.SHIFTER, subrace=self.subrace)


class MinotaurRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Minotaur race and the specified Minotaur subrace to the character."""

    subrace: Literal[
        Subrace.MINOTAUR_MINOTAUR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
    ] = Field(description="Minotaur subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.MINOTAUR, subrace=self.subrace)


class CentaurRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Centaur race and the specified Centaur subrace to the character."""

    subrace: Literal[
        Subrace.CENTAUR_GRUUL_CENTAUR_GUILDMASTERSGUIDETORAVNICA,
        Subrace.CENTAUR_SELESNYA_CENTAUR_GUILDMASTERSGUIDETORAVNICA,
        Subrace.CENTAUR_CENTAURS_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.CENTAUR_LAGONNA_MYTHICODYSSEYSOFTHEROS,
        Subrace.CENTAUR_PHERES_MYTHICODYSSEYSOFTHEROS,
    ] = Field(description="Centaur subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.CENTAUR, subrace=self.subrace)


class SatyrRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Satyr race and the specified Satyr subrace to the character."""

    subrace: Literal[
        Subrace.SATYR_SATYR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.SATYR_SATYR_MYTHICODYSSEYSOFTHEROS,
    ] = Field(description="Satyr subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.SATYR, subrace=self.subrace)


class LeoninRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Leonin race and the specified Leonin subrace to the character."""

    subrace: Literal[Subrace.LEONIN_LEONIN_LEONINFEATURES] = Field(
        description="Leonin subrace selection"
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.LEONIN, subrace=self.subrace)


class VerdanRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Verdan race and the specified Verdan subrace to the character."""

    subrace: Literal[Subrace.VERDAN_VERDAN_PLAYERSHANDBOOK] = Field(
        description="Verdan subrace selection"
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.VERDAN, subrace=self.subrace)


class GrungRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Grung race and the specified Grung subrace to the character."""

    subrace: Literal[Subrace.GRUNG_GRUNG_PLAYERSHANDBOOK] = Field(
        description="Grung subrace selection"
    )

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.GRUNG, subrace=self.subrace)


class KalashtarRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Kalashtar race and the specified Kalashtar subrace to the character."""

    subrace: Literal[
        Subrace.KALASHTAR_KALASHTAR_EBERRONRISINGFROMTHELASTWAR,
        Subrace.KALASHTAR_KALASHTAR_UNEARTHEDARCANA,
    ] = Field(description="Kalashtar subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.KALASHTAR, subrace=self.subrace)


class YuanTiPurebloodRaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns Yuan-Ti Pureblood race and the specified Yuan-Ti subrace to the character."""

    subrace: Literal[
        Subrace.YUAN_TI_PUREBLOOD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        Subrace.YUAN_TI_PUREBLOOD_VOLOSGUIDETOMONSTERS,
    ] = Field(description="Yuan-Ti Pureblood subrace selection")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=Race.YUAN_TI_PUREBLOOD, subrace=self.subrace)


class RaceAssigner[T: HasStats](BaseRaceAssigner[T]):
    """Assigns any race and subrace combination to the character."""

    race: Race = Field(description="The race to assign")
    subrace: Subrace = Field(description="The subrace to assign")

    def _get_race_and_subrace(self) -> RaceSubracePair:
        return RaceSubracePair(race=self.race, subrace=self.subrace)
