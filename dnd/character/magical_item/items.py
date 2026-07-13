from dnd.character.armor.names import ArmorName
from dnd.character.magical_item.item import MagicalItem
from dnd.character.magical_item.level import Level
from dnd.character.magical_item.source import Source
from dnd.character.magical_item.specialized_items import (
    ACAndSavingThrowBonusItem,
)
from dnd.character.magical_item.specialized_items import (
    ACBonusItem,
)
from dnd.character.magical_item.specialized_items import (
    SavingThrowBonusItem,
)
from dnd.character.magical_item.specialized_items import (
    StatAndCapBoostItem,
)
from dnd.character.magical_item.specialized_items import (
    StatBoostItem,
)
from dnd.character.magical_item.specialized_items import (
    StatSettingItem,
)
from dnd.character.magical_item.specialized_items.robe_of_archmagi import (
    RobeOfTheArchmagi,
)
from dnd.choices.stats_creation.statistic import Statistic

# Stat-setting items
amulet_of_health = StatSettingItem(
    name="Amulet of Health",
    description="Your Constitution score is 19 while you wear this amulet. It has no effect on you if your Constitution is already 19 or higher without it.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.CONSTITUTION,
    stat_value=19,
)

gauntlets_of_ogre_power = StatSettingItem(
    name="Gauntlets of Ogre Power",
    description="Your Strength score is 19 while you wear these gauntlets. They have no effect on you if your Strength is already 19 or higher without them.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.STRENGTH,
    stat_value=19,
)

headband_of_intellect = StatSettingItem(
    name="Headband of Intellect",
    description="Your Intelligence score is 19 while you wear this headband. It has no effect on you if your Intelligence is already 19 or higher without it.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.INTELLIGENCE,
    stat_value=19,
)

# Belt of Giant Strength variants
belt_of_hill_giant_strength = StatSettingItem(
    name="Belt of Hill Giant Strength",
    description="Your Strength score is 21 while you wear this belt. It has no effect on you if your Strength is already 21 or higher without it.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.STRENGTH,
    stat_value=21,
)

belt_of_stone_giant_strength = StatSettingItem(
    name="Belt of Stone Giant Strength",
    description="Your Strength score is 23 while you wear this belt. It has no effect on you if your Strength is already 23 or higher without it.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.STRENGTH,
    stat_value=23,
)

belt_of_frost_giant_strength = StatSettingItem(
    name="Belt of Frost Giant Strength",
    description="Your Strength score is 23 while you wear this belt. It has no effect on you if your Strength is already 23 or higher without it.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.STRENGTH,
    stat_value=23,
)

belt_of_fire_giant_strength = StatSettingItem(
    name="Belt of Fire Giant Strength",
    description="Your Strength score is 25 while you wear this belt. It has no effect on you if your Strength is already 25 or higher without it.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.STRENGTH,
    stat_value=25,
)

belt_of_cloud_giant_strength = StatSettingItem(
    name="Belt of Cloud Giant Strength",
    description="Your Strength score is 27 while you wear this belt. It has no effect on you if your Strength is already 27 or higher without it.",
    level=Level.LEGENDARY,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.STRENGTH,
    stat_value=27,
)

belt_of_storm_giant_strength = StatSettingItem(
    name="Belt of Storm Giant Strength",
    description="Your Strength score is 29 while you wear this belt. It has no effect on you if your Strength is already 29 or higher without it.",
    level=Level.LEGENDARY,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.STRENGTH,
    stat_value=29,
)

# AC + Saving Throw bonus items
cloak_of_protection = ACAndSavingThrowBonusItem(
    name="Cloak of Protection",
    description="You gain a +1 bonus to AC and saving throws while you wear this cloak.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
    ac_bonus=1,
    saving_throw_bonus=1,
)

ring_of_protection = ACAndSavingThrowBonusItem(
    name="Ring of Protection",
    description="You gain a +1 bonus to AC and saving throws while wearing this ring.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
    ac_bonus=1,
    saving_throw_bonus=1,
)

# AC bonus only items
bracers_of_defense = ACBonusItem(
    name="Bracers of Defense",
    description="While wearing these bracers, you gain a +2 bonus to AC if you are wearing no armor and using no shield.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
    ac_bonus=2,
)

# Utility items (no blueprint modification - base MagicalItem class)
bag_of_holding = MagicalItem(
    name="Bag of Holding",
    description="This bag has an interior space considerably larger than its outside dimensions, roughly 2 feet in diameter at the mouth and 4 feet deep. The bag can hold up to 500 pounds, not exceeding a volume of 64 cubic feet. The bag weighs 15 pounds, regardless of its contents.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=False,
)

