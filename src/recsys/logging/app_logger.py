# scripts/app_logger.py
"""
This module provides the application-wide logging interface.

It abstracts the underlying logging implementation, allowing the backend
to be swapped out easily in the future (e.g., from console to a full
observability stack like Loki/Grafana).

Application code should ONLY import and use the `logger` from this module.
"""

# --- Backend Selection ---
# We point to our new default logger which handles both console and file logging.
from src.recsys.logging.logging_backends.default_logger import logger as backend_logger

# --- Application-Specific Context ---
# .bind() creates a new logger with bound data that will be included in all
# subsequent log messages. This is perfect for adding consistent context.
logger = backend_logger.bind(app_name="BoardGameRecommender", version="0.1.0")

# --- How to Observe and Query (Documentation for the developer) ---
#
# With the current 'default_logger' backend, all logs are saved as structured
# JSON in 'logs/app_events.log'. You can query them directly from the command line.
#
# PREREQUISITE:
#   Install a command-line JSON processor like 'jq'.
#   - On macOS: brew install jq
#   - On Linux: sudo apt-get install jq
#
# EXAMPLE QUERIES:
#
# 1. Tail the logs in a readable format:
#    tail -f logs/app_events.log | jq
#
# 2. Find all ERROR level messages:
#    cat logs/app_events.log | jq 'select(.record.level.name == "ERROR")'
#
# 3. Show messages only from the 'setup_snowflake_db' module:
#    cat logs/app_events.log | jq 'select(.record.module == "setup_snowflake_db")'
#
# 4. Find logs that contain a specific error message:
#    cat logs/app_events.log | jq 'select(.record.message | contains("Connection failed"))'
#
# This setup provides powerful querying capabilities locally without needing
# a complex observability stack, but is perfectly positioned to be forwarded
# to one (like Loki) in the future.
