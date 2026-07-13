from enum import auto
from enum import StrEnum

from dnd.choices.class_creation.character_class import (
    Class,
)
from frozendict import frozendict


class Spell(StrEnum):
    pass


class Cantrip(Spell):
    ACID_SPLASH = "Acid Splash"
    BLADE_WARD = "Blade Ward"
    BOOMING_BLADE = "Booming Blade"
    CHILL_TOUCH = "Chill Touch"
    CONTROL_FLAMES = "Control Flames"
    CREATE_BONFIRE = "Create Bonfire"
    DANCING_LIGHTS = "Dancing Lights"
    DECOMPOSE = "Decompose"
    DRUIDCRAFT = "Druidcraft"
    ELDRITCH_BLAST = "Eldritch Blast"
    ENCODE_THOUGHTS = "Encode Thoughts"
    FIRE_BOLT = "Fire Bolt"
    FRIENDS = "Friends"
    FROSTBITE = "Frostbite"
    GREEN_FLAME_BLADE = "Green-Flame Blade"
    GUIDANCE = "Guidance"
    GUST = "Gust"
    HAND_OF_RADIANCE = "Hand of Radiance"
    INFESTATION = "Infestation"
    LIGHT = "Light"
    LIGHTNING_LURE = "Lightning Lure"
    MAGE_HAND = "Mage Hand"
    MAGIC_STONE = "Magic Stone"
    MENDING = "Mending"
    MESSAGE = "Message"
    MIND_SLIVER = "Mind Sliver"
    MINOR_ILLUSION = "Minor Illusion"
    MOLD_EARTH = "Mold Earth"
    ON_OFF = "On-Off"
    POISON_SPRAY = "Poison Spray"
    PRESTIDIGITATION = "Prestidigitation"
    PRIMAL_SAVAGERY = "Primal Savagery"
    PRODUCE_FLAME = "Produce Flame"
    RAY_OF_FROST = "Ray of Frost"
    RESISTANCE = "Resistance"
    SACRED_FLAME = "Sacred Flame"
    SAPPING_STING = "Sapping Sting"
    SHAPE_WATER = "Shape Water"
    SHILLELAGH = "Shillelagh"
    SHOCKING_GRASP = "Shocking Grasp"
    SPARE_THE_DYING = "Spare the Dying"
    SWORD_BURST = "Sword Burst"
    THAUMATURGY = "Thaumaturgy"
    THORN_WHIP = "Thorn Whip"
    THUNDERCLAP = "Thunderclap"
    TOLL_THE_DEAD = "Toll the Dead"
    TRUE_STRIKE = "True Strike"
    VICIOUS_MOCKERY = "Vicious Mockery"
    VIRTUE = "Virtue"
    WORD_OF_RADIANCE = "Word of Radiance"


class FirstLevel(Spell):
    ABSORB_ELEMENTS = "Absorb Elements"
    ACID_STREAM = "Acid Stream (UA)"
    ALARM = "Alarm"
    ANIMAL_FRIENDSHIP = "Animal Friendship"
    ARCANE_WEAPON = "Arcane Weapon (UA)"
    ARMOR_OF_AGATHYS = "Armor of Agathys"
    ARMS_OF_HADAR = "Arms of Hadar"
    BANE = "Bane"
    BEAST_BOND = "Beast Bond"
    BLESS = "Bless"
    BURNING_HANDS = "Burning Hands"
    CATAPULT = "Catapult"
    CAUSE_FEAR = "Cause Fear"
    CEREMONY = "Ceremony"
    CHAOS_BOLT = "Chaos Bolt"
    CHARM_PERSON = "Charm Person"
    CHROMATIC_ORB = "Chromatic Orb"
    COLOR_SPRAY = "Color Spray"
    COMMAND = "Command"
    COMPELLED_DUEL = "Compelled Duel"
    COMPREHEND_LANGUAGES = "Comprehend Languages"
    CREATE_OR_DESTROY_WATER = "Create or Destroy Water"
    CURE_WOUNDS = "Cure Wounds"
    DETECT_EVIL_AND_GOOD = "Detect Evil and Good"
    DETECT_MAGIC = "Detect Magic"
    DETECT_POISON_AND_DISEASE = "Detect Poison and Disease"
    DISGUISE_SELF = "Disguise Self"
    DISSONANT_WHISPERS = "Dissonant Whispers"
    DISTORT_VALUE = "Distort Value"
    DIVINE_FAVOR = "Divine Favor"
    EARTH_TREMOR = "Earth Tremor"
    ENSNARING_STRIKE = "Ensnaring Strike"
    ENTANGLE = "Entangle"
    EXPEDITIOUS_RETREAT = "Expeditious Retreat"
    FAERIE_FIRE = "Faerie Fire"
    FALSE_LIFE = "False Life"
    FEATHER_FALL = "Feather Fall"
    FIND_FAMILIAR = "Find Familiar"
    FOG_CLOUD = "Fog Cloud"
    FROST_FINGERS = "Frost Fingers"
    GIFT_OF_ALACRITY = "Gift of Alacrity"
    GOODBERRY = "Goodberry"
    GREASE = "Grease"
    GUIDING_BOLT = "Guiding Bolt"
    GUIDING_HAND = "Guiding Hand (UA)"
    HAIL_OF_THORNS = "Hail of Thorns"
    HEALING_ELIXIR = "Healing Elixir (UA)"
    HEALING_WORD = "Healing Word"
    HELLISH_REBUKE = "Hellish Rebuke"
    HEROISM = "Heroism"
    HEX = "Hex"
    HUNTERS_MARK = "Hunter's Mark"
    ICE_KNIFE = "Ice Knife"
    ID_IN_SINUATION = "Id Insinuation (UA)"
    IDENTIFY = "Identify"
    ILLUSORY_SCRIPT = "Illusory Script"
    INFALLIBLE_RELAY = "Infallible Relay (UA)"
    INFLICT_WOUNDS = "Inflict Wounds"
    JIMS_MAGIC_MISSILE = "Jim's Magic Missile"
    JUMP = "Jump"
    LONGSTRIDER = "Longstrider"
    MAGE_ARMOR = "Mage Armor"
    MAGIC_MISSILE = "Magic Missile"
    MAGNIFY_GRAVITY = "Magnify Gravity"
    PROTECTION_FROM_EVIL_AND_GOOD = "Protection from Evil and Good"
    PUPPET = "Puppet (UA)"
    PURIFY_FOOD_AND_DRINK = "Purify Food and Drink"
    RAY_OF_SICKNESS = "Ray of Sickness"
    REMOTE_ACCESS = "Remote Access (UA)"
    SANCTUARY = "Sanctuary"
    SEARING_SMITE = "Searing Smite"
    SENSE_EMOTION = "Sense Emotion (UA)"
    SHIELD = "Shield"
    SHIELD_OF_FAITH = "Shield of Faith"
    SILENT_IMAGE = "Silent Image"
    SILVERY_BARBS = "Silvery Barbs"
    SLEEP = "Sleep"
    SNARE = "Snare"
    SPEAK_WITH_ANIMALS = "Speak with Animals"
    SUDDEN_AWAKENING = "Sudden Awakening (UA)"
    TASHAS_CAUSTIC_BREW = "Tasha's Caustic Brew"
    TASHAS_HIDEOUS_LAUGHTER = "Tasha's Hideous Laughter"
    TENSERS_FLOATING_DISK = "Tenser's Floating Disk"
    THUNDEROUS_SMITE = "Thunderous Smite"
    THUNDERWAVE = "Thunderwave"
    UNEARTHLY_CHORUS = "Unearthly Chorus (UA)"
    UNSEEN_SERVANT = "Unseen Servant"
    WILD_CUNNING = "Wild Cunning (UA)"
    WITCH_BOLT = "Witch Bolt"
    WRATHFUL_SMITE = "Wrathful Smite"
    ZEPHYR_STRIKE = "Zephyr Strike"


class SecondLevel(Spell):
    AGANAZZARS_SCORCHER = "Aganazzar's Scorcher"
    AID = "Aid"
    AIR_BUBBLE = "Air Bubble"
    ALTER_SELF = "Alter Self"
    ANIMAL_MESSENGER = "Animal Messenger"
    ARCANE_HACKING_UA = "Arcane Hacking (UA)"
    ARCANE_LOCK = "Arcane Lock"
    AUGURY = "Augury"
    BARKSKIN = "Barkskin"
    BEAST_SENSE = "Beast Sense"
    BLINDNESS_DEAFNESS = "Blindness-Deafness"
    BLUR = "Blur"
    BORROWED_KNOWLEDGE = "Borrowed Knowledge"
    BRANDING_SMITE = "Branding Smite"
    CALM_EMOTIONS = "Calm Emotions"
    CLOUD_OF_DAGGERS = "Cloud of Daggers"
    CONTINUAL_FLAME = "Continual Flame"
    CORDON_OF_ARROWS = "Cordon of Arrows"
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
    ENTHRALL = "Enthrall"
    FIND_STEED = "Find Steed"
    FIND_TRAPS = "Find Traps"
    FIND_VEHICLE_UA = "Find Vehicle (UA)"
    FLAME_BLADE = "Flame Blade"
    FLAMING_SPHERE = "Flaming Sphere"
    FLOCK_OF_FAMILIARS = "Flock of Familiars"
    FORTUNES_FAVOR = "Fortune's Favor"
    GENTLE_REPOSE = "Gentle Repose"
    GIFT_OF_GAB = "Gift of Gab"
    GUST_OF_WIND = "Gust of Wind"
    HEALING_SPIRIT = "Healing Spirit"
    HEAT_METAL = "Heat Metal"
    HOLD_PERSON = "Hold Person"
    IMMOVABLE_OBJECT = "Immovable Object"
    INVISIBILITY = "Invisibility"
    JIMS_GLOWING_COIN = "Jim's Glowing Coin"
    KINETIC_JAUNT = "Kinetic Jaunt"
    KNOCK = "Knock"
    LESSER_RESTORATION = "Lesser Restoration"
    LEVITATE = "Levitate"
    LOCATE_ANIMALS_OR_PLANTS = "Locate Animals or Plants"
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
    MOONBEAM = "Moonbeam"
    NATHAIRS_MISCHIEF = "Nathair's Mischief"
    NATHAIRS_MISCHIEF_UA = "Nathair's Mischief (UA)"
    NYSTULS_MAGIC_AURA = "Nystul's Magic Aura"
    PASS_WITHOUT_TRACE = "Pass Without Trace"
    PHANTASMAL_FORCE = "Phantasmal Force"
    PRAYER_OF_HEALING = "Prayer of Healing"
    PROTECTION_FROM_POISON = "Protection from Poison"
    PYROTECHNICS = "Pyrotechnics"
    RAY_OF_ENFEEBLEMENT = "Ray of Enfeeblement"
    RIMES_BINDING_ICE = "Rime's Binding Ice"
    ROPE_TRICK = "Rope Trick"
    SCORCHING_RAY = "Scorching Ray"
    SEE_INVISIBILITY = "See Invisibility"
    SHADOW_BLADE = "Shadow Blade"
    SHATTER = "Shatter"
    SILENCE = "Silence"
    SKYWRITE = "Skywrite"
    SNILLOCS_SNOWBALL_STORM = "Snilloc's Snowball Storm"
    SPIDER_CLIMB = "Spider Climb"
    SPIKE_GROWTH = "Spike Growth"
    SPIRITUAL_WEAPON = "Spiritual Weapon"
    SPRAY_OF_CARDS = "Spray Of Cards"
    SPRAY_OF_CARDS_UA = "Spray of Cards (UA)"
    SUGGESTION = "Suggestion"
    SUMMON_BEAST = "Summon Beast"
    TASHAS_MIND_WHIP = "Tasha's Mind Whip"
    THOUGHT_SHIELD_UA = "Thought Shield (UA)"
    VORTEX_WARP = "Vortex Warp"
    WARDING_BOND = "Warding Bond"
    WARDING_WIND = "Warding Wind"
    WARP_SENSE = "Warp Sense"
    WEB = "Web"
    WITHER_AND_BLOOM = "Wither and Bloom"
    WRISTPOCKET = "Wristpocket"
    ZONE_OF_TRUTH = "Zone of Truth"


