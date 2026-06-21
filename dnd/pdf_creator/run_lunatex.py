from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def run_lualatex(temp_file_name: str, directory: Path) -> None:
    try:
        os.chdir(directory)
        result = subprocess.run(
            ["lualatex", temp_file_name],
            check=True,
            capture_output=True,
            text=True,
        )
        sys.stdout.write(result.stdout)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"Error occurred while running lualatex: {e.stderr}\n")
    except FileNotFoundError:
        sys.stderr.write(f"The directory '{directory}' does not exist.\n")
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")
