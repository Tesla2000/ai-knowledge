from __future__ import annotations

import pytest

from dnd.character.blueprint.building_blocks.race_assigner.base_race_assigner import (
    RaceSubracePair,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    AarakocraRaceAssigner,
    AasimarRaceAssigner,
    BugbearRaceAssigner,
    CentaurRaceAssigner,
    ChangelingRaceAssigner,
    DragonbornRaceAssigner,
    DwarfRaceAssigner,
    ElfRaceAssigner,
    FirbolgRaceAssigner,
    GenasiAirRaceAssigner,
    GenasiEarthRaceAssigner,
    GenasiFireRaceAssigner,
    GenasiWaterRaceAssigner,
    GnomeRaceAssigner,
    GoblinRaceAssigner,
    GoliathRaceAssigner,
    GrungRaceAssigner,
    HalfElfRaceAssigner,
    HalfOrcRaceAssigner,
    HalflingRaceAssigner,
    HobgoblinRaceAssigner,
    HumanRaceAssigner,
    KalashtarRaceAssigner,
    KenkuRaceAssigner,
    KoboldRaceAssigner,
    LeoninRaceAssigner,
    LizardfolkRaceAssigner,
    MinotaurRaceAssigner,
    OrcRaceAssigner,
    SatyrRaceAssigner,
    ShifterRaceAssigner,
    TabaxiRaceAssigner,
    TieflingRaceAssigner,
    TortleRaceAssigner,
    VerdanRaceAssigner,
    WarforgedRaceAssigner,
    YuanTiPurebloodRaceAssigner,
)
from dnd.character.race.race import Race
from dnd.character.race.subraces import SubraceName


