# src/scripts/interaction_tracker.py
"""
This module provides a dedicated tracker for capturing user interaction events.

These events are the lifeblood of the recommendation model and are treated
as structured data, not as application logs. They are saved in a format
(e.g., JSON Lines) suitable for batch processing and model retraining.
"""

import json
from datetime import UTC, datetime
from pathlib import Path

from src.logging.app_logger import logger


class InteractionTracker:
    """
    A tracker for capturing user interaction events.
    Events are stored in a JSON Lines file, with each line representing
    a single event.
    """

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        # Ensure the directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def _write_event(self, event_data: dict):
        """Appends a single event as a new line in the JSON Lines file."""
        try:
            # Use 'a' for append mode
            with open(self.storage_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_data) + "\n")
        except Exception as e:
            # If tracking fails, log it to the *observability* logger

            logger.error(f"Failed to write interaction event: {e}", extra={"event_data": event_data})

    def track_event(self, user_id: str, event_type: str, session_id: str, event_details: dict):
        """
        Tracks a single user interaction event.

        Args:
            user_id (str): The ID of the user performing the action.
            event_type (str): The type of event (e.g., 'rate_game', 'view_recommendation').
            session_id (str): A unique identifier for the user's session.
            event_details (dict): A dictionary containing event-specific data.
        """
        event = {
            "event_id": f"{session_id}-{int(datetime.now(UTC).timestamp() * 1000)}",
            "event_type": event_type,
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "user_id": user_id,
            "session_id": session_id,
            "details": event_details,
        }
        self._write_event(event)


# --- Create a singleton instance for the application to use ---
# This is configured to save events to a dedicated data file.
event_storage_file = Path("data/events/user_interactions.jsonl")
tracker = InteractionTracker(storage_path=event_storage_file)
