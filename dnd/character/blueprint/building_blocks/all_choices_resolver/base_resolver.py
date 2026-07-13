"""Base class for all choices resolution."""

from pydantic import BaseModel


class AllChoicesResolverBase(BaseModel):
    """Abstract base class for resolvers that handle all character choices.

    Implementations must resolve:
    - Language choices (ANY_OF_YOUR_CHOICE placeholders)
    - Skill proficiency choices (ANY_OF_YOUR_CHOICE placeholders)
    - Feat choices (ANY_OF_YOUR_CHOICE placeholders)
    - Tool proficiency choices (ANY_OF_YOUR_CHOICE placeholders)
    - Stat choices (n_stat_choices distribution)
    - Skill choices (n_skill_choices from available pool)
    - Initial data (name, backstory, etc.)
    - Equipment choices

    This base class provides a common type for both sequential resolvers
    (AllChoicesResolver) and holistic AI resolvers
    (AIAllChoicesResolver).

    Subclasses implement apply() via BuildingBlock.
    """
