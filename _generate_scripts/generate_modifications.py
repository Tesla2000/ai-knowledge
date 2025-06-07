from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pydantic.alias_generators import to_snake


def generate_modifications(project_path: Path, answers: dict) -> dict[str, str]:
    project_name = project_path.name
    answers["description"] = answers.get("description") or input("Provide project description: ")
    return {
        "project_name": project_name,
        "project_name_low": to_snake(project_name),
        "description": answers["description"],
        "script_name": to_snake(project_name).replace("_", "-"),
        "project_script_name": to_snake(project_name).replace("/", "."),
        "docker_image_name": project_name,
        "year": str(datetime.now().year),
    }
