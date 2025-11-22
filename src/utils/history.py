"""History management for document modifications."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

# History file path
HISTORY_FILE = Path.home() / ".pdf_table_fixer_history.json"


class ModificationHistory:
    """Represents a single modification history entry."""

    def __init__(
        self,
        input_file: str,
        output_file: str,
        timestamp: str,
        tables_modified: int,
        format_applied: Optional[Dict[str, Any]],
        modifications_detail: List[Dict[str, Any]],
    ) -> None:
        """
        Initialize modification history entry.

        Args:
            input_file: Path to input PDF
            output_file: Path to output PDF
            timestamp: ISO format timestamp
            tables_modified: Number of tables modified
            format_applied: Format information applied
            modifications_detail: List of detailed modifications
        """
        self.input_file = input_file
        self.output_file = output_file
        self.timestamp = timestamp
        self.tables_modified = tables_modified
        self.format_applied = format_applied
        self.modifications_detail = modifications_detail

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "input_file": self.input_file,
            "output_file": self.output_file,
            "timestamp": self.timestamp,
            "tables_modified": self.tables_modified,
            "format_applied": self.format_applied,
            "modifications_detail": self.modifications_detail,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModificationHistory":
        """Create from dictionary."""
        return cls(
            input_file=data["input_file"],
            output_file=data["output_file"],
            timestamp=data["timestamp"],
            tables_modified=data["tables_modified"],
            format_applied=data.get("format_applied"),
            modifications_detail=data.get("modifications_detail", []),
        )


def save_modification_history(history: ModificationHistory) -> None:
    """
    Save modification history to file.

    Args:
        history: ModificationHistory object
    """
    try:
        # Load existing history
        existing_history = load_all_history()
        
        # Add new entry at the beginning (most recent first)
        existing_history.insert(0, history)
        
        # Keep only last 100 entries
        if len(existing_history) > 100:
            existing_history = existing_history[:100]
        
        # Save to file
        history_data = [h.to_dict() for h in existing_history]
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass  # Silently fail if history can't be saved


def load_all_history() -> List[ModificationHistory]:
    """
    Load all modification history.

    Returns:
        List of ModificationHistory objects, most recent first
    """
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history_data = json.load(f)
            return [
                ModificationHistory.from_dict(entry)
                for entry in history_data
            ]
    except Exception:
        return []


def create_history_entry(
    input_file: str,
    output_file: str,
    tables_modified: int,
    format_applied: Optional[Dict[str, Any]],
    modifications_detail: List[Dict[str, Any]],
) -> ModificationHistory:
    """
    Create a new history entry.

    Args:
        input_file: Path to input PDF
        output_file: Path to output PDF
        tables_modified: Number of tables modified
        format_applied: Format information applied
        modifications_detail: List of detailed modifications

    Returns:
        ModificationHistory object
    """
    timestamp = datetime.now().isoformat()
    return ModificationHistory(
        input_file=input_file,
        output_file=output_file,
        timestamp=timestamp,
        tables_modified=tables_modified,
        format_applied=format_applied,
        modifications_detail=modifications_detail,
    )