class ThirdLevel(Spell):
    ANIMATE_DEAD = "Animate Dead"
    ANTAGONIZE = "Antagonize"
    ANTAGONIZE_UA = "Antagonize (UA)"
    ASHARDALONS_STRIDE = "Ashardalon's Stride"
    AURA_OF_VITALITY = "Aura of Vitality"
    BEACON_OF_HOPE = "Beacon of Hope"
    BESTOW_CURSE = "Bestow Curse"
    BLINDING_SMITE = "Blinding Smite"
    BLINK = "Blink"
    CALL_LIGHTNING = "Call Lightning"
    CATNAP = "Catnap"
    CLAIRVOYANCE = "Clairvoyance"
    CONJURE_ANIMALS = "Conjure Animals"
    CONJURE_BARRAGE = "Conjure Barrage"
    CONJURE_LESSER_DEMON_UA = "Conjure Lesser Demon (UA)"
    COUNTERSPELL = "Counterspell"
    CREATE_FOOD_AND_WATER = "Create Food and Water"
    CRUSADERS_MANTLE = "Crusader's Mantle"
    DAYLIGHT = "Daylight"
    DISPEL_MAGIC = "Dispel Magic"
    ELEMENTAL_WEAPON = "Elemental Weapon"
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
    HUNGER_OF_HADAR = "Hunger Of Hadar"
    HYPNOTIC_PATTERN = "Hypnotic Pattern"
    INCITE_GREED = "Incite Greed"
    INTELLECT_FORTRESS = "Intellect Fortress"
    INVISIBILITY_TO_CAMERAS_UA = "Invisibility To Cameras (UA)"
    LEOMUNDS_TINY_HUT = "Leomund's Tiny Hut"
    LIFE_TRANSFERENCE = "Life Transference"
    LIGHTNING_ARROW = "Lightning Arrow"
    LIGHTNING_BOLT = "Lightning Bolt"
    MAGIC_CIRCLE = "Magic Circle"
    MAJOR_IMAGE = "Major Image"
    MASS_HEALING_WORD = "Mass Healing Word"
    MELD_INTO_STONE = "Meld into Stone"
    MELFS_MINUTE_METEORS = "Melf's Minute Meteors"
    MOTIVATIONAL_SPEECH = "Motivational Speech"
    NONDETECTION = "Nondetection"
    PHANTOM_STEED = "Phantom Steed"
    PLANT_GROWTH = "Plant Growth"
    PROTECTION_FROM_BALLISTICS_UA = "Protection from Ballistics (UA)"
    PROTECTION_FROM_ENERGY = "Protection from Energy"
    PSIONIC_BLAST_UA = "Psionic Blast (UA)"
    REMOVE_CURSE = "Remove Curse"
    REVIVIFY = "Revivify"
    SENDING = "Sending"
    SLEET_STORM = "Sleet Storm"
    SLOW = "Slow"
    SPEAK_WITH_DEAD = "Speak with Dead"
    SPEAK_WITH_PLANTS = "Speak with Plants"
    SPIRIT_GUARDIANS = "Spirit Guardians"
    SPIRIT_SHROUD = "Spirit Shroud"
    STINKING_CLOUD = "Stinking Cloud"
    SUMMON_FEY = "Summon Fey"
    SUMMON_LESSER_DEMONS = "Summon Lesser Demons"
    SUMMON_SHADOWSPAWN = "Summon Shadowspawn"
    SUMMON_UNDEAD = "Summon Undead"
    SUMMON_WARRIOR_SPIRIT_UA = "Summon Warrior Spirit (UA)"
    THUNDER_STEP = "Thunder Step"
    TIDAL_WAVE = "Tidal Wave"
    TINY_SERVANT = "Tiny Servant"
    TONGUES = "Tongues"
    VAMPIRIC_TOUCH = "Vampiric Touch"
    WALL_OF_SAND = "Wall of Sand"
    WALL_OF_WATER = "Wall of Water"
    WATER_BREATHING = "Water Breathing"
    WATER_WALK = "Water Walk"
    WIND_WALL = "Wind Wall"


class FourthLevel(Spell):
    ARCANE_EYE = "Arcane Eye"
    AURA_OF_LIFE = "Aura of Life"
    AURA_OF_PURITY = "Aura of Purity"
    BANISHMENT = "Banishment"
    BLIGHT = "Blight"
    CHARM_MONSTER = "Charm Monster"
    COMPULSION = "Compulsion"
    CONFUSION = "Confusion"
    CONJURE_BARLGURA_UA = "Conjure Barlgura (UA)"
    CONJURE_KNOWBOT_UA = "Conjure Knowbot (UA)"
    CONJURE_MINOR_ELEMENTALS = "Conjure Minor Elementals"
    CONJURE_SHADOW_DEMON_UA = "Conjure Shadow Demon (UA)"
    CONJURE_WOODLAND_BEINGS = "Conjure Woodland Beings"
    CONTROL_WATER = "Control Water"
    DEATH_WARD = "Death Ward"
    DIMENSION_DOOR = "Dimension Door"
    DIVINATION = "Divination"
    DOMINATE_BEAST = "Dominate Beast"
    EGO_WHIP_UA = "Ego Whip (UA)"
    ELEMENTAL_BANE = "Elemental Bane"
    EVARDS_BLACK_TENTACLES = "Evard's Black Tentacles"
    FABRICATE = "Fabricate"
    FIND_GREATER_STEED = "Find Greater Steed"
    FIRE_SHIELD = "Fire Shield"
    FREEDOM_OF_MOVEMENT = "Freedom of Movement"
    GALDERS_SPEEDY_COURIER = "Galder's Speedy Courier"
    GATE_SEAL = "Gate Seal"
    GIANT_INSECT = "Giant Insect"
    GRASPING_VINE = "Grasping Vine"
    GRAVITY_SINKHOLE = "Gravity Sinkhole"
    GREATER_INVISIBILITY = "Greater Invisibility"
    GUARDIAN_OF_FAITH = "Guardian of Faith"
    GUARDIAN_OF_NATURE = "Guardian of Nature"
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
    SHADOW_OF_MOIL = "Shadow of Moil"
    SICKENING_RADIANCE = "Sickening Radiance"
    SPIRIT_OF_DEATH = "Spirit of Death"
    SPIRIT_OF_DEATH_UA = "Spirit of Death (UA)"
    STAGGERING_SMITE = "Staggering Smite"
    STONE_SHAPE = "Stone Shape"
    STONESKIN = "Stoneskin"
    STORM_SPHERE = "Storm Sphere"
    SUMMON_ABERRATION = "Summon Aberration"
    SUMMON_CONSTRUCT = "Summon Construct"
    SUMMON_ELEMENTAL = "Summon Elemental"
    SUMMON_GREATER_DEMON = "Summon Greater Demon"
    SYNCHRONICITY_UA = "Synchronicity (UA)"
    SYSTEM_BACKDOOR_UA = "System Backdoor (UA)"
    VITRIOLIC_SPHERE = "Vitriolic Sphere"
    WALL_OF_FIRE = "Wall of Fire"
    WATERY_SPHERE = "Watery Sphere"
    WIDOGASTS_VAULT_OF_AMBER_HB = "Widogast's Vault of Amber (HB)"
    WIDOGASTS_WEB_OF_FIRE_HB = "Widogast's Web of Fire (HB)"


class FifthLevel(Spell):
    ANIMATE_OBJECTS = "Animate Objects"
    ANTILIFE_SHELL = "Antilife Shell"
    AWAKEN = "Awaken"
    BANISHING_SMITE = "Banishing Smite"
    BIGBYS_HAND = "Bigby's Hand"
    CIRCLE_OF_POWER = "Circle of Power"
    CLOUDKILL = "Cloudkill"
    COMMUNE = "Commune"
    COMMUNE_WITH_CITY_UA = "Commune with City (UA)"
    COMMUNE_WITH_NATURE = "Commune with Nature"
    CONE_OF_COLD = "Cone of Cold"
    CONJURE_ELEMENTAL = "Conjure Elemental"
    CONJURE_VOLLEY = "Conjure Volley"
    CONJURE_VROCK_UA = "Conjure Vrock (UA)"
    CONTACT_OTHER_PLANE = "Contact Other Plane"
    CONTAGION = "Contagion"
    CONTROL_WINDS = "Control Winds"
    CREATE_SPELLJAMMING_HELM = "Create Spelljamming Helm"
    CREATION = "Creation"
    DANSE_MACABRE = "Danse Macabre"
    DAWN = "Dawn"
    DESTRUCTIVE_WAVE = "Destructive Wave"
    DISPEL_EVIL_AND_GOOD = "Dispel Evil and Good"
    DOMINATE_PERSON = "Dominate Person"
    DREAM = "Dream"
    ENERVATION = "Enervation"
    FAR_STEP = "Far Step"
    FLAME_STRIKE = "Flame Strike"
    FREEDOM_OF_THE_WINDS_HB = "Freedom of the Winds (HB)"
    GEAS = "Geas"
    GREATER_RESTORATION = "Greater Restoration"
    HALLOW = "Hallow"
    HOLD_MONSTER = "Hold Monster"
    HOLY_WEAPON = "Holy Weapon"
    IMMOLATION = "Immolation"
    INFERNAL_CALLING = "Infernal Calling"
    INSECT_PLAGUE = "Insect Plague"
    LEGEND_LORE = "Legend Lore"
    MAELSTROM = "Maelstrom"
    MASS_CURE_WOUNDS = "Mass Cure Wounds"
    MISLEAD = "Mislead"
    MODIFY_MEMORY = "Modify Memory"
    NEGATIVE_ENERGY_FLOOD = "Negative Energy Flood"
    PASSWALL = "Passwall"
    PLANAR_BINDING = "Planar Binding"
    RAISE_DEAD = "Raise Dead"
    RARYS_TELEPATHIC_BOND = "Rary's Telepathic Bond"
    REINCARNATE = "Reincarnate"
    SCRYING = "Scrying"
    SEEMING = "Seeming"
    SHUTDOWN_UA = "Shutdown (UA)"
    SKILL_EMPOWERMENT = "Skill Empowerment"
    STEEL_WIND_STRIKE = "Steel Wind Strike"
    SUMMON_CELESTIAL = "Summon Celestial"
    SUMMON_DRACONIC_SPIRIT = "Summon Draconic Spirit"
    SUMMON_DRACONIC_SPIRIT_UA = "Summon Draconic Spirit (UA)"
    SWIFT_QUIVER = "Swift Quiver"
    SYNAPTIC_STATIC = "Synaptic Static"
    TELEKINESIS = "Telekinesis"
    TELEPORTATION_CIRCLE = "Teleportation Circle"
    TEMPORAL_SHUNT = "Temporal Shunt"
    TRANSMUTE_ROCK = "Transmute Rock"
    TREE_STRIDE = "Tree Stride"
    WALL_OF_FORCE = "Wall of Force"
    WALL_OF_LIGHT = "Wall of Light"
    WALL_OF_STONE = "Wall of Stone"
    WRATH_OF_NATURE = "Wrath Of Nature"


class SixthLevel(Spell):
    OTILUKES_FREEZING_SPHERE = auto()
    TRUE_SEEING = auto()
    ARCANE_GATE = "Arcane Gate"
    BLADE_BARRIER = "Blade Barrier"
    BONES_OF_THE_EARTH = "Bones of the Earth"
    CHAIN_LIGHTNING = "Chain Lightning"
    CIRCLE_OF_DEATH = "Circle of Death"
    CONJURE_FEY = "Conjure Fey"
    CONTINGENCY = "Contingency"
    CREATE_HOMUNCULUS = "Create Homunculus"
    CREATE_UNDEAD = "Create Undead"
    DISINTEGRATE = "Disintegrate"
    DRAWMIJS_INSTANT_SUMMONS = "Drawmij's Instant Summons"
    DRUID_GROVE = "Druid Grove"
    EYEBITE = "Eyebite"
    FIND_THE_PATH = "Find the Path"
    FIZBANS_PLATINUM_SHIELD = "Fizban's Platinum Shield"
    FIZBANS_PLATINUM_SHIELD_UA = "Fizban's Platinum Shield (UA)"
    FLESH_TO_STONE = "Flesh to Stone"
    FORBIDDANCE = "Forbiddance"
    GLOBE_OF_INVULNERABILITY = "Globe of Invulnerability"
    GRAVITY_FISSURE = "Gravity Fissure"
    GUARDS_AND_WARDS = "Guards and Wards"
    HARM = "Harm"
    HEAL = "Heal"
    HEROES_FEAST = "Heroes' Feast"
    INVESTITURE_OF_FLAME = "Investiture of Flame"
    INVESTITURE_OF_ICE = "Investiture of Ice"
    INVESTITURE_OF_STONE = "Investiture of Stone"
    INVESTITURE_OF_WIND = "Investiture of Wind"
    MAGIC_JAR = "Magic Jar"
    MASS_SUGGESTION = "Mass Suggestion"
    MENTAL_PRISON = "Mental Prison"
    MOVE_EARTH = "Move Earth"
    OTHERWORLDLY_FORM_UA = "Otherworldly Form (UA)"
    OTIULKES_FREEZING_SPHERE = "Otiluke's Freezing Sphere"
    OTTOS_IRRESISTIBLE_DANCE = "Otto's Irresistible Dance"
    PLANAR_ALLY = "Planar Ally"
    PRIMORDIAL_WARD = "Primordial Ward"
    PROGRAMMED_ILLUSION = "Programmed Illusion"
    PSYCHIC_CRUSH_UA = "Psychic Crush (UA)"
    SCATTER = "Scatter"
    SOUL_CAGE = "Soul Cage"
    SUMMON_FIEND = "Summon Fiend"
    SUNBEAM = "Sunbeam"
    TASHAS_OTHERWORLDLY_GUISE = "Tasha's Otherworldly Guise"
    TENSERS_TRANSFORMATION = "Tenser's Transformation"
    TRANSPORT_VIA_PLANTS = "Transport via Plants"
    TRUE_SIGHT = "True Seeing"
    WALL_OF_ICE = "Wall of Ice"
    WALL_OF_THORNS = "Wall of Thorns"
    WIDOGASTS_TRANSMOGRIFICATION_HB = "Widogast's Transmogrification (HB)"
    WIND_WALK = "Wind Walk"
    WORD_OF_RECALL = "Word of Recall"


class SeventhLevel(Spell):
    CONJURE_CELESTIAL = "Conjure Celestial"
    CONJURE_HEZROU_UA = "Conjure Hezrou (UA)"
    CREATE_MAGEN = "Create Magen"
    CROWN_OF_STARS = "Crown of Stars"
    DELAYED_BLAST_FIREBALL = "Delayed Blast Fireball"
    DIVINE_WORD = "Divine Word"
    DRACONIC_TRANSFORMATION = "Draconic Transformation"
    DRACONIC_TRANSFORMATION_UA = "Draconic Transformation (UA)"
    DREAM_OF_THE_BLUE_VEIL = "Dream of the Blue Veil"
    ETHEREALNESS = "Etherealness"
    FINGER_OF_DEATH = "Finger of Death"
    FIRE_STORM = "Fire Storm"
    FORCECAGE = "Forcecage"
    MIRAGE_ARCANE = "Mirage Arcane"
    MORDENKAINENS_MAGNIFICENT_MANSION = "Mordenkainen's Magnificent Mansion"
    MORDENKAINENS_SWORD = "Mordenkainen's Sword"
    PLANE_SHIFT = "Plane Shift"
    POWER_WORD_PAIN = "Power Word: Pain"
    PRISMATIC_SPRAY = "Prismatic Spray"
    PROJECT_IMAGE = "Project Image"
    REGENERATE = "Regenerate"
    RESURRECTION = "Resurrection"
    REVERSE_GRAVITY = "Reverse Gravity"
    SEQUESTER = "Sequester"
    SIMULACRUM = "Simulacrum"
    SYMBOL = "Symbol"
    TELEPORT = "Teleport"
    TEMPLE_OF_THE_GODS = "Temple of the Gods"
    TETHER_ESSENCE = "Tether Essence"
    WHIRLWIND = "Whirlwind"


