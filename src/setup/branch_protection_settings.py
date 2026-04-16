from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BranchProtectionSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    dismiss_stale_reviews: bool = False
    required_approving_review_count: int = 0
    allow_force_pushes: bool = False
    allow_deletions: bool = False
