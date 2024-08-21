from __future__ import annotations

from pathlib import Path


def pick_template(answers: dict) -> Path:
    templates = list(Path("_templates").iterdir())
    templatest_pick_string = "\n".join(
        f"{index}. {template.name}" for index, template in enumerate(templates)
    )
    question = f"Pick project template:\n{templatest_pick_string}\nPass int: "
    answers["template_index"] = int(input(question)) if answers.get("template_index") is None else answers["template_index"]
    template_index = answers["template_index"]
    return templates[template_index]
