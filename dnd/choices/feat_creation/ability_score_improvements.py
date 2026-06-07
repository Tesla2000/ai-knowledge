from __future__ import annotations

from collections import defaultdict

from dnd.choices.class_creation.character_class import (
    Class,
)

fighter_ability_score_improvements = [4, 6, 8, 12, 14, 16, 19]
normal_ability_score_improvements = [4, 8, 12, 16, 19]
rogue_ability_score_improvements = [4, 8, 10, 12, 16, 19]
main_class2ability_score_improvements = defaultdict(
    lambda: normal_ability_score_improvements,
    {
        Class.FIGHTER: fighter_ability_score_improvements,
        Class.ROGUE: rogue_ability_score_improvements,
    },
)
