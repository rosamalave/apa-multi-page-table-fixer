"""Format controls component for customizing table title format."""

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
from src.core.models import FormatInfo
from src.utils.constants import (
    COMMON_FONT_FAMILIES,
    COMMON_FONT_SIZES,
)
from src.utils.i18n import get_text


class FormatControls(ctk.CTkFrame):
    """Component for format customization controls."""

    def __init__(self, parent, **kwargs) -> None:
        """
        Initialize format controls component.

        Args:
            parent: Parent widget
            **kwargs: Additional frame arguments
        """
        # Set default card style with subtle border for shadow effect
        kwargs.setdefault("fg_color", FLUENT_SURFACE)
        kwargs.setdefault("corner_radius", RADIUS_LG)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", FLUENT_BORDER)
        super().__init__(parent, **kwargs)
        self.keep_original = True
        self.format_callback: Optional[Callable] = None

        self._create_widgets()

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
            text=get_text("format.title", "Format Options"),
            font=get_poppins_font(size=18, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.title_label.pack(side="left")

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self,
            text=get_text(
                "format.subtitle",
                "Customize table title formatting"
            ),
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.subtitle_label.pack(pady=(0, SPACING_LG), padx=SPACING_LG, anchor="w")

        # Detected format display section
        self.detected_format_frame = ctk.CTkFrame(
            self,
            fg_color=FLUENT_BACKGROUND,
            corner_radius=RADIUS_MD,
            border_width=1,
            border_color=FLUENT_BORDER,
        )
        self.detected_format_frame.pack(fill="x", padx=SPACING_LG, pady=(0, SPACING_LG))

        # Label for detected format
        self.detected_format_label = ctk.CTkLabel(
            self.detected_format_frame,
            text=get_text("format.detected_format", "Detected Format:"),
            font=get_poppins_font(size=11, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.detected_format_label.pack(anchor="w", padx=SPACING_MD, pady=(SPACING_MD, SPACING_SM))

        # Format details
        self.detected_format_details = ctk.CTkLabel(
            self.detected_format_frame,
            text=get_text("format.no_format", "No format detected"),
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.detected_format_details.pack(anchor="w", padx=SPACING_MD, pady=(0, SPACING_MD))

        # Keep original format section with padding
        checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        checkbox_frame.pack(fill="x", padx=SPACING_LG, pady=(0, SPACING_MD))

        self.keep_original_var = ctk.BooleanVar(value=True)
        self.keep_original_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text=get_text("format.keep_original", "Keep original format"),
            variable=self.keep_original_var,
            command=self._on_keep_original_changed,
            font=get_poppins_font(size=14),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.keep_original_checkbox.pack(anchor="w")

        # Description
        self.description_label = ctk.CTkLabel(
            checkbox_frame,
            text=get_text(
                "format.keep_original.desc",
                "Preserve the existing formatting of table titles"
            ),
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.description_label.pack(anchor="w", pady=(SPACING_MD, SPACING_LG))

        # Format controls frame (hidden by default when keep original is checked)
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Don't pack initially - will be shown/hidden based on checkbox state

        # Font family dropdown
        self.font_label = ctk.CTkLabel(
            self.controls_frame,
            text=get_text("format.font", "Font Family:"),
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.font_label.pack(anchor="w", pady=(0, SPACING_MD))

        self.font_dropdown = ctk.CTkComboBox(
            self.controls_frame,
            values=COMMON_FONT_FAMILIES,
            state="disabled",
            command=self._on_format_option_changed,
            font=get_poppins_font(size=12),
            corner_radius=RADIUS_MD,
            button_color=COMBOBOX_BUTTON,  # Light blue #e8f0ff for arrow
            button_hover_color=COMBOBOX_BUTTON,
            fg_color=FLUENT_SURFACE,
            border_color=COMBOBOX_BUTTON,
            border_width=1,
            dropdown_fg_color=FLUENT_SURFACE,  # White background
            dropdown_hover_color=FLUENT_HOVER,
            dropdown_text_color=FLUENT_TEXT_PRIMARY,  # Dark text for white background
        )
        self.font_dropdown.set(COMMON_FONT_FAMILIES[0])
        self.font_dropdown.pack(fill="x", pady=(0, SPACING_LG))

        # Font size dropdown
        self.size_label = ctk.CTkLabel(
            self.controls_frame,
            text=get_text("format.size", "Font Size:"),
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.size_label.pack(anchor="w", pady=(0, SPACING_MD))

        size_values = [f"{s} pt" for s in COMMON_FONT_SIZES]
        self.size_dropdown = ctk.CTkComboBox(
            self.controls_frame,
            values=size_values,
            state="disabled",
            command=self._on_format_option_changed,
            font=get_poppins_font(size=12),
            corner_radius=RADIUS_MD,
            button_color=COMBOBOX_BUTTON,  # Light blue #e8f0ff for arrow
            button_hover_color=COMBOBOX_BUTTON,
            fg_color=FLUENT_SURFACE,
            border_color=COMBOBOX_BUTTON,
            border_width=1,
            dropdown_fg_color=FLUENT_SURFACE,  # White background
            dropdown_hover_color=FLUENT_HOVER,
            dropdown_text_color=FLUENT_TEXT_PRIMARY,  # Dark text for white background
        )
        self.size_dropdown.set("11 pt")
        self.size_dropdown.pack(fill="x", pady=(0, SPACING_LG))

        # Style checkboxes
        self.style_frame = ctk.CTkFrame(
            self.controls_frame, fg_color="transparent"
        )
        self.style_frame.pack(fill="x")

        self.bold_var = ctk.BooleanVar(value=False)
        self.bold_checkbox = ctk.CTkCheckBox(
            self.style_frame,
            text=get_text("format.bold", "Bold"),
            variable=self.bold_var,
            state="disabled",
            command=self._on_format_option_changed,
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.bold_checkbox.pack(side="left", padx=(0, SPACING_MD))

        self.italic_var = ctk.BooleanVar(value=False)
        self.italic_checkbox = ctk.CTkCheckBox(
            self.style_frame,
            text=get_text("format.italic", "Italic"),
            variable=self.italic_var,
            state="disabled",
            command=self._on_format_option_changed,
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.italic_checkbox.pack(side="left")

        # Preview
        self.preview_label = ctk.CTkLabel(
            self.controls_frame,
            text=get_text("format.preview", "Preview:"),
            font=get_poppins_font(size=12, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.preview_label.pack(anchor="w", pady=(SPACING_LG, SPACING_MD))

        self.preview_text = ctk.CTkLabel(
            self.controls_frame,
            text=get_text("format.preview.example", "Table Title Example"),
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.preview_text.pack(anchor="w", pady=(0, SPACING_MD))

        # Initially disable controls
        self._update_controls_state()

    def _on_keep_original_changed(self) -> None:
        """Handle keep original format checkbox change."""
        self.keep_original = self.keep_original_var.get()
        self._update_controls_state()

        if self.format_callback:
            self.format_callback(self.get_format_info())

    def _on_format_option_changed(self, value=None) -> None:
        """
        Handle format option changes (font, size, bold, italic).
        
        Args:
            value: Optional value from dropdown (ignored, we read current state)
        """
        if self.format_callback:
            self.format_callback(self.get_format_info())

    def _update_controls_state(self) -> None:
        """Update visibility and enabled/disabled state of format controls."""
        if self.keep_original:
            # Hide all format controls when keeping original format
            self.controls_frame.pack_forget()
        else:
            # Show and enable format controls when customizing
            self.controls_frame.pack(fill="x", padx=SPACING_LG, pady=(SPACING_LG, 0))
            state = "normal"
            self.font_dropdown.configure(state=state)
            self.size_dropdown.configure(state=state)
            self.bold_checkbox.configure(state=state)
            self.italic_checkbox.configure(state=state)

    def get_format_info(self) -> Optional[FormatInfo]:
        """
        Get current format information.

        Returns:
            FormatInfo object or None if keeping original
        """
        if self.keep_original:
            return None

        try:
            font_name = self.font_dropdown.get()
            if not font_name:
                return None
            
            size_str = self.size_dropdown.get()
            if not size_str:
                return None
            
            # Remove " pt" suffix if present
            size_str = size_str.replace(" pt", "").strip()
            if not size_str:
                return None
            
            font_size = float(size_str)
            
            # Validate font size
            if font_size <= 0:
                return None

            return FormatInfo(
                font_name=font_name,
                font_size=font_size,
                is_bold=self.bold_var.get(),
                is_italic=self.italic_var.get(),
            )
        except (ValueError, AttributeError):
            # Return None if values are not ready yet
            return None

    def set_format_callback(self, callback: Callable) -> None:
        """
        Set callback for format changes.

        Args:
            callback: Function to call when format changes
        """
        self.format_callback = callback

    def set_enabled(self, enabled: bool) -> None:
        """
        Enable or disable the entire component.

        Args:
            enabled: Whether to enable the component
        """
        state = "normal" if enabled else "disabled"
        self.keep_original_checkbox.configure(state=state)
        if not self.keep_original:
            self._update_controls_state()

    def set_detected_format(self, format_info: Optional[FormatInfo]) -> None:
        """
        Set and display the detected format from analysis.

        Args:
            format_info: FormatInfo object from analysis, or None
        """
        if format_info is None:
            self.detected_format_details.configure(
                text=get_text("format.no_format", "No format detected"),
                text_color=FLUENT_TEXT_SECONDARY,
            )
        else:
            # Format the display text
            format_parts = []
            format_parts.append(
                get_text("format.font_label", "Font: {name}").format(
                    name=format_info.font_name
                )
            )
            # Round size to 1 decimal place for display
            format_parts.append(
                get_text("format.size_label", "Size: {size} pt").format(
                    size=round(format_info.font_size, 1)
                )
            )
            if format_info.is_bold:
                format_parts.append(get_text("format.bold", "Bold"))
            if format_info.is_italic:
                format_parts.append(get_text("format.italic", "Italic"))
            
            format_text = " • ".join(format_parts)
            self.detected_format_details.configure(
                text=format_text,
                text_color=FLUENT_TEXT_PRIMARY,
            )

    def refresh_texts(self) -> None:
        """Refresh all texts after language change."""
        self.title_label.configure(
            text=get_text("format.title", "Format Options")
        )
        self.subtitle_label.configure(
            text=get_text("format.subtitle", "Customize table title formatting")
        )
        self.detected_format_label.configure(
            text=get_text("format.detected_format", "Detected Format:")
        )
        self.keep_original_checkbox.configure(
            text=get_text("format.keep_original", "Keep original format")
        )
        self.description_label.configure(
            text=get_text(
                "format.keep_original.desc",
                "Preserve the existing formatting of table titles"
            )
        )
        self.font_label.configure(
            text=get_text("format.font", "Font Family:")
        )
        self.size_label.configure(
            text=get_text("format.size", "Font Size:")
        )
        self.bold_checkbox.configure(
            text=get_text("format.bold", "Bold")
        )
        self.italic_checkbox.configure(
            text=get_text("format.italic", "Italic")
        )
        self.preview_label.configure(
            text=get_text("format.preview", "Preview:")
        )
        self.preview_text.configure(
            text=get_text("format.preview.example", "Table Title Example")
        )

