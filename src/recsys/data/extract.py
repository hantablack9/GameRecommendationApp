"""
# src/recsys/data/extract.py
Data extraction utilities for the recsys project.
Provides functions to extract data from zip files and load specific extracted files.
"""
import zipfile
from pathlib import Path

import yaml

from recsys.data.loader import load_extracted_data
from recsys.utils.paths import check_config_file_exists, get_project_root


def extract_data(project_root: Path, config: dict) -> tuple[Path, list[str]]:
    """
    Extracts all files from a zip archive specified in the config file.
    """
    # Use Path objects for cleaner, cross-platform path handling
    raw_data_dir = project_root / config["paths"]["raw_data_dir"]
    raw_data_file = config["paths"]["raw_data_file"]
    extract_data_dir = project_root / config["paths"]["extract_data_dir"]
    zipfile_path = raw_data_dir / raw_data_file

    print(f"Attempting to extract '{zipfile_path}' to '{extract_data_dir}'...")

    if not zipfile_path.is_file():
        raise FileNotFoundError(f"Zip file not found at: {zipfile_path}")

    extract_data_dir.mkdir(parents=True, exist_ok=True)

    files = []
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(extract_data_dir)
        files = zip_ref.namelist()
        print(f"Successfully extracted all {len(files)} files to: {extract_data_dir}")

    return extract_data_dir, files


def main():
    """
    Main orchestration function to run the data extraction and loading process.
    """
    try:
        project_root = get_project_root()
        print(f"Project root determined as: {project_root}")

        config_path = project_root / "config" / "local.yml"
        check_config_file_exists(config_path)
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # --- Step 1: Extract the data ---
        _, extracted_files = extract_data(project_root, config)
        print(f"Extracted files: {extracted_files}")

        # --- Step 2: Load a specific file for verification ---
        df_games = load_extracted_data("games.csv", project_root, config)
        print("\nSuccessfully loaded games.csv for verification:")
        print(df_games.head())

    except (FileNotFoundError, OSError, ValueError) as e:
        print(f"\nAn error occurred during the process: {e}")

if __name__ == "__main__":
    main()
