from enum import StrEnum

from dnd.character.race.race import Race
from typing import assert_never


class SubraceName(StrEnum):
    """Enumeration of all available D&D 5e subraces with sources."""

    AARAKOCRA_AARAKOCRA_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Aarakocra (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    AASIMAR_FALLEN_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Fallen Aasimar (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    AASIMAR_PROTECTOR_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Protector Aasimar (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    AASIMAR_SCOURGE_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Scourge Aasimar (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    AASIMAR_FALLEN_AASIMAR_VOLOSGUIDETOMONSTERS = (
        "Fallen Aasimar (VolosGuidetoMonsters)"
    )
    AASIMAR_PROTECTOR_AASIMAR_VOLOSGUIDETOMONSTERS = (
        "Protector Aasimar (VolosGuidetoMonsters)"
    )
    AASIMAR_SCOURGE_AASIMAR_VOLOSGUIDETOMONSTERS = (
        "Scourge Aasimar (VolosGuidetoMonsters)"
    )
    BUGBEAR_BUGBEAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Bugbear (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    BUGBEAR_BUGBEAR_VOLOSGUIDETOMONSTERS = "Bugbear (VolosGuidetoMonsters)"
    CENTAUR_GRUUL_CENTAUR_GUILDMASTERSGUIDETORAVNICA = (
        "Gruul Centaur (GuildmastersGuidetoRavnica)"
    )
    CENTAUR_SELESNYA_CENTAUR_GUILDMASTERSGUIDETORAVNICA = (
        "Selesnya Centaur (GuildmastersGuidetoRavnica)"
    )
    CENTAUR_CENTAURS_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Centaurs (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    CENTAUR_LAGONNA_MYTHICODYSSEYSOFTHEROS = "Lagonna (MythicOdysseysofTheros)"
    CENTAUR_PHERES_MYTHICODYSSEYSOFTHEROS = "Pheres (MythicOdysseysofTheros)"
    CHANGELING_CHANGELING_EBERRONRISINGFROMTHELASTWAR = (
        "Changeling (EberronRisingfromtheLastWar)"
    )
    CHANGELING_CHANGELING_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Changeling (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    CHANGELING_CHANGELING_UNEARTHEDARCANA = "Changeling (UnearthedArcana)"
    DRAGONBORN_DRACONBLOOD_EXPLORERSGUIDETOWILDEMOUNT = (
        "Draconblood (ExplorersGuidetoWildemount)"
    )
    DRAGONBORN_RAVENITE_EXPLORERSGUIDETOWILDEMOUNT = (
        "Ravenite (ExplorersGuidetoWildemount)"
    )
    DRAGONBORN_CHROMATIC_FIZBANSTREASURYOFDRAGONS = (
        "Chromatic (FizbansTreasuryofDragons)"
    )
    DRAGONBORN_GEM_FIZBANSTREASURYOFDRAGONS = "Gem (FizbansTreasuryofDragons)"
    DRAGONBORN_METALLIC_FIZBANSTREASURYOFDRAGONS = "Metallic (FizbansTreasuryofDragons)"
    DRAGONBORN_DRAGONBORN_PLAYERSHANDBOOK = "Dragonborn (PlayersHandbook)"
    DRAGONBORN_CHROMATIC_UNEARTHEDARCANA = "Chromatic (UnearthedArcana)"
    DRAGONBORN_GEM_UNEARTHEDARCANA = "Gem (UnearthedArcana)"
    DRAGONBORN_METALLIC_UNEARTHEDARCANA = "Metallic (UnearthedArcana)"
    DWARF_HILL_DWARF_PLAYERSHANDBOOK = "Hill Dwarf (PlayersHandbook)"
    DWARF_MOUNTAIN_DWARF_PLAYERSHANDBOOK = "Mountain Dwarf (PlayersHandbook)"
    ELF_MARK_OF_SHADOW_EBERRONRISINGFROMTHELASTWAR = (
        "Mark of Shadow (EberronRisingfromtheLastWar)"
    )
    ELF_PALLID_ELF_EXPLORERSGUIDETOWILDEMOUNT = (
        "Pallid Elf (ExplorersGuidetoWildemount)"
    )
    ELF_BISHTAHAR_ELF_PLANESHIFTKALADESH = "Bishtahar Elf (PlaneShiftKaladesh)"
    ELF_TIRAHAR_ELF_PLANESHIFTKALADESH = "Tirahar Elf (PlaneShiftKaladesh)"
    ELF_VAHADAR_ELF_PLANESHIFTKALADESH = "Vahadar Elf (PlaneShiftKaladesh)"
    ELF_JURAGA_PLANESHIFTZENDIKAR = "Juraga (PlaneShiftZendikar)"
    ELF_MUL_DAYA_PLANESHIFTZENDIKAR = "Mul Daya (PlaneShiftZendikar)"
    ELF_TAJURU_PLANESHIFTZENDIKAR = "Tajuru (PlaneShiftZendikar)"
    ELF_DARK_ELF_PLAYERSHANDBOOK = "Dark Elf (PlayersHandbook)"
    ELF_HIGH_ELF_PLAYERSHANDBOOK = "High Elf (PlayersHandbook)"
    ELF_WOOD_ELF_PLAYERSHANDBOOK = "Wood Elf (PlayersHandbook)"
    ELF_ASTRAL_ELF_SPELLJAMMERADVENTURESINSPACE = (
        "Astral Elf (SpelljammerAdventuresinSpace)"
    )
    FIRBOLG_FIRBOLG_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Firbolg (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    FIRBOLG_FIRBOLG_VOLOSGUIDETOMONSTERS = "Firbolg (VolosGuidetoMonsters)"
    GENASI_AIR_AIR_GENASI_ELEMENTALEVILPLAYERSCOMPANION = (
        "Air Genasi (ElementalEvilPlayersCompanion)"
    )
    GENASI_AIR_AIR_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Air Genasi (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    GENASI_EARTH_EARTH_GENASI_ELEMENTALEVILPLAYERSCOMPANION = (
        "Earth Genasi (ElementalEvilPlayersCompanion)"
    )
    GENASI_EARTH_EARTH_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Earth Genasi (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    GENASI_FIRE_FIRE_GENASI_ELEMENTALEVILPLAYERSCOMPANION = (
        "Fire Genasi (ElementalEvilPlayersCompanion)"
    )
    GENASI_FIRE_FIRE_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Fire Genasi (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    GENASI_WATER_WATER_GENASI_ELEMENTALEVILPLAYERSCOMPANION = (
        "Water Genasi (ElementalEvilPlayersCompanion)"
    )
    GENASI_WATER_WATER_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Water Genasi (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    GNOME_MARK_OF_SCRIBING_EBERRONRISINGFROMTHELASTWAR = (
        "Mark of Scribing (EberronRisingfromtheLastWar)"
    )
    GNOME_FOREST_GNOME_PLAYERSHANDBOOK = "Forest Gnome (PlayersHandbook)"
    GNOME_ROCK_GNOME_PLAYERSHANDBOOK = "Rock Gnome (PlayersHandbook)"
    GOBLIN_DANKWOOD_GOBLIN_ADVENTURESWITHMUKDANKWOOD = (
        "Dankwood Goblin (AdventureswithMukDankwood)"
    )
    GOBLIN_GOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Goblin (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    GOBLIN_GOBLIN_PLANESHIFTIXALAN = "Goblin (PlaneShiftIxalan)"
    GOBLIN_GOBLIN_VOLOSGUIDETOMONSTERS = "Goblin (VolosGuidetoMonsters)"
    GOLIATH_GOLIATH_ELEMENTALEVILPLAYERSGUIDE = "Goliath (ElementalEvilPlayersGuide)"
    GOLIATH_GOLIATH_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Goliath (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    GRUNG_GRUNG_PLAYERSHANDBOOK = "Grung (PlayersHandbook)"
    HALF_ELF_AQUATIC_ELF_HERITAGE_PLAYERSHANDBOOK = (
        "Aquatic Elf Heritage (PlayersHandbook)"
    )
    HALF_ELF_DARK_ELF_HERITAGE_PLAYERSHANDBOOK = "Dark Elf Heritage (PlayersHandbook)"
    HALF_ELF_HIGH_ELF_HERITAGE_PLAYERSHANDBOOK = "High Elf Heritage (PlayersHandbook)"
    HALF_ELF_WOOD_ELF_HERITAGE_PLAYERSHANDBOOK = "Wood Elf Heritage (PlayersHandbook)"
    HALF_ORC_MARK_OF_FINDING_EBERRONRISINGFROMTHELASTWAR = (
        "Half orc Mark of Finding (EberronRisingfromtheLastWar)"
    )
    HALF_ORC_HALF_ORC_PLAYERSHANDBOOK = "Half-Orc (PlayersHandbook)"
    HALFLING_MARK_OF_HEALING_EBERRONRISINGFROMTHELASTWAR = (
        "Mark of Healing (EberronRisingfromtheLastWar)"
    )
    HALFLING_MARK_OF_HOSPITALITY_EBERRONRISINGFROMTHELASTWAR = (
        "Mark of Hospitality (EberronRisingfromtheLastWar)"
    )
    HALFLING_LOTUSDEN_HALFLING_EXPLORERSGUIDETOWILDEMOUNT = (
        "Lotusden Halfling (ExplorersGuidetoWildemount)"
    )
    HALFLING_LIGHTFOOT_PLAYERSHANDBOOK = "Lightfoot (PlayersHandbook)"
    HALFLING_STOUT_PLAYERSHANDBOOK = "Stout (PlayersHandbook)"
    HALFLING_GHOSTWISE_SWORDCOASTADVENTURERSGUIDE = (
        "Ghostwise (SwordCoastAdventurersGuide)"
    )
    HOBGOBLIN_HOBGOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Hobgoblin (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    HOBGOBLIN_HOBGOBLIN_UNEARTHEDARCANA = "Hobgoblin (UnearthedArcana)"
    HOBGOBLIN_HOBGOBLIN_VOLOSGUIDETOMONSTERS = "Hobgoblin (VolosGuidetoMonsters)"
    HUMAN_MARK_OF_FINDING_EBERRONRISINGFROMTHELASTWAR = (
        "Mark of Finding (EberronRisingfromtheLastWar)"
    )
    HUMAN_MARK_OF_HANDLING_EBERRONRISINGFROMTHELASTWAR = (
        "Mark of Handling (EberronRisingfromtheLastWar)"
    )
    HUMAN_MARK_OF_MAKING_EBERRONRISINGFROMTHELASTWAR = (
        "Mark of Making (EberronRisingfromtheLastWar)"
    )
    HUMAN_MARK_OF_PASSAGE_EBERRONRISINGFROMTHELASTWAR = (
        "Mark of Passage (EberronRisingfromtheLastWar)"
    )
    HUMAN_MARK_OF_SENTINEL_EBERRONRISINGFROMTHELASTWAR = (
        "Mark of Sentinel (EberronRisingfromtheLastWar)"
    )
    HUMAN_KELDON_PLANESHIFTDOMINARIA = "Keldon (PlaneShiftDominaria)"
    HUMAN_GAVONY_PLANESHIFTINNISTRAD = "Gavony (PlaneShiftInnistrad)"
    HUMAN_KESSIG_PLANESHIFTINNISTRAD = "Kessig (PlaneShiftInnistrad)"
    HUMAN_NEPHALIA_PLANESHIFTINNISTRAD = "Nephalia (PlaneShiftInnistrad)"
    HUMAN_STENSIA_PLANESHIFTINNISTRAD = "Stensia (PlaneShiftInnistrad)"
    HUMAN_STANDARD_HUMAN_PLAYERSHANDBOOK = "Standard Human (PlayersHandbook)"
    HUMAN_VARIANT_HUMAN_PLAYERSHANDBOOK = "Variant Human (PlayersHandbook)"
    KENKU_KENKU_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Kenku (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    KALASHTAR_KALASHTAR_EBERRONRISINGFROMTHELASTWAR = (
        "Kalashtar (EberronRisingfromtheLastWar)"
    )
    KALASHTAR_KALASHTAR_UNEARTHEDARCANA = "Kalashtar (UnearthedArcana)"
    KOBOLD_KOBOLD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Kobold (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    KOBOLD_KOBOLD_UNEARTHEDARCANA = "Kobold (UnearthedArcana)"
    KOBOLD_KOBOLD_VOLOSGUIDETOMONSTERS = "Kobold (VolosGuidetoMonsters)"
    LEONIN_LEONIN_LEONINFEATURES = "Leonin (LeoninFeatures)"
    LIZARDFOLK_LIZARDFOLK_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Lizardfolk (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    LIZARDFOLK_LIZARDFOLK_VOLOSGUIDETOMONSTERS = "Lizardfolk (VolosGuidetoMonsters)"
    MINOTAUR_MINOTAUR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Minotaur (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    ORC_ORC_EBERRONRISINGFROMTHELASTWAR = "Orc (EberronRisingfromtheLastWar)"
    ORC_ORC_EXPLORERSGUIDETOWILDEMOUNT = "Orc (ExplorersGuidetoWildemount)"
    ORC_ORC_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Orc (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    ORC_ORC_PLANESHIFTIXALAN = "Orc (PlaneShiftIxalan)"
    ORC_ORC_VOLOSGUIDETOMONSTERS = "Orc (VolosGuidetoMonsters)"
    YUAN_TI_PUREBLOOD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Yuan-ti (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    YUAN_TI_PUREBLOOD_VOLOSGUIDETOMONSTERS = "Yuan-ti Pureblood (VolosGuidetoMonsters)"
    SATYR_SATYR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Satyr (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    SATYR_SATYR_MYTHICODYSSEYSOFTHEROS = "Satyr (MythicOdysseysofTheros)"
    SHIFTER_BEASTHIDE_EBERRONRISINGFROMTHELASTWAR = (
        "Beasthide (EberronRisingfromtheLastWar)"
    )
    SHIFTER_LONGTOOTH_EBERRONRISINGFROMTHELASTWAR = (
        "Longtooth (EberronRisingfromtheLastWar)"
    )
    SHIFTER_SWIFTSTRIDE_EBERRONRISINGFROMTHELASTWAR = (
        "Swiftstride (EberronRisingfromtheLastWar)"
    )
    SHIFTER_WILDHUNT_EBERRONRISINGFROMTHELASTWAR = (
        "Wildhunt (EberronRisingfromtheLastWar)"
    )
    SHIFTER_BEASTHIDE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Beasthide (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    SHIFTER_LONGTOOTH_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Longtooth (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    SHIFTER_SWIFTSTRIDE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Swiftstride (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    SHIFTER_WILDHUNT_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Wildhunt (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    SHIFTER_CLIFFWALK_UNEARTHEDARCANA = "Cliffwalk (UnearthedArcana)"
    SHIFTER_RAZORCLAW_UNEARTHEDARCANA = "Razorclaw (UnearthedArcana)"
    TABAXI_TABAXI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Tabaxi (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    TABAXI_TABAXI_VOLOSGUIDETOMONSTERS = "Tabaxi (VolosGuidetoMonsters)"
    TIEFLING_BLOODLINE_OF_BAALZEBUL_MORDENKAINENSTOMEOFFOES = (
        "Bloodline of Baalzebul (MordenkainensTomeofFoes)"
    )
    TIEFLING_BLOODLINE_OF_DISPATER_MORDENKAINENSTOMEOFFOES = (
        "Bloodline of Dispater (MordenkainensTomeofFoes)"
    )
    TIEFLING_BLOODLINE_OF_FIERNA_MORDENKAINENSTOMEOFFOES = (
        "Bloodline of Fierna (MordenkainensTomeofFoes)"
    )
    TIEFLING_BLOODLINE_OF_GLASYA_MORDENKAINENSTOMEOFFOES = (
        "Bloodline of Glasya (MordenkainensTomeofFoes)"
    )
    TIEFLING_BLOODLINE_OF_LEVISTUS_MORDENKAINENSTOMEOFFOES = (
        "Bloodline of Levistus (MordenkainensTomeofFoes)"
    )
    TIEFLING_BLOODLINE_OF_MAMMON_MORDENKAINENSTOMEOFFOES = (
        "Bloodline of Mammon (MordenkainensTomeofFoes)"
    )
    TIEFLING_BLOODLINE_OF_MEPHISTOPHELES_MORDENKAINENSTOMEOFFOES = (
        "Bloodline of Mephistopheles (MordenkainensTomeofFoes)"
    )
    TIEFLING_BLOODLINE_OF_ZARIEL_MORDENKAINENSTOMEOFFOES = (
        "Bloodline of Zariel (MordenkainensTomeofFoes)"
    )
    TIEFLING_BLOODLINE_OF_ASMODEUS_PLAYERSHANDBOOK = (
        "Bloodline of Asmodeus (PlayersHandbook)"
    )
    TIEFLING_DEVILS_TONGUE_SWORDCOASTADVENTURERSGUIDE = (
        "Devil's Tongue(SwordCoastAdventurersGuide)"
    )
    TIEFLING_FERAL_SWORDCOASTADVENTURERSGUIDE = "Feral (SwordCoastAdventurersGuide)"
    TIEFLING_HELLFIRE_SWORDCOASTADVENTURERSGUIDE = (
        "Hellfire (SwordCoastAdventurersGuide)"
    )
    TIEFLING_WINGED_SWORDCOASTADVENTURERSGUIDE = "Winged (SwordCoastAdventurersGuide)"
    TIEFLING_ABYSSAL_TIEFLING_UNEARTHEDARCANA = "Abyssal Tiefling (UnearthedArcana)"
    TORTLE_TORTLE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE = (
        "Tortle (MordenkainenPresentsMonstersoftheMultiverse)"
    )
    VERDAN_VERDAN_PLAYERSHANDBOOK = "Verdan (PlayersHandbook)"
    WARFORGED_WARFORGED_EBERRONRISINGFROMTHELASTWAR = (
        "Warforged (EberronRisingfromtheLastWar)"
    )
    WARFORGED_ENVOY_UNEARTHEDARCANA = "Envoy (UnearthedArcana)"
    WARFORGED_JUGGERNAUT_UNEARTHEDARCANA = "Juggernaut (UnearthedArcana)"
    WARFORGED_SKIRMISHER_UNEARTHEDARCANA = "Skirmisher (UnearthedArcana)"


def _get_subraces(race: Race) -> tuple[SubraceName, ...]:
    match race:
        case Race.HUMAN:
            return (
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
            )
        case Race.ELF:
            return (
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
            )
        case Race.DWARF:
            return (
                SubraceName.DWARF_HILL_DWARF_PLAYERSHANDBOOK,
                SubraceName.DWARF_MOUNTAIN_DWARF_PLAYERSHANDBOOK,
            )
        case Race.HALFLING:
            return (
                SubraceName.HALFLING_MARK_OF_HEALING_EBERRONRISINGFROMTHELASTWAR,
                SubraceName.HALFLING_MARK_OF_HOSPITALITY_EBERRONRISINGFROMTHELASTWAR,
                SubraceName.HALFLING_LOTUSDEN_HALFLING_EXPLORERSGUIDETOWILDEMOUNT,
                SubraceName.HALFLING_LIGHTFOOT_PLAYERSHANDBOOK,
                SubraceName.HALFLING_STOUT_PLAYERSHANDBOOK,
                SubraceName.HALFLING_GHOSTWISE_SWORDCOASTADVENTURERSGUIDE,
            )
        case Race.HALF_ELF:
            return (
                SubraceName.HALF_ELF_AQUATIC_ELF_HERITAGE_PLAYERSHANDBOOK,
                SubraceName.HALF_ELF_DARK_ELF_HERITAGE_PLAYERSHANDBOOK,
                SubraceName.HALF_ELF_HIGH_ELF_HERITAGE_PLAYERSHANDBOOK,
                SubraceName.HALF_ELF_WOOD_ELF_HERITAGE_PLAYERSHANDBOOK,
            )
        case Race.HALF_ORC:
            return (
                SubraceName.HALF_ORC_MARK_OF_FINDING_EBERRONRISINGFROMTHELASTWAR,
                SubraceName.HALF_ORC_HALF_ORC_PLAYERSHANDBOOK,
            )
        case Race.TIEFLING:
            return (
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
            )
        case Race.DRAGONBORN:
            return (
                SubraceName.DRAGONBORN_DRACONBLOOD_EXPLORERSGUIDETOWILDEMOUNT,
                SubraceName.DRAGONBORN_RAVENITE_EXPLORERSGUIDETOWILDEMOUNT,
                SubraceName.DRAGONBORN_CHROMATIC_FIZBANSTREASURYOFDRAGONS,
                SubraceName.DRAGONBORN_GEM_FIZBANSTREASURYOFDRAGONS,
                SubraceName.DRAGONBORN_METALLIC_FIZBANSTREASURYOFDRAGONS,
                SubraceName.DRAGONBORN_DRAGONBORN_PLAYERSHANDBOOK,
                SubraceName.DRAGONBORN_CHROMATIC_UNEARTHEDARCANA,
                SubraceName.DRAGONBORN_GEM_UNEARTHEDARCANA,
                SubraceName.DRAGONBORN_METALLIC_UNEARTHEDARCANA,
            )
        case Race.GNOME:
            return (
                SubraceName.GNOME_MARK_OF_SCRIBING_EBERRONRISINGFROMTHELASTWAR,
                SubraceName.GNOME_FOREST_GNOME_PLAYERSHANDBOOK,
                SubraceName.GNOME_ROCK_GNOME_PLAYERSHANDBOOK,
            )
        case Race.AASIMAR:
            return (
                SubraceName.AASIMAR_FALLEN_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.AASIMAR_PROTECTOR_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.AASIMAR_SCOURGE_AASIMAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.AASIMAR_FALLEN_AASIMAR_VOLOSGUIDETOMONSTERS,
                SubraceName.AASIMAR_PROTECTOR_AASIMAR_VOLOSGUIDETOMONSTERS,
                SubraceName.AASIMAR_SCOURGE_AASIMAR_VOLOSGUIDETOMONSTERS,
            )
        case Race.GENASI_AIR:
            return (
                SubraceName.GENASI_AIR_AIR_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
                SubraceName.GENASI_AIR_AIR_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
            )
        case Race.GENASI_WATER:
            return (
                SubraceName.GENASI_WATER_WATER_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
                SubraceName.GENASI_WATER_WATER_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
            )
        case Race.GENASI_FIRE:
            return (
                SubraceName.GENASI_FIRE_FIRE_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
                SubraceName.GENASI_FIRE_FIRE_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
            )
        case Race.GENASI_EARTH:
            return (
                SubraceName.GENASI_EARTH_EARTH_GENASI_ELEMENTALEVILPLAYERSCOMPANION,
                SubraceName.GENASI_EARTH_EARTH_GENASI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
            )
        case Race.GOLIATH:
            return (
                SubraceName.GOLIATH_GOLIATH_ELEMENTALEVILPLAYERSGUIDE,
                SubraceName.GOLIATH_GOLIATH_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
            )
        case Race.FIRBOLG:
            return (
                SubraceName.FIRBOLG_FIRBOLG_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.FIRBOLG_FIRBOLG_VOLOSGUIDETOMONSTERS,
            )
        case Race.TABAXI:
            return (
                SubraceName.TABAXI_TABAXI_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.TABAXI_TABAXI_VOLOSGUIDETOMONSTERS,
            )
        case Race.LIZARDFOLK:
            return (
                SubraceName.LIZARDFOLK_LIZARDFOLK_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.LIZARDFOLK_LIZARDFOLK_VOLOSGUIDETOMONSTERS,
            )
        case Race.KENKU:
            return (
                SubraceName.KENKU_KENKU_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
            )
        case Race.TORTLE:
            return (
                SubraceName.TORTLE_TORTLE_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
            )
        case Race.AARAKOCRA:
            return (
                SubraceName.AARAKOCRA_AARAKOCRA_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
            )
        case Race.BUGBEAR:
            return (
                SubraceName.BUGBEAR_BUGBEAR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.BUGBEAR_BUGBEAR_VOLOSGUIDETOMONSTERS,
            )
        case Race.GOBLIN:
            return (
                SubraceName.GOBLIN_DANKWOOD_GOBLIN_ADVENTURESWITHMUKDANKWOOD,
                SubraceName.GOBLIN_GOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.GOBLIN_GOBLIN_PLANESHIFTIXALAN,
                SubraceName.GOBLIN_GOBLIN_VOLOSGUIDETOMONSTERS,
            )
        case Race.HOBGOBLIN:
            return (
                SubraceName.HOBGOBLIN_HOBGOBLIN_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.HOBGOBLIN_HOBGOBLIN_UNEARTHEDARCANA,
                SubraceName.HOBGOBLIN_HOBGOBLIN_VOLOSGUIDETOMONSTERS,
            )
        case Race.KOBOLD:
            return (
                SubraceName.KOBOLD_KOBOLD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.KOBOLD_KOBOLD_UNEARTHEDARCANA,
                SubraceName.KOBOLD_KOBOLD_VOLOSGUIDETOMONSTERS,
            )
        case Race.ORC:
            return (
                SubraceName.ORC_ORC_EBERRONRISINGFROMTHELASTWAR,
                SubraceName.ORC_ORC_EXPLORERSGUIDETOWILDEMOUNT,
                SubraceName.ORC_ORC_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.ORC_ORC_PLANESHIFTIXALAN,
                SubraceName.ORC_ORC_VOLOSGUIDETOMONSTERS,
            )
        case Race.WARFORGED:
            return (
                SubraceName.WARFORGED_WARFORGED_EBERRONRISINGFROMTHELASTWAR,
                SubraceName.WARFORGED_ENVOY_UNEARTHEDARCANA,
                SubraceName.WARFORGED_JUGGERNAUT_UNEARTHEDARCANA,
                SubraceName.WARFORGED_SKIRMISHER_UNEARTHEDARCANA,
            )
        case Race.CHANGELING:
            return (
                SubraceName.CHANGELING_CHANGELING_EBERRONRISINGFROMTHELASTWAR,
                SubraceName.CHANGELING_CHANGELING_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.CHANGELING_CHANGELING_UNEARTHEDARCANA,
            )
        case Race.SHIFTER:
            return (
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
            )
        case Race.MINOTAUR:
            return (
                SubraceName.MINOTAUR_MINOTAUR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
            )
        case Race.CENTAUR:
            return (
                SubraceName.CENTAUR_GRUUL_CENTAUR_GUILDMASTERSGUIDETORAVNICA,
                SubraceName.CENTAUR_SELESNYA_CENTAUR_GUILDMASTERSGUIDETORAVNICA,
                SubraceName.CENTAUR_CENTAURS_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.CENTAUR_LAGONNA_MYTHICODYSSEYSOFTHEROS,
                SubraceName.CENTAUR_PHERES_MYTHICODYSSEYSOFTHEROS,
            )
        case Race.SATYR:
            return (
                SubraceName.SATYR_SATYR_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.SATYR_SATYR_MYTHICODYSSEYSOFTHEROS,
            )
        case Race.LEONIN:
            return (SubraceName.LEONIN_LEONIN_LEONINFEATURES,)
        case Race.VERDAN:
            return (SubraceName.VERDAN_VERDAN_PLAYERSHANDBOOK,)
        case Race.GRUNG:
            return (SubraceName.GRUNG_GRUNG_PLAYERSHANDBOOK,)
        case Race.KALASHTAR:
            return (
                SubraceName.KALASHTAR_KALASHTAR_EBERRONRISINGFROMTHELASTWAR,
                SubraceName.KALASHTAR_KALASHTAR_UNEARTHEDARCANA,
            )
        case Race.YUAN_TI_PUREBLOOD:
            return (
                SubraceName.YUAN_TI_PUREBLOOD_MORDENKAINENPRESENTSMONSTERSOFTHEMULTIVERSE,
                SubraceName.YUAN_TI_PUREBLOOD_VOLOSGUIDETOMONSTERS,
            )
        case _ as never:
            assert_never(never)
