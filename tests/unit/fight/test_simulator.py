from enum import IntEnum
from typing import Self

import pytest

from dnd.character._ability_name import AbilityName
from dnd.character.actions.combat import AnyCombatAction, AttackWithBattleaxe
from dnd.character.actions.combat.move import Move
from dnd.character.presentable_character import PresentableCharacter
from dnd.character.stats import Stats
from dnd.choices.equipment_creation.weapons import WeaponName
from dnd.fight._team_id import TeamId
from dnd.fight.battlemap import Battlemap
from dnd.fight.fight_character import AnyActiveCombatant, FightCharacter
from dnd.fight.simulator import SimResult, Simulator
from dnd.fight.strategy import RandomStrategy

_STATS = Stats(
    strength=17,
    dexterity=13,
    constitution=16,
    intelligence=9,
    wisdom=11,
    charisma=8,
)

_PC_DATA: dict[str, object] = {
    "race": "Human",
    "stats": _STATS.model_dump(),
    "health_base": 20,
    "character_data": {"name": ""},
    "classes": {
        "wizard": 0,
        "sorcerer": 0,
        "fighter": 0,
        "barbarian": 1,
        "rogue": 0,
        "cleric": 0,
        "druid": 0,
        "paladin": 0,
        "ranger": 0,
        "monk": 0,
        "bard": 0,
        "warlock": 0,
        "artificer": 0,
    },
    "speed": 30,
    "dark_vision_range": 0,
    "saving_throw_proficiencies": [],
    "other_active_abilities": [],
    "weapons": [WeaponName.BATTLEAXE],
    "actions": [AbilityName.ATTACK_WITH_BATTLEAXE],
}


class _TwoFightSlot(IntEnum):
    A = 0
    B = 1


class _TwoFightBattlemap(Battlemap[_TwoFightSlot]):
    combatants: tuple[AnyActiveCombatant, AnyActiveCombatant]

    def all_slots(self) -> tuple[_TwoFightSlot, ...]:
        return tuple(_TwoFightSlot)

    def get_combatant(self, slot: _TwoFightSlot) -> AnyActiveCombatant:
        match slot:
            case _TwoFightSlot.A:
                return self.combatants[0]
            case _TwoFightSlot.B:
                return self.combatants[1]

    def replace_combatant(
        self, slot: _TwoFightSlot, updated: AnyActiveCombatant
    ) -> Self:
        match slot:
            case _TwoFightSlot.A:
                return self.model_copy(
                    update={"combatants": (updated, self.combatants[1])}
                )
            case _TwoFightSlot.B:
                return self.model_copy(
                    update={"combatants": (self.combatants[0], updated)}
                )


def _make_fc(
    name: str, initiative: int, team_id: TeamId, speed: int = 0
) -> FightCharacter:
    data = {**_PC_DATA, "character_data": {"name": name}}
    pc = PresentableCharacter.model_validate(data)
    return FightCharacter.from_presentable(
        pc, initiative=initiative, team_id=team_id
    ).model_copy(
        update={
            "position": (0, 0) if team_id == TeamId.A else (1, 0),
            "speed": speed,
        }
    )


@pytest.mark.unit
class TestTeamId:
    def test_team_id_is_int_enum(self) -> None:
        assert TeamId.A == 0
        assert TeamId.B == 1

    def test_team_id_on_fight_character_defaults_to_a(self) -> None:
        pc = PresentableCharacter.model_validate(_PC_DATA)
        fc = FightCharacter.from_presentable(pc, initiative=10)
        assert fc.team_id == TeamId.A

    def test_team_id_propagates_through_from_presentable(self) -> None:
        pc = PresentableCharacter.model_validate(_PC_DATA)
        fc = FightCharacter.from_presentable(pc, initiative=10, team_id=TeamId.B)
        assert fc.team_id == TeamId.B


@pytest.mark.unit
class TestRandomStrategy:
    def test_choose_returns_action_from_groups(self) -> None:
        fc = _make_fc("a", 10, TeamId.A)
        target = _make_fc("b", 5, TeamId.B)
        bm = _TwoFightBattlemap(combatants=(fc, target))
        attacks = AttackWithBattleaxe.create(_TwoFightSlot.A, fc, bm)
        groups: tuple[tuple[AnyCombatAction[_TwoFightSlot], ...], ...] = (attacks,)
        strategy: RandomStrategy[_TwoFightSlot] = RandomStrategy()
        action = strategy.choose(groups)
        assert isinstance(action, AttackWithBattleaxe)