boots_of_speed = MagicalItem(
    name="Boots of Speed",
    description="While you wear these boots, you can use a bonus action and click the boots' heels together. If you do, the boots double your walking speed, and any creature that makes an opportunity attack against you has disadvantage on the attack roll. If you click your heels together again, you end the effect.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

boots_of_levitation = MagicalItem(
    name="Boots of Levitation",
    description="While you wear these boots, you can use an action to cast the levitate spell on yourself at will.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

boots_of_striding_and_springing = MagicalItem(
    name="Boots of Striding and Springing",
    description="While you wear these boots, your walking speed becomes 30 feet, unless your walking speed is higher, and your speed isn't reduced if you are encumbered or wearing heavy armor. In addition, you can jump three times the normal distance, though you can't jump farther than your remaining movement would allow.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

cloak_of_elvenkind = MagicalItem(
    name="Cloak of Elvenkind",
    description="While you wear this cloak with its hood up, Wisdom (Perception) checks made to see you have disadvantage, and you have advantage on Dexterity (Stealth) checks made to hide, as the cloak's color shifts to camouflage you.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

periapt_of_health = MagicalItem(
    name="Periapt of Health",
    description="You are immune to contracting any disease while you wear this pendant. If you are already infected with a disease, the effects of the disease are suppressed you while you wear the pendant.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=False,
)

ring_of_evasion = MagicalItem(
    name="Ring of Evasion",
    description="This ring has 3 charges, and it regains 1d3 expended charges daily at dawn. When you fail a Dexterity saving throw while wearing it, you can use your reaction to expend 1 of its charges to succeed on that saving throw instead.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

gloves_of_thievery = MagicalItem(
    name="Gloves of Thievery",
    description="These gloves are invisible while worn. While wearing them, you gain a +5 bonus to Dexterity (Sleight of Hand) checks and Dexterity checks made to pick locks.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=False,
)

eyes_of_the_eagle = MagicalItem(
    name="Eyes of the Eagle",
    description="These crystal lenses fit over the eyes. While wearing them, you have advantage on Wisdom (Perception) checks that rely on sight. In conditions of clear visibility, you can make out details of even extremely distant creatures and objects as small as 2 feet across.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

slippers_of_spider_climbing = MagicalItem(
    name="Slippers of Spider Climbing",
    description="While you wear these light shoes, you can move up, down, and across vertical surfaces and upside down along ceilings, while leaving your hands free. You have a climbing speed equal to your walking speed. However, the slippers don't allow you to move this way on a slippery surface, such as one covered by ice or oil.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

gloves_of_missile_snaring = MagicalItem(
    name="Gloves of Missile Snaring",
    description="These gloves seem to almost meld into your hands when you don them. When a ranged weapon attack hits you while you're wearing them, you can use your reaction to reduce the damage by 1d10 + your Dexterity modifier, provided that you have a free hand. If you reduce the damage to 0, you can catch the missile if it is small enough for you to hold in that hand.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

cloak_of_the_bat = MagicalItem(
    name="Cloak of the Bat",
    description="While wearing this cloak, you have advantage on Dexterity (Stealth) checks. In an area of dim light or darkness, you can grip the edges of the cloak with both hands and use it to fly at a speed of 40 feet. If you ever fail to grip the cloak's edges while flying in this way, or if you are no longer in dim light or darkness, you lose this flying speed. While wearing the cloak in an area of dim light or darkness, you can use your action to cast polymorph on yourself, transforming into a bat. While you are in the form of the bat, you retain your Intelligence, Wisdom, and Charisma scores. The cloak can't be used this way again until the next dawn.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

amulet_of_proof_against_detection_and_location = MagicalItem(
    name="Amulet of Proof Against Detection and Location",
    description="While wearing this amulet, you are hidden from divination magic. You can't be targeted by such magic or perceived through magical scrying sensors.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

cape_of_the_mountebank = MagicalItem(
    name="Cape of the Mountebank",
    description="This cape smells faintly of brimstone. While wearing it, you can use it to cast the dimension door spell as an action. This property of the cape can't be used again until the next dawn. When you disappear, you leave behind a cloud of smoke, and you appear in a similar cloud of smoke at your destination. The smoke lightly obscures the space you left and the space you appear in, and it dissipates at the end of your next turn. A light or stronger wind disperses the smoke.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=False,
)

wings_of_flying = MagicalItem(
    name="Wings of Flying",
    description="While wearing this cloak, you can speak its command word as an action to turn the cloak into a pair of bat wings or bird wings on your back for 1 hour or until you repeat the command word as an action. The wings give you a flying speed of 60 feet. When they disappear, you can't use them again for 1d12 hours.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

immovable_rod = MagicalItem(
    name="Immovable Rod",
    description="This flat iron rod has a button on one end. You can use an action to press the button, which causes the rod to become magically fixed in place. Until you or another creature uses an action to push the button again, the rod doesn't move, even if it is defying gravity. The rod can hold up to 8,000 pounds of weight. More weight causes the rod to deactivate and fall. A creature can use an action to make a DC 30 Strength check, moving the fixed rod up to 10 feet on a success.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=False,
)

portable_hole = MagicalItem(
    name="Portable Hole",
    description="This fine black cloth, soft as silk, is folded up to the dimensions of a handkerchief. It unfolds into a circular sheet 6 feet in diameter. You can use an action to unfold a portable hole and place it on or against a solid surface, whereupon the portable hole creates an extradimensional hole 10 feet deep. The cylindrical space within the hole exists on a different plane, so it can't be used to create open passages. Any creature inside an open portable hole can exit the hole by climbing out of it. You can use an action to close a portable hole by taking hold of the edges of the cloth and folding it up. Folding the cloth closes the hole, and any creatures or objects within remain in the extradimensional space. No matter what's in it, the hole weighs next to nothing.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=False,
)

helm_of_telepathy = MagicalItem(
    name="Helm of Telepathy",
    description="While wearing this helm, you can use an action to cast the detect thoughts spell (save DC 13) from it. As long as you maintain concentration on the spell, you can use a bonus action to send a telepathic message to a creature you are focused on. It can reply—using a bonus action—while your focus on it continues. While focusing on a creature with detect thoughts, you can use an action to cast the suggestion spell (save DC 13) from the helm on that creature. Once used, the suggestion property can't be used again until the next dawn.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

ring_of_mind_shielding = MagicalItem(
    name="Ring of Mind Shielding",
    description="While wearing this ring, you are immune to magic that allows other creatures to read your thoughts, determine whether you are lying, know your alignment, or know your creature type. Creatures can telepathically communicate with you only if you allow it. You can use an action to cause the ring to become invisible until you use another action to make it visible, until you remove the ring, or until you die. If you die while wearing the ring, your soul enters it, unless it already houses a soul. You can remain in the ring or depart for the afterlife. As long as your soul is in the ring, you can telepathically communicate with any creature wearing it. A wearer can't prevent this telepathic communication.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

boots_of_elvenkind = MagicalItem(
    name="Boots of Elvenkind",
    description="While you wear these boots, your steps make no sound, regardless of the surface you are moving across. You also have advantage on Dexterity (Stealth) checks that rely on moving silently.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=False,
)

ring_of_free_action = MagicalItem(
    name="Ring of Free Action",
    description="While you wear this ring, difficult terrain doesn't cost you extra movement. In addition, magic can neither reduce your speed nor cause you to be paralyzed or restrained.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

ring_of_water_walking = MagicalItem(
    name="Ring of Water Walking",
    description="While wearing this ring, you can stand on and move across any liquid surface as if it were solid ground.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=False,
)

necklace_of_adaptation = MagicalItem(
    name="Necklace of Adaptation",
    description="While wearing this necklace, you can breathe normally in any environment, and you have advantage on saving throws made against harmful gases and vapors (such as cloudkill and stinking cloud effects, inhaled poisons, and the breath weapons of some dragons).",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

periapt_of_wound_closure = MagicalItem(
    name="Periapt of Wound Closure",
    description="While you wear this pendant, you stabilize whenever you are dying at the start of your turn. In addition, whenever you roll a Hit Die to regain hit points, double the number of hit points it restores.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

goggles_of_night = MagicalItem(
    name="Goggles of Night",
    description="While wearing these dark lenses, you have darkvision out to a range of 60 feet. If you already have darkvision, wearing the goggles increases its range by 60 feet.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=False,
)

rope_of_entanglement = MagicalItem(
    name="Rope of Entanglement",
    description="This rope is 30 feet long and weighs 3 pounds. If you hold one end of the rope and use an action to speak its command word, the other end darts forward to entangle a creature you can see within 20 feet of you. The target must succeed on a DC 15 Dexterity saving throw or become restrained. You can release the creature by using a bonus action to speak a second command word. A target restrained by the rope can use an action to make a DC 15 Strength or Dexterity check (target's choice). On a success, the creature is no longer restrained by the rope. The rope has AC 20 and 20 hit points. It regains 1 hit point every 5 minutes as long as it has at least 1 hit point. If the rope drops to 0 hit points, it is destroyed.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=False,
)

# Ioun Stones - stat boosting (Very Rare, +2 to stat, max 20)
ioun_stone_agility = StatBoostItem(
    name="Ioun Stone (Agility)",
    description="This deep red sphere increases your Dexterity score by 2, to a maximum of 20, while this stone orbits your head.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.DEXTERITY,
    boost_amount=2,
    max_value=20,
)

ioun_stone_fortitude = StatBoostItem(
    name="Ioun Stone (Fortitude)",
    description="This pink rhomboid increases your Constitution score by 2, to a maximum of 20, while this stone orbits your head.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.CONSTITUTION,
    boost_amount=2,
    max_value=20,
)

ioun_stone_insight = StatBoostItem(
    name="Ioun Stone (Insight)",
    description="This incandescent blue sphere increases your Wisdom score by 2, to a maximum of 20, while this stone orbits your head.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.WISDOM,
    boost_amount=2,
    max_value=20,
)

ioun_stone_intellect = StatBoostItem(
    name="Ioun Stone (Intellect)",
    description="This marbled scarlet and blue sphere increases your Intelligence score by 2, to a maximum of 20, while this stone orbits your head.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.INTELLIGENCE,
    boost_amount=2,
    max_value=20,
)

ioun_stone_leadership = StatBoostItem(
    name="Ioun Stone (Leadership)",
    description="This marbled pink and green sphere increases your Charisma score by 2, to a maximum of 20, while this stone orbits your head.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.CHARISMA,
    boost_amount=2,
    max_value=20,
)

ioun_stone_strength = StatBoostItem(
    name="Ioun Stone (Strength)",
    description="This pale blue rhomboid increases your Strength score by 2, to a maximum of 20, while this stone orbits your head.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    stat=Statistic.STRENGTH,
    boost_amount=2,
    max_value=20,
)

# Ioun Stone - AC bonus (Rare)
ioun_stone_protection = ACBonusItem(
    name="Ioun Stone (Protection)",
    description="This dusty rose prism grants you a +1 bonus to AC while this stone orbits your head.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
    ac_bonus=1,
)

# High-tier utility items
decanter_of_endless_water = MagicalItem(
    name="Decanter of Endless Water",
    description="This stoppered flask sloshes when shaken, as if it contains water. You can use an action to remove the stopper and speak one of three command words. Choose from 'Stream' (1 gallon), 'Fountain' (5 gallons), or 'Geyser' (30-foot gush that can push creatures/objects). The water stops pouring at the start of your next turn.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=False,
)

mantle_of_spell_resistance = MagicalItem(
    name="Mantle of Spell Resistance",
    description="You have advantage on saving throws against spells while you wear this cloak.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

ring_of_spell_storing = MagicalItem(
    name="Ring of Spell Storing",
    description="This ring stores spells cast into it, holding them until the attuned wearer uses them. The ring can store up to 5 levels worth of spells at a time. Any creature can cast a spell of 1st through 5th level into the ring. The spell uses the original caster's slot level, DC, attack bonus, and spellcasting ability.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

ring_of_spell_turning = MagicalItem(
    name="Ring of Spell Turning",
    description="You have advantage on saving throws against any spell that targets only you. If you roll a 20 for the save and the spell is 7th level or lower, the spell has no effect on you and instead targets the caster.",
    level=Level.LEGENDARY,
    source=Source.DMG,
    attuned=True,
)

robe_of_the_archmagi = RobeOfTheArchmagi(
    name=ArmorName.ROBE_OF_THE_ARCHMAGI,
    description="This elegant robe grants powerful benefits to spellcasters: If you aren't wearing armor, your base AC is 15 + your Dexterity modifier. You have advantage on saving throws against spells and magical effects. Your spell save DC and spell attack bonus each increase by 2. Requires attunement by a sorcerer, warlock, or wizard.",
    level=Level.LEGENDARY,
    source=Source.DMG,
    attuned=True,
)

# Tomes - Stat and cap boosting (Very Rare, +2 to stat AND +2 to max)
tome_of_clear_thought = StatAndCapBoostItem(
    name="Tome of Clear Thought",
    description="This book contains memory and logic exercises, and its words are charged with magic. If you spend 48 hours over a period of 6 days or fewer studying the book's contents and practicing its guidelines, your Intelligence score increases by 2, as does your maximum for that score. The manual then loses its magic, but regains it in a century.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=False,
    stat=Statistic.INTELLIGENCE,
    boost_amount=2,
)

tome_of_leadership_and_influence = StatAndCapBoostItem(
    name="Tome of Leadership and Influence",
    description="This book contains guidelines for influencing and charming others, and its words are charged with magic. If you spend 48 hours over a period of 6 days or fewer studying the book's contents and practicing its guidelines, your Charisma score increases by 2, as does your maximum for that score. The manual then loses its magic, but regains it in a century.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=False,
    stat=Statistic.CHARISMA,
    boost_amount=2,
)

tome_of_understanding = StatAndCapBoostItem(
    name="Tome of Understanding",
    description="This book contains intuition and insight exercises, and its words are charged with magic. If you spend 48 hours over a period of 6 days or fewer studying the book's contents and practicing its guidelines, your Wisdom score increases by 2, as does your maximum for that score. The manual then loses its magic, but regains it in a century.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=False,
    stat=Statistic.WISDOM,
    boost_amount=2,
)

# Spell utility items
pearl_of_power = MagicalItem(
    name="Pearl of Power",
    description="While this pearl is on your person, you can use an action to speak its command word and regain one expended spell slot. If the expended slot was of 4th level or higher, the new slot is 3rd level. Once you use the pearl, it can't be used again until the next dawn.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

# Legendary protection items
scarab_of_protection = SavingThrowBonusItem(
    name="Scarab of Protection",
    description="If you hold this beetle-shaped medallion in your hand for 1 round, an inscription appears on its surface revealing its magical nature. It provides two benefits: 1) You have advantage on saving throws against spells. 2) The scarab has 12 charges. If you fail a saving throw against a necromancy spell or a harmful effect originating from an undead creature, you can use your reaction to expend 1 charge and turn the failed save into a successful one. The scarab crumbles into powder and is destroyed when its last charge is expended.",
    level=Level.LEGENDARY,
    source=Source.DMG,
    attuned=True,
    saving_throw_bonus=0,  # The advantage is not a numeric bonus, but effect is complex
)

# Additional high-value items
cube_of_force = MagicalItem(
    name="Cube of Force",
    description="This cube is about an inch across. Each face has a distinct marking on it that can be pressed. The cube starts with 36 charges, and it regains 1d20 expended charges daily at dawn. You can use an action to press one of the cube's faces, expending a number of charges based on the chosen face. Each face has a different effect. The barrier is centered on you, moves with you, and lasts for 1 minute, until you use an action to press the cube's sixth face, or the cube runs out of charges.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

robe_of_stars = SavingThrowBonusItem(
    name="Robe of Stars",
    description="This black or dark blue robe is embroidered with small white or silver stars. You gain a +1 bonus to saving throws while you wear it. Six stars, located on the robe's upper front portion, are particularly large. While wearing this robe, you can use an action to pull off one of the stars and use it to cast magic missile as a 5th-level spell. Daily at dusk, 1d6 removed stars reappear on the robe. While you wear the robe, you can use an action to enter the Astral Plane along with everything you are wearing and carrying. You remain there until you use an action to return to the plane you were on. You reappear in the last space you occupied, or if that space is occupied, the nearest unoccupied space.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
    saving_throw_bonus=1,
)

ring_of_regeneration = MagicalItem(
    name="Ring of Regeneration",
    description="While wearing this ring, you regain 1d6 hit points every 10 minutes, provided that you have at least 1 hit point. If you lose a body part, the ring causes the missing part to regrow and return to full functionality after 1d6 + 1 days if you have at least 1 hit point the whole time.",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=True,
)

ring_of_invisibility = MagicalItem(
    name="Ring of Invisibility",
    description="While wearing this ring, you can turn invisible as an action. Anything you are wearing or carrying is invisible with you. You remain invisible until the ring is removed, until you attack or cast a spell, or until you use a bonus action to become visible again.",
    level=Level.LEGENDARY,
    source=Source.DMG,
    attuned=True,
)

boots_of_the_winterlands = MagicalItem(
    name="Boots of the Winterlands",
    description="These furred boots are snug and feel quite warm. While you wear them, you gain the following benefits: You have resistance to cold damage. You ignore difficult terrain created by ice or snow. You can tolerate temperatures as low as -50 degrees Fahrenheit without any additional protection. If you wear heavy clothes, you can tolerate temperatures as low as -100 degrees Fahrenheit.",
    level=Level.UNCOMMON,
    source=Source.DMG,
    attuned=True,
)

carpet_of_flying = MagicalItem(
    name="Carpet of Flying",
    description="You can speak the carpet's command word as an action to make the carpet hover and fly. It moves according to your spoken directions, provided that you are within 30 feet of it. Four sizes of carpet of flying exist. The DM chooses the size of a given carpet or determines it randomly. A carpet can carry up to twice the weight shown on the table, but it flies at half speed if it carries more than its normal capacity. Typical sizes: 3x5 ft (200 lb, 80 ft speed), 4x6 ft (400 lb, 60 ft speed), 5x7 ft (600 lb, 40 ft speed), 6x9 ft (800 lb, 30 ft speed).",
    level=Level.VERY_RARE,
    source=Source.DMG,
    attuned=False,
)

cloak_of_displacement = MagicalItem(
    name="Cloak of Displacement",
    description="While you wear this cloak, it projects an illusion that makes you appear to be standing in a place near your actual location, causing any creature to have disadvantage on attack rolls against you. If you take damage, the property ceases to function until the start of your next turn. This property is suppressed while you are incapacitated, restrained, or otherwise unable to move.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

ring_of_x_ray_vision = MagicalItem(
    name="Ring of X-Ray Vision",
    description="While wearing this ring, you can use an action to speak its command word. When you do so, you can see into and through solid matter for 1 minute. This vision has a radius of 30 feet. To you, solid objects within that radius appear transparent and don't prevent light from passing through them. The vision can penetrate 1 foot of stone, 1 inch of common metal, or up to 3 feet of wood or dirt. Thicker substances block the vision, as does a thin sheet of lead. Whenever you use the ring again before taking a long rest, you must succeed on a DC 15 Constitution saving throw or gain one level of exhaustion.",
    level=Level.RARE,
    source=Source.DMG,
    attuned=True,
)

MAGICAL_ITEMS: tuple[MagicalItem, ...] = (
    # Stat-setting items (sets stat to fixed value)
    amulet_of_health,
    gauntlets_of_ogre_power,
    headband_of_intellect,
    belt_of_hill_giant_strength,
    belt_of_stone_giant_strength,
    belt_of_frost_giant_strength,
    belt_of_fire_giant_strength,
    belt_of_cloud_giant_strength,
    belt_of_storm_giant_strength,
    # Stat-boosting items (adds to stat with cap)
    ioun_stone_agility,
    ioun_stone_fortitude,
    ioun_stone_insight,
    ioun_stone_intellect,
    ioun_stone_leadership,
    ioun_stone_strength,
    # Stat and cap boosting items (increases stat AND maximum)
    tome_of_clear_thought,
    tome_of_leadership_and_influence,
    tome_of_understanding,
    # AC and/or saving throw bonuses
    cloak_of_protection,
    ring_of_protection,
    bracers_of_defense,
    ioun_stone_protection,
    # Movement and mobility
    boots_of_speed,
    boots_of_levitation,
    boots_of_striding_and_springing,
    slippers_of_spider_climbing,
    wings_of_flying,
    ring_of_free_action,
    ring_of_water_walking,
    carpet_of_flying,
    boots_of_the_winterlands,
    # Stealth and utility
    cloak_of_elvenkind,
    cloak_of_the_bat,
    cape_of_the_mountebank,
    gloves_of_thievery,
    boots_of_elvenkind,
    cloak_of_displacement,
    # Perception and senses
    eyes_of_the_eagle,
    goggles_of_night,
    ring_of_x_ray_vision,
    # Mental and psychic
    helm_of_telepathy,
    ring_of_mind_shielding,
    # Spell-related
    mantle_of_spell_resistance,
    ring_of_spell_storing,
    ring_of_spell_turning,
    robe_of_the_archmagi,
    pearl_of_power,
    # Protection and defense
    gloves_of_missile_snaring,
    ring_of_evasion,
    amulet_of_proof_against_detection_and_location,
    periapt_of_health,
    periapt_of_wound_closure,
    necklace_of_adaptation,
    scarab_of_protection,
    cube_of_force,
    robe_of_stars,
    ring_of_regeneration,
    # Storage and utility
    bag_of_holding,
    portable_hole,
    immovable_rod,
    rope_of_entanglement,
    decanter_of_endless_water,
    # Special abilities
    ring_of_invisibility,
)
