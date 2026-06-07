from __future__ import annotations

from enum import Enum


class DNDResource(str, Enum):
    SPELLJAMMER_ADVENTURES_IN_SPACE = "SpelljammerAdventuresinSpace"
    MYTHIC_ODYSSEYS_OF_THEROS = "MythicOdysseysofTheros"
    ELEMENTAL_EVIL_PLAYERS_COMPANION = "ElementalEvilPlayersCompanion"
    PLANE_SHIFT_KALAADESH = "PlaneShiftKaladesh"
    MORDENKAINEN_PRESENTS_MONSTERS_OF_THE_MULTIVERSE = (
        "MordenkainenPresentsMonstersoftheMultiverse"
    )
    ELEMENTAL_EVIL_PLAYERS_GUIDE = "ElementalEvilPlayersGuide"
    ADVENTURES_WITH_MUK_DANKWOOD = "AdventureswithMukDankwood"
    THE_TORTLE_PACKAGE = "TheTortlePackage"
    VOLOS_GUIDE_TO_MONSTERS = "VolosGuidetoMonsters"
    MORDENKAINENS_TOME_OF_FOES = "MordenkainensTomeofFoes"
    SWORD_COAST_ADVENTURERS_GUIDE = "SwordCoastAdventurersGuide"
    PLANE_SHIFT_IXALAN = "PlaneShiftIxalan"
    PLANE_SHIFT_DOMINARIA = "PlaneShiftDominaria"
    EXPLORERS_GUIDE_TO_WILDEMOUNT = "ExplorersGuidetoWildemount"
    GUILDMASTERS_GUIDE_TO_RAVNICA = "GuildmastersGuidetoRavnica"
    PLANE_SHIFT_INNISTRAD = "PlaneShiftInnistrad"
    UNEARTHED_ARCANA = "UnearthedArcana"
    LEONIN_FEATURES = "LeoninFeatures"
    EBERRON_RISING_FROM_THE_LAST_WAR = "EberronRisingfromtheLastWar"
    FIZBANS_TREASURY_OF_DRAGONS = "FizbansTreasuryofDragons"
    PLAYERS_HANDBOOK = "PlayersHandbook"
    PLANE_SHIFT_ZENDIKAR = "PlaneShiftZendikar"
    TASHAS_CAULDRON_OF_EVERYTHING = "Tasha's Cauldron of Everything"
    THE_BOOK_OF_MANY_THINGS = "The Book of Many Things"
