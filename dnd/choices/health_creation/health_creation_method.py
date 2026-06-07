from __future__ import annotations

from enum import Enum


class HealthCreationMethod(str, Enum):
    AVERAGE = "average"
    RANDOM = "random"
