from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from pydantic.alias_generators import to_snake


def generate_modifications(project_path: Path, answers: dict) -> dict[str, str]:
    project_name = project_path.name
    answers["description"] = answers.get("description") or input("Provide project description: ")
    answers["autodoc_args"] = answers.get("autodoc_args") or (
            "--llm, google/gemma-2-2b-it"
            if input("Is project private (y/n): ").strip().lower() == "y"
            else "--llm, gpt-4o-mini, --api_keys=OPENAI_API_KEY"
        )
    return {
        "project_name": project_name,
        "project_name_low": to_snake(project_name),
        "description": answers["description"],
        "script_name": to_snake(project_name).replace("_", "-"),
        "project_script_name": to_snake(project_name).replace("/", "."),
        "docker_image_name": project_name,
        "autodoc_args": answers["autodoc_args"],
        "year": str(datetime.now().year),
    }