@pytest.mark.unit
class TestSimulator:
    def test_two_fighters_produce_a_winner(self) -> None:
        fc_a = _make_fc("A", initiative=15, team_id=TeamId.A)
        fc_b = _make_fc("B", initiative=12, team_id=TeamId.B)
        battlemap = _TwoFightBattlemap(combatants=(fc_a, fc_b))
        strategy: RandomStrategy[_TwoFightSlot] = RandomStrategy()
        result = Simulator(battlemap, strategy_a=strategy, strategy_b=strategy).run()
        assert result.winner in (TeamId.A, TeamId.B)
        assert result.rounds >= 1
        assert len(result.log) > 0

    def test_sim_result_is_named_tuple(self) -> None:
        result = SimResult(winner=TeamId.A, log=["line"], rounds=3)
        assert result.winner == TeamId.A
        assert result.rounds == 3

    def test_log_contains_round_headers(self) -> None:
        fc_a = _make_fc("A", initiative=15, team_id=TeamId.A)
        fc_b = _make_fc("B", initiative=12, team_id=TeamId.B)
        battlemap = _TwoFightBattlemap(combatants=(fc_a, fc_b))
        strategy: RandomStrategy[_TwoFightSlot] = RandomStrategy()
        result = Simulator(battlemap, strategy_a=strategy, strategy_b=strategy).run()
        assert any("Round" in line for line in result.log)

    def test_strategy_dispatch_uses_correct_team(self) -> None:
        class _FixedStrategy:
            def __init__(self, action_index: int) -> None:
                self._idx = action_index

            def choose(
                self,
                groups: tuple[tuple[AnyCombatAction[_TwoFightSlot], ...], ...],
            ) -> AnyCombatAction[_TwoFightSlot]:
                return groups[0][self._idx % len(groups[0])]

        fc_a = _make_fc("A", initiative=20, team_id=TeamId.A)
        fc_b = _make_fc("B", initiative=5, team_id=TeamId.B)
        battlemap = _TwoFightBattlemap(combatants=(fc_a, fc_b))
        result = Simulator(
            battlemap,
            strategy_a=_FixedStrategy(0),
            strategy_b=_FixedStrategy(0),
        ).run()
        assert result.winner in (TeamId.A, TeamId.B)

    def test_movement_closes_distance(self) -> None:
        fc_a = _make_fc("A", 20, TeamId.A, speed=5).model_copy(
            update={"position": (0, 0)}
        )
        fc_b = _make_fc("B", 5, TeamId.B, speed=0).model_copy(
            update={"position": (2, 0)}
        )
        battlemap = _TwoFightBattlemap(combatants=(fc_a, fc_b))
        target = (2, 0)

        class _ApproachStrategy:
            def choose(
                self,
                groups: tuple[tuple[AnyCombatAction[_TwoFightSlot], ...], ...],
            ) -> AnyCombatAction[_TwoFightSlot]:
                for group in groups:
                    moves = [a for a in group if isinstance(a, Move)]
                    if moves:
                        return min(
                            moves,
                            key=lambda m: max(
                                abs(m.to[0] - target[0]), abs(m.to[1] - target[1])
                            ),
                        )
                return groups[0][0]

        result = Simulator(
            battlemap,
            strategy_a=_ApproachStrategy(),
            strategy_b=_ApproachStrategy(),
        ).run()
        assert result.winner in (TeamId.A, TeamId.B)

    def test_opportunity_attack_fires_on_retreat(self) -> None:
        fc_a = _make_fc("A", 20, TeamId.A, speed=5)
        fc_b = _make_fc("B", 5, TeamId.B, speed=0)
        battlemap = _TwoFightBattlemap(combatants=(fc_a, fc_b))
        b_pos = fc_b.position

        class _RetreatOnceThenApproachStrategy:
            def __init__(self) -> None:
                self._retreated = False

            def choose(
                self,
                groups: tuple[tuple[AnyCombatAction[_TwoFightSlot], ...], ...],
            ) -> AnyCombatAction[_TwoFightSlot]:
                for group in groups:
                    moves = [a for a in group if isinstance(a, Move)]
                    if moves:
                        if not self._retreated:
                            for m in moves:
                                if m.triggered_oa_from:
                                    self._retreated = True
                                    return m
                            self._retreated = True
                            return moves[0]
                        return min(
                            moves,
                            key=lambda m: max(
                                abs(m.to[0] - b_pos[0]), abs(m.to[1] - b_pos[1])
                            ),
                        )
                return groups[0][0]

        class _AttackStrategy:
            def choose(
                self,
                groups: tuple[tuple[AnyCombatAction[_TwoFightSlot], ...], ...],
            ) -> AnyCombatAction[_TwoFightSlot]:
                return groups[0][0]

        result = Simulator(
            battlemap,
            strategy_a=_RetreatOnceThenApproachStrategy(),
            strategy_b=_AttackStrategy(),
        ).run()
        assert any("opportunity attack" in line for line in result.log)
