from typing import Annotated
from typing import Union

from dnd.character.blueprint.building_blocks.get_discriminator import (
    get_discriminator,
)
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
from pydantic import Tag

AnyRaceAssigner = Annotated[
    Union[
        Annotated[AarakocraRaceAssigner, Tag(AarakocraRaceAssigner.get_block_type())],
        Annotated[AasimarRaceAssigner, Tag(AasimarRaceAssigner.get_block_type())],
        Annotated[BugbearRaceAssigner, Tag(BugbearRaceAssigner.get_block_type())],
        Annotated[CentaurRaceAssigner, Tag(CentaurRaceAssigner.get_block_type())],
        Annotated[ChangelingRaceAssigner, Tag(ChangelingRaceAssigner.get_block_type())],
        Annotated[DragonbornRaceAssigner, Tag(DragonbornRaceAssigner.get_block_type())],
        Annotated[DwarfRaceAssigner, Tag(DwarfRaceAssigner.get_block_type())],
        Annotated[ElfRaceAssigner, Tag(ElfRaceAssigner.get_block_type())],
        Annotated[FirbolgRaceAssigner, Tag(FirbolgRaceAssigner.get_block_type())],
        Annotated[GenasiAirRaceAssigner, Tag(GenasiAirRaceAssigner.get_block_type())],
        Annotated[
            GenasiEarthRaceAssigner, Tag(GenasiEarthRaceAssigner.get_block_type())
        ],
        Annotated[GenasiFireRaceAssigner, Tag(GenasiFireRaceAssigner.get_block_type())],
        Annotated[
            GenasiWaterRaceAssigner, Tag(GenasiWaterRaceAssigner.get_block_type())
        ],
        Annotated[GnomeRaceAssigner, Tag(GnomeRaceAssigner.get_block_type())],
        Annotated[GoblinRaceAssigner, Tag(GoblinRaceAssigner.get_block_type())],
        Annotated[GoliathRaceAssigner, Tag(GoliathRaceAssigner.get_block_type())],
        Annotated[GrungRaceAssigner, Tag(GrungRaceAssigner.get_block_type())],
        Annotated[HalfElfRaceAssigner, Tag(HalfElfRaceAssigner.get_block_type())],
        Annotated[HalflingRaceAssigner, Tag(HalflingRaceAssigner.get_block_type())],
        Annotated[HalfOrcRaceAssigner, Tag(HalfOrcRaceAssigner.get_block_type())],
        Annotated[HobgoblinRaceAssigner, Tag(HobgoblinRaceAssigner.get_block_type())],
        Annotated[HumanRaceAssigner, Tag(HumanRaceAssigner.get_block_type())],
        Annotated[KalashtarRaceAssigner, Tag(KalashtarRaceAssigner.get_block_type())],
        Annotated[KenkuRaceAssigner, Tag(KenkuRaceAssigner.get_block_type())],
        Annotated[KoboldRaceAssigner, Tag(KoboldRaceAssigner.get_block_type())],
        Annotated[LeoninRaceAssigner, Tag(LeoninRaceAssigner.get_block_type())],
        Annotated[LizardfolkRaceAssigner, Tag(LizardfolkRaceAssigner.get_block_type())],
        Annotated[MinotaurRaceAssigner, Tag(MinotaurRaceAssigner.get_block_type())],
        Annotated[OrcRaceAssigner, Tag(OrcRaceAssigner.get_block_type())],
        Annotated[SatyrRaceAssigner, Tag(SatyrRaceAssigner.get_block_type())],
        Annotated[ShifterRaceAssigner, Tag(ShifterRaceAssigner.get_block_type())],
        Annotated[TabaxiRaceAssigner, Tag(TabaxiRaceAssigner.get_block_type())],
        Annotated[TieflingRaceAssigner, Tag(TieflingRaceAssigner.get_block_type())],
        Annotated[TortleRaceAssigner, Tag(TortleRaceAssigner.get_block_type())],
        Annotated[VerdanRaceAssigner, Tag(VerdanRaceAssigner.get_block_type())],
        Annotated[WarforgedRaceAssigner, Tag(WarforgedRaceAssigner.get_block_type())],
        Annotated[
            YuanTiPurebloodRaceAssigner,
            Tag(YuanTiPurebloodRaceAssigner.get_block_type()),
        ],
        Annotated[RandomRaceAssigner, Tag(RandomRaceAssigner.get_block_type())],
        Annotated[RaceAssigner, Tag(RaceAssigner.get_block_type())],
    ],
    get_discriminator(),
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
