from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Optional

from github import Github
from pydantic import BaseModel
from pydantic import SecretStr
from pydantic.alias_generators import to_snake

from src.setup.branch_protection_settings import BranchProtectionSettings
from src.setup.repo_settings import RepoSettings


class GitHubSetup(BaseModel):
    github_token: Optional[SecretStr] = None
    repo_name: Optional[str] = None
    main_branch: str = "main"
    repo_settings: RepoSettings = RepoSettings()
    branch_protection_settings: BranchProtectionSettings = (
        BranchProtectionSettings()
    )

    def run(self, project_path: Path) -> None:
        env = os.environ.copy()
        env["PATH"] = ":".join(
            [
                str(Path.home() / ".local" / "bin"),
                str(Path.home() / ".cargo" / "bin"),
                env.get("PATH", ""),
            ]
        )
        subprocess.run(
            ["bash", str(Path("src/setup/setup.sh").resolve())],
            cwd=project_path,
            env=env,
            check=True,
        )
        if self.github_token is None:
            return
        repo_name = self.repo_name or to_snake(project_path.name).replace(
            "_", "-"
        )
        g = Github(self.github_token.get_secret_value())
        user = g.get_user()
        repo = user.create_repo(repo_name, **self.repo_settings.model_dump())
        token = self.github_token.get_secret_value()
        remote_url = f"https://{token}@github.com/{user.login}/{repo_name}.git"
        subprocess.run(
            ["git", "remote", "add", "origin", remote_url],
            cwd=project_path,
            check=True,
        )
        subprocess.run(
            ["git", "push", "-u", "origin", self.main_branch],
            cwd=project_path,
            check=True,
        )
        repo.get_branch(self.main_branch).edit_protection(
            **self.branch_protection_settings.model_dump()
        )
