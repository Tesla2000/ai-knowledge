from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    AarakocraRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    AasimarRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    BugbearRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    CentaurRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    ChangelingRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    DragonbornRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    DwarfRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    ElfRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    FirbolgRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    GenasiAirRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    GenasiEarthRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    GenasiFireRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    GenasiWaterRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    GnomeRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    GoblinRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    GoliathRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    GrungRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    HalfElfRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    HalflingRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    HalfOrcRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    HobgoblinRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    HumanRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    KalashtarRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    KenkuRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    KoboldRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    LeoninRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    LizardfolkRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    MinotaurRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    OrcRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    SatyrRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    ShifterRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    TabaxiRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    TieflingRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    TortleRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    VerdanRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    WarforgedRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    RaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.race_assigner import (
    YuanTiPurebloodRaceAssigner,
)
from dnd.character.blueprint.building_blocks.race_assigner.random_race_assigner import (
    RandomRaceAssigner,
)
from pydantic import Field

AnyRaceAssigner = Annotated[
    Union[
        AarakocraRaceAssigner,
        AasimarRaceAssigner,
        BugbearRaceAssigner,
        CentaurRaceAssigner,
        ChangelingRaceAssigner,
        DragonbornRaceAssigner,
        DwarfRaceAssigner,
        ElfRaceAssigner,
        FirbolgRaceAssigner,
        GenasiAirRaceAssigner,
        GenasiEarthRaceAssigner,
        GenasiFireRaceAssigner,
        GenasiWaterRaceAssigner,
        GnomeRaceAssigner,
        GoblinRaceAssigner,
        GoliathRaceAssigner,
        GrungRaceAssigner,
        HalfElfRaceAssigner,
        HalflingRaceAssigner,
        HalfOrcRaceAssigner,
        HobgoblinRaceAssigner,
        HumanRaceAssigner,
        KalashtarRaceAssigner,
        KenkuRaceAssigner,
        KoboldRaceAssigner,
        LeoninRaceAssigner,
        LizardfolkRaceAssigner,
        MinotaurRaceAssigner,
        OrcRaceAssigner,
        SatyrRaceAssigner,
        ShifterRaceAssigner,
        TabaxiRaceAssigner,
        TieflingRaceAssigner,
        TortleRaceAssigner,
        VerdanRaceAssigner,
        WarforgedRaceAssigner,
        YuanTiPurebloodRaceAssigner,
        RandomRaceAssigner,
        RaceAssigner,
    ],
    Field(discriminator="type"),
]

__all__ = [
    "AarakocraRaceAssigner",
    "AasimarRaceAssigner",
    "BugbearRaceAssigner",
    "CentaurRaceAssigner",
    "ChangelingRaceAssigner",
    "DragonbornRaceAssigner",
    "DwarfRaceAssigner",
    "ElfRaceAssigner",
    "FirbolgRaceAssigner",
    "GenasiAirRaceAssigner",
    "GenasiEarthRaceAssigner",
    "GenasiFireRaceAssigner",
    "GenasiWaterRaceAssigner",
    "GnomeRaceAssigner",
    "GoblinRaceAssigner",
    "GoliathRaceAssigner",
    "GrungRaceAssigner",
    "HalfElfRaceAssigner",
    "HalflingRaceAssigner",
    "HalfOrcRaceAssigner",
    "HobgoblinRaceAssigner",
    "HumanRaceAssigner",
    "KalashtarRaceAssigner",
    "KenkuRaceAssigner",
    "KoboldRaceAssigner",
    "LeoninRaceAssigner",
    "LizardfolkRaceAssigner",
    "MinotaurRaceAssigner",
    "OrcRaceAssigner",
    "SatyrRaceAssigner",
    "ShifterRaceAssigner",
    "TabaxiRaceAssigner",
    "TieflingRaceAssigner",
    "TortleRaceAssigner",
    "VerdanRaceAssigner",
    "WarforgedRaceAssigner",
    "YuanTiPurebloodRaceAssigner",
    "RandomRaceAssigner",
    "RaceAssigner",
    "AnyRaceAssigner",
]
