# src/recsys/scripts/generate_db_schema.py
"""
This module is responsible for generating a Snowflake SQL schema from CSV files.
It handles data type inference and SQL syntax generation.
"""

import re
from pathlib import Path

import pandas as pd


def _sanitize_column_name(col_name) -> str:
    """(Internal) Sanitizes column names for SQL compatibility by quoting them."""
    s = str(col_name)
    s_escaped = s.replace('"', "''")
    if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", s_escaped):
        return s_escaped
    else:
        return f'"{col_name}"'


def _map_pandas_to_snowflake_type(pd_dtype: str) -> str:
    """(Internal) Maps a pandas data type to a corresponding Snowflake SQL type."""
    dtype_str = str(pd_dtype).lower()
    if "int" in dtype_str:
        return "NUMBER"
    if "float" in dtype_str:
        return "FLOAT"
    if "bool" in dtype_str:
        return "BOOLEAN"
    if "datetime" in dtype_str:
        return "TIMESTAMP_NTZ"
    if "object" in dtype_str:
        return "VARCHAR"
    return "VARCHAR"


def generate_schema_sql_from_csvs(data_dir: Path, sample_rows: int) -> str:
    """
    Generates a complete Snowflake setup SQL script from all CSVs in a directory.

    Args:
        data_dir (Path): The directory containing the source CSV files.
        sample_rows (int): The number of rows to sample for dtype inference.

    Returns:
        str: A single string containing the complete, executable SQL script.
    """
    if not data_dir.is_dir():
        raise FileNotFoundError(f"Data directory not found: '{data_dir}'")

    # --- Static SQL Header ---
    sql_header = """-- ============================================================================
-- Snowflake Setup Script (Auto-Generated)
-- ============================================================================
USE ROLE ACCOUNTADMIN;
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH WITH WAREHOUSE_SIZE = 'X-SMALL';
USE WAREHOUSE COMPUTE_WH;
CREATE DATABASE IF NOT EXISTS BOARDGAME_DB;
USE DATABASE BOARDGAME_DB;
CREATE SCHEMA IF NOT EXISTS RAW_DATA;
USE SCHEMA RAW_DATA;
CREATE OR REPLACE FILE FORMAT my_csv_format TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1 NULL_IF = ('NULL', 'null', '', '\\N') EMPTY_FIELD_AS_NULL = true FIELD_OPTIONALLY_ENCLOSED_BY = '"';
CREATE OR REPLACE STAGE my_internal_stage FILE_FORMAT = my_csv_format;
-- ============================================================================
-- Table Creation
-- ============================================================================
"""
    table_creation_statements = []
    csv_files = sorted(data_dir.glob("*.csv"))

    if not csv_files:
        print(f"Warning: No CSV files found in '{data_dir}'.")
        return sql_header

    for csv_file in csv_files:
        try:
            df_sample = pd.read_csv(csv_file, nrows=sample_rows if sample_rows > 0 else None, encoding="utf-8")
            table_name = csv_file.stem.upper().replace("-", "_")

            cols_sql = ",\n".join([
                f"    {_sanitize_column_name(col)} {_map_pandas_to_snowflake_type(dtype)}"
                for col, dtype in df_sample.dtypes.items()
            ])
            table_sql = f"-- Schema for: {csv_file.name}\nCREATE OR REPLACE TABLE {table_name} (\n{cols_sql}\n);"
            table_creation_statements.append(table_sql)
        except Exception as e:
            error_sql = f"-- ERROR generating schema for {csv_file.name}: {e}"
            table_creation_statements.append(error_sql)
            print(f"  - ❌ ERROR for {csv_file.name}: {e}")
    return sql_header + "\n\n".join(table_creation_statements)
