from __future__ import annotations

from pathlib import Path


def pick_template(answers: dict) -> Path:
    templates = list(Path("_templates").iterdir())
    templatest_pick_string = "\n".join(
        f"{index}. {template.name}" for index, template in enumerate(templates)
    )
    question = f"Pick project template:\n{templatest_pick_string}\nPass int: "
    if answers.get("template_index") is None:
        response = input(question)
        if response:
            answers["template_index"] = int(response)
        else:
            answers["template_index"] = next(index for index, elem in enumerate(templates) if "default" in elem.name)
    template_index = answers["template_index"]
    return templates[template_index]
