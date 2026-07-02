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
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "workspaceFolder": "/workspace",
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached",
  "remoteUser": "dev",
  "mounts": [
    {
      "source": "claude-config",
      "target": "/home/dev/.claude",
      "type": "volume"
    },
    {
      "source": "${localEnv:SSH_AUTH_SOCK}",
      "target": "/ssh-agent",
      "type": "bind"
    }
  ],
  "postStartCommand": "chown -R dev:dev /home/dev/.claude",
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
    "IS_SANDBOX": "1",
    "SSH_AUTH_SOCK": "/ssh-agent"
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
