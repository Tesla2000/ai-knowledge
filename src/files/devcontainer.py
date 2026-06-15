from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Literal

from src.files._base import FileBase
from src.files._types import FileType


class DevcontainerJsonFile(FileBase):
    type: Literal[FileType.DEVCONTAINER_JSON] = FileType.DEVCONTAINER_JSON
    relative_path: Path = Path(".devcontainer/devcontainer.json")
    repo_name: str
    content: str = """\
{
  "name": "$display_name",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "lts"
    }
  },
  "postCreateCommand": "bash .devcontainer/post-create.sh",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "charliermarsh.ruff",
        "anthropic.claude-code"
      ]
    },
    "jetbrains": {
      "backend": "PyCharm",
      "plugins": ["31507", "16313"]
    }
  },
  "containerEnv": {
    "IS_SANDBOX": "1"
  }
}
"""

    def _get_content(self, _: Path) -> str:
        display_name = "".join(
            part.capitalize() for part in self.repo_name.split("-")
        )
        return Template(self.content).safe_substitute(
            display_name=display_name
        )


class DevcontainerDockerComposeFile(FileBase):
    type: Literal[FileType.DEVCONTAINER_DOCKER_COMPOSE] = (
        FileType.DEVCONTAINER_DOCKER_COMPOSE
    )
    relative_path: Path = Path(".devcontainer/docker-compose.yml")
    repo_name: str
    content: str = """\
services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    image: $image_name
    volumes:
      - ..:/workspace:cached
      - claude-config:/root/.claude
    command: sleep infinity

volumes:
  claude-config:
"""

    def _get_content(self, _: Path) -> str:
        return Template(self.content).safe_substitute(
            image_name=f"{self.repo_name}-devcontainer"
        )
