# Feature Assignment System

This module provides a flexible system for assigning features to character blueprints, similar to the magical item assignment system.

## Overview

Features represent abilities, traits, or characteristics that a character can gain from their race, class, background, feats, or other sources. Each feature can modify the character's blueprint when assigned through the builder pattern.

## Architecture

The feature system follows the same pattern as magical items:

1. **Feature** - Base class with a `name` and `description`
2. **Specialized Features** - Subclasses that modify specific blueprint fields
3. **FeatureAssigner** - BuildingBlock that wraps a Feature and applies it to a blueprint

## Base Feature Class

```python
from dnd.character.feature import Feature

# Simple descriptive feature
trance = Feature(
    name="Trance",
    description="Elves don't need to sleep. Instead, they meditate deeply for 4 hours a day."
)
```

## Specialized Features

### AbilityFeature

For features that add descriptive abilities without mechanical modifiers.

```python
from dnd.character.feature.specialized_features import AbilityFeature

relentless_endurance = AbilityFeature(
    name="Relentless Endurance",
    description="When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point instead."
)
```

### StatBoostFeature

For features that increase ability scores.

```python
from dnd.character.feature.specialized_features import StatBoostFeature
from dnd.choices.stats_creation.statistic import Statistic

asi = StatBoostFeature(
    name="Ability Score Improvement",
    description="Increase Strength by 2",
    stat=Statistic.STRENGTH,
    boost_amount=2
)
```

The stat boost respects the character's `stats_cup` (maximum stat values).

### SkillProficiencyFeature

For features that grant skill proficiencies.

```python
from dnd.character.feature.specialized_features import SkillProficiencyFeature
from dnd.skill_proficiency import Skill

skill_expert = SkillProficiencyFeature(
    name="Skill Expert",
    description="Gain proficiency in Perception and Stealth",
    skills=frozenset([Skill.PERCEPTION, Skill.STEALTH])
)
```

### ACBonusFeature

For features that provide AC bonuses.

```python
from dnd.character.feature.specialized_features import ACBonusFeature

defense = ACBonusFeature(
    name="Defense Fighting Style",
    description="While wearing armor, you gain +1 AC",
    ac_bonus=1
)
```

### SavingThrowBonusFeature

For features that provide saving throw bonuses.

```python
from dnd.character.feature.specialized_features import SavingThrowBonusFeature
from dnd.choices.stats_creation.statistic import Statistic

# Bonus to a specific save
resilient = SavingThrowBonusFeature(
    name="Resilient (Constitution)",
    description="Gain +1 bonus to Constitution saving throws",
    stat=Statistic.CONSTITUTION,
    bonus=1
)

# Universal bonus to all saves
bless = SavingThrowBonusFeature(
    name="Bless",
    description="Gain +1 bonus to all saving throws",
    stat=None,  # None means all saves
    bonus=1
)
```

## Using Features with the Builder Pattern

Features are applied through the `FeatureAssigner` BuildingBlock:

```python
from dnd.character.builder import Builder
from dnd.character.blueprint.building_blocks import FeatureAssigner
from dnd.character.feature.specialized_features import StatBoostFeature
from dnd.choices.stats_creation.statistic import Statistic

# Create a feature
asi = StatBoostFeature(
    name="Ability Score Improvement",
    description="Increase Strength by 2",
    stat=Statistic.STRENGTH,
    boost_amount=2
)

# Wrap it in a FeatureAssigner
feature_assigner = FeatureAssigner(feature=asi)

# Add it to the builder
builder = Builder(
    building_blocks=(
        # ... other building blocks ...
        feature_assigner,
    ),
    increment_storage=increment_storage
)

# Build the character
character = builder.build()
```

## Creating Custom Features

To create a custom feature type, extend the `Feature` class and override the `assign_to` method:

```python
from dnd.character.feature.feature import Feature
from dnd.character.blueprint.blueprint import Blueprint

class CustomFeature(Feature):
    """Your custom feature with additional fields."""

    # Add your custom fields
    custom_field: int

    def assign_to(self, blueprint: Blueprint) -> Blueprint:
        """Apply this feature to the blueprint.

        Returns a new blueprint with modifications.
        """
        # Modify the blueprint as needed
        return type(blueprint)(
            # Set fields you want to modify
            some_field=new_value,
            # Always add to other_active_abilities
            other_active_abilities=blueprint.other_active_abilities
                + (f"{self.name}: {self.description}",)
        )
```

## Implementation Details

### Blueprint Fields

Features can modify any blueprint field:
- `stats` - Ability scores
- `stats_cup` - Maximum ability scores
- `ac_bonus` - Armor class bonus
- `saving_throw_bonuses` - Saving throw modifiers
- `skill_proficiencies` - Skill proficiency tuple
- `other_active_abilities` - Text descriptions of abilities

### Important Notes

1. **Immutability**: Blueprints are immutable (frozen). Always return a new blueprint instance.
2. **Type Consistency**: Be aware of field types (e.g., `skill_proficiencies` is a tuple in Blueprint, not a frozenset).
3. **Always Add to other_active_abilities**: Every feature should add its name and description to `other_active_abilities` for tracking.

## Testing

See `dnd_character_creator/character/tests/test_feature_assignment.py` for comprehensive test examples demonstrating all feature types.
