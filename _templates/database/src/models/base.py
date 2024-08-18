from __future__ import annotations

from typing import Any

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id: Any

    def __init__(self, **kw: Any):
        from . import maker

        if "id" in kw:
            session = maker()
            existing_element = (
                session.query(type(self)).filter_by(id=kw["id"]).first()
            )
            for column in type(self).__table__.columns:
                name = column.description
                setattr(
                    self, name, kw.get(name, getattr(existing_element, name))
                )
        super().__init__()
