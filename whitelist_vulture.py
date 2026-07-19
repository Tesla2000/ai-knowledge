from dnd.character.actions.conditional_immunity_modifier._base import (
    _ConditionalImmunityModifier,
)
from dnd.character.actions.damage_resistance_modifier._base import (
    _DamageResistanceModifier,
)
from dnd.character.blueprint.building_blocks.totem_choice_resolver.base import (
    TotemChoiceResolverBase,
)
from dnd.character.blueprint.states.barbarian._info import BarbarianInfo
from dnd.character.blueprint.states.sorcerer._info import SorcererInfo
from dnd.character.spells.max_spell_levels import SpellSlots
from dnd.choices.abilities.action import AnyAction
from dnd.fight.fight_character import (
    DeadFightCharacter,
    DownedFightCharacter,
    FightCharacter,
    StabilizedFightCharacter,
)

_ConditionalImmunityModifier.get_immunities
_DamageResistanceModifier.get_resistances
TotemChoiceResolverBase.resolve
BarbarianInfo
SorcererInfo
SpellSlots.spend_level_2_slot
SpellSlots.spend_level_4_slot
SpellSlots.spend_level_5_slot
SpellSlots.spend_level_6_slot
SpellSlots.spend_level_7_slot
SpellSlots.spend_level_8_slot
SpellSlots.spend_level_9_slot
AnyAction
FightCharacter.add_condition
FightCharacter.remove_condition
FightCharacter.add_temporary_health
FightCharacter.spend_bonus_action
FightCharacter.spend_free_action
FightCharacter.heal
DownedFightCharacter.make_death_save
DownedFightCharacter.heal
StabilizedFightCharacter.heal
DeadFightCharacter.revive
