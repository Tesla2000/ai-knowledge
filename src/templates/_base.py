from __future__ import annotations

from abc import ABC
from collections.abc import Mapping
from contextlib import ExitStack
from pathlib import Path

from pydantic import BaseModel, Field

from src.files import (
    ClaudeReviewWorkflow,
    CodeOwnersFile,
    DevcontainerDockerComposeFile,
    DevcontainerJsonFile,
    File,
    Gitignore,
    MitLicense,
    PackageFile,
    PreCommitConfig,
    PreCommitRunWorkflow,
    PythonVersion,
    PythonVersionFile,
    ReadmeFile,
    SetupScript,
    TestsWorkflow,
)
from src.files._base import FileBase
from src.templates._type import TemplateType

_DEVCONTAINER_DOCKERFILE = """\
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \\
        git \\
        curl \\
        ca-certificates \\
        build-essential \\
        bubblewrap \\
        socat \\
        nodejs \\
        npm \\
        openssh-client \\
        locales-all \\
        micro \\
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN npm install -g @anthropic-ai/claude-code

RUN groupadd --gid 1000 dev && useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home dev

ENV UV_LINK_MODE=copy
ENV PATH="/workspace/.venv/bin:${PATH}"
ENV PRE_COMMIT_HOME="/.jbdevcontainer/pre-commit"
ENV EDITOR=micro

RUN mkdir -p /.jbdevcontainer/pre-commit && chown -R dev:dev /.jbdevcontainer

WORKDIR /workspace
RUN chown dev:dev /workspace

USER dev

COPY --chown=dev:dev pyproject.toml uv.lock .pre-commit-config.yaml README.md ./
RUN uv sync --group dev --no-install-project
RUN git config --global user.email "build@example.com" && \\
    git config --global user.name "Build" && \\
    git init && git add -A && git commit -m init && \\
    pre-commit run --all-files; rm -rf .git
"""

_DEVCONTAINER_CLAUDE_SETTINGS = """\
{
  "theme": "dark"
}
"""

_DEVCONTAINER_POST_CREATE = """\
#!/usr/bin/env bash
set -e

git config --global --add safe.directory /workspace

if [ ! -f /home/dev/.claude/settings.json ]; then
    cp /workspace/.devcontainer/claude-settings.json /home/dev/.claude/settings.json
fi

uv sync --group dev
echo 'source /workspace/.venv/bin/activate' >> /home/dev/.bashrc
uv run pre-commit install --overwrite --hook-type pre-commit --hook-type pre-push
"""

_CLAUDE_SETTINGS = """\
{
  "sandbox": {
    "enabled": true,
    "network": {
      "allowedDomains": [
        "api.anthropic.com",
        "github.com",
        "*.github.com",
        "*.githubusercontent.com",
        "pypi.org",
        "files.pythonhosted.org",
        "registry.npmjs.org"
      ]
    }
  }
}
"""


def _default_readme(data: Mapping[str, object]) -> ReadmeFile | None:
    description = data.get("description")
    if not isinstance(description, str):
        return None
    python_version = data.get("python_version")
    if not isinstance(python_version, PythonVersion):
        msg = (
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
        raise TypeError(msg)
    return ReadmeFile(description=description, python_version=python_version)


def _default_python_version_file(
    data: Mapping[str, object],  # ignore
) -> PythonVersionFile:
    python_version = data["python_version"]
    if not isinstance(python_version, PythonVersion):
        msg = (
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
        raise TypeError(msg)
    return PythonVersionFile(python_version=python_version)


def _default_pre_commit_config(
    data: Mapping[str, object],  # ignore
) -> PreCommitConfig:
    python_version = data["python_version"]
    if not isinstance(python_version, PythonVersion):
        msg = (
            f"{python_version=} is not an instance of {PythonVersion.__name__}"
        )
        raise TypeError(msg)
    return PreCommitConfig(python_version=python_version)


def _default_devcontainer_json(
    data: Mapping[str, object],  # ignore
) -> DevcontainerJsonFile:
    repo_name = data["repo_name"]
    if not isinstance(repo_name, str):
        msg = f"{repo_name=} is not an instance of str"
        raise TypeError(msg)
    return DevcontainerJsonFile(repo_name=repo_name)


def _default_devcontainer_docker_compose(
    data: Mapping[str, object],  # ignore
) -> DevcontainerDockerComposeFile:
    repo_name = data["repo_name"]
    if not isinstance(repo_name, str):
        msg = f"{repo_name=} is not an instance of str"
        raise TypeError(msg)
    return DevcontainerDockerComposeFile(repo_name=repo_name)


class Template(BaseModel, ABC):
    type: TemplateType
    description: str | None = None
    python_version: PythonVersion = PythonVersion(minor=12)
    author: str = "Tesla2000"
    repo_name: str
    license: MitLicense | None = MitLicense()
    readme: ReadmeFile | None = Field(default_factory=_default_readme)
    pre_commit_run_workflow: PreCommitRunWorkflow | None = (
        PreCommitRunWorkflow()
    )
    tests_workflow: TestsWorkflow | None = TestsWorkflow()
    code_owners_file: CodeOwnersFile | None = CodeOwnersFile()
    pre_commit_config: PreCommitConfig | None = Field(
        default_factory=_default_pre_commit_config
    )
    setup_script: SetupScript | None = SetupScript()
    env_file: File | None = File(relative_path=Path(".env"), content="")
    python_version_file: PythonVersionFile | None = Field(
        default_factory=_default_python_version_file
    )
    gitignore: Gitignore | None = Gitignore()
    package_file: PackageFile | None = PackageFile()
    tests_init_file: File | None = File(
        relative_path=Path("tests/__init__.py"), content=""
    )
    devcontainer_json: DevcontainerJsonFile = Field(
        default_factory=_default_devcontainer_json
    )
    devcontainer_docker_compose: DevcontainerDockerComposeFile = Field(
        default_factory=_default_devcontainer_docker_compose
    )
    devcontainer_dockerfile: File = File(
        relative_path=Path(".devcontainer/Dockerfile"),
        content=_DEVCONTAINER_DOCKERFILE,
    )
    devcontainer_claude_settings: File = File(
        relative_path=Path(".devcontainer/claude-settings.json"),
        content=_DEVCONTAINER_CLAUDE_SETTINGS,
    )
    devcontainer_post_create: File = File(
        relative_path=Path(".devcontainer/post-create.sh"),
        content=_DEVCONTAINER_POST_CREATE,
    )
    claude_settings: File = File(
        relative_path=Path(".claude/settings.json"),
        content=_CLAUDE_SETTINGS,
    )
    claude_review_workflow: ClaudeReviewWorkflow | None = (
        ClaudeReviewWorkflow()
    )

    @property
    def files(self) -> tuple[FileBase, ...]:
        return tuple(
            filter(
                None,
                (
                    self.readme,
                    self.pre_commit_run_workflow,
                    self.tests_workflow,
                    self.code_owners_file,
                    self.pre_commit_config,
                    self.setup_script,
                    self.env_file,
                    self.python_version_file,
                    self.gitignore,
                    self.package_file,
                    self.tests_init_file,
                    self.license,
                    self.devcontainer_json,
                    self.devcontainer_docker_compose,
                    self.devcontainer_dockerfile,
                    self.devcontainer_claude_settings,
                    self.devcontainer_post_create,
                    self.claude_settings,
                    self.claude_review_workflow,
                ),
            )
        )

    def generate(self, project_root: Path) -> None:
        with ExitStack() as stack:
            for file in self.files:
                stack.enter_context(file.revert_on_fail(project_root))
                file.write(project_root)
