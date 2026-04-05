from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import TestCase

from files.stub_generation_workflow import fix_pydantic_stubs


def _run(py_content: str, pyi_content: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        directory = Path(tmp)
        (directory / "model.py").write_text(py_content)
        (directory / "model.pyi").write_text(pyi_content)
        fix_pydantic_stubs(directory)
        return (directory / "model.pyi").read_text()


class TestFixPydanticStubs(TestCase):
    def test_direct_default_gets_ellipsis(self) -> None:
        result = _run(
            'from pydantic import BaseModel\nclass M(BaseModel):\n    x: str = "hi"\n',
            "class M:\n    x: str\n",
        )
        self.assertIn("x: str = ...", result)

    def test_field_default_gets_ellipsis(self) -> None:
        result = _run(
            "from pydantic import BaseModel, Field\nclass M(BaseModel):\n    x: str = Field(default='hi')\n",
            "class M:\n    x: str\n",
        )
        self.assertIn("x: str = ...", result)

    def test_field_default_factory_gets_ellipsis(self) -> None:
        result = _run(
            "from pydantic import BaseModel, Field\nclass M(BaseModel):\n    x: list = Field(default_factory=list)\n",
            "class M:\n    x: list\n",
        )
        self.assertIn("x: list = ...", result)

    def test_annotated_field_default_gets_ellipsis(self) -> None:
        result = _run(
            "from typing import Annotated\nfrom pydantic import BaseModel, Field\nclass M(BaseModel):\n    x: Annotated[str, Field(default='hi')]\n",
            "class M:\n    x: str\n",
        )
        self.assertIn("x: str = ...", result)

    def test_annotated_field_default_factory_gets_ellipsis(self) -> None:
        result = _run(
            "from typing import Annotated\nfrom pydantic import BaseModel, Field\nclass M(BaseModel):\n    x: Annotated[list, Field(default_factory=list)]\n",
            "class M:\n    x: list\n",
        )
        self.assertIn("x: list = ...", result)

    def test_required_field_unchanged(self) -> None:
        result = _run(
            "from pydantic import BaseModel\nclass M(BaseModel):\n    x: str\n",
            "class M:\n    x: str\n",
        )
        self.assertNotIn("= ...", result)

    def test_existing_default_not_duplicated(self) -> None:
        result = _run(
            'from pydantic import BaseModel\nclass M(BaseModel):\n    x: str = "hi"\n',
            "class M:\n    x: str = ...\n",
        )
        self.assertEqual(result.count("= ..."), 1)

    def test_non_model_class_unchanged(self) -> None:
        result = _run(
            'class M:\n    x: str = "hi"\n',
            "class M:\n    x: str\n",
        )
        self.assertNotIn("= ...", result)

    def test_no_stub_file_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / "model.py").write_text(
                "from pydantic import BaseModel\nclass M(BaseModel):\n    x: str = 'hi'\n"
            )
            fix_pydantic_stubs(directory)

    def test_mixed_fields_only_defaults_get_ellipsis(self) -> None:
        result = _run(
            "from pydantic import BaseModel\nclass M(BaseModel):\n    required: str\n    optional: str = 'hi'\n",
            "class M:\n    required: str\n    optional: str\n",
        )
        self.assertNotIn("required: str = ...", result)
        self.assertIn("optional: str = ...", result)
