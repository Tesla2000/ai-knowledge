from __future__ import annotations

from enum import IntEnum, auto
from enum import StrEnum

from dnd.choices.equipment_creation.item import Item


class HitDieSize(IntEnum):
    ONE = 1
    FOUR = 4
    SIX = 6
    EIGHT = 8
    TEN = 10
    TWELVE = 12


class DamageType(StrEnum):
    BLUDGEONING = auto()
    PIERCING = auto()
    SLASHING = auto()


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


class Weapon(Item):
    name: WeaponName
    damage_type: DamageType | None
    base_hit_die: HitDieSize | None
    two_dies: bool = False
    is_martial: bool = False
    is_ammunition: bool = False
    is_finesse: bool = False
    is_heavy: bool = False
    is_light: bool = False
    is_range: bool = False
    is_reach: bool = False
    is_special: bool = False
    is_thrown: bool = False
    is_two_handed: bool = False
    is_versatile: bool = False

    # def get_attack_bonus(
    #     self, character_wrapper: "CharacterWrapper"
    # ) -> SignedInt:
    #     proficient = character_wrapper.is_proficient_with(self)
    #     return (
    #         self._get_raw_bonus(character_wrapper)
    #         + character_wrapper.proficiency_bonus * proficient
    #     )
    #
    # def get_damage_bonus(
    #     self, character_wrapper: "CharacterWrapper"
    # ) -> SignedInt:
    #     return self._get_raw_bonus(character_wrapper)
    #
    # def get_damage_die(self, character_wrapper: "CharacterWrapper"):
    #     return self.base_hit_die.value + 2 * (
    #         self.is_versatile and not character_wrapper.character.uses_shield
    #     )
    #
    # def get_damage(self, character_wrapper: "CharacterWrapper") -> str:
    #     if self.base_hit_die and self.damage_type:
    #         return (
    #             f"{1 + self.two_dies}d"
    #             f"{self.get_damage_die(character_wrapper)}"
    #             f"{self.get_damage_bonus(character_wrapper)} / "
    #             f"{self.damage_type.value[:1]}"
    #         )
    #     return ""
    #
    # def _get_raw_bonus(
    #     self, character_wrapper: "CharacterWrapper"
    # ) -> SignedInt:
    #     if self.is_finesse:
    #         bonus = max(
    #             character_wrapper.modifiers[Statistic.STRENGTH],
    #             character_wrapper.modifiers[Statistic.DEXTERITY],
    #         )
    #     elif self.is_range:
    #         bonus = character_wrapper.modifiers[Statistic.DEXTERITY]
    #     else:
    #         bonus = character_wrapper.modifiers[Statistic.STRENGTH]
    #     return SignedInt(bonus)


