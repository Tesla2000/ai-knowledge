import re
import subprocess
from hashlib import sha256
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class PytestCommandMatcher(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    @staticmethod
    def is_pytest_command(command: str) -> bool:
        return bool(re.search(r"(?:^|[\s;&|])pytest\b", command))


class CodeStateHasher(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    repo_root: Path

    def hash_working_tree(self) -> str:
        head = self._run("git", "rev-parse", "HEAD")
        diff = self._run("git", "diff", "HEAD")
        untracked_paths = self._run(
            "git", "ls-files", "--others", "--exclude-standard"
        ).splitlines()
        untracked_content = "\n".join(
            f"{path}:{(self.repo_root / path).read_text()}"
            for path in sorted(untracked_paths)
        )
        digest = sha256()
        digest.update(head.encode())
        digest.update(diff.encode())
        digest.update(untracked_content.encode())
        return digest.hexdigest()

    def _run(self, *args: str) -> str:
        return subprocess.run(
            args, cwd=self.repo_root, capture_output=True, text=True, check=True
        ).stdout


class PytestRunRecord(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    code_hash: str
    passed: bool
    output: str


class PytestGuardStateStore(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    state_path: Path

    def load(self) -> PytestRunRecord | None:
        try:
            return PytestRunRecord.model_validate_json(self.state_path.read_text())
        except FileNotFoundError:
            return None

    def save(self, record: PytestRunRecord) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(record.model_dump_json())
