from __future__ import annotations

import os
import subprocess
from pathlib import Path


def run_lualatex(temp_file_name: str, directory: Path):
    try:
        os.chdir(directory)
        result = subprocess.run(
            ["lualatex", temp_file_name],
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running lualatex: {e.stderr}")
    except FileNotFoundError:
        print(f"The directory '{directory}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
