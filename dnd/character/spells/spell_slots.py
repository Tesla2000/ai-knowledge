from __future__ import annotations

from enum import auto
from enum import StrEnum
from typing import (
    Generic,
    Literal,
    Annotated,
    TypeVar,
    cast,
    get_args,
)
from collections.abc import Iterable, Sequence
from typing import assert_never

from pydantic import BaseModel, ConfigDict, PositiveInt, Field

from dnd.choices.class_creation.character_class import Class

type SpellLevel = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

type ClassSpellLevel = (
    tuple[Literal[Class.ARTIFICER], Literal[0, 1, 2, 3, 4, 5]]
    | tuple[Literal[Class.BARD], Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    | tuple[Literal[Class.CLERIC], Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    | tuple[Literal[Class.DRUID], Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    | tuple[Literal[Class.PALADIN], Literal[1, 2, 3, 4, 5]]
    | tuple[Literal[Class.RANGER], Literal[1, 2, 3, 4, 5]]
    | tuple[Literal[Class.SORCERER], Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    | tuple[Literal[Class.WARLOCK], Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    | tuple[Literal[Class.WIZARD], Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
)


class ArtificerCantrip(StrEnum):
    ACID_SPLASH = "Acid Splash"
    BOOMING_BLADE = "Booming Blade"
    CREATE_BONFIRE = "Create Bonfire"
    DANCING_LIGHTS = "Dancing Lights"
    FIRE_BOLT = "Fire Bolt"
    FROSTBITE = "Frostbite"
    GREEN_FLAME_BLADE = "Green-Flame Blade"
    GUIDANCE = "Guidance"
    LIGHT = "Light"
    LIGHTNING_LURE = "Lightning Lure"
    MAGE_HAND = "Mage Hand"
    MAGIC_STONE = "Magic Stone"
    MENDING = "Mending"
    MESSAGE = "Message"
    POISON_SPRAY = "Poison Spray"
    PRESTIDIGITATION = "Prestidigitation"
    RAY_OF_FROST = "Ray of Frost"
    RESISTANCE = "Resistance"
    SHOCKING_GRASP = "Shocking Grasp"
    SPARE_THE_DYING = "Spare the Dying"
    SWORD_BURST = "Sword Burst"
    THORN_WHIP = "Thorn Whip"
    THUNDERCLAP = "Thunderclap"


class ArtificerFirstLevel(StrEnum):
    ABSORB_ELEMENTS = "Absorb Elements"
    ALARM = "Alarm"
    CATAPULT = "Catapult"
    CURE_WOUNDS = "Cure Wounds"
    DETECT_MAGIC = "Detect Magic"
    DISGUISE_SELF = "Disguise Self"
    EXPEDITIOUS_RETREAT = "Expeditious Retreat"
    FAERIE_FIRE = "Faerie Fire"
    FALSE_LIFE = "False Life"
    FEATHER_FALL = "Feather Fall"
    GREASE = "Grease"
    IDENTIFY = "Identify"
    JUMP = "Jump"
    LONGSTRIDER = "Longstrider"
    PURIFY_FOOD_AND_DRINK = "Purify Food and Drink"
    SANCTUARY = "Sanctuary"
    SNARE = "Snare"
    TASHAS_CAUSTIC_BREW = "Tasha's Caustic Brew"


class ArtificerSecondLevel(StrEnum):
    AID = "Aid"
    AIR_BUBBLE = "Air Bubble"
    ALTER_SELF = "Alter Self"
    ARCANE_LOCK = "Arcane Lock"
    BLUR = "Blur"
    CONTINUAL_FLAME = "Continual Flame"
    DARKVISION = "Darkvision"
    ENHANCE_ABILITY = "Enhance Ability"
    ENLARGE_REDUCE = "Enlarge-Reduce"
    HEAT_METAL = "Heat Metal"
    INVISIBILITY = "Invisibility"
    KINETIC_JAUNT = "Kinetic Jaunt"
    LESSER_RESTORATION = "Lesser Restoration"
    LEVITATE = "Levitate"
    MAGIC_MOUTH = "Magic Mouth"
    MAGIC_WEAPON = "Magic Weapon"
    PROTECTION_FROM_POISON = "Protection from Poison"
    PYROTECHNICS = "Pyrotechnics"
    ROPE_TRICK = "Rope Trick"
    SEE_INVISIBILITY = "See Invisibility"
    SKYWRITE = "Skywrite"
    SPIDER_CLIMB = "Spider Climb"
    VORTEX_WARP = "Vortex Warp"
    WEB = "Web"


class ArtificerThirdLevel(StrEnum):
    ASHARDALONS_STRIDE = "Ashardalon's Stride"
    BLINK = "Blink"
    CATNAP = "Catnap"
    CREATE_FOOD_AND_WATER = "Create Food and Water"
    DISPEL_MAGIC = "Dispel Magic"
    ELEMENTAL_WEAPON = "Elemental Weapon"
    FLAME_ARROWS = "Flame Arrows"
    FLAME_STRIDE_UA = "Flame Stride (UA)"
    FLY = "Fly"
    GLYPH_OF_WARDING = "Glyph of Warding"
    HASTE = "Haste"
    INTELLECT_FORTRESS = "Intellect Fortress"
    PROTECTION_FROM_ENERGY = "Protection from Energy"
    REVIVIFY = "Revivify"
    TINY_SERVANT = "Tiny Servant"
    WATER_BREATHING = "Water Breathing"
    WATER_WALK = "Water Walk"


class ArtificerFourthLevel(StrEnum):
    ARCANE_EYE = "Arcane Eye"
    ELEMENTAL_BANE = "Elemental Bane"
    FABRICATE = "Fabricate"
    FREEDOM_OF_MOVEMENT = "Freedom of Movement"
    LEOMUNDS_SECRET_CHEST = "Leomund's Secret Chest"
    MORDENKAINENS_FAITHFUL_HOUND = "Mordenkainen's Faithful Hound"
    MORDENKAINENS_PRIVATE_SANCTUM = "Mordenkainen's Private Sanctum"
    OTILUKES_RESILIENT_SPHERE = "Otiluke's Resilient Sphere"
    STONE_SHAPE = "Stone Shape"
    STONESKIN = "Stoneskin"
    SUMMON_CONSTRUCT = "Summon Construct"


class ArtificerFifthLevel(StrEnum):
    ANIMATE_OBJECTS = "Animate Objects"
    BIGBYS_HAND = "Bigby's Hand"
    CREATE_SPELLJAMMING_HELM = "Create Spelljamming Helm"
    CREATION = "Creation"
    GREATER_RESTORATION = "Greater Restoration"
    SKILL_EMPOWERMENT = "Skill Empowerment"
    TRANSMUTE_ROCK = "Transmute Rock"
    WALL_OF_STONE = "Wall of Stone"


class BardCantrip(StrEnum):
    BLADE_WARD = "Blade Ward"
    DANCING_LIGHTS = "Dancing Lights"
    FRIENDS = "Friends"
    LIGHT = "Light"
    MAGE_HAND = "Mage Hand"
    MENDING = "Mending"
    MESSAGE = "Message"
    MINOR_ILLUSION = "Minor Illusion"
    PRESTIDIGITATION = "Prestidigitation"
    THUNDERCLAP = "Thunderclap"
    TRUE_STRIKE = "True Strike"
    VICIOUS_MOCKERY = "Vicious Mockery"


class BardFirstLevel(StrEnum):
    ANIMAL_FRIENDSHIP = "Animal Friendship"
    BANE = "Bane"
    CHARM_PERSON = "Charm Person"
    COMPREHEND_LANGUAGES = "Comprehend Languages"
    CURE_WOUNDS = "Cure Wounds"
    DETECT_MAGIC = "Detect Magic"
    DISGUISE_SELF = "Disguise Self"
    DISSONANT_WHISPERS = "Dissonant Whispers"
    DISTORT_VALUE = "Distort Value"
    EARTH_TREMOR = "Earth Tremor"
    FAERIE_FIRE = "Faerie Fire"
    FEATHER_FALL = "Feather Fall"
    HEALING_WORD = "Healing Word"
    HEROISM = "Heroism"
    IDENTIFY = "Identify"
    ILLUSORY_SCRIPT = "Illusory Script"
    LONGSTRIDER = "Longstrider"
    SILENT_IMAGE = "Silent Image"
    SILVERY_BARBS = "Silvery Barbs"
    SLEEP = "Sleep"
    SPEAK_WITH_ANIMALS = "Speak with Animals"
    TASHAS_HIDEOUS_LAUGHTER = "Tasha's Hideous Laughter"
    THUNDERWAVE = "Thunderwave"
    UNSEEN_SERVANT = "Unseen Servant"


class BardSecondLevel(StrEnum):
    ANIMAL_MESSENGER = "Animal Messenger"
    BLINDNESS_DEAFNESS = "Blindness-Deafness"
    BORROWED_KNOWLEDGE = "Borrowed Knowledge"
    CALM_EMOTIONS = "Calm Emotions"
    CLOUD_OF_DAGGERS = "Cloud of Daggers"
    CROWN_OF_MADNESS = "Crown of Madness"
    DETECT_THOUGHTS = "Detect Thoughts"
    ENHANCE_ABILITY = "Enhance Ability"
    ENTHRALL = "Enthrall"
    GIFT_OF_GAB = "Gift of Gab"
    HEAT_METAL = "Heat Metal"
    HOLD_PERSON = "Hold Person"
    INVISIBILITY = "Invisibility"
    KINETIC_JAUNT = "Kinetic Jaunt"
    KNOCK = "Knock"
    LESSER_RESTORATION = "Lesser Restoration"
    LOCATE_ANIMALS_OR_PLANTS = "Locate Animals or Plants"
    LOCATE_OBJECT = "Locate Object"
    MAGIC_MOUTH = "Magic Mouth"
    NATHAIRS_MISCHIEF = "Nathair's Mischief"
    NATHAIRS_MISCHIEF_UA = "Nathair's Mischief (UA)"
    PHANTASMAL_FORCE = "Phantasmal Force"
    PYROTECHNICS = "Pyrotechnics"
    SEE_INVISIBILITY = "See Invisibility"
    SHATTER = "Shatter"
    SILENCE = "Silence"
    SKYWRITE = "Skywrite"
    SPRAY_OF_CARDS = "Spray Of Cards"
    SPRAY_OF_CARDS_UA = "Spray of Cards (UA)"
    SUGGESTION = "Suggestion"
    WARDING_WIND = "Warding Wind"
    ZONE_OF_TRUTH = "Zone of Truth"


class BardThirdLevel(StrEnum):
    ANTAGONIZE = "Antagonize"
    ANTAGONIZE_UA = "Antagonize (UA)"
    BESTOW_CURSE = "Bestow Curse"
    CATNAP = "Catnap"
    CLAIRVOYANCE = "Clairvoyance"
    DISPEL_MAGIC = "Dispel Magic"
    ENEMIES_ABOUND = "Enemies Abound"
    FAST_FRIENDS = "Fast Friends"
    FEAR = "Fear"
    FEIGN_DEATH = "Feign Death"
    GLYPH_OF_WARDING = "Glyph of Warding"
    HYPNOTIC_PATTERN = "Hypnotic Pattern"
    LEOMUNDS_TINY_HUT = "Leomund's Tiny Hut"
    MAJOR_IMAGE = "Major Image"
    MOTIVATIONAL_SPEECH = "Motivational Speech"
    NONDETECTION = "Nondetection"
    PLANT_GROWTH = "Plant Growth"
    SENDING = "Sending"
    SPEAK_WITH_DEAD = "Speak with Dead"
    SPEAK_WITH_PLANTS = "Speak with Plants"
    STINKING_CLOUD = "Stinking Cloud"
    TONGUES = "Tongues"


class BardFourthLevel(StrEnum):
    CHARM_MONSTER = "Charm Monster"
    COMPULSION = "Compulsion"
    CONFUSION = "Confusion"
    DIMENSION_DOOR = "Dimension Door"
    EGO_WHIP_UA = "Ego Whip (UA)"
    FREEDOM_OF_MOVEMENT = "Freedom of Movement"
    GREATER_INVISIBILITY = "Greater Invisibility"
    HALLUCINATORY_TERRAIN = "Hallucinatory Terrain"
    LOCATE_CREATURE = "Locate Creature"
    POLYMORPH = "Polymorph"
    RAULOTHIMS_PSYCHIC_LANCE = "Raulothim's Psychic Lance"
    RAULOTHIMS_PSYCHIC_LANCE_UA = "Raulothim's Psychic Lance (UA)"


class BardFifthLevel(StrEnum):
    ANIMATE_OBJECTS = "Animate Objects"
    AWAKEN = "Awaken"
    DOMINATE_PERSON = "Dominate Person"
    DREAM = "Dream"
    GEAS = "Geas"
    GREATER_RESTORATION = "Greater Restoration"
    HOLD_MONSTER = "Hold Monster"
    LEGEND_LORE = "Legend Lore"
    MASS_CURE_WOUNDS = "Mass Cure Wounds"
    MISLEAD = "Mislead"
    MODIFY_MEMORY = "Modify Memory"
    PLANAR_BINDING = "Planar Binding"
    RAISE_DEAD = "Raise Dead"
    SCRYING = "Scrying"
    SEEMING = "Seeming"
    SKILL_EMPOWERMENT = "Skill Empowerment"
    SYNAPTIC_STATIC = "Synaptic Static"
    TELEPORTATION_CIRCLE = "Teleportation Circle"


class BardSixthLevel(StrEnum):
    EYEBITE = "Eyebite"
    FIND_THE_PATH = "Find the Path"
    GUARDS_AND_WARDS = "Guards and Wards"
    MASS_SUGGESTION = "Mass Suggestion"
    OTTOS_IRRESISTIBLE_DANCE = "Otto's Irresistible Dance"
    PROGRAMMED_ILLUSION = "Programmed Illusion"
    TRUE_SEEING = auto()


class BardSeventhLevel(StrEnum):
    ETHEREALNESS = "Etherealness"
    FORCECAGE = "Forcecage"
    MIRAGE_ARCANE = "Mirage Arcane"
    MORDENKAINENS_MAGNIFICENT_MANSION = "Mordenkainen's Magnificent Mansion"
    MORDENKAINENS_SWORD = "Mordenkainen's Sword"
    PRISMATIC_SPRAY = "Prismatic Spray"
    PROJECT_IMAGE = "Project Image"
    REGENERATE = "Regenerate"
    RESURRECTION = "Resurrection"
    SYMBOL = "Symbol"
    TELEPORT = "Teleport"


class BardEighthLevel(StrEnum):
    DOMINATE_MONSTER = "Dominate Monster"
    FEEBLEMIND = "Feeblemind"
    GLIBNESS = "Glibness"
    MIND_BLANK = "Mind Blank"
    POWER_WORD_STUN = "Power Word: Stun"


class BardNinthLevel(StrEnum):
    FORESIGHT = "Foresight"
    MASS_POLYMORPH = "Mass Polymorph"
    POWER_WORD_HEAL = "Power Word: Heal"
    POWER_WORD_KILL = "Power Word: Kill"
    PSYCHIC_SCREAM = "Psychic Scream"
    TRUE_POLYMORPH = "True Polymorph"


class ClericCantrip(StrEnum):
    DECOMPOSE = "Decompose"
    GUIDANCE = "Guidance"
    HAND_OF_RADIANCE = "Hand of Radiance"
    LIGHT = "Light"
    MENDING = "Mending"
    RESISTANCE = "Resistance"
    SACRED_FLAME = "Sacred Flame"
    SPARE_THE_DYING = "Spare the Dying"
    THAUMATURGY = "Thaumaturgy"
    TOLL_THE_DEAD = "Toll the Dead"
    VIRTUE = "Virtue"
    WORD_OF_RADIANCE = "Word of Radiance"


class ClericFirstLevel(StrEnum):
    BANE = "Bane"
    BLESS = "Bless"
    CEREMONY = "Ceremony"
    COMMAND = "Command"
    CREATE_OR_DESTROY_WATER = "Create or Destroy Water"
    CURE_WOUNDS = "Cure Wounds"
    DETECT_EVIL_AND_GOOD = "Detect Evil and Good"
    DETECT_MAGIC = "Detect Magic"
    DETECT_POISON_AND_DISEASE = "Detect Poison and Disease"
    GUIDING_BOLT = "Guiding Bolt"
    HEALING_WORD = "Healing Word"
    INFLICT_WOUNDS = "Inflict Wounds"
    PROTECTION_FROM_EVIL_AND_GOOD = "Protection from Evil and Good"
    PURIFY_FOOD_AND_DRINK = "Purify Food and Drink"
    SANCTUARY = "Sanctuary"
    SHIELD_OF_FAITH = "Shield of Faith"


class ClericSecondLevel(StrEnum):
    AID = "Aid"
    AUGURY = "Augury"
    BLINDNESS_DEAFNESS = "Blindness-Deafness"
    BORROWED_KNOWLEDGE = "Borrowed Knowledge"
    CALM_EMOTIONS = "Calm Emotions"
    CONTINUAL_FLAME = "Continual Flame"
    ENHANCE_ABILITY = "Enhance Ability"
    FIND_TRAPS = "Find Traps"
    GENTLE_REPOSE = "Gentle Repose"
    HOLD_PERSON = "Hold Person"
    LESSER_RESTORATION = "Lesser Restoration"
    LOCATE_OBJECT = "Locate Object"
    PRAYER_OF_HEALING = "Prayer of Healing"
    PROTECTION_FROM_POISON = "Protection from Poison"
    SILENCE = "Silence"
    SPIRITUAL_WEAPON = "Spiritual Weapon"
    WARDING_BOND = "Warding Bond"
    ZONE_OF_TRUTH = "Zone of Truth"


class ClericThirdLevel(StrEnum):
    ANIMATE_DEAD = "Animate Dead"
    BEACON_OF_HOPE = "Beacon of Hope"
    BESTOW_CURSE = "Bestow Curse"
    CLAIRVOYANCE = "Clairvoyance"
    CREATE_FOOD_AND_WATER = "Create Food and Water"
    DAYLIGHT = "Daylight"
    DISPEL_MAGIC = "Dispel Magic"
    FAST_FRIENDS = "Fast Friends"
    FEIGN_DEATH = "Feign Death"
    GLYPH_OF_WARDING = "Glyph of Warding"
    INCITE_GREED = "Incite Greed"
    LIFE_TRANSFERENCE = "Life Transference"
    MAGIC_CIRCLE = "Magic Circle"
    MASS_HEALING_WORD = "Mass Healing Word"
    MELD_INTO_STONE = "Meld into Stone"
    MOTIVATIONAL_SPEECH = "Motivational Speech"
    PROTECTION_FROM_ENERGY = "Protection from Energy"
    REMOVE_CURSE = "Remove Curse"
    REVIVIFY = "Revivify"
    SENDING = "Sending"
    SPEAK_WITH_DEAD = "Speak with Dead"
    SPIRIT_GUARDIANS = "Spirit Guardians"
    TONGUES = "Tongues"
    WATER_WALK = "Water Walk"


class ClericFourthLevel(StrEnum):
    BANISHMENT = "Banishment"
    CONTROL_WATER = "Control Water"
    DEATH_WARD = "Death Ward"
    DIVINATION = "Divination"
    FREEDOM_OF_MOVEMENT = "Freedom of Movement"
    GUARDIAN_OF_FAITH = "Guardian of Faith"
    LOCATE_CREATURE = "Locate Creature"
    STONE_SHAPE = "Stone Shape"


class ClericFifthLevel(StrEnum):
    COMMUNE = "Commune"
    CONTAGION = "Contagion"
    DAWN = "Dawn"
    DISPEL_EVIL_AND_GOOD = "Dispel Evil and Good"
    FLAME_STRIKE = "Flame Strike"
    GEAS = "Geas"
    GREATER_RESTORATION = "Greater Restoration"
    HALLOW = "Hallow"
    HOLY_WEAPON = "Holy Weapon"
    INSECT_PLAGUE = "Insect Plague"
    LEGEND_LORE = "Legend Lore"
    MASS_CURE_WOUNDS = "Mass Cure Wounds"
    PLANAR_BINDING = "Planar Binding"
    RAISE_DEAD = "Raise Dead"
    SCRYING = "Scrying"


class ClericSixthLevel(StrEnum):
    BLADE_BARRIER = "Blade Barrier"
    CREATE_UNDEAD = "Create Undead"
    FIND_THE_PATH = "Find the Path"
    FORBIDDANCE = "Forbiddance"
    HARM = "Harm"
    HEAL = "Heal"
    HEROES_FEAST = "Heroes' Feast"
    OTHERWORLDLY_FORM_UA = "Otherworldly Form (UA)"
    PLANAR_ALLY = "Planar Ally"
    TRUE_SEEING = auto()
    WORD_OF_RECALL = "Word of Recall"


class ClericSeventhLevel(StrEnum):
    CONJURE_CELESTIAL = "Conjure Celestial"
    DIVINE_WORD = "Divine Word"
    ETHEREALNESS = "Etherealness"
    FIRE_STORM = "Fire Storm"
    PLANE_SHIFT = "Plane Shift"
    REGENERATE = "Regenerate"
    RESURRECTION = "Resurrection"
    SYMBOL = "Symbol"
    TEMPLE_OF_THE_GODS = "Temple of the Gods"


class ClericEighthLevel(StrEnum):
    ANTIMAGIC_FIELD = "Antimagic Field"
    CONTROL_WEATHER = "Control Weather"
    EARTHQUAKE = "Earthquake"
    HOLY_AURA = "Holy Aura"


class ClericNinthLevel(StrEnum):
    ASTRAL_PROJECTION = "Astral Projection"
    GATE = "Gate"
    MASS_HEAL = "Mass Heal"
    TRUE_RESURRECTION = "True Resurrection"


class DruidCantrip(StrEnum):
    CONTROL_FLAMES = "Control Flames"
    CREATE_BONFIRE = "Create Bonfire"
    DRUIDCRAFT = "Druidcraft"
    FROSTBITE = "Frostbite"
    GUIDANCE = "Guidance"
    GUST = "Gust"
    INFESTATION = "Infestation"
    MAGIC_STONE = "Magic Stone"
    MENDING = "Mending"
    MOLD_EARTH = "Mold Earth"
    POISON_SPRAY = "Poison Spray"
    PRIMAL_SAVAGERY = "Primal Savagery"
    PRODUCE_FLAME = "Produce Flame"
    RESISTANCE = "Resistance"
    SHAPE_WATER = "Shape Water"
    SHILLELAGH = "Shillelagh"
    THORN_WHIP = "Thorn Whip"
    THUNDERCLAP = "Thunderclap"


class DruidFirstLevel(StrEnum):
    ABSORB_ELEMENTS = "Absorb Elements"
    ANIMAL_FRIENDSHIP = "Animal Friendship"
    BEAST_BOND = "Beast Bond"
    CHARM_PERSON = "Charm Person"
    CREATE_OR_DESTROY_WATER = "Create or Destroy Water"
    CURE_WOUNDS = "Cure Wounds"
    DETECT_MAGIC = "Detect Magic"
    DETECT_POISON_AND_DISEASE = "Detect Poison and Disease"
    EARTH_TREMOR = "Earth Tremor"
    ENTANGLE = "Entangle"
    FAERIE_FIRE = "Faerie Fire"
    FOG_CLOUD = "Fog Cloud"
    GOODBERRY = "Goodberry"
    HEALING_WORD = "Healing Word"
    ICE_KNIFE = "Ice Knife"
    JUMP = "Jump"
    LONGSTRIDER = "Longstrider"
    PURIFY_FOOD_AND_DRINK = "Purify Food and Drink"
    SNARE = "Snare"
    SPEAK_WITH_ANIMALS = "Speak with Animals"
    THUNDERWAVE = "Thunderwave"


class DruidSecondLevel(StrEnum):
    AIR_BUBBLE = "Air Bubble"
    ANIMAL_MESSENGER = "Animal Messenger"
    BARKSKIN = "Barkskin"
    BEAST_SENSE = "Beast Sense"
    DARKVISION = "Darkvision"
    DUST_DEVIL = "Dust Devil"
    EARTHBIND = "Earthbind"
    ENHANCE_ABILITY = "Enhance Ability"
    FIND_TRAPS = "Find Traps"
    FLAME_BLADE = "Flame Blade"
    FLAMING_SPHERE = "Flaming Sphere"
    GUST_OF_WIND = "Gust of Wind"
    HEALING_SPIRIT = "Healing Spirit"
    HEAT_METAL = "Heat Metal"
    HOLD_PERSON = "Hold Person"
    LESSER_RESTORATION = "Lesser Restoration"
    LOCATE_ANIMALS_OR_PLANTS = "Locate Animals or Plants"
    LOCATE_OBJECT = "Locate Object"
    MOONBEAM = "Moonbeam"
    PASS_WITHOUT_TRACE = "Pass Without Trace"
    PROTECTION_FROM_POISON = "Protection from Poison"
    SKYWRITE = "Skywrite"
    SPIKE_GROWTH = "Spike Growth"
    WARDING_WIND = "Warding Wind"
    WITHER_AND_BLOOM = "Wither and Bloom"


class DruidThirdLevel(StrEnum):
    CALL_LIGHTNING = "Call Lightning"
    CONJURE_ANIMALS = "Conjure Animals"
    DAYLIGHT = "Daylight"
    DISPEL_MAGIC = "Dispel Magic"
    ERUPTING_EARTH = "Erupting Earth"
    FEIGN_DEATH = "Feign Death"
    FLAME_ARROWS = "Flame Arrows"
    MELD_INTO_STONE = "Meld into Stone"
    PLANT_GROWTH = "Plant Growth"
    PROTECTION_FROM_ENERGY = "Protection from Energy"
    SLEET_STORM = "Sleet Storm"
    SPEAK_WITH_PLANTS = "Speak with Plants"
    TIDAL_WAVE = "Tidal Wave"
    WALL_OF_WATER = "Wall of Water"
    WATER_BREATHING = "Water Breathing"
    WATER_WALK = "Water Walk"
    WIND_WALL = "Wind Wall"


class DruidFourthLevel(StrEnum):
    BLIGHT = "Blight"
    CHARM_MONSTER = "Charm Monster"
    CONFUSION = "Confusion"
    CONJURE_MINOR_ELEMENTALS = "Conjure Minor Elementals"
    CONJURE_WOODLAND_BEINGS = "Conjure Woodland Beings"
    CONTROL_WATER = "Control Water"
    DOMINATE_BEAST = "Dominate Beast"
    ELEMENTAL_BANE = "Elemental Bane"
    FREEDOM_OF_MOVEMENT = "Freedom of Movement"
    GIANT_INSECT = "Giant Insect"
    GRASPING_VINE = "Grasping Vine"
    GUARDIAN_OF_NATURE = "Guardian of Nature"
    HALLUCINATORY_TERRAIN = "Hallucinatory Terrain"
    ICE_STORM = "Ice Storm"
    LOCATE_CREATURE = "Locate Creature"
    POLYMORPH = "Polymorph"
    STONE_SHAPE = "Stone Shape"
    STONESKIN = "Stoneskin"
    WALL_OF_FIRE = "Wall of Fire"
    WATERY_SPHERE = "Watery Sphere"


class DruidFifthLevel(StrEnum):
    ANTILIFE_SHELL = "Antilife Shell"
    AWAKEN = "Awaken"
    COMMUNE_WITH_NATURE = "Commune with Nature"
    CONJURE_ELEMENTAL = "Conjure Elemental"
    CONTAGION = "Contagion"
    CONTROL_WINDS = "Control Winds"
    FREEDOM_OF_THE_WINDS_HB = "Freedom of the Winds (HB)"
    GEAS = "Geas"
    GREATER_RESTORATION = "Greater Restoration"
    INSECT_PLAGUE = "Insect Plague"
    MAELSTROM = "Maelstrom"
    MASS_CURE_WOUNDS = "Mass Cure Wounds"
    PLANAR_BINDING = "Planar Binding"
    REINCARNATE = "Reincarnate"
    SCRYING = "Scrying"
    SUMMON_DRACONIC_SPIRIT = "Summon Draconic Spirit"
    SUMMON_DRACONIC_SPIRIT_UA = "Summon Draconic Spirit (UA)"
    TRANSMUTE_ROCK = "Transmute Rock"
    TREE_STRIDE = "Tree Stride"
    WALL_OF_STONE = "Wall of Stone"
    WRATH_OF_NATURE = "Wrath Of Nature"


class DruidSixthLevel(StrEnum):
    BONES_OF_THE_EARTH = "Bones of the Earth"
    CONJURE_FEY = "Conjure Fey"
    DRUID_GROVE = "Druid Grove"
    FIND_THE_PATH = "Find the Path"
    HEAL = "Heal"
    HEROES_FEAST = "Heroes' Feast"
    INVESTITURE_OF_FLAME = "Investiture of Flame"
    INVESTITURE_OF_ICE = "Investiture of Ice"
    INVESTITURE_OF_STONE = "Investiture of Stone"
    INVESTITURE_OF_WIND = "Investiture of Wind"
    MOVE_EARTH = "Move Earth"
    PRIMORDIAL_WARD = "Primordial Ward"
    SUNBEAM = "Sunbeam"
    TRANSPORT_VIA_PLANTS = "Transport via Plants"
    WALL_OF_THORNS = "Wall of Thorns"
    WIND_WALK = "Wind Walk"


class DruidSeventhLevel(StrEnum):
    DRACONIC_TRANSFORMATION = "Draconic Transformation"
    DRACONIC_TRANSFORMATION_UA = "Draconic Transformation (UA)"
    FIRE_STORM = "Fire Storm"
    MIRAGE_ARCANE = "Mirage Arcane"
    PLANE_SHIFT = "Plane Shift"
    REGENERATE = "Regenerate"
    REVERSE_GRAVITY = "Reverse Gravity"
    WHIRLWIND = "Whirlwind"


class DruidEighthLevel(StrEnum):
    ANIMAL_SHAPES = "Animal Shapes"
    ANTIPATHY_SYMPATHY = "Antipathy/Sympathy"
    CONTROL_WEATHER = "Control Weather"
    EARTHQUAKE = "Earthquake"
    FEEBLEMIND = "Feeblemind"
    SUNBURST = "Sunburst"
    TSUNAMI = "Tsunami"


class DruidNinthLevel(StrEnum):
    FORESIGHT = "Foresight"
    SHAPECHANGE = "Shapechange"
    STORM_OF_VENGEANCE = "Storm of Vengeance"
    TRUE_RESURRECTION = "True Resurrection"


class PaladinFirstLevel(StrEnum):
    BLESS = "Bless"
    CEREMONY = "Ceremony"
    COMMAND = "Command"
    COMPELLED_DUEL = "Compelled Duel"
    CURE_WOUNDS = "Cure Wounds"
    DETECT_EVIL_AND_GOOD = "Detect Evil and Good"
    DETECT_MAGIC = "Detect Magic"
    DETECT_POISON_AND_DISEASE = "Detect Poison and Disease"
    DIVINE_FAVOR = "Divine Favor"
    HEROISM = "Heroism"
    PROTECTION_FROM_EVIL_AND_GOOD = "Protection from Evil and Good"
    PURIFY_FOOD_AND_DRINK = "Purify Food and Drink"
    SEARING_SMITE = "Searing Smite"
    SHIELD_OF_FAITH = "Shield of Faith"
    THUNDEROUS_SMITE = "Thunderous Smite"
    WRATHFUL_SMITE = "Wrathful Smite"


class PaladinSecondLevel(StrEnum):
    AID = "Aid"
    BRANDING_SMITE = "Branding Smite"
    FIND_STEED = "Find Steed"
    FIND_VEHICLE_UA = "Find Vehicle (UA)"
    LESSER_RESTORATION = "Lesser Restoration"
    LOCATE_OBJECT = "Locate Object"
    MAGIC_WEAPON = "Magic Weapon"
    PROTECTION_FROM_POISON = "Protection from Poison"
    ZONE_OF_TRUTH = "Zone of Truth"


class PaladinThirdLevel(StrEnum):
    AURA_OF_VITALITY = "Aura of Vitality"
    BLINDING_SMITE = "Blinding Smite"
    CREATE_FOOD_AND_WATER = "Create Food and Water"
    CRUSADERS_MANTLE = "Crusader's Mantle"
    DAYLIGHT = "Daylight"
    DISPEL_MAGIC = "Dispel Magic"
    ELEMENTAL_WEAPON = "Elemental Weapon"
    MAGIC_CIRCLE = "Magic Circle"
    REMOVE_CURSE = "Remove Curse"
    REVIVIFY = "Revivify"


class PaladinFourthLevel(StrEnum):
    AURA_OF_LIFE = "Aura of Life"
    AURA_OF_PURITY = "Aura of Purity"
    BANISHMENT = "Banishment"
    DEATH_WARD = "Death Ward"
    FIND_GREATER_STEED = "Find Greater Steed"
    LOCATE_CREATURE = "Locate Creature"
    STAGGERING_SMITE = "Staggering Smite"


class PaladinFifthLevel(StrEnum):
    BANISHING_SMITE = "Banishing Smite"
    CIRCLE_OF_POWER = "Circle of Power"
    DESTRUCTIVE_WAVE = "Destructive Wave"
    DISPEL_EVIL_AND_GOOD = "Dispel Evil and Good"
    GEAS = "Geas"
    HOLY_WEAPON = "Holy Weapon"
    RAISE_DEAD = "Raise Dead"


class RangerFirstLevel(StrEnum):
    ABSORB_ELEMENTS = "Absorb Elements"
    ALARM = "Alarm"
    ANIMAL_FRIENDSHIP = "Animal Friendship"
    BEAST_BOND = "Beast Bond"
    CURE_WOUNDS = "Cure Wounds"
    DETECT_MAGIC = "Detect Magic"
    DETECT_POISON_AND_DISEASE = "Detect Poison and Disease"
    ENSNARING_STRIKE = "Ensnaring Strike"
    FOG_CLOUD = "Fog Cloud"
    GOODBERRY = "Goodberry"
    HAIL_OF_THORNS = "Hail of Thorns"
    HUNTERS_MARK = "Hunter's Mark"
    JUMP = "Jump"
    LONGSTRIDER = "Longstrider"
    SNARE = "Snare"
    SPEAK_WITH_ANIMALS = "Speak with Animals"
    ZEPHYR_STRIKE = "Zephyr Strike"


class RangerSecondLevel(StrEnum):
    AIR_BUBBLE = "Air Bubble"
    ANIMAL_MESSENGER = "Animal Messenger"
    BARKSKIN = "Barkskin"
    BEAST_SENSE = "Beast Sense"
    CORDON_OF_ARROWS = "Cordon of Arrows"
    DARKVISION = "Darkvision"
    FIND_TRAPS = "Find Traps"
    HEALING_SPIRIT = "Healing Spirit"
    LESSER_RESTORATION = "Lesser Restoration"
    LOCATE_ANIMALS_OR_PLANTS = "Locate Animals or Plants"
    LOCATE_OBJECT = "Locate Object"
    PASS_WITHOUT_TRACE = "Pass Without Trace"
    PROTECTION_FROM_POISON = "Protection from Poison"
    SILENCE = "Silence"
    SPIKE_GROWTH = "Spike Growth"


class RangerThirdLevel(StrEnum):
    ASHARDALONS_STRIDE = "Ashardalon's Stride"
    CONJURE_ANIMALS = "Conjure Animals"
    CONJURE_BARRAGE = "Conjure Barrage"
    DAYLIGHT = "Daylight"
    FLAME_ARROWS = "Flame Arrows"
    FLAME_STRIDE_UA = "Flame Stride (UA)"
    LIGHTNING_ARROW = "Lightning Arrow"
    NONDETECTION = "Nondetection"
    PLANT_GROWTH = "Plant Growth"
    PROTECTION_FROM_ENERGY = "Protection from Energy"
    SPEAK_WITH_PLANTS = "Speak with Plants"
    WATER_BREATHING = "Water Breathing"
    WATER_WALK = "Water Walk"
    WIND_WALL = "Wind Wall"


class RangerFourthLevel(StrEnum):
    CONJURE_WOODLAND_BEINGS = "Conjure Woodland Beings"
    FREEDOM_OF_MOVEMENT = "Freedom of Movement"
    GRASPING_VINE = "Grasping Vine"
    GUARDIAN_OF_NATURE = "Guardian of Nature"
    LOCATE_CREATURE = "Locate Creature"
    STONESKIN = "Stoneskin"


class RangerFifthLevel(StrEnum):
    COMMUNE_WITH_NATURE = "Commune with Nature"
    CONJURE_VOLLEY = "Conjure Volley"
    FREEDOM_OF_THE_WINDS_HB = "Freedom of the Winds (HB)"
    STEEL_WIND_STRIKE = "Steel Wind Strike"
    SWIFT_QUIVER = "Swift Quiver"
    TREE_STRIDE = "Tree Stride"
    WRATH_OF_NATURE = "Wrath Of Nature"


class SorcererCantrip(StrEnum):
    ACID_SPLASH = "Acid Splash"
    BLADE_WARD = "Blade Ward"
    CHILL_TOUCH = "Chill Touch"
    CONTROL_FLAMES = "Control Flames"
    CREATE_BONFIRE = "Create Bonfire"
    DANCING_LIGHTS = "Dancing Lights"
    FIRE_BOLT = "Fire Bolt"
    FRIENDS = "Friends"
    FROSTBITE = "Frostbite"
    GUST = "Gust"
    INFESTATION = "Infestation"
    LIGHT = "Light"
    MAGE_HAND = "Mage Hand"
    MENDING = "Mending"
    MESSAGE = "Message"
    MINOR_ILLUSION = "Minor Illusion"
    MOLD_EARTH = "Mold Earth"
    ON_OFF = "On-Off"
    POISON_SPRAY = "Poison Spray"
    PRESTIDIGITATION = "Prestidigitation"
    RAY_OF_FROST = "Ray of Frost"
    SHAPE_WATER = "Shape Water"
    SHOCKING_GRASP = "Shocking Grasp"
    THUNDERCLAP = "Thunderclap"
    TRUE_STRIKE = "True Strike"


class SorcererFirstLevel(StrEnum):
    ABSORB_ELEMENTS = "Absorb Elements"
    BURNING_HANDS = "Burning Hands"
    CATAPULT = "Catapult"
    CHAOS_BOLT = "Chaos Bolt"
    CHARM_PERSON = "Charm Person"
    CHROMATIC_ORB = "Chromatic Orb"
    COLOR_SPRAY = "Color Spray"
    COMPREHEND_LANGUAGES = "Comprehend Languages"
    DETECT_MAGIC = "Detect Magic"
    DISGUISE_SELF = "Disguise Self"
    DISTORT_VALUE = "Distort Value"
    EARTH_TREMOR = "Earth Tremor"
    EXPEDITIOUS_RETREAT = "Expeditious Retreat"
    FALSE_LIFE = "False Life"
    FEATHER_FALL = "Feather Fall"
    FOG_CLOUD = "Fog Cloud"
    ICE_KNIFE = "Ice Knife"
    JUMP = "Jump"
    MAGE_ARMOR = "Mage Armor"
    MAGIC_MISSILE = "Magic Missile"
    RAY_OF_SICKNESS = "Ray of Sickness"
    SHIELD = "Shield"
    SILENT_IMAGE = "Silent Image"
    SILVERY_BARBS = "Silvery Barbs"
    SLEEP = "Sleep"
    THUNDERWAVE = "Thunderwave"
    WITCH_BOLT = "Witch Bolt"


class SorcererSecondLevel(StrEnum):
    AGANAZZARS_SCORCHER = "Aganazzar's Scorcher"
    AIR_BUBBLE = "Air Bubble"
    ALTER_SELF = "Alter Self"
    ARCANE_HACKING_UA = "Arcane Hacking (UA)"
    BLINDNESS_DEAFNESS = "Blindness-Deafness"
    BLUR = "Blur"
    CLOUD_OF_DAGGERS = "Cloud of Daggers"
    CROWN_OF_MADNESS = "Crown of Madness"
    DARKNESS = "Darkness"
    DARKVISION = "Darkvision"
    DETECT_THOUGHTS = "Detect Thoughts"
    DIGITAL_PHANTOM_UA = "Digital Phantom (UA)"
    DRAGONS_BREATH = "Dragon's Breath"
    DUST_DEVIL = "Dust Devil"
    EARTHBIND = "Earthbind"
    ENHANCE_ABILITY = "Enhance Ability"
    ENLARGE_REDUCE = "Enlarge-Reduce"
    FIND_VEHICLE_UA = "Find Vehicle (UA)"
    GUST_OF_WIND = "Gust of Wind"
    HOLD_PERSON = "Hold Person"
    INVISIBILITY = "Invisibility"
    KINETIC_JAUNT = "Kinetic Jaunt"
    KNOCK = "Knock"
    LEVITATE = "Levitate"
    MAXIMILLIANS_EARTHEN_GRASP = "Maximillian's Earthen Grasp"
    MENTAL_BARRIER_UA = "Mental Barrier (UA)"
    MIND_SPIKE = "Mind Spike"
    MIND_THRUST_UA = "Mind Thrust (UA)"
    MIRROR_IMAGE = "Mirror Image"
    MISTY_STEP = "Misty Step"
    NATHAIRS_MISCHIEF = "Nathair's Mischief"
    NATHAIRS_MISCHIEF_UA = "Nathair's Mischief (UA)"
    PHANTASMAL_FORCE = "Phantasmal Force"
    PYROTECHNICS = "Pyrotechnics"
    RIMES_BINDING_ICE = "Rime's Binding Ice"
    SCORCHING_RAY = "Scorching Ray"
    SEE_INVISIBILITY = "See Invisibility"
    SHADOW_BLADE = "Shadow Blade"
    SHATTER = "Shatter"
    SNILLOCS_SNOWBALL_STORM = "Snilloc's Snowball Storm"
    SPIDER_CLIMB = "Spider Climb"
    SPRAY_OF_CARDS = "Spray Of Cards"
    SPRAY_OF_CARDS_UA = "Spray of Cards (UA)"
    SUGGESTION = "Suggestion"
    THOUGHT_SHIELD_UA = "Thought Shield (UA)"
    VORTEX_WARP = "Vortex Warp"
    WARDING_WIND = "Warding Wind"
    WARP_SENSE = "Warp Sense"
    WEB = "Web"
    WITHER_AND_BLOOM = "Wither and Bloom"


class SorcererThirdLevel(StrEnum):
    ANTAGONIZE = "Antagonize"
    ANTAGONIZE_UA = "Antagonize (UA)"
    ASHARDALONS_STRIDE = "Ashardalon's Stride"
    BLINK = "Blink"
    CATNAP = "Catnap"
    CLAIRVOYANCE = "Clairvoyance"
    CONJURE_LESSER_DEMON_UA = "Conjure Lesser Demon (UA)"
    COUNTERSPELL = "Counterspell"
    DAYLIGHT = "Daylight"
    DISPEL_MAGIC = "Dispel Magic"
    ENEMIES_ABOUND = "Enemies Abound"
    ERUPTING_EARTH = "Erupting Earth"
    FEAR = "Fear"
    FIREBALL = "Fireball"
    FLAME_ARROWS = "Flame Arrows"
    FLAME_STRIDE_UA = "Flame Stride (UA)"
    FLY = "Fly"
    GASEOUS_FORM = "Gaseous Form"
    HASTE = "Haste"
    HAYWIRE_UA = "Haywire (UA)"
    HYPNOTIC_PATTERN = "Hypnotic Pattern"
    INCITE_GREED = "Incite Greed"
    INVISIBILITY_TO_CAMERAS_UA = "Invisibility To Cameras (UA)"
    LIGHTNING_BOLT = "Lightning Bolt"
    MAJOR_IMAGE = "Major Image"
    MELFS_MINUTE_METEORS = "Melf's Minute Meteors"
    PROTECTION_FROM_BALLISTICS_UA = "Protection from Ballistics (UA)"
    PROTECTION_FROM_ENERGY = "Protection from Energy"
    PSIONIC_BLAST_UA = "Psionic Blast (UA)"
    SLEET_STORM = "Sleet Storm"
    SLOW = "Slow"
    STINKING_CLOUD = "Stinking Cloud"
    SUMMON_WARRIOR_SPIRIT_UA = "Summon Warrior Spirit (UA)"
    THUNDER_STEP = "Thunder Step"
    TIDAL_WAVE = "Tidal Wave"
    TONGUES = "Tongues"
    VAMPIRIC_TOUCH = "Vampiric Touch"
    WALL_OF_WATER = "Wall of Water"
    WATER_BREATHING = "Water Breathing"
    WATER_WALK = "Water Walk"


class SorcererFourthLevel(StrEnum):
    BANISHMENT = "Banishment"
    BLIGHT = "Blight"
    CHARM_MONSTER = "Charm Monster"
    CONFUSION = "Confusion"
    CONJURE_BARLGURA_UA = "Conjure Barlgura (UA)"
    CONJURE_KNOWBOT_UA = "Conjure Knowbot (UA)"
    CONJURE_SHADOW_DEMON_UA = "Conjure Shadow Demon (UA)"
    DIMENSION_DOOR = "Dimension Door"
    DOMINATE_BEAST = "Dominate Beast"
    EGO_WHIP_UA = "Ego Whip (UA)"
    GATE_SEAL = "Gate Seal"
    GREATER_INVISIBILITY = "Greater Invisibility"
    ICE_STORM = "Ice Storm"
    POLYMORPH = "Polymorph"
    RAULOTHIMS_PSYCHIC_LANCE = "Raulothim's Psychic Lance"
    RAULOTHIMS_PSYCHIC_LANCE_UA = "Raulothim's Psychic Lance (UA)"
    SICKENING_RADIANCE = "Sickening Radiance"
    SPIRIT_OF_DEATH = "Spirit of Death"
    SPIRIT_OF_DEATH_UA = "Spirit of Death (UA)"
    STONESKIN = "Stoneskin"
    STORM_SPHERE = "Storm Sphere"
    SYNCHRONICITY_UA = "Synchronicity (UA)"
    SYSTEM_BACKDOOR_UA = "System Backdoor (UA)"
    VITRIOLIC_SPHERE = "Vitriolic Sphere"
    WALL_OF_FIRE = "Wall of Fire"
    WATERY_SPHERE = "Watery Sphere"


class SorcererFifthLevel(StrEnum):
    ANIMATE_OBJECTS = "Animate Objects"
    CLOUDKILL = "Cloudkill"
    COMMUNE_WITH_CITY_UA = "Commune with City (UA)"
    CONE_OF_COLD = "Cone of Cold"
    CONJURE_VROCK_UA = "Conjure Vrock (UA)"
    CONTROL_WINDS = "Control Winds"
    CREATION = "Creation"
    DOMINATE_PERSON = "Dominate Person"
    ENERVATION = "Enervation"
    FAR_STEP = "Far Step"
    FREEDOM_OF_THE_WINDS_HB = "Freedom of the Winds (HB)"
    HOLD_MONSTER = "Hold Monster"
    IMMOLATION = "Immolation"
    INSECT_PLAGUE = "Insect Plague"
    SEEMING = "Seeming"
    SHUTDOWN_UA = "Shutdown (UA)"
    SKILL_EMPOWERMENT = "Skill Empowerment"
    SUMMON_DRACONIC_SPIRIT = "Summon Draconic Spirit"
    SUMMON_DRACONIC_SPIRIT_UA = "Summon Draconic Spirit (UA)"
    SYNAPTIC_STATIC = "Synaptic Static"
    TELEKINESIS = "Telekinesis"
    TELEPORTATION_CIRCLE = "Teleportation Circle"
    WALL_OF_LIGHT = "Wall of Light"
    WALL_OF_STONE = "Wall of Stone"


class SorcererSixthLevel(StrEnum):
    ARCANE_GATE = "Arcane Gate"
    CHAIN_LIGHTNING = "Chain Lightning"
    CIRCLE_OF_DEATH = "Circle of Death"
    DISINTEGRATE = "Disintegrate"
    EYEBITE = "Eyebite"
    FIZBANS_PLATINUM_SHIELD = "Fizban's Platinum Shield"
    FIZBANS_PLATINUM_SHIELD_UA = "Fizban's Platinum Shield (UA)"
    GLOBE_OF_INVULNERABILITY = "Globe of Invulnerability"
    INVESTITURE_OF_FLAME = "Investiture of Flame"
    INVESTITURE_OF_ICE = "Investiture of Ice"
    INVESTITURE_OF_STONE = "Investiture of Stone"
    INVESTITURE_OF_WIND = "Investiture of Wind"
    MASS_SUGGESTION = "Mass Suggestion"
    MENTAL_PRISON = "Mental Prison"
    MOVE_EARTH = "Move Earth"
    OTHERWORLDLY_FORM_UA = "Otherworldly Form (UA)"
    PSYCHIC_CRUSH_UA = "Psychic Crush (UA)"
    SCATTER = "Scatter"
    SUNBEAM = "Sunbeam"
    TRUE_SEEING = auto()


class SorcererSeventhLevel(StrEnum):
    CONJURE_HEZROU_UA = "Conjure Hezrou (UA)"
    CROWN_OF_STARS = "Crown of Stars"
    DELAYED_BLAST_FIREBALL = "Delayed Blast Fireball"
    DRACONIC_TRANSFORMATION = "Draconic Transformation"
    DRACONIC_TRANSFORMATION_UA = "Draconic Transformation (UA)"
    ETHEREALNESS = "Etherealness"
    FINGER_OF_DEATH = "Finger of Death"
    FIRE_STORM = "Fire Storm"
    PLANE_SHIFT = "Plane Shift"
    POWER_WORD_PAIN = "Power Word: Pain"
    PRISMATIC_SPRAY = "Prismatic Spray"
    REVERSE_GRAVITY = "Reverse Gravity"
    TELEPORT = "Teleport"


class SorcererEighthLevel(StrEnum):
    ABI_DALZIMS_HORRID_WILTING = "Abi-Dalzim's Horrid Wilting"
    DOMINATE_MONSTER = "Dominate Monster"
    EARTHQUAKE = "Earthquake"
    INCENDIARY_CLOUD = "Incendiary Cloud"
    POWER_WORD_STUN = "Power Word: Stun"
    SUNBURST = "Sunburst"


class SorcererNinthLevel(StrEnum):
    GATE = "Gate"
    MASS_POLYMORPH = "Mass Polymorph"
    METEOR_SWARM = "Meteor Swarm"
    POWER_WORD_KILL = "Power Word: Kill"
    PSYCHIC_SCREAM = "Psychic Scream"
    TIME_STOP = "Time Stop"
    WISH = "Wish"


class WarlockCantrip(StrEnum):
    BLADE_WARD = "Blade Ward"
    CHILL_TOUCH = "Chill Touch"
    CREATE_BONFIRE = "Create Bonfire"
    ELDRITCH_BLAST = "Eldritch Blast"
    FRIENDS = "Friends"
    FROSTBITE = "Frostbite"
    INFESTATION = "Infestation"
    MAGE_HAND = "Mage Hand"
    MAGIC_STONE = "Magic Stone"
    MINOR_ILLUSION = "Minor Illusion"
    ON_OFF = "On-Off"
    POISON_SPRAY = "Poison Spray"
    PRESTIDIGITATION = "Prestidigitation"
    THUNDERCLAP = "Thunderclap"
    TOLL_THE_DEAD = "Toll the Dead"
    TRUE_STRIKE = "True Strike"


class WarlockFirstLevel(StrEnum):
    ARMOR_OF_AGATHYS = "Armor of Agathys"
    ARMS_OF_HADAR = "Arms of Hadar"
    CAUSE_FEAR = "Cause Fear"
    CHARM_PERSON = "Charm Person"
    COMPREHEND_LANGUAGES = "Comprehend Languages"
    DISTORT_VALUE = "Distort Value"
    EXPEDITIOUS_RETREAT = "Expeditious Retreat"
    HELLISH_REBUKE = "Hellish Rebuke"
    HEX = "Hex"
    ILLUSORY_SCRIPT = "Illusory Script"
    PROTECTION_FROM_EVIL_AND_GOOD = "Protection from Evil and Good"
    UNSEEN_SERVANT = "Unseen Servant"
    WITCH_BOLT = "Witch Bolt"


class WarlockSecondLevel(StrEnum):
    ARCANE_HACKING_UA = "Arcane Hacking (UA)"
    BORROWED_KNOWLEDGE = "Borrowed Knowledge"
    CLOUD_OF_DAGGERS = "Cloud of Daggers"
    CROWN_OF_MADNESS = "Crown of Madness"
    DARKNESS = "Darkness"
    DIGITAL_PHANTOM_UA = "Digital Phantom (UA)"
    EARTHBIND = "Earthbind"
    ENTHRALL = "Enthrall"
    FIND_VEHICLE_UA = "Find Vehicle (UA)"
    FLOCK_OF_FAMILIARS = "Flock of Familiars"
    HOLD_PERSON = "Hold Person"
    INVISIBILITY = "Invisibility"
    MENTAL_BARRIER_UA = "Mental Barrier (UA)"
    MIND_SPIKE = "Mind Spike"
    MIND_THRUST_UA = "Mind Thrust (UA)"
    MIRROR_IMAGE = "Mirror Image"
    MISTY_STEP = "Misty Step"
    RAY_OF_ENFEEBLEMENT = "Ray of Enfeeblement"
    SHADOW_BLADE = "Shadow Blade"
    SHATTER = "Shatter"
    SPIDER_CLIMB = "Spider Climb"
    SPRAY_OF_CARDS = "Spray Of Cards"
    SPRAY_OF_CARDS_UA = "Spray of Cards (UA)"
    SUGGESTION = "Suggestion"
    THOUGHT_SHIELD_UA = "Thought Shield (UA)"
    WARP_SENSE = "Warp Sense"


class WarlockThirdLevel(StrEnum):
    ANTAGONIZE = "Antagonize"
    ANTAGONIZE_UA = "Antagonize (UA)"
    COUNTERSPELL = "Counterspell"
    DISPEL_MAGIC = "Dispel Magic"
    ENEMIES_ABOUND = "Enemies Abound"
    FEAR = "Fear"
    FLY = "Fly"
    GASEOUS_FORM = "Gaseous Form"
    HAYWIRE_UA = "Haywire (UA)"
    HUNGER_OF_HADAR = "Hunger Of Hadar"
    HYPNOTIC_PATTERN = "Hypnotic Pattern"
    INCITE_GREED = "Incite Greed"
    INVISIBILITY_TO_CAMERAS_UA = "Invisibility To Cameras (UA)"
    MAGIC_CIRCLE = "Magic Circle"
    MAJOR_IMAGE = "Major Image"
    PROTECTION_FROM_BALLISTICS_UA = "Protection from Ballistics (UA)"
    PSIONIC_BLAST_UA = "Psionic Blast (UA)"
    REMOVE_CURSE = "Remove Curse"
    SUMMON_LESSER_DEMONS = "Summon Lesser Demons"
    SUMMON_WARRIOR_SPIRIT_UA = "Summon Warrior Spirit (UA)"
    THUNDER_STEP = "Thunder Step"
    TONGUES = "Tongues"
    VAMPIRIC_TOUCH = "Vampiric Touch"


class WarlockFourthLevel(StrEnum):
    BANISHMENT = "Banishment"
    BLIGHT = "Blight"
    CHARM_MONSTER = "Charm Monster"
    CONJURE_KNOWBOT_UA = "Conjure Knowbot (UA)"
    DIMENSION_DOOR = "Dimension Door"
    EGO_WHIP_UA = "Ego Whip (UA)"
    ELEMENTAL_BANE = "Elemental Bane"
    GALDERS_SPEEDY_COURIER = "Galder's Speedy Courier"
    GATE_SEAL = "Gate Seal"
    HALLUCINATORY_TERRAIN = "Hallucinatory Terrain"
    RAULOTHIMS_PSYCHIC_LANCE = "Raulothim's Psychic Lance"
    RAULOTHIMS_PSYCHIC_LANCE_UA = "Raulothim's Psychic Lance (UA)"
    SHADOW_OF_MOIL = "Shadow of Moil"
    SICKENING_RADIANCE = "Sickening Radiance"
    SPIRIT_OF_DEATH = "Spirit of Death"
    SPIRIT_OF_DEATH_UA = "Spirit of Death (UA)"
    SYNCHRONICITY_UA = "Synchronicity (UA)"
    SYSTEM_BACKDOOR_UA = "System Backdoor (UA)"


class WarlockFifthLevel(StrEnum):
    COMMUNE_WITH_CITY_UA = "Commune with City (UA)"
    CONTACT_OTHER_PLANE = "Contact Other Plane"
    DANSE_MACABRE = "Danse Macabre"
    DREAM = "Dream"
    ENERVATION = "Enervation"
    FAR_STEP = "Far Step"
    HOLD_MONSTER = "Hold Monster"
    INFERNAL_CALLING = "Infernal Calling"
    NEGATIVE_ENERGY_FLOOD = "Negative Energy Flood"
    SCRYING = "Scrying"
    SHUTDOWN_UA = "Shutdown (UA)"
    SYNAPTIC_STATIC = "Synaptic Static"
    WALL_OF_LIGHT = "Wall of Light"


class WarlockSixthLevel(StrEnum):
    ARCANE_GATE = "Arcane Gate"
    CIRCLE_OF_DEATH = "Circle of Death"
    CONJURE_FEY = "Conjure Fey"
    CREATE_UNDEAD = "Create Undead"
    EYEBITE = "Eyebite"
    FLESH_TO_STONE = "Flesh to Stone"
    INVESTITURE_OF_FLAME = "Investiture of Flame"
    INVESTITURE_OF_ICE = "Investiture of Ice"
    INVESTITURE_OF_STONE = "Investiture of Stone"
    INVESTITURE_OF_WIND = "Investiture of Wind"
    MASS_SUGGESTION = "Mass Suggestion"
    MENTAL_PRISON = "Mental Prison"
    OTHERWORLDLY_FORM_UA = "Otherworldly Form (UA)"
    PSYCHIC_CRUSH_UA = "Psychic Crush (UA)"
    SCATTER = "Scatter"
    SOUL_CAGE = "Soul Cage"
    TRUE_SEEING = auto()


class WarlockSeventhLevel(StrEnum):
    CROWN_OF_STARS = "Crown of Stars"
    ETHEREALNESS = "Etherealness"
    FINGER_OF_DEATH = "Finger of Death"
    FORCECAGE = "Forcecage"
    PLANE_SHIFT = "Plane Shift"
    POWER_WORD_PAIN = "Power Word: Pain"


class WarlockEighthLevel(StrEnum):
    DEMIPLANE = "Demiplane"
    DOMINATE_MONSTER = "Dominate Monster"
    FEEBLEMIND = "Feeblemind"
    GLIBNESS = "Glibness"
    MADDENING_DARKNESS = "Maddening Darkness"
    POWER_WORD_STUN = "Power Word: Stun"


class WarlockNinthLevel(StrEnum):
    ASTRAL_PROJECTION = "Astral Projection"
    FORESIGHT = "Foresight"
    IMPRISONMENT = "Imprisonment"
    POWER_WORD_KILL = "Power Word: Kill"
    PSYCHIC_SCREAM = "Psychic Scream"
    TRUE_POLYMORPH = "True Polymorph"


class WizardCantrip(StrEnum):
    ACID_SPLASH = "Acid Splash"
    BLADE_WARD = "Blade Ward"
    CHILL_TOUCH = "Chill Touch"
    CONTROL_FLAMES = "Control Flames"
    CREATE_BONFIRE = "Create Bonfire"
    DANCING_LIGHTS = "Dancing Lights"
    ENCODE_THOUGHTS = "Encode Thoughts"
    FIRE_BOLT = "Fire Bolt"
    FRIENDS = "Friends"
    FROSTBITE = "Frostbite"
    GUST = "Gust"
    INFESTATION = "Infestation"
    LIGHT = "Light"
    MAGE_HAND = "Mage Hand"
    MENDING = "Mending"
    MESSAGE = "Message"
    MINOR_ILLUSION = "Minor Illusion"
    MOLD_EARTH = "Mold Earth"
    ON_OFF = "On-Off"
    POISON_SPRAY = "Poison Spray"
    PRESTIDIGITATION = "Prestidigitation"
    RAY_OF_FROST = "Ray of Frost"
    SHAPE_WATER = "Shape Water"
    SHOCKING_GRASP = "Shocking Grasp"
    THUNDERCLAP = "Thunderclap"
    TOLL_THE_DEAD = "Toll the Dead"
    TRUE_STRIKE = "True Strike"


class WizardFirstLevel(StrEnum):
    ABSORB_ELEMENTS = "Absorb Elements"
    ALARM = "Alarm"
    BURNING_HANDS = "Burning Hands"
    CATAPULT = "Catapult"
    CAUSE_FEAR = "Cause Fear"
    CHARM_PERSON = "Charm Person"
    CHROMATIC_ORB = "Chromatic Orb"
    COLOR_SPRAY = "Color Spray"
    COMPREHEND_LANGUAGES = "Comprehend Languages"
    DETECT_MAGIC = "Detect Magic"
    DISGUISE_SELF = "Disguise Self"
    DISTORT_VALUE = "Distort Value"
    EARTH_TREMOR = "Earth Tremor"
    EXPEDITIOUS_RETREAT = "Expeditious Retreat"
    FALSE_LIFE = "False Life"
    FEATHER_FALL = "Feather Fall"
    FIND_FAMILIAR = "Find Familiar"
    FOG_CLOUD = "Fog Cloud"
    FROST_FINGERS = "Frost Fingers"
    GREASE = "Grease"
    ICE_KNIFE = "Ice Knife"
    IDENTIFY = "Identify"
    ILLUSORY_SCRIPT = "Illusory Script"
    JIMS_MAGIC_MISSILE = "Jim's Magic Missile"
    JUMP = "Jump"
    LONGSTRIDER = "Longstrider"
    MAGE_ARMOR = "Mage Armor"
    MAGIC_MISSILE = "Magic Missile"
    PROTECTION_FROM_EVIL_AND_GOOD = "Protection from Evil and Good"
    RAY_OF_SICKNESS = "Ray of Sickness"
    SHIELD = "Shield"
    SILENT_IMAGE = "Silent Image"
    SILVERY_BARBS = "Silvery Barbs"
    SLEEP = "Sleep"
    SNARE = "Snare"
    TASHAS_HIDEOUS_LAUGHTER = "Tasha's Hideous Laughter"
    TENSERS_FLOATING_DISK = "Tenser's Floating Disk"
    THUNDERWAVE = "Thunderwave"
    UNSEEN_SERVANT = "Unseen Servant"
    WITCH_BOLT = "Witch Bolt"


class WizardSecondLevel(StrEnum):
    AGANAZZARS_SCORCHER = "Aganazzar's Scorcher"
    AIR_BUBBLE = "Air Bubble"
    ALTER_SELF = "Alter Self"
    ARCANE_HACKING_UA = "Arcane Hacking (UA)"
    ARCANE_LOCK = "Arcane Lock"
    BLINDNESS_DEAFNESS = "Blindness-Deafness"
    BLUR = "Blur"
    BORROWED_KNOWLEDGE = "Borrowed Knowledge"
    CLOUD_OF_DAGGERS = "Cloud of Daggers"
    CONTINUAL_FLAME = "Continual Flame"
    CROWN_OF_MADNESS = "Crown of Madness"
    DARKNESS = "Darkness"
    DARKVISION = "Darkvision"
    DETECT_THOUGHTS = "Detect Thoughts"
    DIGITAL_PHANTOM_UA = "Digital Phantom (UA)"
    DRAGONS_BREATH = "Dragon's Breath"
    DUST_DEVIL = "Dust Devil"
    EARTHBIND = "Earthbind"
    ENLARGE_REDUCE = "Enlarge-Reduce"
    FIND_VEHICLE_UA = "Find Vehicle (UA)"
    FLAMING_SPHERE = "Flaming Sphere"
    FLOCK_OF_FAMILIARS = "Flock of Familiars"
    GENTLE_REPOSE = "Gentle Repose"
    GIFT_OF_GAB = "Gift of Gab"
    GUST_OF_WIND = "Gust of Wind"
    HOLD_PERSON = "Hold Person"
    INVISIBILITY = "Invisibility"
    JIMS_GLOWING_COIN = "Jim's Glowing Coin"
    KINETIC_JAUNT = "Kinetic Jaunt"
    KNOCK = "Knock"
    LEVITATE = "Levitate"
    LOCATE_OBJECT = "Locate Object"
    MAGIC_MOUTH = "Magic Mouth"
    MAGIC_WEAPON = "Magic Weapon"
    MAXIMILLIANS_EARTHEN_GRASP = "Maximillian's Earthen Grasp"
    MELFS_ACID_ARROW = "Melf's Acid Arrow"
    MENTAL_BARRIER_UA = "Mental Barrier (UA)"
    MIND_SPIKE = "Mind Spike"
    MIND_THRUST_UA = "Mind Thrust (UA)"
    MIRROR_IMAGE = "Mirror Image"
    MISTY_STEP = "Misty Step"
    NATHAIRS_MISCHIEF = "Nathair's Mischief"
    NATHAIRS_MISCHIEF_UA = "Nathair's Mischief (UA)"
    NYSTULS_MAGIC_AURA = "Nystul's Magic Aura"
    PHANTASMAL_FORCE = "Phantasmal Force"
    PYROTECHNICS = "Pyrotechnics"
    RAY_OF_ENFEEBLEMENT = "Ray of Enfeeblement"
    RIMES_BINDING_ICE = "Rime's Binding Ice"
    ROPE_TRICK = "Rope Trick"
    SCORCHING_RAY = "Scorching Ray"
    SEE_INVISIBILITY = "See Invisibility"
    SHADOW_BLADE = "Shadow Blade"
    SHATTER = "Shatter"
    SKYWRITE = "Skywrite"
    SNILLOCS_SNOWBALL_STORM = "Snilloc's Snowball Storm"
    SPIDER_CLIMB = "Spider Climb"
    SPRAY_OF_CARDS = "Spray Of Cards"
    SPRAY_OF_CARDS_UA = "Spray of Cards (UA)"
    SUGGESTION = "Suggestion"
    THOUGHT_SHIELD_UA = "Thought Shield (UA)"
    VORTEX_WARP = "Vortex Warp"
    WARDING_WIND = "Warding Wind"
    WARP_SENSE = "Warp Sense"
    WEB = "Web"
    WITHER_AND_BLOOM = "Wither and Bloom"


class WizardThirdLevel(StrEnum):
    ANIMATE_DEAD = "Animate Dead"
    ANTAGONIZE = "Antagonize"
    ANTAGONIZE_UA = "Antagonize (UA)"
    ASHARDALONS_STRIDE = "Ashardalon's Stride"
    BESTOW_CURSE = "Bestow Curse"
    BLINK = "Blink"
    CATNAP = "Catnap"
    CLAIRVOYANCE = "Clairvoyance"
    CONJURE_LESSER_DEMON_UA = "Conjure Lesser Demon (UA)"
    COUNTERSPELL = "Counterspell"
    DISPEL_MAGIC = "Dispel Magic"
    ENEMIES_ABOUND = "Enemies Abound"
    ERUPTING_EARTH = "Erupting Earth"
    FAST_FRIENDS = "Fast Friends"
    FEAR = "Fear"
    FEIGN_DEATH = "Feign Death"
    FIREBALL = "Fireball"
    FLAME_ARROWS = "Flame Arrows"
    FLAME_STRIDE_UA = "Flame Stride (UA)"
    FLY = "Fly"
    GALDERS_TOWER = "Galder's Tower"
    GASEOUS_FORM = "Gaseous Form"
    GLYPH_OF_WARDING = "Glyph of Warding"
    HASTE = "Haste"
    HAYWIRE_UA = "Haywire (UA)"
    HYPNOTIC_PATTERN = "Hypnotic Pattern"
    INCITE_GREED = "Incite Greed"
    INVISIBILITY_TO_CAMERAS_UA = "Invisibility To Cameras (UA)"
    LEOMUNDS_TINY_HUT = "Leomund's Tiny Hut"
    LIFE_TRANSFERENCE = "Life Transference"
    LIGHTNING_BOLT = "Lightning Bolt"
    MAGIC_CIRCLE = "Magic Circle"
    MAJOR_IMAGE = "Major Image"
    MELFS_MINUTE_METEORS = "Melf's Minute Meteors"
    NONDETECTION = "Nondetection"
    PHANTOM_STEED = "Phantom Steed"
    PROTECTION_FROM_BALLISTICS_UA = "Protection from Ballistics (UA)"
    PROTECTION_FROM_ENERGY = "Protection from Energy"
    PSIONIC_BLAST_UA = "Psionic Blast (UA)"
    REMOVE_CURSE = "Remove Curse"
    SENDING = "Sending"
    SLEET_STORM = "Sleet Storm"
    SLOW = "Slow"
    STINKING_CLOUD = "Stinking Cloud"
    SUMMON_LESSER_DEMONS = "Summon Lesser Demons"
    SUMMON_WARRIOR_SPIRIT_UA = "Summon Warrior Spirit (UA)"
    THUNDER_STEP = "Thunder Step"
    TIDAL_WAVE = "Tidal Wave"
    TINY_SERVANT = "Tiny Servant"
    TONGUES = "Tongues"
    VAMPIRIC_TOUCH = "Vampiric Touch"
    WALL_OF_SAND = "Wall of Sand"
    WALL_OF_WATER = "Wall of Water"
    WATER_BREATHING = "Water Breathing"


class WizardFourthLevel(StrEnum):
    ARCANE_EYE = "Arcane Eye"
    BANISHMENT = "Banishment"
    BLIGHT = "Blight"
    CHARM_MONSTER = "Charm Monster"
    CONFUSION = "Confusion"
    CONJURE_BARLGURA_UA = "Conjure Barlgura (UA)"
    CONJURE_KNOWBOT_UA = "Conjure Knowbot (UA)"
    CONJURE_MINOR_ELEMENTALS = "Conjure Minor Elementals"
    CONJURE_SHADOW_DEMON_UA = "Conjure Shadow Demon (UA)"
    CONTROL_WATER = "Control Water"
    DIMENSION_DOOR = "Dimension Door"
    EGO_WHIP_UA = "Ego Whip (UA)"
    ELEMENTAL_BANE = "Elemental Bane"
    EVARDS_BLACK_TENTACLES = "Evard's Black Tentacles"
    FABRICATE = "Fabricate"
    FIRE_SHIELD = "Fire Shield"
    GALDERS_SPEEDY_COURIER = "Galder's Speedy Courier"
    GATE_SEAL = "Gate Seal"
    GRAVITY_SINKHOLE = "Gravity Sinkhole"
    GREATER_INVISIBILITY = "Greater Invisibility"
    HALLUCINATORY_TERRAIN = "Hallucinatory Terrain"
    ICE_STORM = "Ice Storm"
    LEOMUNDS_SECRET_CHEST = "Leomund's Secret Chest"
    LOCATE_CREATURE = "Locate Creature"
    MORDENKAINENS_FAITHFUL_HOUND = "Mordenkainen's Faithful Hound"
    MORDENKAINENS_PRIVATE_SANCTUM = "Mordenkainen's Private Sanctum"
    OTILUKES_RESILIENT_SPHERE = "Otiluke's Resilient Sphere"
    PHANTASMAL_KILLER = "Phantasmal Killer"
    POLYMORPH = "Polymorph"
    RAULOTHIMS_PSYCHIC_LANCE = "Raulothim's Psychic Lance"
    RAULOTHIMS_PSYCHIC_LANCE_UA = "Raulothim's Psychic Lance (UA)"
    SICKENING_RADIANCE = "Sickening Radiance"
    SPIRIT_OF_DEATH = "Spirit of Death"
    SPIRIT_OF_DEATH_UA = "Spirit of Death (UA)"
    STONE_SHAPE = "Stone Shape"
    STONESKIN = "Stoneskin"
    STORM_SPHERE = "Storm Sphere"
    SUMMON_GREATER_DEMON = "Summon Greater Demon"
    SYNCHRONICITY_UA = "Synchronicity (UA)"
    SYSTEM_BACKDOOR_UA = "System Backdoor (UA)"
    VITRIOLIC_SPHERE = "Vitriolic Sphere"
    WALL_OF_FIRE = "Wall of Fire"
    WATERY_SPHERE = "Watery Sphere"
    WIDOGASTS_VAULT_OF_AMBER_HB = "Widogast's Vault of Amber (HB)"
    WIDOGASTS_WEB_OF_FIRE_HB = "Widogast's Web of Fire (HB)"


class WizardFifthLevel(StrEnum):
    ANIMATE_OBJECTS = "Animate Objects"
    BIGBYS_HAND = "Bigby's Hand"
    CLOUDKILL = "Cloudkill"
    COMMUNE_WITH_CITY_UA = "Commune with City (UA)"
    CONE_OF_COLD = "Cone of Cold"
    CONJURE_ELEMENTAL = "Conjure Elemental"
    CONJURE_VROCK_UA = "Conjure Vrock (UA)"
    CONTACT_OTHER_PLANE = "Contact Other Plane"
    CONTROL_WINDS = "Control Winds"
    CREATE_SPELLJAMMING_HELM = "Create Spelljamming Helm"
    CREATION = "Creation"
    DANSE_MACABRE = "Danse Macabre"
    DAWN = "Dawn"
    DOMINATE_PERSON = "Dominate Person"
    DREAM = "Dream"
    ENERVATION = "Enervation"
    FAR_STEP = "Far Step"
    GEAS = "Geas"
    HOLD_MONSTER = "Hold Monster"
    IMMOLATION = "Immolation"
    INFERNAL_CALLING = "Infernal Calling"
    LEGEND_LORE = "Legend Lore"
    MISLEAD = "Mislead"
    MODIFY_MEMORY = "Modify Memory"
    NEGATIVE_ENERGY_FLOOD = "Negative Energy Flood"
    PASSWALL = "Passwall"
    PLANAR_BINDING = "Planar Binding"
    RARYS_TELEPATHIC_BOND = "Rary's Telepathic Bond"
    SCRYING = "Scrying"
    SEEMING = "Seeming"
    SHUTDOWN_UA = "Shutdown (UA)"
    SKILL_EMPOWERMENT = "Skill Empowerment"
    STEEL_WIND_STRIKE = "Steel Wind Strike"
    SUMMON_DRACONIC_SPIRIT = "Summon Draconic Spirit"
    SUMMON_DRACONIC_SPIRIT_UA = "Summon Draconic Spirit (UA)"
    SYNAPTIC_STATIC = "Synaptic Static"
    TELEKINESIS = "Telekinesis"
    TELEPORTATION_CIRCLE = "Teleportation Circle"
    TEMPORAL_SHUNT = "Temporal Shunt"
    TRANSMUTE_ROCK = "Transmute Rock"
    WALL_OF_FORCE = "Wall of Force"
    WALL_OF_LIGHT = "Wall of Light"
    WALL_OF_STONE = "Wall of Stone"


class WizardSixthLevel(StrEnum):
    ARCANE_GATE = "Arcane Gate"
    CHAIN_LIGHTNING = "Chain Lightning"
    CIRCLE_OF_DEATH = "Circle of Death"
    CONTINGENCY = "Contingency"
    CREATE_HOMUNCULUS = "Create Homunculus"
    CREATE_UNDEAD = "Create Undead"
    DISINTEGRATE = "Disintegrate"
    DRAWMIJS_INSTANT_SUMMONS = "Drawmij's Instant Summons"
    EYEBITE = "Eyebite"
    FIZBANS_PLATINUM_SHIELD = "Fizban's Platinum Shield"
    FIZBANS_PLATINUM_SHIELD_UA = "Fizban's Platinum Shield (UA)"
    FLESH_TO_STONE = "Flesh to Stone"
    GLOBE_OF_INVULNERABILITY = "Globe of Invulnerability"
    GRAVITY_FISSURE = "Gravity Fissure"
    GUARDS_AND_WARDS = "Guards and Wards"
    INVESTITURE_OF_FLAME = "Investiture of Flame"
    INVESTITURE_OF_ICE = "Investiture of Ice"
    INVESTITURE_OF_STONE = "Investiture of Stone"
    INVESTITURE_OF_WIND = "Investiture of Wind"
    MAGIC_JAR = "Magic Jar"
    MASS_SUGGESTION = "Mass Suggestion"
    MENTAL_PRISON = "Mental Prison"
    MOVE_EARTH = "Move Earth"
    OTHERWORLDLY_FORM_UA = "Otherworldly Form (UA)"
    OTILUKES_FREEZING_SPHERE = auto()
    OTTOS_IRRESISTIBLE_DANCE = "Otto's Irresistible Dance"
    PROGRAMMED_ILLUSION = "Programmed Illusion"
    PSYCHIC_CRUSH_UA = "Psychic Crush (UA)"
    SCATTER = "Scatter"
    SOUL_CAGE = "Soul Cage"
    SUNBEAM = "Sunbeam"
    TENSERS_TRANSFORMATION = "Tenser's Transformation"
    TRUE_SEEING = auto()
    WALL_OF_ICE = "Wall of Ice"
    WIDOGASTS_TRANSMOGRIFICATION_HB = "Widogast's Transmogrification (HB)"


class WizardSeventhLevel(StrEnum):
    CONJURE_HEZROU_UA = "Conjure Hezrou (UA)"
    CREATE_MAGEN = "Create Magen"
    CROWN_OF_STARS = "Crown of Stars"
    DELAYED_BLAST_FIREBALL = "Delayed Blast Fireball"
    DRACONIC_TRANSFORMATION = "Draconic Transformation"
    DRACONIC_TRANSFORMATION_UA = "Draconic Transformation (UA)"
    ETHEREALNESS = "Etherealness"
    FINGER_OF_DEATH = "Finger of Death"
    FORCECAGE = "Forcecage"
    MIRAGE_ARCANE = "Mirage Arcane"
    MORDENKAINENS_MAGNIFICENT_MANSION = "Mordenkainen's Magnificent Mansion"
    MORDENKAINENS_SWORD = "Mordenkainen's Sword"
    PLANE_SHIFT = "Plane Shift"
    POWER_WORD_PAIN = "Power Word: Pain"
    PRISMATIC_SPRAY = "Prismatic Spray"
    PROJECT_IMAGE = "Project Image"
    REVERSE_GRAVITY = "Reverse Gravity"
    SEQUESTER = "Sequester"
    SIMULACRUM = "Simulacrum"
    SYMBOL = "Symbol"
    TELEPORT = "Teleport"
    TETHER_ESSENCE = "Tether Essence"
    WHIRLWIND = "Whirlwind"


class WizardEighthLevel(StrEnum):
    ABI_DALZIMS_HORRID_WILTING = "Abi-Dalzim's Horrid Wilting"
    ANTIMAGIC_FIELD = "Antimagic Field"
    ANTIPATHY_SYMPATHY = "Antipathy/Sympathy"
    CLONE = "Clone"
    CONTROL_WEATHER = "Control Weather"
    DARK_STAR = "Dark Star"
    DEMIPLANE = "Demiplane"
    DOMINATE_MONSTER = "Dominate Monster"
    FEEBLEMIND = "Feeblemind"
    ILLUSORY_DRAGON = "Illusory Dragon"
    INCENDIARY_CLOUD = "Incendiary Cloud"
    MADDENING_DARKNESS = "Maddening Darkness"
    MAZE = "Maze"
    MIGHTY_FORTRESS = "Mighty Fortress"
    MIND_BLANK = "Mind Blank"
    POWER_WORD_STUN = "Power Word: Stun"
    REALITY_BREAK = "Reality Break"
    SUNBURST = "Sunburst"
    TELEPATHY = "Telepathy"


class WizardNinthLevel(StrEnum):
    ASTRAL_PROJECTION = "Astral Projection"
    FORESIGHT = "Foresight"
    GATE = "Gate"
    IMPRISONMENT = "Imprisonment"
    INVULNERABILITY = "Invulnerability"
    MASS_POLYMORPH = "Mass Polymorph"
    METEOR_SWARM = "Meteor Swarm"
    POWER_WORD_KILL = "Power Word: Kill"
    PRISMATIC_WALL = "Prismatic Wall"
    PSYCHIC_SCREAM = "Psychic Scream"
    RAVENOUS_VOID = "Ravenous Void"
    SHAPECHANGE = "Shapechange"
    TIME_RAVAGE = "Time Ravage"
    TIME_STOP = "Time Stop"
    TRUE_POLYMORPH = "True Polymorph"
    WEIRD = "Weird"
    WISH = "Wish"


type Cantrip = (
    ArtificerCantrip
    | BardCantrip
    | ClericCantrip
    | DruidCantrip
    | SorcererCantrip
    | WarlockCantrip
    | WizardCantrip
)

type FirstLevel = (
    ArtificerFirstLevel
    | BardFirstLevel
    | ClericFirstLevel
    | DruidFirstLevel
    | PaladinFirstLevel
    | RangerFirstLevel
    | SorcererFirstLevel
    | WarlockFirstLevel
    | WizardFirstLevel
)

type SecondLevel = (
    ArtificerSecondLevel
    | BardSecondLevel
    | ClericSecondLevel
    | DruidSecondLevel
    | PaladinSecondLevel
    | RangerSecondLevel
    | SorcererSecondLevel
    | WarlockSecondLevel
    | WizardSecondLevel
)

type ThirdLevel = (
    ArtificerThirdLevel
    | BardThirdLevel
    | ClericThirdLevel
    | DruidThirdLevel
    | PaladinThirdLevel
    | RangerThirdLevel
    | SorcererThirdLevel
    | WarlockThirdLevel
    | WizardThirdLevel
)

type FourthLevel = (
    ArtificerFourthLevel
    | BardFourthLevel
    | ClericFourthLevel
    | DruidFourthLevel
    | PaladinFourthLevel
    | RangerFourthLevel
    | SorcererFourthLevel
    | WarlockFourthLevel
    | WizardFourthLevel
)

type FifthLevel = (
    ArtificerFifthLevel
    | BardFifthLevel
    | ClericFifthLevel
    | DruidFifthLevel
    | PaladinFifthLevel
    | RangerFifthLevel
    | SorcererFifthLevel
    | WarlockFifthLevel
    | WizardFifthLevel
)

type SixthLevel = (
    BardSixthLevel
    | ClericSixthLevel
    | DruidSixthLevel
    | SorcererSixthLevel
    | WarlockSixthLevel
    | WizardSixthLevel
)

type SeventhLevel = (
    BardSeventhLevel
    | ClericSeventhLevel
    | DruidSeventhLevel
    | SorcererSeventhLevel
    | WarlockSeventhLevel
    | WizardSeventhLevel
)

type EighthLevel = (
    BardEighthLevel
    | ClericEighthLevel
    | DruidEighthLevel
    | SorcererEighthLevel
    | WarlockEighthLevel
    | WizardEighthLevel
)

type NinthLevel = (
    BardNinthLevel
    | ClericNinthLevel
    | DruidNinthLevel
    | SorcererNinthLevel
    | WarlockNinthLevel
    | WizardNinthLevel
)

type Spell = (
    Cantrip
    | FirstLevel
    | SecondLevel
    | ThirdLevel
    | FourthLevel
    | FifthLevel
    | SixthLevel
    | SeventhLevel
    | EighthLevel
    | NinthLevel
)


_T_co = TypeVar("_T_co", bound=Sequence[Spell], covariant=True)


class _SpellSelector(BaseModel, Generic[_T_co]):
    model_config = ConfigDict(title="SpellSelection")
    spells: _T_co

    def __class_getitem__(
        cls,
        item: type[object] | tuple[type[object], ...],
    ) -> type[BaseModel]:
        result = cast(type[BaseModel], super().__class_getitem__(item))
        result.__name__ = "SpellSelection"
        return result

    @classmethod
    def spell_type(cls) -> Iterable[Spell]:
        annotation = cls.model_fields["spells"].annotation
        (element_type,) = get_args(annotation)
        return cast(Iterable[Spell], element_type)


def get_class_spell_selector(
    query: ClassSpellLevel, n_spells: PositiveInt
) -> type[_SpellSelector[Sequence[Spell]]]:
    length_field = Field(min_length=n_spells, max_length=n_spells)
    match query:
        case (Class.ARTIFICER, 0):
            return _SpellSelector[Annotated[list[ArtificerCantrip], length_field]]
        case (Class.ARTIFICER, 1):
            return _SpellSelector[Annotated[list[ArtificerFirstLevel], length_field]]
        case (Class.ARTIFICER, 2):
            return _SpellSelector[Annotated[list[ArtificerSecondLevel], length_field]]
        case (Class.ARTIFICER, 3):
            return _SpellSelector[Annotated[list[ArtificerThirdLevel], length_field]]
        case (Class.ARTIFICER, 4):
            return _SpellSelector[Annotated[list[ArtificerFourthLevel], length_field]]
        case (Class.ARTIFICER, 5):
            return _SpellSelector[Annotated[list[ArtificerFifthLevel], length_field]]

        case (Class.BARD, 0):
            return _SpellSelector[Annotated[list[BardCantrip], length_field]]
        case (Class.BARD, 1):
            return _SpellSelector[Annotated[list[BardFirstLevel], length_field]]
        case (Class.BARD, 2):
            return _SpellSelector[Annotated[list[BardSecondLevel], length_field]]
        case (Class.BARD, 3):
            return _SpellSelector[Annotated[list[BardThirdLevel], length_field]]
        case (Class.BARD, 4):
            return _SpellSelector[Annotated[list[BardFourthLevel], length_field]]
        case (Class.BARD, 5):
            return _SpellSelector[Annotated[list[BardFifthLevel], length_field]]
        case (Class.BARD, 6):
            return _SpellSelector[Annotated[list[BardSixthLevel], length_field]]
        case (Class.BARD, 7):
            return _SpellSelector[Annotated[list[BardSeventhLevel], length_field]]
        case (Class.BARD, 8):
            return _SpellSelector[Annotated[list[BardEighthLevel], length_field]]
        case (Class.BARD, 9):
            return _SpellSelector[Annotated[list[BardNinthLevel], length_field]]

        case (Class.CLERIC, 0):
            return _SpellSelector[Annotated[list[ClericCantrip], length_field]]
        case (Class.CLERIC, 1):
            return _SpellSelector[Annotated[list[ClericFirstLevel], length_field]]
        case (Class.CLERIC, 2):
            return _SpellSelector[Annotated[list[ClericSecondLevel], length_field]]
        case (Class.CLERIC, 3):
            return _SpellSelector[Annotated[list[ClericThirdLevel], length_field]]
        case (Class.CLERIC, 4):
            return _SpellSelector[Annotated[list[ClericFourthLevel], length_field]]
        case (Class.CLERIC, 5):
            return _SpellSelector[Annotated[list[ClericFifthLevel], length_field]]
        case (Class.CLERIC, 6):
            return _SpellSelector[Annotated[list[ClericSixthLevel], length_field]]
        case (Class.CLERIC, 7):
            return _SpellSelector[Annotated[list[ClericSeventhLevel], length_field]]
        case (Class.CLERIC, 8):
            return _SpellSelector[Annotated[list[ClericEighthLevel], length_field]]
        case (Class.CLERIC, 9):
            return _SpellSelector[Annotated[list[ClericNinthLevel], length_field]]

        case (Class.DRUID, 0):
            return _SpellSelector[Annotated[list[DruidCantrip], length_field]]
        case (Class.DRUID, 1):
            return _SpellSelector[Annotated[list[DruidFirstLevel], length_field]]
        case (Class.DRUID, 2):
            return _SpellSelector[Annotated[list[DruidSecondLevel], length_field]]
        case (Class.DRUID, 3):
            return _SpellSelector[Annotated[list[DruidThirdLevel], length_field]]
        case (Class.DRUID, 4):
            return _SpellSelector[Annotated[list[DruidFourthLevel], length_field]]
        case (Class.DRUID, 5):
            return _SpellSelector[Annotated[list[DruidFifthLevel], length_field]]
        case (Class.DRUID, 6):
            return _SpellSelector[Annotated[list[DruidSixthLevel], length_field]]
        case (Class.DRUID, 7):
            return _SpellSelector[Annotated[list[DruidSeventhLevel], length_field]]
        case (Class.DRUID, 8):
            return _SpellSelector[Annotated[list[DruidEighthLevel], length_field]]
        case (Class.DRUID, 9):
            return _SpellSelector[Annotated[list[DruidNinthLevel], length_field]]

        case (Class.PALADIN, 1):
            return _SpellSelector[Annotated[list[PaladinFirstLevel], length_field]]
        case (Class.PALADIN, 2):
            return _SpellSelector[Annotated[list[PaladinSecondLevel], length_field]]
        case (Class.PALADIN, 3):
            return _SpellSelector[Annotated[list[PaladinThirdLevel], length_field]]
        case (Class.PALADIN, 4):
            return _SpellSelector[Annotated[list[PaladinFourthLevel], length_field]]
        case (Class.PALADIN, 5):
            return _SpellSelector[Annotated[list[PaladinFifthLevel], length_field]]

        case (Class.RANGER, 1):
            return _SpellSelector[Annotated[list[RangerFirstLevel], length_field]]
        case (Class.RANGER, 2):
            return _SpellSelector[Annotated[list[RangerSecondLevel], length_field]]
        case (Class.RANGER, 3):
            return _SpellSelector[Annotated[list[RangerThirdLevel], length_field]]
        case (Class.RANGER, 4):
            return _SpellSelector[Annotated[list[RangerFourthLevel], length_field]]
        case (Class.RANGER, 5):
            return _SpellSelector[Annotated[list[RangerFifthLevel], length_field]]

        case (Class.SORCERER, 0):
            return _SpellSelector[Annotated[list[SorcererCantrip], length_field]]
        case (Class.SORCERER, 1):
            return _SpellSelector[Annotated[list[SorcererFirstLevel], length_field]]
        case (Class.SORCERER, 2):
            return _SpellSelector[Annotated[list[SorcererSecondLevel], length_field]]
        case (Class.SORCERER, 3):
            return _SpellSelector[Annotated[list[SorcererThirdLevel], length_field]]
        case (Class.SORCERER, 4):
            return _SpellSelector[Annotated[list[SorcererFourthLevel], length_field]]
        case (Class.SORCERER, 5):
            return _SpellSelector[Annotated[list[SorcererFifthLevel], length_field]]
        case (Class.SORCERER, 6):
            return _SpellSelector[Annotated[list[SorcererSixthLevel], length_field]]
        case (Class.SORCERER, 7):
            return _SpellSelector[Annotated[list[SorcererSeventhLevel], length_field]]
        case (Class.SORCERER, 8):
            return _SpellSelector[Annotated[list[SorcererEighthLevel], length_field]]
        case (Class.SORCERER, 9):
            return _SpellSelector[Annotated[list[SorcererNinthLevel], length_field]]

        case (Class.WARLOCK, 0):
            return _SpellSelector[Annotated[list[WarlockCantrip], length_field]]
        case (Class.WARLOCK, 1):
            return _SpellSelector[Annotated[list[WarlockFirstLevel], length_field]]
        case (Class.WARLOCK, 2):
            return _SpellSelector[Annotated[list[WarlockSecondLevel], length_field]]
        case (Class.WARLOCK, 3):
            return _SpellSelector[Annotated[list[WarlockThirdLevel], length_field]]
        case (Class.WARLOCK, 4):
            return _SpellSelector[Annotated[list[WarlockFourthLevel], length_field]]
        case (Class.WARLOCK, 5):
            return _SpellSelector[Annotated[list[WarlockFifthLevel], length_field]]
        case (Class.WARLOCK, 6):
            return _SpellSelector[Annotated[list[WarlockSixthLevel], length_field]]
        case (Class.WARLOCK, 7):
            return _SpellSelector[Annotated[list[WarlockSeventhLevel], length_field]]
        case (Class.WARLOCK, 8):
            return _SpellSelector[Annotated[list[WarlockEighthLevel], length_field]]
        case (Class.WARLOCK, 9):
            return _SpellSelector[Annotated[list[WarlockNinthLevel], length_field]]

        case (Class.WIZARD, 0):
            return _SpellSelector[Annotated[list[WizardCantrip], length_field]]
        case (Class.WIZARD, 1):
            return _SpellSelector[Annotated[list[WizardFirstLevel], length_field]]
        case (Class.WIZARD, 2):
            return _SpellSelector[Annotated[list[WizardSecondLevel], length_field]]
        case (Class.WIZARD, 3):
            return _SpellSelector[Annotated[list[WizardThirdLevel], length_field]]
        case (Class.WIZARD, 4):
            return _SpellSelector[Annotated[list[WizardFourthLevel], length_field]]
        case (Class.WIZARD, 5):
            return _SpellSelector[Annotated[list[WizardFifthLevel], length_field]]
        case (Class.WIZARD, 6):
            return _SpellSelector[Annotated[list[WizardSixthLevel], length_field]]
        case (Class.WIZARD, 7):
            return _SpellSelector[Annotated[list[WizardSeventhLevel], length_field]]
        case (Class.WIZARD, 8):
            return _SpellSelector[Annotated[list[WizardEighthLevel], length_field]]
        case (Class.WIZARD, 9):
            return _SpellSelector[Annotated[list[WizardNinthLevel], length_field]]

        case _ as never:
            assert_never(never)


def get_class_spells_set(query: ClassSpellLevel) -> frozenset[Spell]:
    return frozenset(get_class_spell_selector(query, 1).spell_type())
