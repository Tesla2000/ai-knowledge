from __future__ import annotations

from enum import IntEnum
from enum import StrEnum


class HitDieSize(IntEnum):
    ONE = 1
    FOUR = 4
    SIX = 6
    EIGHT = 8
    TEN = 10
    TWELVE = 12


class WeaponName(StrEnum):
    CLUB = "Club"
    DAGGER = "Dagger"
    GREATCLUB = "Greatclub"
    HANDAXE = "Handaxe"
    JAVELIN = "Javelin"
    LIGHT_HAMMER = "Light hammer"
    MACE = "Mace"
    QUARTERSTAFF = "Quarterstaff"
    SICKLE = "Sickle"
    SPEAR = "Spear"
    CROSSBOW_LIGHT = "Crossbow, light"
    DART = "Dart"
    SHORTBOW = "Shortbow"
    SLING = "Sling"
    BATTLEAXE = "Battleaxe"
    FLAIL = "Flail"
    GLAIVE = "Glaive"
    GREATAXE = "Greataxe"
    GREATSWORD = "Greatsword"
    HALBERD = "Halberd"
    LANCE = "Lance"
    LONGSWORD = "Longsword"
    MAUL = "Maul"
    MORNINGSTAR = "Morningstar"
    PIKE = "Pike"
    RAPIER = "Rapier"
    SCIMITAR = "Scimitar"
    SHORTSWORD = "Shortsword"
    TRIDENT = "Trident"
    WAR_PICK = "War pick"
    WARHAMMER = "Warhammer"
    WHIP = "Whip"
    BLOWGUN = "Blowgun"
    CROSSBOW_HAND = "Crossbow, hand"
    CROSSBOW_HEAVY = "Crossbow, heavy"
    LONGBOW = "Longbow"
    NET = "Net"
