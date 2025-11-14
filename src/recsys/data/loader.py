# src/data/loader.py

import os
from unittest.util import strclass
import zipfile
import pandas as pd


def get_project_root():
    """Finds the project root directory by going up two levels from this file."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def extract_data(zip_filename='poc_kaggle.zip'):
    """
    Extracts all files from a zip archive in the raw data directory.

    Args:
        zip_filename (str): The name of the zip file in 'data/poc/raw/'.

    Returns:
        tuple: A tuple containing (extract_path, list_of_extracted_files).
    """
    project_root = get_project_root()
    zip_path = os.path.join(project_root, 'data', 'poc', 'raw', zip_filename)
    extract_path = os.path.join(project_root, 'data', 'poc', 'interim')

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"The zip file was not found at the expected path: {zip_path}")

    os.makedirs(extract_path, exist_ok=True)

    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        extracted_files = zip_ref.namelist()
        print(f"Successfully extracted all {len(extracted_files)} files to: {extract_path}")
    
    return extract_path, extracted_files

def load_extracted_data(filename: str, dtype_backend='pyarrow') -> pd.DataFrame:
    """
    Loads a specific file (e.g., a CSV) from the 'interim' data directory.

    Args:
        filename (str): The name of the file to load (e.g., 'games.csv').

    Returns:
        pandas.DataFrame: The loaded data.
    """
    project_root = get_project_root()
    file_path = os.path.join(project_root, 'data', 'poc', 'interim', filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{filename}' was not found at '{file_path}'. Please check the filename.")

    # You can add more logic here for other file types, like .json, .xlsx, etc.
    if filename.endswith('.csv'):
        try:
            df = pd.read_csv(file_path, dtype_backend = dtype_backend)
            print(f"Successfully loaded '{filename}'.")
            return df
        except Exception as e:
            raise IOError(f"Error reading the CSV file '{filename}': {e}") from e
    else:
        raise ValueError(f"Unsupported file type for '{filename}'. This function currently only supports .csv files.")