weapon_list = [
    Weapon(
        name=WeaponName.CLUB,
        damage_type=DamageType.BLUDGEONING,
        base_hit_die=HitDieSize.FOUR,
        is_light=True,
        cost=1,
        weight=2,
    ),
    Weapon(
        name=WeaponName.DAGGER,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.FOUR,
        is_finesse=True,
        is_light=True,
        is_thrown=True,
        is_range=True,
        cost=2,
        weight=1,
    ),
    Weapon(
        name=WeaponName.GREATCLUB,
        damage_type=DamageType.BLUDGEONING,
        base_hit_die=HitDieSize.EIGHT,
        is_two_handed=True,
        cost=2,
        weight=10,
    ),
    Weapon(
        name=WeaponName.HANDAXE,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.SIX,
        is_light=True,
        is_thrown=True,
        is_range=True,
        cost=5,
        weight=2,
    ),
    Weapon(
        name=WeaponName.JAVELIN,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.SIX,
        is_thrown=True,
        is_range=True,
        cost=0.5,
        weight=2,
    ),
    Weapon(
        name=WeaponName.LIGHT_HAMMER,
        damage_type=DamageType.BLUDGEONING,
        base_hit_die=HitDieSize.FOUR,
        is_light=True,
        is_thrown=True,
        is_range=True,
        cost=2,
        weight=2,
    ),
    Weapon(
        name=WeaponName.MACE,
        damage_type=DamageType.BLUDGEONING,
        base_hit_die=HitDieSize.SIX,
        cost=5,
        weight=4,
    ),
    Weapon(
        name=WeaponName.QUARTERSTAFF,
        damage_type=DamageType.BLUDGEONING,
        base_hit_die=HitDieSize.SIX,
        is_versatile=True,
        cost=2,
        weight=4,
    ),
    Weapon(
        name=WeaponName.SICKLE,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.FOUR,
        is_light=True,
        cost=1,
        weight=2,
    ),
    Weapon(
        name=WeaponName.SPEAR,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.SIX,
        is_thrown=True,
        is_range=True,
        is_versatile=True,
        cost=1,
        weight=3,
    ),
    Weapon(
        name=WeaponName.CROSSBOW_LIGHT,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.EIGHT,
        is_range=True,
        is_two_handed=True,
        cost=25,
        weight=5,
    ),
    Weapon(
        name=WeaponName.DART,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.FOUR,
        is_finesse=True,
        is_thrown=True,
        is_range=True,
        cost=0.05,
        weight=0.25,
    ),
    Weapon(
        name=WeaponName.SHORTBOW,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.SIX,
        is_range=True,
        is_two_handed=True,
        cost=25,
        weight=2,
    ),
    Weapon(
        name=WeaponName.SLING,
        damage_type=DamageType.BLUDGEONING,
        base_hit_die=HitDieSize.FOUR,
        is_range=True,
        cost=0.1,
        weight=0,
    ),
    Weapon(
        name=WeaponName.BATTLEAXE,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.EIGHT,
        is_martial=True,
        is_versatile=True,
        cost=10,
        weight=4,
    ),
    Weapon(
        name=WeaponName.FLAIL,
        damage_type=DamageType.BLUDGEONING,
        base_hit_die=HitDieSize.EIGHT,
        is_martial=True,
        cost=10,
        weight=2,
    ),
    Weapon(
        name=WeaponName.GLAIVE,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.TEN,
        is_martial=True,
        is_heavy=True,
        is_reach=True,
        is_two_handed=True,
        cost=20,
        weight=6,
    ),
    Weapon(
        name=WeaponName.GREATAXE,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.TWELVE,
        is_martial=True,
        is_heavy=True,
        is_two_handed=True,
        cost=30,
        weight=7,
    ),
    Weapon(
        name=WeaponName.GREATSWORD,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.SIX,
        two_dies=True,
        is_martial=True,
        is_heavy=True,
        is_two_handed=True,
        cost=50,
        weight=6,
    ),
    Weapon(
        name=WeaponName.HALBERD,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.TEN,
        is_martial=True,
        is_heavy=True,
        is_reach=True,
        is_two_handed=True,
        cost=20,
        weight=6,
    ),
    Weapon(
        name=WeaponName.LANCE,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.TWELVE,
        is_martial=True,
        is_reach=True,
        is_special=True,
        cost=10,
        weight=6,
    ),
    Weapon(
        name=WeaponName.LONGSWORD,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.EIGHT,
        is_martial=True,
        is_versatile=True,
        cost=15,
        weight=3,
    ),
    Weapon(
        name=WeaponName.MAUL,
        damage_type=DamageType.BLUDGEONING,
        base_hit_die=HitDieSize.SIX,
        two_dies=True,
        is_martial=True,
        is_heavy=True,
        is_two_handed=True,
        cost=10,
        weight=10,
    ),
    Weapon(
        name=WeaponName.MORNINGSTAR,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.EIGHT,
        is_martial=True,
        cost=15,
        weight=4,
    ),
    Weapon(
        name=WeaponName.PIKE,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.TEN,
        is_martial=True,
        is_heavy=True,
        is_reach=True,
        is_two_handed=True,
        cost=5,
        weight=18,
    ),
    Weapon(
        name=WeaponName.RAPIER,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.EIGHT,
        is_martial=True,
        is_finesse=True,
        cost=25,
        weight=2,
    ),
    Weapon(
        name=WeaponName.SCIMITAR,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.SIX,
        is_martial=True,
        is_finesse=True,
        is_light=True,
        cost=25,
        weight=3,
    ),
    Weapon(
        name=WeaponName.SHORTSWORD,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.SIX,
        is_martial=True,
        is_finesse=True,
        is_light=True,
        cost=10,
        weight=2,
    ),
    Weapon(
        name=WeaponName.TRIDENT,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.SIX,
        is_martial=True,
        is_thrown=True,
        is_range=True,
        is_versatile=True,
        cost=5,
        weight=4,
    ),
    Weapon(
        name=WeaponName.WAR_PICK,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.EIGHT,
        is_martial=True,
        cost=5,
        weight=2,
    ),
    Weapon(
        name=WeaponName.WARHAMMER,
        damage_type=DamageType.BLUDGEONING,
        base_hit_die=HitDieSize.EIGHT,
        is_martial=True,
        is_versatile=True,
        cost=15,
        weight=2,
    ),
    Weapon(
        name=WeaponName.WHIP,
        damage_type=DamageType.SLASHING,
        base_hit_die=HitDieSize.FOUR,
        is_martial=True,
        is_finesse=True,
        is_reach=True,
        cost=2,
        weight=3,
    ),
    # Martial Ranged Weapons
    Weapon(
        name=WeaponName.BLOWGUN,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.ONE,
        is_martial=True,
        is_ammunition=True,
        is_range=True,
        cost=10,
        weight=1,
    ),
    Weapon(
        name=WeaponName.CROSSBOW_HAND,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.SIX,
        is_martial=True,
        is_ammunition=True,
        is_range=True,
        is_light=True,
        cost=75,
        weight=3,
    ),
    Weapon(
        name=WeaponName.CROSSBOW_HEAVY,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.TEN,
        is_martial=True,
        is_ammunition=True,
        is_range=True,
        is_heavy=True,
        is_two_handed=True,
        cost=50,
        weight=18,
    ),
    Weapon(
        name=WeaponName.LONGBOW,
        damage_type=DamageType.PIERCING,
        base_hit_die=HitDieSize.EIGHT,
        is_martial=True,
        is_ammunition=True,
        is_range=True,
        is_heavy=True,
        is_two_handed=True,
        cost=50,
        weight=2,
    ),
    Weapon(
        name=WeaponName.NET,
        damage_type=None,
        base_hit_die=None,
        is_martial=True,
        is_special=True,
        is_thrown=True,
        is_range=True,
        cost=1,
        weight=3,
    ),
]
