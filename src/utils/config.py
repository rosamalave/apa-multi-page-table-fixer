"""Configuration management for the application."""

import json
from pathlib import Path
from typing import Optional

# Configuration file path
CONFIG_FILE = Path.home() / ".pdf_table_fixer_config.json"

# Default configuration
DEFAULT_CONFIG = {
    "language": "en",
}


def load_config() -> dict:
    """
    Load configuration from file.

    Returns:
        Configuration dictionary
    """
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**DEFAULT_CONFIG, **config}
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    """
    Save configuration to file.

    Args:
        config: Configuration dictionary
    """
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception:
        pass  # Silently fail if config can't be saved


def get_config_value(key: str, default=None) -> Optional[str]:
    """
    Get a configuration value.

    Args:
        key: Configuration key
        default: Default value if key not found

    Returns:
        Configuration value or default
    """
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: str) -> None:
    """
    Set a configuration value.

    Args:
        key: Configuration key
        value: Configuration value
    """
    config = load_config()
    config[key] = value
    save_config(config)

