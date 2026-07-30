import json
import re
import subprocess
from hashlib import sha256
from pathlib import Path
from typing import NamedTuple

_PYTEST_COMMAND_PATTERN = re.compile(r"(?:^|[\s;&|])pytest\b")


def is_pytest_command(command: str) -> bool:
    return bool(_PYTEST_COMMAND_PATTERN.search(command))


def _run(repo_root: Path, *args: str) -> str:
    return subprocess.run(
        args, cwd=repo_root, capture_output=True, text=True, check=True
    ).stdout


def hash_working_tree(repo_root: Path) -> str:
    head = _run(repo_root, "git", "rev-parse", "HEAD")
    diff = _run(repo_root, "git", "diff", "HEAD")
    untracked_paths = _run(
        repo_root, "git", "ls-files", "--others", "--exclude-standard"
    ).splitlines()
    untracked_content = "\n".join(
        f"{path}:{(repo_root / path).read_text()}" for path in sorted(untracked_paths)
    )
    digest = sha256()
    digest.update(head.encode())
    digest.update(diff.encode())
    digest.update(untracked_content.encode())
    return digest.hexdigest()


class PytestRunRecord(NamedTuple):
    code_hash: str
    passed: bool
    output: str


def load_record(state_path: Path) -> PytestRunRecord | None:
    try:
        data = json.loads(state_path.read_text())
    except FileNotFoundError:
        return None
    return PytestRunRecord(
        code_hash=data["code_hash"], passed=data["passed"], output=data["output"]
    )


def save_record(state_path: Path, record: PytestRunRecord) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(record._asdict()))
