from __future__ import annotations

from dnd.choices.class_creation.character_class import (
    Class,
)

none_caster_spell_slots = [
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
]

half_caster_spell_slots = [
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (2, 0, 0, 0, 0, 0, 0, 0, 0),
    (3, 0, 0, 0, 0, 0, 0, 0, 0),
    (3, 0, 0, 0, 0, 0, 0, 0, 0),
    (4, 2, 0, 0, 0, 0, 0, 0, 0),
    (4, 2, 0, 0, 0, 0, 0, 0, 0),
    (4, 3, 0, 0, 0, 0, 0, 0, 0),
    (4, 3, 0, 0, 0, 0, 0, 0, 0),
    (4, 3, 2, 0, 0, 0, 0, 0, 0),
    (4, 3, 2, 0, 0, 0, 0, 0, 0),
    (4, 3, 3, 0, 0, 0, 0, 0, 0),
    (4, 3, 3, 0, 0, 0, 0, 0, 0),
    (4, 3, 3, 1, 0, 0, 0, 0, 0),
    (4, 3, 3, 1, 0, 0, 0, 0, 0),
    (4, 3, 3, 2, 0, 0, 0, 0, 0),
    (4, 3, 3, 2, 0, 0, 0, 0, 0),
    (4, 3, 3, 3, 1, 0, 0, 0, 0),
    (4, 3, 3, 3, 1, 0, 0, 0, 0),
    (4, 3, 3, 3, 2, 0, 0, 0, 0),
    (4, 3, 3, 3, 2, 0, 0, 0, 0),
]

full_caster_spell_slots = [
    (2, 2, 0, 0, 0, 0, 0, 0, 0),  # 1st level
    (2, 3, 0, 0, 0, 0, 0, 0, 0),  # 2nd level
    (2, 4, 2, 0, 0, 0, 0, 0, 0),  # 3rd level
    (3, 4, 3, 0, 0, 0, 0, 0, 0),  # 4th level
    (3, 4, 3, 2, 0, 0, 0, 0, 0),  # 5th level
    (3, 4, 3, 3, 0, 0, 0, 0, 0),  # 6th level
    (3, 4, 3, 3, 1, 0, 0, 0, 0),  # 7th level
    (3, 4, 3, 3, 2, 0, 0, 0, 0),  # 8th level
    (3, 4, 3, 3, 3, 1, 0, 0, 0),  # 9th level
    (4, 4, 3, 3, 3, 2, 0, 0, 0),  # 10th level
    (4, 4, 3, 3, 3, 2, 1, 0, 0),  # 11th level
    (4, 4, 3, 3, 3, 2, 1, 0, 0),  # 12th level
    (4, 4, 3, 3, 3, 2, 1, 1, 0),  # 13th level
    (4, 4, 3, 3, 3, 2, 1, 1, 0),  # 14th level
    (4, 4, 3, 3, 3, 2, 1, 1, 1),  # 15th level
    (4, 4, 3, 3, 3, 2, 1, 1, 1),  # 16th level
    (4, 4, 3, 3, 3, 2, 1, 1, 1, 1),  # 17th level
    (4, 4, 3, 3, 3, 3, 1, 1, 1, 1),  # 18th level
    (4, 4, 3, 3, 3, 3, 2, 1, 1, 1),  # 19th level
    (4, 4, 3, 3, 3, 3, 2, 2, 1, 1),  # 20th level
]

main_class2spell_slots = {
    Class.ARTIFICER: half_caster_spell_slots,
    Class.BARD: full_caster_spell_slots,
    Class.BARBARIAN: none_caster_spell_slots,
    Class.CLERIC: full_caster_spell_slots,
    Class.DRUID: full_caster_spell_slots,
    Class.FIGHTER: none_caster_spell_slots,
    Class.MONK: none_caster_spell_slots,
    Class.PALADIN: half_caster_spell_slots,
    Class.RANGER: half_caster_spell_slots,
    Class.ROGUE: none_caster_spell_slots,
    Class.SORCERER: full_caster_spell_slots,
    Class.WARLOCK: half_caster_spell_slots,
    Class.WIZARD: full_caster_spell_slots,
}
