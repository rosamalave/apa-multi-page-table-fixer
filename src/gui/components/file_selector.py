"""File selector component for PDF files."""

import customtkinter as ctk
from pathlib import Path
from typing import Optional
from tkinter import filedialog

from src.gui.themes.fluent_theme import (
    FLUENT_PRIMARY,
    FLUENT_TEXT_PRIMARY,
    FLUENT_TEXT_SECONDARY,
    FLUENT_BACKGROUND,
    FLUENT_BORDER,
    FLUENT_SURFACE,
    SPACING_MD,
    SPACING_LG,
    RADIUS_MD,
    RADIUS_LG,
)
from src.gui.themes.fonts import get_poppins_font
from src.utils.validators import validate_pdf_path
from src.utils.exceptions import ValidationError


class FileSelector(ctk.CTkFrame):
    """Component for selecting PDF files."""

    def __init__(self, parent, **kwargs) -> None:
        """
        Initialize file selector component.

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
        self.selected_file: Optional[Path] = None
        self.callback = None

        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        # Title with icon
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(SPACING_LG, SPACING_MD), padx=SPACING_LG)

        # Icon
        icon_label = ctk.CTkLabel(
            title_frame,
            text="📁",
            font=get_poppins_font(size=20),
        )
        icon_label.pack(side="left", padx=(0, SPACING_MD))

        # Title
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Select PDF File",
            font=get_poppins_font(size=18, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.title_label.pack(side="left")

        # Instructions
        self.instructions_label = ctk.CTkLabel(
            self,
            text="Choose a PDF file to analyze and modify table titles",
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.instructions_label.pack(pady=(0, SPACING_LG), padx=SPACING_LG, anchor="w")

        # Upload area frame with dashed border effect
        self.upload_frame = ctk.CTkFrame(
            self,
            fg_color=FLUENT_BACKGROUND,
            corner_radius=RADIUS_LG,
            border_width=2,
            border_color=FLUENT_BORDER,
        )
        self.upload_frame.pack(fill="both", expand=True, pady=(0, SPACING_MD), padx=SPACING_LG)
        self.upload_frame.pack_propagate(False)

        # Configure upload frame to have minimum height
        self.upload_frame.configure(height=220)

        # Inner content frame
        self.upload_content = ctk.CTkFrame(
            self.upload_frame,
            fg_color="transparent",
        )
        self.upload_content.pack(expand=True, fill="both", padx=SPACING_LG, pady=SPACING_LG)

        # Upload icon container
        icon_container = ctk.CTkFrame(
            self.upload_content,
            fg_color=FLUENT_PRIMARY,
            corner_radius=RADIUS_MD,
            width=80,
            height=80,
        )
        icon_container.pack(pady=(SPACING_MD, SPACING_MD))
        icon_container.pack_propagate(False)

        # Upload icon (using emoji as placeholder, can be replaced with image)
        self.upload_icon_label = ctk.CTkLabel(
            icon_container,
            text="📤",
            font=get_poppins_font(size=40),
            text_color="white",
        )
        self.upload_icon_label.pack(expand=True)

        # Browse button
        self.browse_button = ctk.CTkButton(
            self.upload_content,
            text="Browse Files",
            command=self._browse_file,
            fg_color=FLUENT_PRIMARY,
            hover_color="#106EBE",
            corner_radius=RADIUS_MD,
            font=get_poppins_font(size=14, weight="bold"),
            width=150,
            height=40,
        )
        self.browse_button.pack(pady=(0, SPACING_MD))

        # Drag and drop text
        self.drag_text = ctk.CTkLabel(
            self.upload_content,
            text="or drag and drop your PDF file here",
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.drag_text.pack(pady=(0, SPACING_MD))

        # File format info
        self.format_info = ctk.CTkLabel(
            self.upload_content,
            text="Supported format: PDF (Max 50MB)",
            font=get_poppins_font(size=10),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.format_info.pack()

        # File status indicator
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.pack(fill="x", pady=(SPACING_MD, SPACING_LG), padx=SPACING_LG)

        # Status icon
        status_icon = ctk.CTkLabel(
            self.status_frame,
            text="📄",
            font=ctk.CTkFont(size=14),
        )
        status_icon.pack(side="left", padx=(0, SPACING_MD))

        self.file_path_label = ctk.CTkLabel(
            self.status_frame,
            text="No file selected",
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
            anchor="w",
        )
        self.file_path_label.pack(side="left")

    def _browse_file(self) -> None:
        """Open file dialog to select PDF."""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )

        if file_path:
            try:
                validated_path = validate_pdf_path(file_path)
                self.selected_file = validated_path
                self._update_display()
                if self.callback:
                    self.callback(validated_path)
            except ValidationError as e:
                self._show_error(str(e))

    def _update_display(self) -> None:
        """Update file path display."""
        if self.selected_file:
            file_name = self.selected_file.name
            self.file_path_label.configure(
                text=f"Selected: {file_name}",
                text_color=FLUENT_TEXT_PRIMARY,
            )
        else:
            self.file_path_label.configure(
                text="No file selected",
                text_color=FLUENT_TEXT_SECONDARY,
            )

    def _show_error(self, message: str) -> None:
        """Show error message."""
        self.file_path_label.configure(
            text=f"Error: {message}",
            text_color="#D13438",
        )

    def get_selected_file(self) -> Optional[Path]:
        """
        Get currently selected file.

        Returns:
            Path object or None
        """
        return self.selected_file

    def set_callback(self, callback) -> None:
        """
        Set callback function for file selection.

        Args:
            callback: Function to call when file is selected
        """
        self.callback = callback

    def clear_selection(self) -> None:
        """Clear current file selection."""
        self.selected_file = None
        self._update_display()

