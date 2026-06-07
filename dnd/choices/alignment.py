from __future__ import annotations

from enum import Enum


class Alignment(str, Enum):
    LAWFUL_GOOD = "lawful_good"
    TRUE_LAWFUL = "true_lawful"
    LAWFUL_NEUTRAL = "lawful_neutral"
    LAWFUL_EVIL = "lawful_evil"
    TRUE_GOOD = "true_good"
    NEUTRAL_GOOD = "neutral_good"
    NEUTRAL_EVIL = "neutral_evil"
    TRUE_NEUTRAL = "true_neutral"
    NEUTRAL_NEUTRAL = "neutral_neutral"
    TRUE_EVIL = "true_evil"
    CHAOTIC_GOOD = "chaotic_good"
    TRUE_CHAOTIC = "true_chaotic"
    CHAOTIC_NEUTRAL = "chaotic_neutral"
    CHAOTIC_EVIL = "chaotic_evil"
