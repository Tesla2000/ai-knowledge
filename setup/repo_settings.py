from __future__ import annotations

from pydantic import BaseModel


class RepoSettings(BaseModel, frozen=True):
    private: bool = True
    delete_branch_on_merge: bool = True
    allow_squash_merge: bool = True
    allow_merge_commit: bool = False
    allow_rebase_merge: bool = False
