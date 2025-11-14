# scripts/logging_backends/default_logger.py
"""
The default logging backend for the application.

This setup provides a two-pronged approach:
1.  Human-Readable Console Logs: For immediate feedback during development.
2.  Machine-Readable File Logs: Saves logs in a structured JSON format,
    which is essential for persistence, observation, and querying.
"""
import sys
from loguru import logger
from pathlib import Path

def setup_default_logger():
    """
    Configures a logger that outputs to both the console and a structured JSON file.
    """
    # Ensure the 'logs' directory exists.
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file_path = log_dir / "app_events.log"

    logger.remove()  # Start with a clean slate

    # --- Handler 1: Human-Readable Console Output ---
    logger.add(
        sys.stderr,
        level="INFO",  # Keep console output clean (INFO and above).
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}:{function}:{line}</cyan> - <level>{message}</level>"
        ),
        colorize=True,
    )

    # --- Handler 2: Machine-Readable File Output for Querying ---
    logger.add(
        log_file_path,
        level="DEBUG",  # Log everything to the file for detailed analysis.
        format="{message}",  # The serializer handles the structure.
        serialize=True,  # <-- The most important part! This creates JSON logs.
        rotation="10 MB",  # Start a new file when the log reaches 10 MB.
        retention="7 days", # Keep log files for up to 7 days.
        catch=True,  # Catch and log exceptions from your code automatically.
    )

    return logger

# The logger instance that will be imported by the facade.
# Renamed to 'logger' for clarity, as it's the sole export.
logger = setup_default_logger()
