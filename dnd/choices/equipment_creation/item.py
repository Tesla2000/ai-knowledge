from pydantic import BaseModel


class Item(BaseModel):
    name: str
    cost: float
    weight: float = 0
