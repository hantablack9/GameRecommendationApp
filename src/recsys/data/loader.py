# src/data/loader.py

import os
import zipfile

import pandas as pd
import yaml


def get_project_root():
    """Finds the project root directory by going up two levels from this file."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def extract_data():
    """
    Extracts all files from a zip archive in the raw data directory.

    Args:
        zip_filename (str): The name of the zip file in 'data/poc/raw/'.

    Returns:
        tuple: A tuple containing (extract_path, list_of_extracted_files).
    """
    project_root = get_project_root()
    with open(os.path.join(project_root, "config.yml"), encoding="utf-8") as f:
        config = yaml.safe_load(f)

    raw_data_dir = config["paths"]["raw_data_dir"]
    raw_data_file = config["paths"]["raw_data_file"]
    extract_data_dir = config["paths"]["extract_data_dir"]
    zipfile_path = os.path.join(project_root, raw_data_dir, raw_data_file)
    extract_path = os.path.join(project_root, extract_data_dir)
    os.makedirs(extract_path, exist_ok=True)
    if not os.path.exists(zipfile_path):
        raise FileNotFoundError(f"The zip file was not found at the expected path: {zipfile_path}")

    extracted_files = []
    with zipfile.ZipFile(zipfile_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
        extracted_files = zip_ref.namelist()
        print(f"Successfully extracted all {len(extracted_files)} files to: {extract_path}")

    return extract_path, extracted_files


def load_extracted_data(filename: str) -> pd.DataFrame:
    """
    Loads a specific file (e.g., a CSV) from the 'interim' data directory.

    Args:
        filename (str): The name of the file to load (e.g., 'games.csv').

    Returns:
        pandas.DataFrame: The loaded data.
    """
    project_root = get_project_root()
    with open(os.path.join(project_root, "config.yml"), encoding="utf-8") as f:
        config = yaml.safe_load(f)
    interim_data_dir = config["paths"]["interim_data_dir"]
    interim_file_path = os.path.join(project_root, interim_data_dir, filename)
    # file_path = os.path.join(interim_file_path, filename)
    if not os.path.exists(interim_file_path):
        raise FileNotFoundError(
            f"The file '{filename}' was not found at '{interim_file_path}'. Please check the filename."
        )

    # You can add more logic here for other file types, like .json, .xlsx, etc.
    if filename.endswith(".csv"):
        try:
            df = pd.read_csv(interim_file_path, dtype_backend="pyarrow")
            print(f"Successfully loaded '{filename}'.")
            return df
        except Exception as e:
            raise OSError(f"Error reading the CSV file '{filename}': {e}") from e
    else:
        raise ValueError(f"Unsupported file type for '{filename}'. This function currently only supports .csv files.")


# if __name__ == "__main__":
#     # Example usage
#     extract_path, extracted_files = extract_data()
#     print(f"Extracted files: {extracted_files}")

#     # Load a specific file (adjust filename as needed)
#     try:
#         df_games = load_extracted_data("games.csv")
#         print(df_games.head())
#     except Exception as e:
#         print(e)
