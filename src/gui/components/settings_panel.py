"""Settings panel component."""

import customtkinter as ctk
from typing import Callable, Optional

from src.gui.themes.fluent_theme import (
    FLUENT_PRIMARY,
    FLUENT_TEXT_PRIMARY,
    FLUENT_TEXT_SECONDARY,
    FLUENT_SURFACE,
    FLUENT_BACKGROUND,
    FLUENT_BORDER,
    FLUENT_HOVER,
    COMBOBOX_BUTTON,
    COMBOBOX_DROPDOWN,
    SPACING_SM,
    SPACING_MD,
    SPACING_LG,
    RADIUS_MD,
    RADIUS_LG,
)
from src.gui.themes.fonts import get_poppins_font
from src.utils.i18n import get_text, set_language, get_current_language
from src.utils.config import get_config_value, set_config_value


class SettingsPanel(ctk.CTkFrame):
    """Component for application settings."""

    def __init__(self, parent, language_callback: Optional[Callable] = None, **kwargs) -> None:
        """
        Initialize settings panel component.

        Args:
            parent: Parent widget
            language_callback: Optional callback function for language changes
            **kwargs: Additional frame arguments (language_callback will be extracted)
        """
        # Extract language_callback from kwargs if passed there (before passing to super)
        if "language_callback" in kwargs:
            language_callback = kwargs.pop("language_callback")
        
        # Set default card style with subtle border for shadow effect
        kwargs.setdefault("fg_color", FLUENT_SURFACE)
        kwargs.setdefault("corner_radius", RADIUS_LG)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", FLUENT_BORDER)
        super().__init__(parent, **kwargs)
        self.language_callback: Optional[Callable] = language_callback

        self._create_widgets()
        self._load_settings()

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        # Title with icon
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(SPACING_LG, SPACING_MD), padx=SPACING_LG)

        # Icon
        icon_label = ctk.CTkLabel(
            title_frame,
            text="⚙️",
            font=get_poppins_font(size=20),
        )
        icon_label.pack(side="left", padx=(0, SPACING_MD))

        # Title
        self.title_label = ctk.CTkLabel(
            title_frame,
            text=get_text("settings.title", "Settings"),
            font=get_poppins_font(size=18, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.title_label.pack(side="left")

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self,
            text=get_text("settings.subtitle", "Configure application preferences"),
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.subtitle_label.pack(pady=(0, SPACING_LG), padx=SPACING_LG)

        # Language section
        self._create_language_section()

    def _create_language_section(self) -> None:
        """Create language selection section."""
        # Language frame
        language_frame = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        language_frame.pack(
            fill="x", padx=SPACING_LG, pady=(0, SPACING_LG)
        )

        # Language label
        language_label = ctk.CTkLabel(
            language_frame,
            text=get_text("settings.language", "Language"),
            font=get_poppins_font(size=14, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        language_label.pack(anchor="w", pady=(0, SPACING_SM))

        # Language description
        desc_label = ctk.CTkLabel(
            language_frame,
            text=get_text(
                "settings.language.description",
                "Choose your preferred language"
            ),
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        desc_label.pack(anchor="w", pady=(0, SPACING_MD))

        # Language dropdown
        self.language_var = ctk.StringVar(value="en")
        language_options = [
            get_text("settings.language.english", "English"),
            get_text("settings.language.spanish", "Spanish"),
        ]
        language_values = ["en", "es"]

        self.language_dropdown = ctk.CTkComboBox(
            language_frame,
            values=language_options,
            variable=self.language_var,
            command=self._on_language_changed,
            fg_color=FLUENT_BACKGROUND,
            button_color=COMBOBOX_BUTTON,
            dropdown_fg_color=FLUENT_SURFACE,
            dropdown_text_color=FLUENT_TEXT_PRIMARY,
            border_color=COMBOBOX_BUTTON,
            border_width=1,
            corner_radius=RADIUS_MD,
            font=get_poppins_font(size=13),
            text_color=FLUENT_TEXT_PRIMARY,
            dropdown_font=get_poppins_font(size=13),
        )
        self.language_dropdown.pack(
            fill="x", pady=(0, SPACING_LG)
        )

        # Store language values mapping
        self.language_values = language_values

    def _on_language_changed(self, value: str) -> None:
        """
        Handle language change.

        Args:
            value: Selected language display name
        """
        # Find the language code
        language_options = [
            get_text("settings.language.english", "English"),
            get_text("settings.language.spanish", "Spanish"),
        ]
        try:
            index = language_options.index(value)
            language_code = self.language_values[index]
        except (ValueError, IndexError):
            language_code = "en"

        # Save to config
        set_config_value("language", language_code)

        # Update i18n
        set_language(language_code)

        # Notify callback if set
        if self.language_callback:
            self.language_callback(language_code)

    def _load_settings(self) -> None:
        """Load settings from configuration."""
        # Load language
        saved_language = get_config_value("language", "en")
        set_language(saved_language)

        # Update dropdown to show current language
        language_options = [
            get_text("settings.language.english", "English"),
            get_text("settings.language.spanish", "Spanish"),
        ]
        try:
            index = self.language_values.index(saved_language)
            self.language_var.set(language_options[index])
        except (ValueError, IndexError):
            self.language_var.set(language_options[0])

    def set_language_callback(self, callback: Callable) -> None:
        """
        Set callback for language changes.

        Args:
            callback: Function to call when language changes
        """
        self.language_callback = callback

    def refresh_texts(self) -> None:
        """Refresh all texts after language change."""
        # Update title
        self.title_label.configure(
            text=get_text("settings.title", "Settings")
        )
        # Update subtitle
        self.subtitle_label.configure(
            text=get_text("settings.subtitle", "Configure application preferences")
        )
        # Update language section
        language_label_text = get_text("settings.language", "Language")
        desc_label_text = get_text(
            "settings.language.description",
            "Choose your preferred language"
        )
        # Note: We can't easily update labels in language_frame without storing references
        # For now, reload settings to update dropdown
        self._load_settings()

