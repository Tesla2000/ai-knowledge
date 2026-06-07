from __future__ import annotations

import shutil
from collections.abc import MutableMapping
from os import PathLike
from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, Field, model_validator
from pydantic.alias_generators import to_snake
from pydantic_settings import (
    BaseSettings,
    CliApp,
    CliPositionalArg,
    SettingsConfigDict,
)

from src.setup import GitHubSetup
from src.templates import AnyTemplate


def _ensure_absolute(path: Path) -> Path:
    if not path.is_absolute():
        raise ValueError(f"{path} is not absolute")
    return path


class Generate(BaseSettings):
    model_config = SettingsConfigDict(
        cli_kebab_case=True,
        cli_parse_args=True,
        env_nested_delimiter="__",
    )

    project_path: CliPositionalArg[Annotated[Path, AfterValidator(_ensure_absolute)]]
    template: AnyTemplate
    setup: GitHubSetup = Field(default_factory=GitHubSetup)

    @model_validator(mode="before")
    @staticmethod
    def _assign_repo_name(
        data: MutableMapping[str, object],
    ) -> MutableMapping[str, object]:
        template = data.setdefault("template", {})
        if not isinstance(template, MutableMapping):
            return data
        project_path = data.get("project_path")
        if not isinstance(project_path, (str, PathLike)):
            return data
        template["repo_name"] = data.get(
            "repo_name", to_snake(Path(project_path).name).replace("_", "-")
        )
        return data

    def cli_cmd(self) -> None:
        self.project_path.mkdir()
        try:
            self.template.generate(self.project_path)
            self.setup.run(self.project_path)
        except:  # noqa: E722
            shutil.rmtree(self.project_path)
            raise


if __name__ == "__main__":
    CliApp.run(Generate)
