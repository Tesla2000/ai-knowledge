from __future__ import annotations

from typing import cast
from typing import Literal
from typing import TYPE_CHECKING

from typing_protocol_intersection import ProtocolIntersection

from dnd.character.blueprint.state import Blueprint
from dnd.character.blueprint.state import BlueprintProtocol
from dnd.character.blueprint.state import HasFeats
from dnd.character.blueprint.state import HasLanguages
from dnd.character.blueprint.state import HasSkillProficiencies
from dnd.character.blueprint.state import HasToolProficiencies
from dnd.character.delta.delta import Delta
from dnd.character.feature.feats import FeatName
from dnd.choices.language import Language
from dnd.other_profficiencies import GamingSet
from dnd.other_profficiencies import MusicalInstrument
from dnd.other_profficiencies import ToolProficiency
from dnd.skill_proficiency import Skill


class AIChoicesResolutionDelta(Delta):
    """Delta produced by AIAllNonStatChoicesResolver — resolves all non-stat choices at once."""

    delta_type: Literal["AIChoicesResolutionDelta"] = "AIChoicesResolutionDelta"
    languages: tuple[Language, ...]
    skill_proficiencies: tuple[Skill, ...]
    feats: tuple[FeatName, ...]
    tool_proficiencies: tuple[ToolProficiency | GamingSet | MusicalInstrument, ...]
    n_skill_choices: int
    skills_to_choose_from: frozenset[Skill]

    def apply[T: BlueprintProtocol](
        self, state: T
    ) -> ProtocolIntersection[
        T,
        ProtocolIntersection[
            HasLanguages,
            ProtocolIntersection[
                HasSkillProficiencies,
                ProtocolIntersection[HasFeats, HasToolProficiencies],
            ],
        ],
    ]:
        if TYPE_CHECKING:

            class BlueprintWithChoicesResolved(Blueprint):
                languages: tuple[Language, ...]
                skill_proficiencies: tuple[Skill, ...]
                feats: tuple[FeatName, ...]
                tool_proficiencies: tuple[
                    ToolProficiency | GamingSet | MusicalInstrument, ...
                ]
                n_skill_choices: int
                skills_to_choose_from: frozenset[Skill]

        else:

            class BlueprintWithChoicesResolved(type(state)):
                languages: tuple[Language, ...]
                skill_proficiencies: tuple[Skill, ...]
                feats: tuple[FeatName, ...]
                tool_proficiencies: tuple[
                    ToolProficiency | GamingSet | MusicalInstrument, ...
                ]
                n_skill_choices: int
                skills_to_choose_from: frozenset[Skill]

        return cast(
            ProtocolIntersection[
                T,
                ProtocolIntersection[
                    HasLanguages,
                    ProtocolIntersection[
                        HasSkillProficiencies,
                        ProtocolIntersection[HasFeats, HasToolProficiencies],
                    ],
                ],
            ],
            BlueprintWithChoicesResolved.model_validate(
                dict(state)
                | {
                    "languages": self.languages,
                    "skill_proficiencies": self.skill_proficiencies,
                    "feats": self.feats,
                    "tool_proficiencies": self.tool_proficiencies,
                    "n_skill_choices": self.n_skill_choices,
                    "skills_to_choose_from": self.skills_to_choose_from,
                }
            ),
        )
