"""Internationalization (i18n) support for the application."""

import json
from pathlib import Path
from typing import Dict

# Default language
DEFAULT_LANGUAGE = "en"

# Supported languages
SUPPORTED_LANGUAGES = ["en", "es"]

# Translations cache
_translations: Dict[str, Dict[str, str]] = {}
_current_language = DEFAULT_LANGUAGE


def load_translations(language: str = DEFAULT_LANGUAGE) -> None:
    """
    Load translations for the specified language.

    Args:
        language: Language code (e.g., 'en', 'es')
    """
    global _translations, _current_language

    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE

    _current_language = language

    # Path to translations directory
    translations_dir = Path(__file__).parent.parent / "i18n"
    translation_file = translations_dir / f"{language}.json"

    if translation_file.exists():
        try:
            with open(translation_file, "r", encoding="utf-8") as f:
                _translations[language] = json.load(f)
        except Exception:
            # Fallback to empty dict if loading fails
            _translations[language] = {}
    else:
        _translations[language] = {}


def get_text(key: str, default: str = None) -> str:
    """
    Get translated text for a key.

    Args:
        key: Translation key (e.g., 'app.title')
        default: Default text if key not found

    Returns:
        Translated text or default
    """
    if _current_language not in _translations:
        load_translations(_current_language)

    translations = _translations.get(_current_language, {})
    return translations.get(key, default or key)


def get_current_language() -> str:
    """
    Get current language code.

    Returns:
        Current language code
    """
    return _current_language


def set_language(language: str) -> None:
    """
    Set current language.

    Args:
        language: Language code (e.g., 'en', 'es')
    """
    global _current_language
    if language in SUPPORTED_LANGUAGES:
        _current_language = language
        load_translations(language)


# Initialize translations
load_translations(DEFAULT_LANGUAGE)