class EighthLevel(Spell):
    ABI_DALZIMS_HORRID_WILTING = "Abi-Dalzim's Horrid Wilting"
    ANIMAL_SHAPES = "Animal Shapes"
    ANTIMAGIC_FIELD = "Antimagic Field"
    ANTIPATHY_SYMPATHY = "Antipathy/Sympathy"
    CLONE = "Clone"
    CONTROL_WEATHER = "Control Weather"
    DARK_STAR = "Dark Star"
    DEMIPLANE = "Demiplane"
    DOMINATE_MONSTER = "Dominate Monster"
    EARTHQUAKE = "Earthquake"
    FEEBLEMIND = "Feeblemind"
    GLIBNESS = "Glibness"
    HOLY_AURA = "Holy Aura"
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
    TSUNAMI = "Tsunami"


class NinthLevel(Spell):
    ASTRAL_PROJECTION = "Astral Projection"
    BLADE_OF_DISASTER = "Blade of Disaster"
    FORESIGHT = "Foresight"
    GATE = "Gate"
    IMPRISONMENT = "Imprisonment"
    INVULNERABILITY = "Invulnerability"
    MASS_HEAL = "Mass Heal"
    MASS_POLYMORPH = "Mass Polymorph"
    METEOR_SWARM = "Meteor Swarm"
    POWER_WORD_HEAL = "Power Word: Heal"
    POWER_WORD_KILL = "Power Word: Kill"
    PRISMATIC_WALL = "Prismatic Wall"
    PSYCHIC_SCREAM = "Psychic Scream"
    RAVENOUS_VOID = "Ravenous Void"
    SHAPECHANGE = "Shapechange"
    STORM_OF_VENGEANCE = "Storm of Vengeance"
    TIME_RAVAGE = "Time Ravage"
    TIME_STOP = "Time Stop"
    TRUE_POLYMORPH = "True Polymorph"
    TRUE_RESURRECTION = "True Resurrection"
    WEIRD = "Weird"
    WISH = "Wish"


