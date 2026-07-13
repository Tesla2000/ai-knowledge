from dnd.character.magical_item.level import Level
from dnd.character.magical_item.source import Source
from pydantic import BaseModel


class MagicalItem(BaseModel):
    name: str
    description: str
    level: Level
    source: Source
    attuned: bool
