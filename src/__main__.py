from __future__ import annotations

from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, Field
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

    project_path: CliPositionalArg[
        Annotated[Path, AfterValidator(_ensure_absolute)]
    ]
    template: AnyTemplate
    setup: GitHubSetup = Field(default_factory=GitHubSetup)

    def cli_cmd(self) -> None:
        self.project_path.mkdir(exist_ok=True)
        self.template.generate(self.project_path)
        self.setup.run(self.project_path)


if __name__ == "__main__":
    CliApp.run(Generate)