SPELLS_BY_CLASS = frozendict(
    {
        Class.ARTIFICER: frozendict(
            {
                Cantrip: frozenset(
                    {
                        Cantrip.ACID_SPLASH,
                        Cantrip.BOOMING_BLADE,
                        Cantrip.CREATE_BONFIRE,
                        Cantrip.DANCING_LIGHTS,
                        Cantrip.FIRE_BOLT,
                        Cantrip.FROSTBITE,
                        Cantrip.GREEN_FLAME_BLADE,
                        Cantrip.GUIDANCE,
                        Cantrip.LIGHT,
                        Cantrip.LIGHTNING_LURE,
                        Cantrip.MAGE_HAND,
                        Cantrip.MAGIC_STONE,
                        Cantrip.MENDING,
                        Cantrip.MESSAGE,
                        Cantrip.POISON_SPRAY,
                        Cantrip.PRESTIDIGITATION,
                        Cantrip.RAY_OF_FROST,
                        Cantrip.RESISTANCE,
                        Cantrip.SHOCKING_GRASP,
                        Cantrip.SPARE_THE_DYING,
                        Cantrip.SWORD_BURST,
                        Cantrip.THORN_WHIP,
                        Cantrip.THUNDERCLAP,
                    }
                ),
                FirstLevel: frozenset(
                    {
                        FirstLevel.ABSORB_ELEMENTS,
                        FirstLevel.ALARM,
                        FirstLevel.CATAPULT,
                        FirstLevel.CURE_WOUNDS,
                        FirstLevel.DETECT_MAGIC,
                        FirstLevel.DISGUISE_SELF,
                        FirstLevel.EXPEDITIOUS_RETREAT,
                        FirstLevel.FAERIE_FIRE,
                        FirstLevel.FALSE_LIFE,
                        FirstLevel.FEATHER_FALL,
                        FirstLevel.GREASE,
                        FirstLevel.IDENTIFY,
                        FirstLevel.JUMP,
                        FirstLevel.LONGSTRIDER,
                        FirstLevel.PURIFY_FOOD_AND_DRINK,
                        FirstLevel.SANCTUARY,
                        FirstLevel.SNARE,
                        FirstLevel.TASHAS_CAUSTIC_BREW,
                    }
                ),
                SecondLevel: frozenset(
                    {
                        SecondLevel.AID,
                        SecondLevel.AIR_BUBBLE,
                        SecondLevel.ALTER_SELF,
                        SecondLevel.ARCANE_LOCK,
                        SecondLevel.BLUR,
                        SecondLevel.CONTINUAL_FLAME,
                        SecondLevel.DARKVISION,
                        SecondLevel.ENHANCE_ABILITY,
                        SecondLevel.ENLARGE_REDUCE,
                        SecondLevel.HEAT_METAL,
                        SecondLevel.INVISIBILITY,
                        SecondLevel.KINETIC_JAUNT,
                        SecondLevel.LESSER_RESTORATION,
                        SecondLevel.LEVITATE,
                        SecondLevel.MAGIC_MOUTH,
                        SecondLevel.MAGIC_WEAPON,
                        SecondLevel.PROTECTION_FROM_POISON,
                        SecondLevel.PYROTECHNICS,
                        SecondLevel.ROPE_TRICK,
                        SecondLevel.SEE_INVISIBILITY,
                        SecondLevel.SKYWRITE,
                        SecondLevel.SPIDER_CLIMB,
                        SecondLevel.VORTEX_WARP,
                        SecondLevel.WEB,
                    }
                ),
                ThirdLevel: frozenset(
                    {
                        ThirdLevel.ASHARDALONS_STRIDE,
                        ThirdLevel.BLINK,
                        ThirdLevel.CATNAP,
                        ThirdLevel.CREATE_FOOD_AND_WATER,
                        ThirdLevel.DISPEL_MAGIC,
                        ThirdLevel.ELEMENTAL_WEAPON,
                        ThirdLevel.FLAME_ARROWS,
                        ThirdLevel.FLAME_STRIDE_UA,
                        ThirdLevel.FLY,
                        ThirdLevel.GLYPH_OF_WARDING,
                        ThirdLevel.HASTE,
                        ThirdLevel.INTELLECT_FORTRESS,
                        ThirdLevel.PROTECTION_FROM_ENERGY,
                        ThirdLevel.REVIVIFY,
                        ThirdLevel.TINY_SERVANT,
                        ThirdLevel.WATER_BREATHING,
                        ThirdLevel.WATER_WALK,
                    }
                ),
                FourthLevel: frozenset(
                    {
                        FourthLevel.ARCANE_EYE,
                        FourthLevel.ELEMENTAL_BANE,
                        FourthLevel.FABRICATE,
                        FourthLevel.FREEDOM_OF_MOVEMENT,
                        FourthLevel.LEOMUNDS_SECRET_CHEST,
                        FourthLevel.MORDENKAINENS_FAITHFUL_HOUND,
                        FourthLevel.MORDENKAINENS_PRIVATE_SANCTUM,
                        FourthLevel.OTILUKES_RESILIENT_SPHERE,
                        FourthLevel.STONE_SHAPE,
                        FourthLevel.STONESKIN,
                        FourthLevel.SUMMON_CONSTRUCT,
                    }
                ),
                FifthLevel: frozenset(
                    {
                        FifthLevel.ANIMATE_OBJECTS,
                        FifthLevel.BIGBYS_HAND,
                        FifthLevel.CREATE_SPELLJAMMING_HELM,
                        FifthLevel.CREATION,
                        FifthLevel.GREATER_RESTORATION,
                        FifthLevel.SKILL_EMPOWERMENT,
                        FifthLevel.TRANSMUTE_ROCK,
                        FifthLevel.WALL_OF_STONE,
                    }
                ),
            }
        ),
        Class.BARD: frozendict(
            {
                Cantrip: frozenset(
                    {
                        Cantrip.BLADE_WARD,
                        Cantrip.DANCING_LIGHTS,
                        Cantrip.FRIENDS,
                        Cantrip.LIGHT,
                        Cantrip.MAGE_HAND,
                        Cantrip.MENDING,
                        Cantrip.MESSAGE,
                        Cantrip.MINOR_ILLUSION,
                        Cantrip.PRESTIDIGITATION,
                        Cantrip.THUNDERCLAP,
                        Cantrip.TRUE_STRIKE,
                        Cantrip.VICIOUS_MOCKERY,
                    }
                ),
                FirstLevel: frozenset(
                    {
                        FirstLevel.ANIMAL_FRIENDSHIP,
                        FirstLevel.BANE,
                        FirstLevel.CHARM_PERSON,
                        FirstLevel.COMPREHEND_LANGUAGES,
                        FirstLevel.CURE_WOUNDS,
                        FirstLevel.DETECT_MAGIC,
                        FirstLevel.DISGUISE_SELF,
                        FirstLevel.DISSONANT_WHISPERS,
                        FirstLevel.DISTORT_VALUE,
                        FirstLevel.EARTH_TREMOR,
                        FirstLevel.FAERIE_FIRE,
                        FirstLevel.FEATHER_FALL,
                        FirstLevel.HEALING_WORD,
                        FirstLevel.HEROISM,
                        FirstLevel.IDENTIFY,
                        FirstLevel.ILLUSORY_SCRIPT,
                        FirstLevel.LONGSTRIDER,
                        FirstLevel.SILENT_IMAGE,
                        FirstLevel.SILVERY_BARBS,
                        FirstLevel.SLEEP,
                        FirstLevel.SPEAK_WITH_ANIMALS,
                        FirstLevel.TASHAS_HIDEOUS_LAUGHTER,
                        FirstLevel.THUNDERWAVE,
                        FirstLevel.UNSEEN_SERVANT,
                    }
                ),
                SecondLevel: frozenset(
                    {
                        SecondLevel.ANIMAL_MESSENGER,
                        SecondLevel.BLINDNESS_DEAFNESS,
                        SecondLevel.BORROWED_KNOWLEDGE,
                        SecondLevel.CALM_EMOTIONS,
                        SecondLevel.CLOUD_OF_DAGGERS,
                        SecondLevel.CROWN_OF_MADNESS,
                        SecondLevel.DETECT_THOUGHTS,
                        SecondLevel.ENHANCE_ABILITY,
                        SecondLevel.ENTHRALL,
                        SecondLevel.GIFT_OF_GAB,
                        SecondLevel.HEAT_METAL,
                        SecondLevel.HOLD_PERSON,
                        SecondLevel.INVISIBILITY,
                        SecondLevel.KINETIC_JAUNT,
                        SecondLevel.KNOCK,
                        SecondLevel.LESSER_RESTORATION,
                        SecondLevel.LOCATE_ANIMALS_OR_PLANTS,
                        SecondLevel.LOCATE_OBJECT,
                        SecondLevel.MAGIC_MOUTH,
                        SecondLevel.NATHAIRS_MISCHIEF,
                        SecondLevel.NATHAIRS_MISCHIEF_UA,
                        SecondLevel.PHANTASMAL_FORCE,
                        SecondLevel.PYROTECHNICS,
                        SecondLevel.SEE_INVISIBILITY,
                        SecondLevel.SHATTER,
                        SecondLevel.SILENCE,
                        SecondLevel.SKYWRITE,
                        SecondLevel.SPRAY_OF_CARDS,
                        SecondLevel.SPRAY_OF_CARDS_UA,
                        SecondLevel.SUGGESTION,
                        SecondLevel.WARDING_WIND,
                        SecondLevel.ZONE_OF_TRUTH,
                    }
                ),
                ThirdLevel: frozenset(
                    {
                        ThirdLevel.ANTAGONIZE,
                        ThirdLevel.ANTAGONIZE_UA,
                        ThirdLevel.BESTOW_CURSE,
                        ThirdLevel.CATNAP,
                        ThirdLevel.CLAIRVOYANCE,
                        ThirdLevel.DISPEL_MAGIC,
                        ThirdLevel.ENEMIES_ABOUND,
                        ThirdLevel.FAST_FRIENDS,
                        ThirdLevel.FEAR,
                        ThirdLevel.FEIGN_DEATH,
                        ThirdLevel.GLYPH_OF_WARDING,
                        ThirdLevel.HYPNOTIC_PATTERN,
                        ThirdLevel.LEOMUNDS_TINY_HUT,
                        ThirdLevel.MAJOR_IMAGE,
                        ThirdLevel.MOTIVATIONAL_SPEECH,
                        ThirdLevel.NONDETECTION,
                        ThirdLevel.PLANT_GROWTH,
                        ThirdLevel.SENDING,
                        ThirdLevel.SPEAK_WITH_DEAD,
                        ThirdLevel.SPEAK_WITH_PLANTS,
                        ThirdLevel.STINKING_CLOUD,
                        ThirdLevel.TONGUES,
                    }
                ),
                FourthLevel: frozenset(
                    {
                        FourthLevel.CHARM_MONSTER,
                        FourthLevel.COMPULSION,
                        FourthLevel.CONFUSION,
                        FourthLevel.DIMENSION_DOOR,
                        FourthLevel.EGO_WHIP_UA,
                        FourthLevel.FREEDOM_OF_MOVEMENT,
                        FourthLevel.GREATER_INVISIBILITY,
                        FourthLevel.HALLUCINATORY_TERRAIN,
                        FourthLevel.LOCATE_CREATURE,
                        FourthLevel.POLYMORPH,
                        FourthLevel.RAULOTHIMS_PSYCHIC_LANCE,
                        FourthLevel.RAULOTHIMS_PSYCHIC_LANCE_UA,
                    }
                ),
                FifthLevel: frozenset(
                    {
                        FifthLevel.ANIMATE_OBJECTS,
                        FifthLevel.AWAKEN,
                        FifthLevel.DOMINATE_PERSON,
                        FifthLevel.DREAM,
                        FifthLevel.GEAS,
                        FifthLevel.GREATER_RESTORATION,
                        FifthLevel.HOLD_MONSTER,
                        FifthLevel.LEGEND_LORE,
                        FifthLevel.MASS_CURE_WOUNDS,
                        FifthLevel.MISLEAD,
                        FifthLevel.MODIFY_MEMORY,
                        FifthLevel.PLANAR_BINDING,
                        FifthLevel.RAISE_DEAD,
                        FifthLevel.SCRYING,
                        FifthLevel.SEEMING,
                        FifthLevel.SKILL_EMPOWERMENT,
                        FifthLevel.SYNAPTIC_STATIC,
                        FifthLevel.TELEPORTATION_CIRCLE,
                    }
                ),
                SixthLevel: frozenset(
                    {
                        SixthLevel.EYEBITE,
                        SixthLevel.FIND_THE_PATH,
                        SixthLevel.GUARDS_AND_WARDS,
                        SixthLevel.MASS_SUGGESTION,
                        SixthLevel.OTTOS_IRRESISTIBLE_DANCE,
                        SixthLevel.PROGRAMMED_ILLUSION,
                        SixthLevel.TRUE_SEEING,
                    }
                ),
                SeventhLevel: frozenset(
                    {
                        SeventhLevel.ETHEREALNESS,
                        SeventhLevel.FORCECAGE,
                        SeventhLevel.MIRAGE_ARCANE,
                        SeventhLevel.MORDENKAINENS_MAGNIFICENT_MANSION,
                        SeventhLevel.MORDENKAINENS_SWORD,
                        SeventhLevel.PRISMATIC_SPRAY,
                        SeventhLevel.PROJECT_IMAGE,
                        SeventhLevel.REGENERATE,
                        SeventhLevel.RESURRECTION,
                        SeventhLevel.SYMBOL,
                        SeventhLevel.TELEPORT,
                    }
                ),
                EighthLevel: frozenset(
                    {
                        EighthLevel.DOMINATE_MONSTER,
                        EighthLevel.FEEBLEMIND,
                        EighthLevel.GLIBNESS,
                        EighthLevel.MIND_BLANK,
                        EighthLevel.POWER_WORD_STUN,
                    }
                ),
                NinthLevel: frozenset(
                    {
                        NinthLevel.FORESIGHT,
                        NinthLevel.MASS_POLYMORPH,
                        NinthLevel.POWER_WORD_HEAL,
                        NinthLevel.POWER_WORD_KILL,
                        NinthLevel.PSYCHIC_SCREAM,
                        NinthLevel.TRUE_POLYMORPH,
                    }
                ),
            }
        ),
        Class.CLERIC: frozendict(
            {
                Cantrip: frozenset(
                    {
                        Cantrip.DECOMPOSE,
                        Cantrip.GUIDANCE,
                        Cantrip.HAND_OF_RADIANCE,
                        Cantrip.LIGHT,
                        Cantrip.MENDING,
                        Cantrip.RESISTANCE,
                        Cantrip.SACRED_FLAME,
                        Cantrip.SPARE_THE_DYING,
                        Cantrip.THAUMATURGY,
                        Cantrip.TOLL_THE_DEAD,
                        Cantrip.VIRTUE,
                        Cantrip.WORD_OF_RADIANCE,
                    }
                ),
                FirstLevel: frozenset(
                    {
                        FirstLevel.BANE,
                        FirstLevel.BLESS,
                        FirstLevel.CEREMONY,
                        FirstLevel.COMMAND,
                        FirstLevel.CREATE_OR_DESTROY_WATER,
                        FirstLevel.CURE_WOUNDS,
                        FirstLevel.DETECT_EVIL_AND_GOOD,
                        FirstLevel.DETECT_MAGIC,
                        FirstLevel.DETECT_POISON_AND_DISEASE,
                        FirstLevel.GUIDING_BOLT,
                        FirstLevel.HEALING_WORD,
                        FirstLevel.INFLICT_WOUNDS,
                        FirstLevel.PROTECTION_FROM_EVIL_AND_GOOD,
                        FirstLevel.PURIFY_FOOD_AND_DRINK,
                        FirstLevel.SANCTUARY,
                        FirstLevel.SHIELD_OF_FAITH,
                    }
                ),
                SecondLevel: frozenset(
                    {
                        SecondLevel.AID,
                        SecondLevel.AUGURY,
                        SecondLevel.BLINDNESS_DEAFNESS,
                        SecondLevel.BORROWED_KNOWLEDGE,
                        SecondLevel.CALM_EMOTIONS,
                        SecondLevel.CONTINUAL_FLAME,
                        SecondLevel.ENHANCE_ABILITY,
                        SecondLevel.FIND_TRAPS,
                        SecondLevel.GENTLE_REPOSE,
                        SecondLevel.HOLD_PERSON,
                        SecondLevel.LESSER_RESTORATION,
                        SecondLevel.LOCATE_OBJECT,
                        SecondLevel.PRAYER_OF_HEALING,
                        SecondLevel.PROTECTION_FROM_POISON,
                        SecondLevel.SILENCE,
                        SecondLevel.SPIRITUAL_WEAPON,
                        SecondLevel.WARDING_BOND,
                        SecondLevel.ZONE_OF_TRUTH,
                    }
                ),
                ThirdLevel: frozenset(
                    {
                        ThirdLevel.ANIMATE_DEAD,
                        ThirdLevel.BEACON_OF_HOPE,
                        ThirdLevel.BESTOW_CURSE,
                        ThirdLevel.CLAIRVOYANCE,
                        ThirdLevel.CREATE_FOOD_AND_WATER,
                        ThirdLevel.DAYLIGHT,
                        ThirdLevel.DISPEL_MAGIC,
                        ThirdLevel.FAST_FRIENDS,
                        ThirdLevel.FEIGN_DEATH,
                        ThirdLevel.GLYPH_OF_WARDING,
                        ThirdLevel.INCITE_GREED,
                        ThirdLevel.LIFE_TRANSFERENCE,
                        ThirdLevel.MAGIC_CIRCLE,
                        ThirdLevel.MASS_HEALING_WORD,
                        ThirdLevel.MELD_INTO_STONE,
                        ThirdLevel.MOTIVATIONAL_SPEECH,
                        ThirdLevel.PROTECTION_FROM_ENERGY,
                        ThirdLevel.REMOVE_CURSE,
                        ThirdLevel.REVIVIFY,
                        ThirdLevel.SENDING,
                        ThirdLevel.SPEAK_WITH_DEAD,
                        ThirdLevel.SPIRIT_GUARDIANS,
                        ThirdLevel.TONGUES,
                        ThirdLevel.WATER_WALK,
                    }
                ),
                FourthLevel: frozenset(
                    {
                        FourthLevel.BANISHMENT,
                        FourthLevel.CONTROL_WATER,
                        FourthLevel.DEATH_WARD,
                        FourthLevel.DIVINATION,
                        FourthLevel.FREEDOM_OF_MOVEMENT,
                        FourthLevel.GUARDIAN_OF_FAITH,
                        FourthLevel.LOCATE_CREATURE,
                        FourthLevel.STONE_SHAPE,
                    }
                ),
                FifthLevel: frozenset(
                    {
                        FifthLevel.COMMUNE,
                        FifthLevel.CONTAGION,
                        FifthLevel.DAWN,
                        FifthLevel.DISPEL_EVIL_AND_GOOD,
                        FifthLevel.FLAME_STRIKE,
                        FifthLevel.GEAS,
                        FifthLevel.GREATER_RESTORATION,
                        FifthLevel.HALLOW,
                        FifthLevel.HOLY_WEAPON,
                        FifthLevel.INSECT_PLAGUE,
                        FifthLevel.LEGEND_LORE,
                        FifthLevel.MASS_CURE_WOUNDS,
                        FifthLevel.PLANAR_BINDING,
                        FifthLevel.RAISE_DEAD,
                        FifthLevel.SCRYING,
                    }
                ),
                SixthLevel: frozenset(
                    {
                        SixthLevel.BLADE_BARRIER,
                        SixthLevel.CREATE_UNDEAD,
                        SixthLevel.FIND_THE_PATH,
                        SixthLevel.FORBIDDANCE,
                        SixthLevel.HARM,
                        SixthLevel.HEAL,
                        SixthLevel.HEROES_FEAST,
                        SixthLevel.OTHERWORLDLY_FORM_UA,
                        SixthLevel.PLANAR_ALLY,
                        SixthLevel.TRUE_SEEING,
                        SixthLevel.WORD_OF_RECALL,
                    }
                ),
                SeventhLevel: frozenset(
                    {
                        SeventhLevel.CONJURE_CELESTIAL,
                        SeventhLevel.DIVINE_WORD,
                        SeventhLevel.ETHEREALNESS,
                        SeventhLevel.FIRE_STORM,
                        SeventhLevel.PLANE_SHIFT,
                        SeventhLevel.REGENERATE,
                        SeventhLevel.RESURRECTION,
                        SeventhLevel.SYMBOL,
                        SeventhLevel.TEMPLE_OF_THE_GODS,
                    }
                ),
                EighthLevel: frozenset(
                    {
                        EighthLevel.ANTIMAGIC_FIELD,
                        EighthLevel.CONTROL_WEATHER,
                        EighthLevel.EARTHQUAKE,
                        EighthLevel.HOLY_AURA,
                    }
                ),
                NinthLevel: frozenset(
                    {
                        NinthLevel.ASTRAL_PROJECTION,
                        NinthLevel.GATE,
                        NinthLevel.MASS_HEAL,
                        NinthLevel.TRUE_RESURRECTION,
                    }
                ),
            }
        ),
        Class.DRUID: frozendict(
            {
                Cantrip: frozenset(
                    {
                        Cantrip.CONTROL_FLAMES,
                        Cantrip.CREATE_BONFIRE,
                        Cantrip.DRUIDCRAFT,
                        Cantrip.FROSTBITE,
                        Cantrip.GUIDANCE,
                        Cantrip.GUST,
                        Cantrip.INFESTATION,
                        Cantrip.MAGIC_STONE,
                        Cantrip.MENDING,
                        Cantrip.MOLD_EARTH,
                        Cantrip.POISON_SPRAY,
                        Cantrip.PRIMAL_SAVAGERY,
                        Cantrip.PRODUCE_FLAME,
                        Cantrip.RESISTANCE,
                        Cantrip.SHAPE_WATER,
                        Cantrip.SHILLELAGH,
                        Cantrip.THORN_WHIP,
                        Cantrip.THUNDERCLAP,
                    }
                ),
                FirstLevel: frozenset(
                    {
                        FirstLevel.ABSORB_ELEMENTS,
                        FirstLevel.ANIMAL_FRIENDSHIP,
                        FirstLevel.BEAST_BOND,
                        FirstLevel.CHARM_PERSON,
                        FirstLevel.CREATE_OR_DESTROY_WATER,
                        FirstLevel.CURE_WOUNDS,
                        FirstLevel.DETECT_MAGIC,
                        FirstLevel.DETECT_POISON_AND_DISEASE,
                        FirstLevel.EARTH_TREMOR,
                        FirstLevel.ENTANGLE,
                        FirstLevel.FAERIE_FIRE,
                        FirstLevel.FOG_CLOUD,
                        FirstLevel.GOODBERRY,
                        FirstLevel.HEALING_WORD,
                        FirstLevel.ICE_KNIFE,
                        FirstLevel.JUMP,
                        FirstLevel.LONGSTRIDER,
                        FirstLevel.PURIFY_FOOD_AND_DRINK,
                        FirstLevel.SNARE,
                        FirstLevel.SPEAK_WITH_ANIMALS,
                        FirstLevel.THUNDERWAVE,
                    }
                ),
                SecondLevel: frozenset(
                    {
                        SecondLevel.AIR_BUBBLE,
                        SecondLevel.ANIMAL_MESSENGER,
                        SecondLevel.BARKSKIN,
                        SecondLevel.BEAST_SENSE,
                        SecondLevel.DARKVISION,
                        SecondLevel.DUST_DEVIL,
                        SecondLevel.EARTHBIND,
                        SecondLevel.ENHANCE_ABILITY,
                        SecondLevel.FIND_TRAPS,
                        SecondLevel.FLAME_BLADE,
                        SecondLevel.FLAMING_SPHERE,
                        SecondLevel.GUST_OF_WIND,
                        SecondLevel.HEALING_SPIRIT,
                        SecondLevel.HEAT_METAL,
                        SecondLevel.HOLD_PERSON,
                        SecondLevel.LESSER_RESTORATION,
                        SecondLevel.LOCATE_ANIMALS_OR_PLANTS,
                        SecondLevel.LOCATE_OBJECT,
                        SecondLevel.MOONBEAM,
                        SecondLevel.PASS_WITHOUT_TRACE,
                        SecondLevel.PROTECTION_FROM_POISON,
                        SecondLevel.SKYWRITE,
                        SecondLevel.SPIKE_GROWTH,
                        SecondLevel.WARDING_WIND,
                        SecondLevel.WITHER_AND_BLOOM,
                    }
                ),
                ThirdLevel: frozenset(
                    {
                        ThirdLevel.CALL_LIGHTNING,
                        ThirdLevel.CONJURE_ANIMALS,
                        ThirdLevel.DAYLIGHT,
                        ThirdLevel.DISPEL_MAGIC,
                        ThirdLevel.ERUPTING_EARTH,
                        ThirdLevel.FEIGN_DEATH,
                        ThirdLevel.FLAME_ARROWS,
                        ThirdLevel.MELD_INTO_STONE,
                        ThirdLevel.PLANT_GROWTH,
                        ThirdLevel.PROTECTION_FROM_ENERGY,
                        ThirdLevel.SLEET_STORM,
                        ThirdLevel.SPEAK_WITH_PLANTS,
                        ThirdLevel.TIDAL_WAVE,
                        ThirdLevel.WALL_OF_WATER,
                        ThirdLevel.WATER_BREATHING,
                        ThirdLevel.WATER_WALK,
                        ThirdLevel.WIND_WALL,
                    }
                ),
                FourthLevel: frozenset(
                    {
                        FourthLevel.BLIGHT,
                        FourthLevel.CHARM_MONSTER,
                        FourthLevel.CONFUSION,
                        FourthLevel.CONJURE_MINOR_ELEMENTALS,
                        FourthLevel.CONJURE_WOODLAND_BEINGS,
                        FourthLevel.CONTROL_WATER,
                        FourthLevel.DOMINATE_BEAST,
                        FourthLevel.ELEMENTAL_BANE,
                        FourthLevel.FREEDOM_OF_MOVEMENT,
                        FourthLevel.GIANT_INSECT,
                        FourthLevel.GRASPING_VINE,
                        FourthLevel.GUARDIAN_OF_NATURE,
                        FourthLevel.HALLUCINATORY_TERRAIN,
                        FourthLevel.ICE_STORM,
                        FourthLevel.LOCATE_CREATURE,
                        FourthLevel.POLYMORPH,
                        FourthLevel.STONE_SHAPE,
                        FourthLevel.STONESKIN,
                        FourthLevel.WALL_OF_FIRE,
                        FourthLevel.WATERY_SPHERE,
                    }
                ),
                FifthLevel: frozenset(
                    {
                        FifthLevel.ANTILIFE_SHELL,
                        FifthLevel.AWAKEN,
                        FifthLevel.COMMUNE_WITH_NATURE,
                        FifthLevel.CONJURE_ELEMENTAL,
                        FifthLevel.CONTAGION,
                        FifthLevel.CONTROL_WINDS,
                        FifthLevel.FREEDOM_OF_THE_WINDS_HB,
                        FifthLevel.GEAS,
                        FifthLevel.GREATER_RESTORATION,
                        FifthLevel.INSECT_PLAGUE,
                        FifthLevel.MAELSTROM,
                        FifthLevel.MASS_CURE_WOUNDS,
                        FifthLevel.PLANAR_BINDING,
                        FifthLevel.REINCARNATE,
                        FifthLevel.SCRYING,
                        FifthLevel.SUMMON_DRACONIC_SPIRIT,
                        FifthLevel.SUMMON_DRACONIC_SPIRIT_UA,
                        FifthLevel.TRANSMUTE_ROCK,
                        FifthLevel.TREE_STRIDE,
                        FifthLevel.WALL_OF_STONE,
                        FifthLevel.WRATH_OF_NATURE,
                    }
                ),
                SixthLevel: frozenset(
                    {
                        SixthLevel.BONES_OF_THE_EARTH,
                        SixthLevel.CONJURE_FEY,
                        SixthLevel.DRUID_GROVE,
                        SixthLevel.FIND_THE_PATH,
                        SixthLevel.HEAL,
                        SixthLevel.HEROES_FEAST,
                        SixthLevel.INVESTITURE_OF_FLAME,
                        SixthLevel.INVESTITURE_OF_ICE,
                        SixthLevel.INVESTITURE_OF_STONE,
                        SixthLevel.INVESTITURE_OF_WIND,
                        SixthLevel.MOVE_EARTH,
                        SixthLevel.PRIMORDIAL_WARD,
                        SixthLevel.SUNBEAM,
                        SixthLevel.TRANSPORT_VIA_PLANTS,
                        SixthLevel.WALL_OF_THORNS,
                        SixthLevel.WIND_WALK,
                    }
                ),
                SeventhLevel: frozenset(
                    {
                        SeventhLevel.DRACONIC_TRANSFORMATION,
                        SeventhLevel.DRACONIC_TRANSFORMATION_UA,
                        SeventhLevel.FIRE_STORM,
                        SeventhLevel.MIRAGE_ARCANE,
                        SeventhLevel.PLANE_SHIFT,
                        SeventhLevel.REGENERATE,
                        SeventhLevel.REVERSE_GRAVITY,
                        SeventhLevel.WHIRLWIND,
                    }
                ),
                EighthLevel: frozenset(
                    {
                        EighthLevel.ANIMAL_SHAPES,
                        EighthLevel.ANTIPATHY_SYMPATHY,
                        EighthLevel.CONTROL_WEATHER,
                        EighthLevel.EARTHQUAKE,
                        EighthLevel.FEEBLEMIND,
                        EighthLevel.SUNBURST,
                        EighthLevel.TSUNAMI,
                    }
                ),
                NinthLevel: frozenset(
                    {
                        NinthLevel.FORESIGHT,
                        NinthLevel.SHAPECHANGE,
                        NinthLevel.STORM_OF_VENGEANCE,
                        NinthLevel.TRUE_RESURRECTION,
                    }
                ),
            }
        ),
        Class.PALADIN: frozendict(
            {
                FirstLevel: frozenset(
                    {
                        FirstLevel.BLESS,
                        FirstLevel.CEREMONY,
                        FirstLevel.COMMAND,
                        FirstLevel.COMPELLED_DUEL,
                        FirstLevel.CURE_WOUNDS,
                        FirstLevel.DETECT_EVIL_AND_GOOD,
                        FirstLevel.DETECT_MAGIC,
                        FirstLevel.DETECT_POISON_AND_DISEASE,
                        FirstLevel.DIVINE_FAVOR,
                        FirstLevel.HEROISM,
                        FirstLevel.PROTECTION_FROM_EVIL_AND_GOOD,
                        FirstLevel.PURIFY_FOOD_AND_DRINK,
                        FirstLevel.SEARING_SMITE,
                        FirstLevel.SHIELD_OF_FAITH,
                        FirstLevel.THUNDEROUS_SMITE,
                        FirstLevel.WRATHFUL_SMITE,
                    }
                ),
                SecondLevel: frozenset(
                    {
                        SecondLevel.AID,
                        SecondLevel.BRANDING_SMITE,
                        SecondLevel.FIND_STEED,
                        SecondLevel.FIND_VEHICLE_UA,
                        SecondLevel.LESSER_RESTORATION,
                        SecondLevel.LOCATE_OBJECT,
                        SecondLevel.MAGIC_WEAPON,
                        SecondLevel.PROTECTION_FROM_POISON,
                        SecondLevel.ZONE_OF_TRUTH,
                    }
                ),
                ThirdLevel: frozenset(
                    {
                        ThirdLevel.AURA_OF_VITALITY,
                        ThirdLevel.BLINDING_SMITE,
                        ThirdLevel.CREATE_FOOD_AND_WATER,
                        ThirdLevel.CRUSADERS_MANTLE,
                        ThirdLevel.DAYLIGHT,
                        ThirdLevel.DISPEL_MAGIC,
                        ThirdLevel.ELEMENTAL_WEAPON,
                        ThirdLevel.MAGIC_CIRCLE,
                        ThirdLevel.REMOVE_CURSE,
                        ThirdLevel.REVIVIFY,
                    }
                ),
                FourthLevel: frozenset(
                    {
                        FourthLevel.AURA_OF_LIFE,
                        FourthLevel.AURA_OF_PURITY,
                        FourthLevel.BANISHMENT,
                        FourthLevel.DEATH_WARD,
                        FourthLevel.FIND_GREATER_STEED,
                        FourthLevel.LOCATE_CREATURE,
                        FourthLevel.STAGGERING_SMITE,
                    }
                ),
                FifthLevel: frozenset(
                    {
                        FifthLevel.BANISHING_SMITE,
                        FifthLevel.CIRCLE_OF_POWER,
                        FifthLevel.DESTRUCTIVE_WAVE,
                        FifthLevel.DISPEL_EVIL_AND_GOOD,
                        FifthLevel.GEAS,
                        FifthLevel.HOLY_WEAPON,
                        FifthLevel.RAISE_DEAD,
                    }
                ),
            }
        ),
        Class.RANGER: frozendict(
            {
                FirstLevel: frozenset(
                    {
                        FirstLevel.ABSORB_ELEMENTS,
                        FirstLevel.ALARM,
                        FirstLevel.ANIMAL_FRIENDSHIP,
                        FirstLevel.BEAST_BOND,
                        FirstLevel.CURE_WOUNDS,
                        FirstLevel.DETECT_MAGIC,
                        FirstLevel.DETECT_POISON_AND_DISEASE,
                        FirstLevel.ENSNARING_STRIKE,
                        FirstLevel.FOG_CLOUD,
                        FirstLevel.GOODBERRY,
                        FirstLevel.HAIL_OF_THORNS,
                        FirstLevel.HUNTERS_MARK,
                        FirstLevel.JUMP,
                        FirstLevel.LONGSTRIDER,
                        FirstLevel.SNARE,
                        FirstLevel.SPEAK_WITH_ANIMALS,
                        FirstLevel.ZEPHYR_STRIKE,
                    }
                ),
                SecondLevel: frozenset(
                    {
                        SecondLevel.AIR_BUBBLE,
                        SecondLevel.ANIMAL_MESSENGER,
                        SecondLevel.BARKSKIN,
                        SecondLevel.BEAST_SENSE,
                        SecondLevel.CORDON_OF_ARROWS,
                        SecondLevel.DARKVISION,
                        SecondLevel.FIND_TRAPS,
                        SecondLevel.HEALING_SPIRIT,
                        SecondLevel.LESSER_RESTORATION,
                        SecondLevel.LOCATE_ANIMALS_OR_PLANTS,
                        SecondLevel.LOCATE_OBJECT,
                        SecondLevel.PASS_WITHOUT_TRACE,
                        SecondLevel.PROTECTION_FROM_POISON,
                        SecondLevel.SILENCE,
                        SecondLevel.SPIKE_GROWTH,
                    }
                ),
                ThirdLevel: frozenset(
                    {
                        ThirdLevel.ASHARDALONS_STRIDE,
                        ThirdLevel.CONJURE_ANIMALS,
                        ThirdLevel.CONJURE_BARRAGE,
                        ThirdLevel.DAYLIGHT,
                        ThirdLevel.FLAME_ARROWS,
                        ThirdLevel.FLAME_STRIDE_UA,
                        ThirdLevel.LIGHTNING_ARROW,
                        ThirdLevel.NONDETECTION,
                        ThirdLevel.PLANT_GROWTH,
                        ThirdLevel.PROTECTION_FROM_ENERGY,
                        ThirdLevel.SPEAK_WITH_PLANTS,
                        ThirdLevel.WATER_BREATHING,
                        ThirdLevel.WATER_WALK,
                        ThirdLevel.WIND_WALL,
                    }
                ),
                FourthLevel: frozenset(
                    {
                        FourthLevel.CONJURE_WOODLAND_BEINGS,
                        FourthLevel.FREEDOM_OF_MOVEMENT,
                        FourthLevel.GRASPING_VINE,
                        FourthLevel.GUARDIAN_OF_NATURE,
                        FourthLevel.LOCATE_CREATURE,
                        FourthLevel.STONESKIN,
                    }
                ),
                FifthLevel: frozenset(
                    {
                        FifthLevel.COMMUNE_WITH_NATURE,
                        FifthLevel.CONJURE_VOLLEY,
                        FifthLevel.FREEDOM_OF_THE_WINDS_HB,
                        FifthLevel.STEEL_WIND_STRIKE,
                        FifthLevel.SWIFT_QUIVER,
                        FifthLevel.TREE_STRIDE,
                        FifthLevel.WRATH_OF_NATURE,
                    }
                ),
            }
        ),
        Class.SORCERER: frozendict(
            {
                Cantrip: frozenset(
                    {
                        Cantrip.ACID_SPLASH,
                        Cantrip.BLADE_WARD,
                        Cantrip.CHILL_TOUCH,
                        Cantrip.CONTROL_FLAMES,
                        Cantrip.CREATE_BONFIRE,
                        Cantrip.DANCING_LIGHTS,
                        Cantrip.FIRE_BOLT,
                        Cantrip.FRIENDS,
                        Cantrip.FROSTBITE,
                        Cantrip.GUST,
                        Cantrip.INFESTATION,
                        Cantrip.LIGHT,
                        Cantrip.MAGE_HAND,
                        Cantrip.MENDING,
                        Cantrip.MESSAGE,
                        Cantrip.MINOR_ILLUSION,
                        Cantrip.MOLD_EARTH,
                        Cantrip.ON_OFF,
                        Cantrip.POISON_SPRAY,
                        Cantrip.PRESTIDIGITATION,
                        Cantrip.RAY_OF_FROST,
                        Cantrip.SHAPE_WATER,
                        Cantrip.SHOCKING_GRASP,
                        Cantrip.THUNDERCLAP,
                        Cantrip.TRUE_STRIKE,
                    }
                ),
                FirstLevel: frozenset(
                    {
                        FirstLevel.ABSORB_ELEMENTS,
                        FirstLevel.BURNING_HANDS,
                        FirstLevel.CATAPULT,
                        FirstLevel.CHAOS_BOLT,
                        FirstLevel.CHARM_PERSON,
                        FirstLevel.CHROMATIC_ORB,
                        FirstLevel.COLOR_SPRAY,
                        FirstLevel.COMPREHEND_LANGUAGES,
                        FirstLevel.DETECT_MAGIC,
                        FirstLevel.DISGUISE_SELF,
                        FirstLevel.DISTORT_VALUE,
                        FirstLevel.EARTH_TREMOR,
                        FirstLevel.EXPEDITIOUS_RETREAT,
                        FirstLevel.FALSE_LIFE,
                        FirstLevel.FEATHER_FALL,
                        FirstLevel.FOG_CLOUD,
                        FirstLevel.ICE_KNIFE,
                        FirstLevel.JUMP,
                        FirstLevel.MAGE_ARMOR,
                        FirstLevel.MAGIC_MISSILE,
                        FirstLevel.RAY_OF_SICKNESS,
                        FirstLevel.SHIELD,
                        FirstLevel.SILENT_IMAGE,
                        FirstLevel.SILVERY_BARBS,
                        FirstLevel.SLEEP,
                        FirstLevel.THUNDERWAVE,
                        FirstLevel.WITCH_BOLT,
                    }
                ),
                SecondLevel: frozenset(
                    {
                        SecondLevel.AGANAZZARS_SCORCHER,
                        SecondLevel.AIR_BUBBLE,
                        SecondLevel.ALTER_SELF,
                        SecondLevel.ARCANE_HACKING_UA,
                        SecondLevel.BLINDNESS_DEAFNESS,
                        SecondLevel.BLUR,
                        SecondLevel.CLOUD_OF_DAGGERS,
                        SecondLevel.CROWN_OF_MADNESS,
                        SecondLevel.DARKNESS,
                        SecondLevel.DARKVISION,
                        SecondLevel.DETECT_THOUGHTS,
                        SecondLevel.DIGITAL_PHANTOM_UA,
                        SecondLevel.DRAGONS_BREATH,
                        SecondLevel.DUST_DEVIL,
                        SecondLevel.EARTHBIND,
                        SecondLevel.ENHANCE_ABILITY,
                        SecondLevel.ENLARGE_REDUCE,
                        SecondLevel.FIND_VEHICLE_UA,
                        SecondLevel.GUST_OF_WIND,
                        SecondLevel.HOLD_PERSON,
                        SecondLevel.INVISIBILITY,
                        SecondLevel.KINETIC_JAUNT,
                        SecondLevel.KNOCK,
                        SecondLevel.LEVITATE,
                        SecondLevel.MAXIMILLIANS_EARTHEN_GRASP,
                        SecondLevel.MENTAL_BARRIER_UA,
                        SecondLevel.MIND_SPIKE,
                        SecondLevel.MIND_THRUST_UA,
                        SecondLevel.MIRROR_IMAGE,
                        SecondLevel.MISTY_STEP,
                        SecondLevel.NATHAIRS_MISCHIEF,
                        SecondLevel.NATHAIRS_MISCHIEF_UA,
                        SecondLevel.PHANTASMAL_FORCE,
                        SecondLevel.PYROTECHNICS,
                        SecondLevel.RIMES_BINDING_ICE,
                        SecondLevel.SCORCHING_RAY,
                        SecondLevel.SEE_INVISIBILITY,
                        SecondLevel.SHADOW_BLADE,
                        SecondLevel.SHATTER,
                        SecondLevel.SNILLOCS_SNOWBALL_STORM,
                        SecondLevel.SPIDER_CLIMB,
                        SecondLevel.SPRAY_OF_CARDS,
                        SecondLevel.SPRAY_OF_CARDS_UA,
                        SecondLevel.SUGGESTION,
                        SecondLevel.THOUGHT_SHIELD_UA,
                        SecondLevel.VORTEX_WARP,
                        SecondLevel.WARDING_WIND,
                        SecondLevel.WARP_SENSE,
                        SecondLevel.WEB,
                        SecondLevel.WITHER_AND_BLOOM,
                    }
                ),
                ThirdLevel: frozenset(
                    {
                        ThirdLevel.ANTAGONIZE,
                        ThirdLevel.ANTAGONIZE_UA,
                        ThirdLevel.ASHARDALONS_STRIDE,
                        ThirdLevel.BLINK,
                        ThirdLevel.CATNAP,
                        ThirdLevel.CLAIRVOYANCE,
                        ThirdLevel.CONJURE_LESSER_DEMON_UA,
                        ThirdLevel.COUNTERSPELL,
                        ThirdLevel.DAYLIGHT,
                        ThirdLevel.DISPEL_MAGIC,
                        ThirdLevel.ENEMIES_ABOUND,
                        ThirdLevel.ERUPTING_EARTH,
                        ThirdLevel.FEAR,
                        ThirdLevel.FIREBALL,
                        ThirdLevel.FLAME_ARROWS,
                        ThirdLevel.FLAME_STRIDE_UA,
                        ThirdLevel.FLY,
                        ThirdLevel.GASEOUS_FORM,
                        ThirdLevel.HASTE,
                        ThirdLevel.HAYWIRE_UA,
                        ThirdLevel.HYPNOTIC_PATTERN,
                        ThirdLevel.INCITE_GREED,
                        ThirdLevel.INVISIBILITY_TO_CAMERAS_UA,
                        ThirdLevel.LIGHTNING_BOLT,
                        ThirdLevel.MAJOR_IMAGE,
                        ThirdLevel.MELFS_MINUTE_METEORS,
                        ThirdLevel.PROTECTION_FROM_BALLISTICS_UA,
                        ThirdLevel.PROTECTION_FROM_ENERGY,
                        ThirdLevel.PSIONIC_BLAST_UA,
                        ThirdLevel.SLEET_STORM,
                        ThirdLevel.SLOW,
                        ThirdLevel.STINKING_CLOUD,
                        ThirdLevel.SUMMON_WARRIOR_SPIRIT_UA,
                        ThirdLevel.THUNDER_STEP,
                        ThirdLevel.TIDAL_WAVE,
                        ThirdLevel.TONGUES,
                        ThirdLevel.VAMPIRIC_TOUCH,
                        ThirdLevel.WALL_OF_WATER,
                        ThirdLevel.WATER_BREATHING,
                        ThirdLevel.WATER_WALK,
                    }
                ),
                FourthLevel: frozenset(
                    {
                        FourthLevel.BANISHMENT,
                        FourthLevel.BLIGHT,
                        FourthLevel.CHARM_MONSTER,
                        FourthLevel.CONFUSION,
                        FourthLevel.CONJURE_BARLGURA_UA,
                        FourthLevel.CONJURE_KNOWBOT_UA,
                        FourthLevel.CONJURE_SHADOW_DEMON_UA,
                        FourthLevel.DIMENSION_DOOR,
                        FourthLevel.DOMINATE_BEAST,
                        FourthLevel.EGO_WHIP_UA,
                        FourthLevel.GATE_SEAL,
                        FourthLevel.GREATER_INVISIBILITY,
                        FourthLevel.ICE_STORM,
                        FourthLevel.POLYMORPH,
                        FourthLevel.RAULOTHIMS_PSYCHIC_LANCE,
                        FourthLevel.RAULOTHIMS_PSYCHIC_LANCE_UA,
                        FourthLevel.SICKENING_RADIANCE,
                        FourthLevel.SPIRIT_OF_DEATH,
                        FourthLevel.SPIRIT_OF_DEATH_UA,
                        FourthLevel.STONESKIN,
                        FourthLevel.STORM_SPHERE,
                        FourthLevel.SYNCHRONICITY_UA,
                        FourthLevel.SYSTEM_BACKDOOR_UA,
                        FourthLevel.VITRIOLIC_SPHERE,
                        FourthLevel.WALL_OF_FIRE,
                        FourthLevel.WATERY_SPHERE,
                    }
                ),
                FifthLevel: frozenset(
                    {
                        FifthLevel.ANIMATE_OBJECTS,
                        FifthLevel.CLOUDKILL,
                        FifthLevel.COMMUNE_WITH_CITY_UA,
                        FifthLevel.CONE_OF_COLD,
                        FifthLevel.CONJURE_VROCK_UA,
                        FifthLevel.CONTROL_WINDS,
                        FifthLevel.CREATION,
                        FifthLevel.DOMINATE_PERSON,
                        FifthLevel.ENERVATION,
                        FifthLevel.FAR_STEP,
                        FifthLevel.FREEDOM_OF_THE_WINDS_HB,
                        FifthLevel.HOLD_MONSTER,
                        FifthLevel.IMMOLATION,
                        FifthLevel.INSECT_PLAGUE,
                        FifthLevel.SEEMING,
                        FifthLevel.SHUTDOWN_UA,
                        FifthLevel.SKILL_EMPOWERMENT,
                        FifthLevel.SUMMON_DRACONIC_SPIRIT,
                        FifthLevel.SUMMON_DRACONIC_SPIRIT_UA,
                        FifthLevel.SYNAPTIC_STATIC,
                        FifthLevel.TELEKINESIS,
                        FifthLevel.TELEPORTATION_CIRCLE,
                        FifthLevel.WALL_OF_LIGHT,
                        FifthLevel.WALL_OF_STONE,
                    }
                ),
                SixthLevel: frozenset(
                    {
                        SixthLevel.ARCANE_GATE,
                        SixthLevel.CHAIN_LIGHTNING,
                        SixthLevel.CIRCLE_OF_DEATH,
                        SixthLevel.DISINTEGRATE,
                        SixthLevel.EYEBITE,
                        SixthLevel.FIZBANS_PLATINUM_SHIELD,
                        SixthLevel.FIZBANS_PLATINUM_SHIELD_UA,
                        SixthLevel.GLOBE_OF_INVULNERABILITY,
                        SixthLevel.INVESTITURE_OF_FLAME,
                        SixthLevel.INVESTITURE_OF_ICE,
                        SixthLevel.INVESTITURE_OF_STONE,
                        SixthLevel.INVESTITURE_OF_WIND,
                        SixthLevel.MASS_SUGGESTION,
                        SixthLevel.MENTAL_PRISON,
                        SixthLevel.MOVE_EARTH,
                        SixthLevel.OTHERWORLDLY_FORM_UA,
                        SixthLevel.PSYCHIC_CRUSH_UA,
                        SixthLevel.SCATTER,
                        SixthLevel.SUNBEAM,
                        SixthLevel.TRUE_SEEING,
                    }
                ),
                SeventhLevel: frozenset(
                    {
                        SeventhLevel.CONJURE_HEZROU_UA,
                        SeventhLevel.CROWN_OF_STARS,
                        SeventhLevel.DELAYED_BLAST_FIREBALL,
                        SeventhLevel.DRACONIC_TRANSFORMATION,
                        SeventhLevel.DRACONIC_TRANSFORMATION_UA,
                        SeventhLevel.ETHEREALNESS,
                        SeventhLevel.FINGER_OF_DEATH,
                        SeventhLevel.FIRE_STORM,
                        SeventhLevel.PLANE_SHIFT,
                        SeventhLevel.POWER_WORD_PAIN,
                        SeventhLevel.PRISMATIC_SPRAY,
                        SeventhLevel.REVERSE_GRAVITY,
                        SeventhLevel.TELEPORT,
                    }
                ),
                EighthLevel: frozenset(
                    {
                        EighthLevel.ABI_DALZIMS_HORRID_WILTING,
                        EighthLevel.DOMINATE_MONSTER,
                        EighthLevel.EARTHQUAKE,
                        EighthLevel.INCENDIARY_CLOUD,
                        EighthLevel.POWER_WORD_STUN,
                        EighthLevel.SUNBURST,
                    }
                ),
                NinthLevel: frozenset(
                    {
                        NinthLevel.GATE,
                        NinthLevel.MASS_POLYMORPH,
                        NinthLevel.METEOR_SWARM,
                        NinthLevel.POWER_WORD_KILL,
                        NinthLevel.PSYCHIC_SCREAM,
                        NinthLevel.TIME_STOP,
                        NinthLevel.WISH,
                    }
                ),
            }
        ),
        Class.WARLOCK: frozendict(
            {
                Cantrip: frozenset(
                    {
                        Cantrip.BLADE_WARD,
                        Cantrip.CHILL_TOUCH,
                        Cantrip.CREATE_BONFIRE,
                        Cantrip.ELDRITCH_BLAST,
                        Cantrip.FRIENDS,
                        Cantrip.FROSTBITE,
                        Cantrip.INFESTATION,
                        Cantrip.MAGE_HAND,
                        Cantrip.MAGIC_STONE,
                        Cantrip.MINOR_ILLUSION,
                        Cantrip.ON_OFF,
                        Cantrip.POISON_SPRAY,
                        Cantrip.PRESTIDIGITATION,
                        Cantrip.THUNDERCLAP,
                        Cantrip.TOLL_THE_DEAD,
                        Cantrip.TRUE_STRIKE,
                    }
                ),
                FirstLevel: frozenset(
                    {
                        FirstLevel.ARMOR_OF_AGATHYS,
                        FirstLevel.ARMS_OF_HADAR,
                        FirstLevel.CAUSE_FEAR,
                        FirstLevel.CHARM_PERSON,
                        FirstLevel.COMPREHEND_LANGUAGES,
                        FirstLevel.DISTORT_VALUE,
                        FirstLevel.EXPEDITIOUS_RETREAT,
                        FirstLevel.HELLISH_REBUKE,
                        FirstLevel.HEX,
                        FirstLevel.ILLUSORY_SCRIPT,
                        FirstLevel.PROTECTION_FROM_EVIL_AND_GOOD,
                        FirstLevel.UNSEEN_SERVANT,
                        FirstLevel.WITCH_BOLT,
                    }
                ),
                SecondLevel: frozenset(
                    {
                        SecondLevel.ARCANE_HACKING_UA,
                        SecondLevel.BORROWED_KNOWLEDGE,
                        SecondLevel.CLOUD_OF_DAGGERS,
                        SecondLevel.CROWN_OF_MADNESS,
                        SecondLevel.DARKNESS,
                        SecondLevel.DIGITAL_PHANTOM_UA,
                        SecondLevel.EARTHBIND,
                        SecondLevel.ENTHRALL,
                        SecondLevel.FIND_VEHICLE_UA,
                        SecondLevel.FLOCK_OF_FAMILIARS,
                        SecondLevel.HOLD_PERSON,
                        SecondLevel.INVISIBILITY,
                        SecondLevel.MENTAL_BARRIER_UA,
                        SecondLevel.MIND_SPIKE,
                        SecondLevel.MIND_THRUST_UA,
                        SecondLevel.MIRROR_IMAGE,
                        SecondLevel.MISTY_STEP,
                        SecondLevel.RAY_OF_ENFEEBLEMENT,
                        SecondLevel.SHADOW_BLADE,
                        SecondLevel.SHATTER,
                        SecondLevel.SPIDER_CLIMB,
                        SecondLevel.SPRAY_OF_CARDS,
                        SecondLevel.SPRAY_OF_CARDS_UA,
                        SecondLevel.SUGGESTION,
                        SecondLevel.THOUGHT_SHIELD_UA,
                        SecondLevel.WARP_SENSE,
                    }
                ),
                ThirdLevel: frozenset(
                    {
                        ThirdLevel.ANTAGONIZE,
                        ThirdLevel.ANTAGONIZE_UA,
                        ThirdLevel.COUNTERSPELL,
                        ThirdLevel.DISPEL_MAGIC,
                        ThirdLevel.ENEMIES_ABOUND,
                        ThirdLevel.FEAR,
                        ThirdLevel.FLY,
                        ThirdLevel.GASEOUS_FORM,
                        ThirdLevel.HAYWIRE_UA,
                        ThirdLevel.HUNGER_OF_HADAR,
                        ThirdLevel.HYPNOTIC_PATTERN,
                        ThirdLevel.INCITE_GREED,
                        ThirdLevel.INVISIBILITY_TO_CAMERAS_UA,
                        ThirdLevel.MAGIC_CIRCLE,
                        ThirdLevel.MAJOR_IMAGE,
                        ThirdLevel.PROTECTION_FROM_BALLISTICS_UA,
                        ThirdLevel.PSIONIC_BLAST_UA,
                        ThirdLevel.REMOVE_CURSE,
                        ThirdLevel.SUMMON_LESSER_DEMONS,
                        ThirdLevel.SUMMON_WARRIOR_SPIRIT_UA,
                        ThirdLevel.THUNDER_STEP,
                        ThirdLevel.TONGUES,
                        ThirdLevel.VAMPIRIC_TOUCH,
                    }
                ),
                FourthLevel: frozenset(
                    {
                        FourthLevel.BANISHMENT,
                        FourthLevel.BLIGHT,
                        FourthLevel.CHARM_MONSTER,
                        FourthLevel.CONJURE_KNOWBOT_UA,
                        FourthLevel.DIMENSION_DOOR,
                        FourthLevel.EGO_WHIP_UA,
                        FourthLevel.ELEMENTAL_BANE,
                        FourthLevel.GALDERS_SPEEDY_COURIER,
                        FourthLevel.GATE_SEAL,
                        FourthLevel.HALLUCINATORY_TERRAIN,
                        FourthLevel.RAULOTHIMS_PSYCHIC_LANCE,
                        FourthLevel.RAULOTHIMS_PSYCHIC_LANCE_UA,
                        FourthLevel.SHADOW_OF_MOIL,
                        FourthLevel.SICKENING_RADIANCE,
                        FourthLevel.SPIRIT_OF_DEATH,
                        FourthLevel.SPIRIT_OF_DEATH_UA,
                        FourthLevel.SYNCHRONICITY_UA,
                        FourthLevel.SYSTEM_BACKDOOR_UA,
                    }
                ),
                FifthLevel: frozenset(
                    {
                        FifthLevel.COMMUNE_WITH_CITY_UA,
                        FifthLevel.CONTACT_OTHER_PLANE,
                        FifthLevel.DANSE_MACABRE,
                        FifthLevel.DREAM,
                        FifthLevel.ENERVATION,
                        FifthLevel.FAR_STEP,
                        FifthLevel.HOLD_MONSTER,
                        FifthLevel.INFERNAL_CALLING,
                        FifthLevel.NEGATIVE_ENERGY_FLOOD,
                        FifthLevel.SCRYING,
                        FifthLevel.SHUTDOWN_UA,
                        FifthLevel.SYNAPTIC_STATIC,
                        FifthLevel.WALL_OF_LIGHT,
                    }
                ),
                SixthLevel: frozenset(
                    {
                        SixthLevel.ARCANE_GATE,
                        SixthLevel.CIRCLE_OF_DEATH,
                        SixthLevel.CONJURE_FEY,
                        SixthLevel.CREATE_UNDEAD,
                        SixthLevel.EYEBITE,
                        SixthLevel.FLESH_TO_STONE,
                        SixthLevel.INVESTITURE_OF_FLAME,
                        SixthLevel.INVESTITURE_OF_ICE,
                        SixthLevel.INVESTITURE_OF_STONE,
                        SixthLevel.INVESTITURE_OF_WIND,
                        SixthLevel.MASS_SUGGESTION,
                        SixthLevel.MENTAL_PRISON,
                        SixthLevel.OTHERWORLDLY_FORM_UA,
                        SixthLevel.PSYCHIC_CRUSH_UA,
                        SixthLevel.SCATTER,
                        SixthLevel.SOUL_CAGE,
                        SixthLevel.TRUE_SEEING,
                    }
                ),
                SeventhLevel: frozenset(
                    {
                        SeventhLevel.CROWN_OF_STARS,
                        SeventhLevel.ETHEREALNESS,
                        SeventhLevel.FINGER_OF_DEATH,
                        SeventhLevel.FORCECAGE,
                        SeventhLevel.PLANE_SHIFT,
                        SeventhLevel.POWER_WORD_PAIN,
                    }
                ),
                EighthLevel: frozenset(
                    {
                        EighthLevel.DEMIPLANE,
                        EighthLevel.DOMINATE_MONSTER,
                        EighthLevel.FEEBLEMIND,
                        EighthLevel.GLIBNESS,
                        EighthLevel.MADDENING_DARKNESS,
                        EighthLevel.POWER_WORD_STUN,
                    }
                ),
                NinthLevel: frozenset(
                    {
                        NinthLevel.ASTRAL_PROJECTION,
                        NinthLevel.FORESIGHT,
                        NinthLevel.IMPRISONMENT,
                        NinthLevel.POWER_WORD_KILL,
                        NinthLevel.PSYCHIC_SCREAM,
                        NinthLevel.TRUE_POLYMORPH,
                    }
                ),
            }
        ),
        Class.WIZARD: frozendict(
            {
                Cantrip: frozenset(
                    {
                        Cantrip.ACID_SPLASH,
                        Cantrip.BLADE_WARD,
                        Cantrip.CHILL_TOUCH,
                        Cantrip.CONTROL_FLAMES,
                        Cantrip.CREATE_BONFIRE,
                        Cantrip.DANCING_LIGHTS,
                        Cantrip.ENCODE_THOUGHTS,
                        Cantrip.FIRE_BOLT,
                        Cantrip.FRIENDS,
                        Cantrip.FROSTBITE,
                        Cantrip.GUST,
                        Cantrip.INFESTATION,
                        Cantrip.LIGHT,
                        Cantrip.MAGE_HAND,
                        Cantrip.MENDING,
                        Cantrip.MESSAGE,
                        Cantrip.MINOR_ILLUSION,
                        Cantrip.MOLD_EARTH,
                        Cantrip.ON_OFF,
                        Cantrip.POISON_SPRAY,
                        Cantrip.PRESTIDIGITATION,
                        Cantrip.RAY_OF_FROST,
                        Cantrip.SHAPE_WATER,
                        Cantrip.SHOCKING_GRASP,
                        Cantrip.THUNDERCLAP,
                        Cantrip.TOLL_THE_DEAD,
                        Cantrip.TRUE_STRIKE,
                    }
                ),
                FirstLevel: frozenset(
                    {
                        FirstLevel.ABSORB_ELEMENTS,
                        FirstLevel.ALARM,
                        FirstLevel.BURNING_HANDS,
                        FirstLevel.CATAPULT,
                        FirstLevel.CAUSE_FEAR,
                        FirstLevel.CHARM_PERSON,
                        FirstLevel.CHROMATIC_ORB,
                        FirstLevel.COLOR_SPRAY,
                        FirstLevel.COMPREHEND_LANGUAGES,
                        FirstLevel.DETECT_MAGIC,
                        FirstLevel.DISGUISE_SELF,
                        FirstLevel.DISTORT_VALUE,
                        FirstLevel.EARTH_TREMOR,
                        FirstLevel.EXPEDITIOUS_RETREAT,
                        FirstLevel.FALSE_LIFE,
                        FirstLevel.FEATHER_FALL,
                        FirstLevel.FIND_FAMILIAR,
                        FirstLevel.FOG_CLOUD,
                        FirstLevel.FROST_FINGERS,
                        FirstLevel.GREASE,
                        FirstLevel.ICE_KNIFE,
                        FirstLevel.IDENTIFY,
                        FirstLevel.ILLUSORY_SCRIPT,
                        FirstLevel.JIMS_MAGIC_MISSILE,
                        FirstLevel.JUMP,
                        FirstLevel.LONGSTRIDER,
                        FirstLevel.MAGE_ARMOR,
                        FirstLevel.MAGIC_MISSILE,
                        FirstLevel.PROTECTION_FROM_EVIL_AND_GOOD,
                        FirstLevel.RAY_OF_SICKNESS,
                        FirstLevel.SHIELD,
                        FirstLevel.SILENT_IMAGE,
                        FirstLevel.SILVERY_BARBS,
                        FirstLevel.SLEEP,
                        FirstLevel.SNARE,
                        FirstLevel.TASHAS_HIDEOUS_LAUGHTER,
                        FirstLevel.TENSERS_FLOATING_DISK,
                        FirstLevel.THUNDERWAVE,
                        FirstLevel.UNSEEN_SERVANT,
                        FirstLevel.WITCH_BOLT,
                    }
                ),
                SecondLevel: frozenset(
                    {
                        SecondLevel.AGANAZZARS_SCORCHER,
                        SecondLevel.AIR_BUBBLE,
                        SecondLevel.ALTER_SELF,
                        SecondLevel.ARCANE_HACKING_UA,
                        SecondLevel.ARCANE_LOCK,
                        SecondLevel.BLINDNESS_DEAFNESS,
                        SecondLevel.BLUR,
                        SecondLevel.BORROWED_KNOWLEDGE,
                        SecondLevel.CLOUD_OF_DAGGERS,
                        SecondLevel.CONTINUAL_FLAME,
                        SecondLevel.CROWN_OF_MADNESS,
                        SecondLevel.DARKNESS,
                        SecondLevel.DARKVISION,
                        SecondLevel.DETECT_THOUGHTS,
                        SecondLevel.DIGITAL_PHANTOM_UA,
                        SecondLevel.DRAGONS_BREATH,
                        SecondLevel.DUST_DEVIL,
                        SecondLevel.EARTHBIND,
                        SecondLevel.ENLARGE_REDUCE,
                        SecondLevel.FIND_VEHICLE_UA,
                        SecondLevel.FLAMING_SPHERE,
                        SecondLevel.FLOCK_OF_FAMILIARS,
                        SecondLevel.GENTLE_REPOSE,
                        SecondLevel.GIFT_OF_GAB,
                        SecondLevel.GUST_OF_WIND,
                        SecondLevel.HOLD_PERSON,
                        SecondLevel.INVISIBILITY,
                        SecondLevel.JIMS_GLOWING_COIN,
                        SecondLevel.KINETIC_JAUNT,
                        SecondLevel.KNOCK,
                        SecondLevel.LEVITATE,
                        SecondLevel.LOCATE_OBJECT,
                        SecondLevel.MAGIC_MOUTH,
                        SecondLevel.MAGIC_WEAPON,
                        SecondLevel.MAXIMILLIANS_EARTHEN_GRASP,
                        SecondLevel.MELFS_ACID_ARROW,
                        SecondLevel.MENTAL_BARRIER_UA,
                        SecondLevel.MIND_SPIKE,
                        SecondLevel.MIND_THRUST_UA,
                        SecondLevel.MIRROR_IMAGE,
                        SecondLevel.MISTY_STEP,
                        SecondLevel.NATHAIRS_MISCHIEF,
                        SecondLevel.NATHAIRS_MISCHIEF_UA,
                        SecondLevel.NYSTULS_MAGIC_AURA,
                        SecondLevel.PHANTASMAL_FORCE,
                        SecondLevel.PYROTECHNICS,
                        SecondLevel.RAY_OF_ENFEEBLEMENT,
                        SecondLevel.RIMES_BINDING_ICE,
                        SecondLevel.ROPE_TRICK,
                        SecondLevel.SCORCHING_RAY,
                        SecondLevel.SEE_INVISIBILITY,
                        SecondLevel.SHADOW_BLADE,
                        SecondLevel.SHATTER,
                        SecondLevel.SKYWRITE,
                        SecondLevel.SNILLOCS_SNOWBALL_STORM,
                        SecondLevel.SPIDER_CLIMB,
                        SecondLevel.SPRAY_OF_CARDS,
                        SecondLevel.SPRAY_OF_CARDS_UA,
                        SecondLevel.SUGGESTION,
                        SecondLevel.THOUGHT_SHIELD_UA,
                        SecondLevel.VORTEX_WARP,
                        SecondLevel.WARDING_WIND,
                        SecondLevel.WARP_SENSE,
                        SecondLevel.WEB,
                        SecondLevel.WITHER_AND_BLOOM,
                    }
                ),
                ThirdLevel: frozenset(
                    {
                        ThirdLevel.ANIMATE_DEAD,
                        ThirdLevel.ANTAGONIZE,
                        ThirdLevel.ANTAGONIZE_UA,
                        ThirdLevel.ASHARDALONS_STRIDE,
                        ThirdLevel.BESTOW_CURSE,
                        ThirdLevel.BLINK,
                        ThirdLevel.CATNAP,
                        ThirdLevel.CLAIRVOYANCE,
                        ThirdLevel.CONJURE_LESSER_DEMON_UA,
                        ThirdLevel.COUNTERSPELL,
                        ThirdLevel.DISPEL_MAGIC,
                        ThirdLevel.ENEMIES_ABOUND,
                        ThirdLevel.ERUPTING_EARTH,
                        ThirdLevel.FAST_FRIENDS,
                        ThirdLevel.FEAR,
                        ThirdLevel.FEIGN_DEATH,
                        ThirdLevel.FIREBALL,
                        ThirdLevel.FLAME_ARROWS,
                        ThirdLevel.FLAME_STRIDE_UA,
                        ThirdLevel.FLY,
                        ThirdLevel.GALDERS_TOWER,
                        ThirdLevel.GASEOUS_FORM,
                        ThirdLevel.GLYPH_OF_WARDING,
                        ThirdLevel.HASTE,
                        ThirdLevel.HAYWIRE_UA,
                        ThirdLevel.HYPNOTIC_PATTERN,
                        ThirdLevel.INCITE_GREED,
                        ThirdLevel.INVISIBILITY_TO_CAMERAS_UA,
                        ThirdLevel.LEOMUNDS_TINY_HUT,
                        ThirdLevel.LIFE_TRANSFERENCE,
                        ThirdLevel.LIGHTNING_BOLT,
                        ThirdLevel.MAGIC_CIRCLE,
                        ThirdLevel.MAJOR_IMAGE,
                        ThirdLevel.MELFS_MINUTE_METEORS,
                        ThirdLevel.NONDETECTION,
                        ThirdLevel.PHANTOM_STEED,
                        ThirdLevel.PROTECTION_FROM_BALLISTICS_UA,
                        ThirdLevel.PROTECTION_FROM_ENERGY,
                        ThirdLevel.PSIONIC_BLAST_UA,
                        ThirdLevel.REMOVE_CURSE,
                        ThirdLevel.SENDING,
                        ThirdLevel.SLEET_STORM,
                        ThirdLevel.SLOW,
                        ThirdLevel.STINKING_CLOUD,
                        ThirdLevel.SUMMON_LESSER_DEMONS,
                        ThirdLevel.SUMMON_WARRIOR_SPIRIT_UA,
                        ThirdLevel.THUNDER_STEP,
                        ThirdLevel.TIDAL_WAVE,
                        ThirdLevel.TINY_SERVANT,
                        ThirdLevel.TONGUES,
                        ThirdLevel.VAMPIRIC_TOUCH,
                        ThirdLevel.WALL_OF_SAND,
                        ThirdLevel.WALL_OF_WATER,
                        ThirdLevel.WATER_BREATHING,
                    }
                ),
                FourthLevel: frozenset(
                    {
                        FourthLevel.ARCANE_EYE,
                        FourthLevel.BANISHMENT,
                        FourthLevel.BLIGHT,
                        FourthLevel.CHARM_MONSTER,
                        FourthLevel.CONFUSION,
                        FourthLevel.CONJURE_BARLGURA_UA,
                        FourthLevel.CONJURE_KNOWBOT_UA,
                        FourthLevel.CONJURE_MINOR_ELEMENTALS,
                        FourthLevel.CONJURE_SHADOW_DEMON_UA,
                        FourthLevel.CONTROL_WATER,
                        FourthLevel.DIMENSION_DOOR,
                        FourthLevel.EGO_WHIP_UA,
                        FourthLevel.ELEMENTAL_BANE,
                        FourthLevel.EVARDS_BLACK_TENTACLES,
                        FourthLevel.FABRICATE,
                        FourthLevel.FIRE_SHIELD,
                        FourthLevel.GALDERS_SPEEDY_COURIER,
                        FourthLevel.GATE_SEAL,
                        FourthLevel.GRAVITY_SINKHOLE,
                        FourthLevel.GREATER_INVISIBILITY,
                        FourthLevel.HALLUCINATORY_TERRAIN,
                        FourthLevel.ICE_STORM,
                        FourthLevel.LEOMUNDS_SECRET_CHEST,
                        FourthLevel.LOCATE_CREATURE,
                        FourthLevel.MORDENKAINENS_FAITHFUL_HOUND,
                        FourthLevel.MORDENKAINENS_PRIVATE_SANCTUM,
                        FourthLevel.OTILUKES_RESILIENT_SPHERE,
                        FourthLevel.PHANTASMAL_KILLER,
                        FourthLevel.POLYMORPH,
                        FourthLevel.RAULOTHIMS_PSYCHIC_LANCE,
                        FourthLevel.RAULOTHIMS_PSYCHIC_LANCE_UA,
                        FourthLevel.SICKENING_RADIANCE,
                        FourthLevel.SPIRIT_OF_DEATH,
                        FourthLevel.SPIRIT_OF_DEATH_UA,
                        FourthLevel.STONE_SHAPE,
                        FourthLevel.STONESKIN,
                        FourthLevel.STORM_SPHERE,
                        FourthLevel.SUMMON_GREATER_DEMON,
                        FourthLevel.SYNCHRONICITY_UA,
                        FourthLevel.SYSTEM_BACKDOOR_UA,
                        FourthLevel.VITRIOLIC_SPHERE,
                        FourthLevel.WALL_OF_FIRE,
                        FourthLevel.WATERY_SPHERE,
                        FourthLevel.WIDOGASTS_VAULT_OF_AMBER_HB,
                        FourthLevel.WIDOGASTS_WEB_OF_FIRE_HB,
                    }
                ),
                FifthLevel: frozenset(
                    {
                        FifthLevel.ANIMATE_OBJECTS,
                        FifthLevel.BIGBYS_HAND,
                        FifthLevel.CLOUDKILL,
                        FifthLevel.COMMUNE_WITH_CITY_UA,
                        FifthLevel.CONE_OF_COLD,
                        FifthLevel.CONJURE_ELEMENTAL,
                        FifthLevel.CONJURE_VROCK_UA,
                        FifthLevel.CONTACT_OTHER_PLANE,
                        FifthLevel.CONTROL_WINDS,
                        FifthLevel.CREATE_SPELLJAMMING_HELM,
                        FifthLevel.CREATION,
                        FifthLevel.DANSE_MACABRE,
                        FifthLevel.DAWN,
                        FifthLevel.DOMINATE_PERSON,
                        FifthLevel.DREAM,
                        FifthLevel.ENERVATION,
                        FifthLevel.FAR_STEP,
                        FifthLevel.GEAS,
                        FifthLevel.HOLD_MONSTER,
                        FifthLevel.IMMOLATION,
                        FifthLevel.INFERNAL_CALLING,
                        FifthLevel.LEGEND_LORE,
                        FifthLevel.MISLEAD,
                        FifthLevel.MODIFY_MEMORY,
                        FifthLevel.NEGATIVE_ENERGY_FLOOD,
                        FifthLevel.PASSWALL,
                        FifthLevel.PLANAR_BINDING,
                        FifthLevel.RARYS_TELEPATHIC_BOND,
                        FifthLevel.SCRYING,
                        FifthLevel.SEEMING,
                        FifthLevel.SHUTDOWN_UA,
                        FifthLevel.SKILL_EMPOWERMENT,
                        FifthLevel.STEEL_WIND_STRIKE,
                        FifthLevel.SUMMON_DRACONIC_SPIRIT,
                        FifthLevel.SUMMON_DRACONIC_SPIRIT_UA,
                        FifthLevel.SYNAPTIC_STATIC,
                        FifthLevel.TELEKINESIS,
                        FifthLevel.TELEPORTATION_CIRCLE,
                        FifthLevel.TEMPORAL_SHUNT,
                        FifthLevel.TRANSMUTE_ROCK,
                        FifthLevel.WALL_OF_FORCE,
                        FifthLevel.WALL_OF_LIGHT,
                        FifthLevel.WALL_OF_STONE,
                    }
                ),
                SixthLevel: frozenset(
                    {
                        SixthLevel.ARCANE_GATE,
                        SixthLevel.CHAIN_LIGHTNING,
                        SixthLevel.CIRCLE_OF_DEATH,
                        SixthLevel.CONTINGENCY,
                        SixthLevel.CREATE_HOMUNCULUS,
                        SixthLevel.CREATE_UNDEAD,
                        SixthLevel.DISINTEGRATE,
                        SixthLevel.DRAWMIJS_INSTANT_SUMMONS,
                        SixthLevel.EYEBITE,
                        SixthLevel.FIZBANS_PLATINUM_SHIELD,
                        SixthLevel.FIZBANS_PLATINUM_SHIELD_UA,
                        SixthLevel.FLESH_TO_STONE,
                        SixthLevel.GLOBE_OF_INVULNERABILITY,
                        SixthLevel.GRAVITY_FISSURE,
                        SixthLevel.GUARDS_AND_WARDS,
                        SixthLevel.INVESTITURE_OF_FLAME,
                        SixthLevel.INVESTITURE_OF_ICE,
                        SixthLevel.INVESTITURE_OF_STONE,
                        SixthLevel.INVESTITURE_OF_WIND,
                        SixthLevel.MAGIC_JAR,
                        SixthLevel.MASS_SUGGESTION,
                        SixthLevel.MENTAL_PRISON,
                        SixthLevel.MOVE_EARTH,
                        SixthLevel.OTHERWORLDLY_FORM_UA,
                        SixthLevel.OTILUKES_FREEZING_SPHERE,
                        SixthLevel.OTTOS_IRRESISTIBLE_DANCE,
                        SixthLevel.PROGRAMMED_ILLUSION,
                        SixthLevel.PSYCHIC_CRUSH_UA,
                        SixthLevel.SCATTER,
                        SixthLevel.SOUL_CAGE,
                        SixthLevel.SUNBEAM,
                        SixthLevel.TENSERS_TRANSFORMATION,
                        SixthLevel.TRUE_SEEING,
                        SixthLevel.WALL_OF_ICE,
                        SixthLevel.WIDOGASTS_TRANSMOGRIFICATION_HB,
                    }
                ),
                SeventhLevel: frozenset(
                    {
                        SeventhLevel.CONJURE_HEZROU_UA,
                        SeventhLevel.CREATE_MAGEN,
                        SeventhLevel.CROWN_OF_STARS,
                        SeventhLevel.DELAYED_BLAST_FIREBALL,
                        SeventhLevel.DRACONIC_TRANSFORMATION,
                        SeventhLevel.DRACONIC_TRANSFORMATION_UA,
                        SeventhLevel.ETHEREALNESS,
                        SeventhLevel.FINGER_OF_DEATH,
                        SeventhLevel.FORCECAGE,
                        SeventhLevel.MIRAGE_ARCANE,
                        SeventhLevel.MORDENKAINENS_MAGNIFICENT_MANSION,
                        SeventhLevel.MORDENKAINENS_SWORD,
                        SeventhLevel.PLANE_SHIFT,
                        SeventhLevel.POWER_WORD_PAIN,
                        SeventhLevel.PRISMATIC_SPRAY,
                        SeventhLevel.PROJECT_IMAGE,
                        SeventhLevel.REVERSE_GRAVITY,
                        SeventhLevel.SEQUESTER,
                        SeventhLevel.SIMULACRUM,
                        SeventhLevel.SYMBOL,
                        SeventhLevel.TELEPORT,
                        SeventhLevel.TETHER_ESSENCE,
                        SeventhLevel.WHIRLWIND,
                    }
                ),
                EighthLevel: frozenset(
                    {
                        EighthLevel.ABI_DALZIMS_HORRID_WILTING,
                        EighthLevel.ANTIMAGIC_FIELD,
                        EighthLevel.ANTIPATHY_SYMPATHY,
                        EighthLevel.CLONE,
                        EighthLevel.CONTROL_WEATHER,
                        EighthLevel.DARK_STAR,
                        EighthLevel.DEMIPLANE,
                        EighthLevel.DOMINATE_MONSTER,
                        EighthLevel.FEEBLEMIND,
                        EighthLevel.ILLUSORY_DRAGON,
                        EighthLevel.INCENDIARY_CLOUD,
                        EighthLevel.MADDENING_DARKNESS,
                        EighthLevel.MAZE,
                        EighthLevel.MIGHTY_FORTRESS,
                        EighthLevel.MIND_BLANK,
                        EighthLevel.POWER_WORD_STUN,
                        EighthLevel.REALITY_BREAK,
                        EighthLevel.SUNBURST,
                        EighthLevel.TELEPATHY,
                    }
                ),
                NinthLevel: frozenset(
                    {
                        NinthLevel.ASTRAL_PROJECTION,
                        NinthLevel.FORESIGHT,
                        NinthLevel.GATE,
                        NinthLevel.IMPRISONMENT,
                        NinthLevel.INVULNERABILITY,
                        NinthLevel.MASS_POLYMORPH,
                        NinthLevel.METEOR_SWARM,
                        NinthLevel.POWER_WORD_KILL,
                        NinthLevel.PRISMATIC_WALL,
                        NinthLevel.PSYCHIC_SCREAM,
                        NinthLevel.RAVENOUS_VOID,
                        NinthLevel.SHAPECHANGE,
                        NinthLevel.TIME_RAVAGE,
                        NinthLevel.TIME_STOP,
                        NinthLevel.TRUE_POLYMORPH,
                        NinthLevel.WEIRD,
                        NinthLevel.WISH,
                    }
                ),
            }
        ),
    }
)


def filter_accessible(spell_type: type[Spell], class_: Class) -> frozenset[Spell]:
    return SPELLS_BY_CLASS[class_][spell_type]
