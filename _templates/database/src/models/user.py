from __future__ import annotations

from peewee import CharField

base import Base


class User(Base):
    name: str = CharField()
