from abc import ABC
from abc import abstractmethod

from dnd.character.presentable_character import PresentableCharacter


class ConvertibleBlueprint(ABC):
    @abstractmethod
    def to_presentable_character(self) -> PresentableCharacter: ...
