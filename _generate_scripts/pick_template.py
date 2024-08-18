from pathlib import Path


def pick_template() -> Path:
    templates = list(Path("_templates").iterdir())
    templatest_pick_string = "\n".join(f"{index}. {template.name}" for index, template in enumerate(templates))
    question = f"Pick project template:\n{templatest_pick_string}\nPass int: "
    template_index = int(input(question))
    return templates[template_index]
