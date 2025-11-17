""" Path utilities for the recsys project. 
Provides functions to get the project root and check for configuration file existence.# src/recsys/utils/paths.py
"""

from pathlib import Path

def check_config_file_exists(config_path):
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

def get_project_root() -> Path:
    """
    Finds the project root directory by walking up until 'pyproject.toml' is found.
    """
    current_path = Path(__file__).resolve().parent

    while not (current_path / 'pyproject.toml').is_file():
        if current_path == current_path.parent:
            raise FileNotFoundError("Could not find project root."
                                    " Make sure 'pyproject.toml' exists.")
        current_path = current_path.parent
    return current_path

