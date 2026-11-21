---
name: write-skills
description: skill, SKILL.md, frontmatter, description, keywords, trigger, create skill, edit skill, write skill, skill format, skill name, skill directory
---

# Write skills

- A skill is `.claude/skills/<name>/SKILL.md`. The directory name and the `name` field are identical.
- Frontmatter has exactly two fields: `name` and `description`. Add nothing else.
- `name`: lowercase kebab-case, no spaces, no `skill` suffix.
- `description` is a keyword list, not a sentence. Its only job is to make the skill match the task.
  - Comma-separated terms a task or user would mention: library and tool names, class and method names,
    file names, decorator and marker names, and the workflow name.
  - Include the names that appear in the body, so the skill matches the code it governs.
  - Lowercase, except proper nouns and code identifiers.
  - No full sentences, no label prefix (`Pydantic rules:`), no `Use when`, no `This skill`, no imperative verbs.
  - Keep it under about 200 characters.
- Do not repeat a rule in both the description and the body. The description names the topic. The body states the rules.
- Body: short bullets for rules. Use a code block only when the pattern is not clear from a bullet.
  Start with the rule, not with a summary of the skill.
- Bad description: `Pydantic model rules: frozen, Annotated validators, cross-field defaults, InstanceOf for non-pydantic fields`
- Good description: `pydantic, BaseModel, ConfigDict frozen, Annotated validator, cross-field default, InstanceOf, non-pydantic field`
- Bad description: `When writing tests for a new class, function or module that does not exist yet, never edit production code.`
- Good description: `write tests, new class, new function, new module, red test, import path, TDD, production code`
- After writing or editing a skill, check its frontmatter: two fields, a keyword description, and a `name` that matches the directory.
