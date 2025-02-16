from __future__ import annotations

from datetime import date
from json import JSONEncoder

from pydantic import BaseModel


class BaseModelJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.model_dump()
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)
