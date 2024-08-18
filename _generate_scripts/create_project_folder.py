import shutil
from pathlib import Path


def create_project_folders(project_path: Path):
    project_name = project_path.name
    shutil.move(project_path / "src", project_path / project_name / "src")
    docs_path = project_path / "docs/source"
    shutil.move(docs_path / "src", docs_path / project_name / "src")
    (project_path / project_name / "__init__.py").write_bytes(b"")
