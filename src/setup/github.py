from __future__ import annotations

import os
import subprocess
from collections.abc import Mapping
from pathlib import Path

from github import Github
from github.AuthenticatedUser import AuthenticatedUser
from pydantic import BaseModel, Field, SecretStr
from pydantic.alias_generators import to_snake

from src.setup.branch_protection_settings import BranchProtectionSettings
from src.setup.repo_settings import RepoSettings


class GitHubSetup(BaseModel):
    github_token: SecretStr | None = None
    repo_name: str | None = None
    main_branch: str = "main"
    repo_settings: RepoSettings = RepoSettings()
    branch_protection_settings: BranchProtectionSettings | None = None
    repo_secrets: Mapping[str, SecretStr] = Field(default_factory=dict)

    def run(self, project_path: Path) -> None:
        env = os.environ.copy()
        env["PATH"] = ":".join(
            [
                str(Path.home() / ".local" / "bin"),
                str(Path.home() / ".cargo" / "bin"),
                env.get("PATH", ""),
            ]
        )
        subprocess.run(  # nosec B603 B607
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
        if not isinstance(user, AuthenticatedUser):
            msg = f"{user=} is not an instance of {AuthenticatedUser.__name__}"
            raise TypeError(msg)
        repo = user.create_repo(repo_name, **self.repo_settings.model_dump())
        try:
            token = self.github_token.get_secret_value()
            remote_url = (
                f"https://{token}@github.com/{user.login}/{repo_name}.git"
            )
            subprocess.run(  # nosec B603 B607
                ["git", "remote", "add", "origin", remote_url],
                cwd=project_path,
                check=True,
            )
            subprocess.run(  # nosec B603 B607
                ["git", "push", "-u", "origin", self.main_branch],
                cwd=project_path,
                check=True,
            )
            if self.branch_protection_settings is not None:
                repo.get_branch(self.main_branch).edit_protection(
                    **self.branch_protection_settings.model_dump(mode="json")
                )
            for name, secret in self.repo_secrets.items():
                repo.create_secret(name, secret.get_secret_value())
        except:
            repo.delete()
            raise
