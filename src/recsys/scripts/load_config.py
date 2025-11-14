# scripts/load_config.py
"""
This module provides a function to load configuration settings from a YAML file.
"""

import yaml

def load_config(config_path: str = 'config.yml') -> dict:
    """
    Loads the YAML configuration file.

    Args:
        config_path (str): The path to the configuration YAML file. 
                           Defaults to 'config.yml'.

    Returns:
        dict: A dictionary containing the configuration settings.
    
    Raises:
        SystemExit: If the file is not found or cannot be parsed.
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"FATAL: Configuration file not found at '{config_path}'.")
        exit(1) # Exits the script if config is missing.
    except yaml.YAMLError as e:
        print(f"FATAL: Error parsing YAML configuration file '{config_path}': {e}")
        exit(1)
    except Exception as e:
        print(f"FATAL: An unexpected error occurred while loading config '{config_path}': {e}")
        exit(1)
