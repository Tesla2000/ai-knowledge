from datetime import datetime
from pathlib import Path


def generate_modifications(project_path: Path) -> dict[str, str]:
    project_name = project_path.name
    return {
        "project_name": project_name,
        "project_name_low": project_name.lower(),
        "description": input("Provide project description"),
        "script_name": project_name.replace("_", "-"),
        "docker_image_name": project_name,
        "autodoc_args": "--llm, google/gemma-2-2b-it" if input(
            "Is project private (y/n)").strip().lower() == "y" else "--llm, gpt-4o-mini, --api_keys=OPENAI_API_KEY",
        "year": str(datetime.now().year),
    }