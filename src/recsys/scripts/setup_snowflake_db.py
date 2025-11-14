# scripts/setup_snowflake_db.py
"""
Main orchestrator script to set up the Snowflake database.
It loads configuration, generates the DB schema, and executes it.
"""

import os
from pathlib import Path

import snowflake.connector
from snowflake.connector import ProgrammingError

from src.scripts.generate_db_schema import generate_schema_sql_from_csvs

# --- Import from our custom modules ---
from src.scripts.load_config import load_config


def execute_snowflake_script(sql_script):
    """Connects to Snowflake and executes a multi-statement SQL script."""
    print("\nConnecting to Snowflake to execute script...")
    conn = None
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
        )
        print("  - Connection successful.")
        print("  - Executing SQL statements...")
        for cursor in conn.execute_stream(sql_script):
            for row in cursor:
                print(f"    - {row[0]}")
        print("\n✅✅ Snowflake database setup complete! ✅✅")
    except ProgrammingError as e:
        print(f"❌ Snowflake Programming Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("\n  - Snowflake connection closed.")


def main():
    """Orchestrates the entire database setup process."""
    print("--- Starting Snowflake Database Setup ---")
    # 1. Load Configuration
    config = load_config("config.yml")
    paths = config.get("paths", {})
    settings = config.get("settings", {})

    raw_data_dir = Path(paths.get("raw_data_dir", "data/raw"))
    dtype_sample_rows = settings.get("dtype_inference_rows", 1000)
    print(f"Configuration loaded. Using raw data from '{raw_data_dir}'.")
    try:
        # 2. Generate SQL Schema Script
        print("\nGenerating SQL schema from CSV files...")
        schema_sql = generate_schema_sql_from_csvs(raw_data_dir, dtype_sample_rows)
        print("✅ SQL schema generation complete.")

        # 3. Execute SQL Script
        execute_snowflake_script(schema_sql)

    except FileNotFoundError as e:
        print(f"❌ Process failed: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred during the process: {e}")


if __name__ == "__main__":
    # This setup allows the script to be run directly from the command line
    # while correctly handling package imports.
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[1]))
    main()
