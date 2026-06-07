#!/usr/bin/env python3
"""Generate SimplifiedBlocks JSON schema as static file for Monaco editor."""

import json
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dnd.character.checkpoint import (  # noqa: E402
    MemoryStorage,
)
from dnd.server.app import create_app  # noqa: E402


def generate_schema():
    """Generate schema and save to static directory."""
    # Create app to access the schema generation function
    app = create_app(MemoryStorage())

    # Call the schema endpoint to get the schema
    from starlette.testclient import TestClient

    client = TestClient(app)
    response = client.get("/schema/simplified-blocks")

    if response.status_code != 200:
        raise RuntimeError(f"Failed to generate schema: {response.text}")

    schema = response.json()

    # Write to static directory
    static_dir = project_root / "dnd_character_creator" / "server" / "static"
    static_dir.mkdir(parents=True, exist_ok=True)

    output_file = static_dir / "simplified-blocks-schema.json"
    with output_file.open("w") as f:
        json.dump(schema, f, indent=2)

    print(f"✓ Generated schema: {output_file}")
    print(f"  - {len(schema['properties'])} top-level properties")
    union_fields = [
        p
        for p in schema["properties"].values()
        if "block_type" in p.get("properties", {})
    ]
    print(f"  - {len(union_fields)} Union type fields")


if __name__ == "__main__":
    generate_schema()
