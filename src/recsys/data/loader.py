import yaml
from pathlib import Path
import pandas as pd

def load_extracted_data(filename: str, project_root: Path, config: dict) -> pd.DataFrame:
    """
    Loads a specific file (e.g., a CSV) from the 'interim' data directory.
    """
    extract_data_dir = project_root / config["paths"]["extract_data_dir"]
    interim_file_path = extract_data_dir / filename

    if not interim_file_path.is_file():
        raise FileNotFoundError(f"The file '{filename}' was not found at '{interim_file_path}'. Please check the filename.")

    if filename.endswith(".csv"):
        try:
            df = pd.read_csv(interim_file_path, dtype_backend="pyarrow")
            print(f"Successfully loaded '{filename}'.")
            return df
        except Exception as e:
            raise OSError(f"Error reading the CSV file '{filename}': {e}") from e
    else:
        raise ValueError(f"Unsupported file type for '{filename}'. This function currently only supports .csv files.")