@pytest.mark.unit
class TestSpecificRaceAssigners:
    def test_human_race_assigner(self) -> None:
        a = HumanRaceAssigner(subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.HUMAN,
            subrace=SubraceName.HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK,
        )

    def test_elf_race_assigner(self) -> None:
        a = ElfRaceAssigner(subrace=SubraceName.ELF_HIGH_ELF_PLAYERSHANDBOOK)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.ELF,
            subrace=SubraceName.ELF_HIGH_ELF_PLAYERSHANDBOOK,
        )

    def test_dwarf_race_assigner(self) -> None:
        a = DwarfRaceAssigner(subrace=SubraceName.DWARF_HILL_DWARF_PLAYERSHANDBOOK)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.DWARF,
            subrace=SubraceName.DWARF_HILL_DWARF_PLAYERSHANDBOOK,
        )

    def test_halfling_race_assigner(self) -> None:
        a = HalflingRaceAssigner(subrace=SubraceName.HALFLING_LIGHTFOOT_PLAYERSHANDBOOK)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.HALFLING,
            subrace=SubraceName.HALFLING_LIGHTFOOT_PLAYERSHANDBOOK,
        )

    def test_half_elf_race_assigner(self) -> None:
        a = HalfElfRaceAssigner(
            subrace=SubraceName.HALF_ELF_HIGH_ELF_HERITAGE_PLAYERSHANDBOOK
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.HALF_ELF,
            subrace=SubraceName.HALF_ELF_HIGH_ELF_HERITAGE_PLAYERSHANDBOOK,
        )

    def test_half_orc_race_assigner(self) -> None:
        a = HalfOrcRaceAssigner(subrace=SubraceName.HALF_ORC_HALF_ORC_PLAYERSHANDBOOK)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.HALF_ORC,
            subrace=SubraceName.HALF_ORC_HALF_ORC_PLAYERSHANDBOOK,
        )

    def test_tiefling_race_assigner(self) -> None:
        a = TieflingRaceAssigner(
            subrace=SubraceName.TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.TIEFLING,
            subrace=SubraceName.TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK,
        )

    def test_dragonborn_race_assigner(self) -> None:
        a = DragonbornRaceAssigner(
            subrace=SubraceName.DRAGONBORN_DRAGONBORN_PLAYERSHANDBOOK
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.DRAGONBORN,
            subrace=SubraceName.DRAGONBORN_DRAGONBORN_PLAYERSHANDBOOK,
        )

    def test_gnome_race_assigner(self) -> None:
        a = GnomeRaceAssigner(subrace=SubraceName.GNOME_ROCK_GNOME_PLAYERSHANDBOOK)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.GNOME,
            subrace=SubraceName.GNOME_ROCK_GNOME_PLAYERSHANDBOOK,
        )

    def test_aasimar_race_assigner(self) -> None:
        a = AasimarRaceAssigner(
            subrace=SubraceName.AASIMAR_FALLEN_AASIMAR_VOLOSGUIDETOMONSTERS
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.AASIMAR,
            subrace=SubraceName.AASIMAR_FALLEN_AASIMAR_VOLOSGUIDETOMONSTERS,
        )

    def test_genasi_air_race_assigner(self) -> None:
        a = GenasiAirRaceAssigner(
            subrace=SubraceName.GENASI_AIR_AIR_GENASI_ELEMENTALEVILPLAYERSCOMPANION
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.GENASI_AIR,
            subrace=SubraceName.GENASI_AIR_AIR_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        )

    def test_genasi_water_race_assigner(self) -> None:
        a = GenasiWaterRaceAssigner(
            subrace=SubraceName.GENASI_WATER_WATER_GENASI_ELEMENTALEVILPLAYERSCOMPANION
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.GENASI_WATER,
            subrace=SubraceName.GENASI_WATER_WATER_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        )

    def test_genasi_fire_race_assigner(self) -> None:
        a = GenasiFireRaceAssigner(
            subrace=SubraceName.GENASI_FIRE_FIRE_GENASI_ELEMENTALEVILPLAYERSCOMPANION
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.GENASI_FIRE,
            subrace=SubraceName.GENASI_FIRE_FIRE_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        )

    def test_genasi_earth_race_assigner(self) -> None:
        a = GenasiEarthRaceAssigner(
            subrace=SubraceName.GENASI_EARTH_EARTH_GENASI_ELEMENTALEVILPLAYERSCOMPANION
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.GENASI_EARTH,
            subrace=SubraceName.GENASI_EARTH_EARTH_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
        )

    def test_goliath_race_assigner(self) -> None:
        a = GoliathRaceAssigner(
            subrace=SubraceName.GOLIATH_GOLIATH_ELEMENTALEVILPLAYERSGUIDE
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.GOLIATH,
            subrace=SubraceName.GOLIATH_GOLIATH_ELEMENTALEVILPLAYERSGUIDE,
        )

    def test_firbolg_race_assigner(self) -> None:
        a = FirbolgRaceAssigner(
            subrace=SubraceName.FIRBOLG_FIRBOLG_VOLOSGUIDETOMONSTERS
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.FIRBOLG,
            subrace=SubraceName.FIRBOLG_FIRBOLG_VOLOSGUIDETOMONSTERS,
        )

    def test_tabaxi_race_assigner(self) -> None:
        a = TabaxiRaceAssigner(subrace=SubraceName.TABAXI_TABAXI_VOLOSGUIDETOMONSTERS)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.TABAXI,
            subrace=SubraceName.TABAXI_TABAXI_VOLOSGUIDETOMONSTERS,
        )

    def test_lizardfolk_race_assigner(self) -> None:
        a = LizardfolkRaceAssigner(
            subrace=SubraceName.LIZARDFOLK_LIZARDFOLK_VOLOSGUIDETOMONSTERS
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.LIZARDFOLK,
            subrace=SubraceName.LIZARDFOLK_LIZARDFOLK_VOLOSGUIDETOMONSTERS,
        )

    def test_kenku_race_assigner(self) -> None:
        a = KenkuRaceAssigner(
            subrace=SubraceName.KENKU_KENKU_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.KENKU,
            subrace=SubraceName.KENKU_KENKU_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        )

    def test_tortle_race_assigner(self) -> None:
        a = TortleRaceAssigner(
            subrace=SubraceName.TORTLE_TORTLE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.TORTLE,
            subrace=SubraceName.TORTLE_TORTLE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        )

    def test_aarakocra_race_assigner(self) -> None:
        a = AarakocraRaceAssigner(
            subrace=SubraceName.AARAKOCRA_AARAKOCRA_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.AARAKOCRA,
            subrace=SubraceName.AARAKOCRA_AARAKOCRA_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        )

    def test_bugbear_race_assigner(self) -> None:
        a = BugbearRaceAssigner(
            subrace=SubraceName.BUGBEAR_BUGBEAR_VOLOSGUIDETOMONSTERS
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.BUGBEAR,
            subrace=SubraceName.BUGBEAR_BUGBEAR_VOLOSGUIDETOMONSTERS,
        )

    def test_goblin_race_assigner(self) -> None:
        a = GoblinRaceAssigner(subrace=SubraceName.GOBLIN_GOBLIN_VOLOSGUIDETOMONSTERS)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.GOBLIN,
            subrace=SubraceName.GOBLIN_GOBLIN_VOLOSGUIDETOMONSTERS,
        )

    def test_hobgoblin_race_assigner(self) -> None:
        a = HobgoblinRaceAssigner(
            subrace=SubraceName.HOBGOBLIN_HOBGOBLIN_VOLOSGUIDETOMONSTERS
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.HOBGOBLIN,
            subrace=SubraceName.HOBGOBLIN_HOBGOBLIN_VOLOSGUIDETOMONSTERS,
        )

    def test_kobold_race_assigner(self) -> None:
        a = KoboldRaceAssigner(subrace=SubraceName.KOBOLD_KOBOLD_VOLOSGUIDETOMONSTERS)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.KOBOLD,
            subrace=SubraceName.KOBOLD_KOBOLD_VOLOSGUIDETOMONSTERS,
        )

    def test_orc_race_assigner(self) -> None:
        a = OrcRaceAssigner(subrace=SubraceName.ORC_ORC_VOLOSGUIDETOMONSTERS)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.ORC,
            subrace=SubraceName.ORC_ORC_VOLOSGUIDETOMONSTERS,
        )

    def test_warforged_race_assigner(self) -> None:
        a = WarforgedRaceAssigner(
            subrace=SubraceName.WARFORGED_WARFORGED_EBERRONRISINGFROMTHELASTWAR
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.WARFORGED,
            subrace=SubraceName.WARFORGED_WARFORGED_EBERRONRISINGFROMTHELASTWAR,
        )

    def test_changeling_race_assigner(self) -> None:
        a = ChangelingRaceAssigner(
            subrace=SubraceName.CHANGELING_CHANGELING_EBERRONRISINGFROMTHELASTWAR
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.CHANGELING,
            subrace=SubraceName.CHANGELING_CHANGELING_EBERRONRISINGFROMTHELASTWAR,
        )

    def test_shifter_race_assigner(self) -> None:
        a = ShifterRaceAssigner(
            subrace=SubraceName.SHIFTER_BEASTHIDE_EBERRONRISINGFROMTHELASTWAR
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.SHIFTER,
            subrace=SubraceName.SHIFTER_BEASTHIDE_EBERRONRISINGFROMTHELASTWAR,
        )

    def test_minotaur_race_assigner(self) -> None:
        a = MinotaurRaceAssigner(
            subrace=SubraceName.MINOTAUR_MINOTAUR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.MINOTAUR,
            subrace=SubraceName.MINOTAUR_MINOTAUR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        )

    def test_centaur_race_assigner(self) -> None:
        a = CentaurRaceAssigner(
            subrace=SubraceName.CENTAUR_GRUUL_CENTAUR_GUILDMASTERSGUIDETORAVNICA
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.CENTAUR,
            subrace=SubraceName.CENTAUR_GRUUL_CENTAUR_GUILDMASTERSGUIDETORAVNICA,
        )

    def test_satyr_race_assigner(self) -> None:
        a = SatyrRaceAssigner(
            subrace=SubraceName.SATYR_SATYR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.SATYR,
            subrace=SubraceName.SATYR_SATYR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
        )

    def test_leonin_race_assigner(self) -> None:
        a = LeoninRaceAssigner(subrace=SubraceName.LEONIN_LEONIN_LEONINFEATURES)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.LEONIN,
            subrace=SubraceName.LEONIN_LEONIN_LEONINFEATURES,
        )

    def test_verdan_race_assigner(self) -> None:
        a = VerdanRaceAssigner(subrace=SubraceName.VERDAN_VERDAN_PLAYERSHANDBOOK)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.VERDAN,
            subrace=SubraceName.VERDAN_VERDAN_PLAYERSHANDBOOK,
        )

    def test_grung_race_assigner(self) -> None:
        a = GrungRaceAssigner(subrace=SubraceName.GRUNG_GRUNG_PLAYERSHANDBOOK)
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.GRUNG,
            subrace=SubraceName.GRUNG_GRUNG_PLAYERSHANDBOOK,
        )

    def test_kalashtar_race_assigner(self) -> None:
        a = KalashtarRaceAssigner(
            subrace=SubraceName.KALASHTAR_KALASHTAR_EBERRONRISINGFROMTHELASTWAR
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.KALASHTAR,
            subrace=SubraceName.KALASHTAR_KALASHTAR_EBERRONRISINGFROMTHELASTWAR,
        )

    def test_yuan_ti_pureblood_race_assigner(self) -> None:
        a = YuanTiPurebloodRaceAssigner(
            subrace=SubraceName.YUAN_TI_PUREBLOOD_VOLOSGUIDETOMONSTERS
        )
        assert a._get_race_and_subrace() == RaceSubracePair(
            race=Race.YUAN_TI_PUREBLOOD,
            subrace=SubraceName.YUAN_TI_PUREBLOOD_VOLOSGUIDETOMONSTERS,
        )
