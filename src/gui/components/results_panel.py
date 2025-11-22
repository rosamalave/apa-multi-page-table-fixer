"""Results panel component for displaying analysis results."""

import customtkinter as ctk

from src.gui.themes.fluent_theme import (
    FLUENT_PRIMARY,
    FLUENT_SUCCESS,
    FLUENT_TEXT_PRIMARY,
    FLUENT_TEXT_SECONDARY,
    FLUENT_BACKGROUND,
    FLUENT_BORDER,
    FLUENT_SURFACE,
    SPACING_MD,
    SPACING_LG,
    RADIUS_MD,
    RADIUS_LG,
    RADIUS_SM,
)
from src.gui.themes.fonts import get_poppins_font
from src.core.models import AnalysisResult


class ResultsPanel(ctk.CTkFrame):
    """Component for displaying analysis results."""

    def __init__(self, parent, **kwargs) -> None:
        """
        Initialize results panel component.

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
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        # Title with icon
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(SPACING_LG, SPACING_MD), padx=SPACING_LG)

        # Icon
        icon_label = ctk.CTkLabel(
            title_frame,
            text="📊",
            font=get_poppins_font(size=20),
        )
        icon_label.pack(side="left", padx=(0, SPACING_MD))

        # Title
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Analysis Results",
            font=get_poppins_font(size=18, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.title_label.pack(side="left")

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Document analysis summary",
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.subtitle_label.pack(pady=(0, SPACING_LG), padx=SPACING_LG, anchor="w")

        # Cards container
        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, padx=SPACING_LG, pady=(0, SPACING_LG))

        # Card 1: Tables Detected
        self.total_card = ctk.CTkFrame(
            cards_container,
            fg_color=FLUENT_SURFACE,
            corner_radius=RADIUS_LG,
            border_width=1,
            border_color=FLUENT_BORDER,
        )
        self.total_card.pack(fill="both", expand=True, pady=(0, SPACING_MD))

        self.total_label = ctk.CTkLabel(
            self.total_card,
            text="0",
            font=get_poppins_font(size=48, weight="bold"),
            text_color=FLUENT_PRIMARY,
        )
        self.total_label.pack(pady=(SPACING_LG, SPACING_MD))

        self.total_text_label = ctk.CTkLabel(
            self.total_card,
            text="Tables Detected",
            font=get_poppins_font(size=14),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.total_text_label.pack(pady=(0, SPACING_LG))

        # Stats frame for side-by-side cards
        self.stats_frame = ctk.CTkFrame(cards_container, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(0, 0))

        # Card 2: Tables to Modify
        self.modify_card = ctk.CTkFrame(
            self.stats_frame,
            fg_color=FLUENT_SURFACE,
            corner_radius=RADIUS_LG,
            border_width=1,
            border_color=FLUENT_BORDER,
        )
        self.modify_card.pack(side="left", fill="both", expand=True, padx=(0, SPACING_MD))

        self.modify_number_label = ctk.CTkLabel(
            self.modify_card,
            text="0",
            font=get_poppins_font(size=24, weight="bold"),
            text_color=FLUENT_PRIMARY,
        )
        self.modify_number_label.pack(pady=(SPACING_LG, SPACING_MD))

        self.modify_text_label = ctk.CTkLabel(
            self.modify_card,
            text="Tables to Modify",
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.modify_text_label.pack(pady=(0, SPACING_MD))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.modify_card,
            fg_color="#E0E0E0",
            progress_color=FLUENT_PRIMARY,
            corner_radius=RADIUS_SM,
        )
        self.progress_bar.pack(
            fill="x", padx=SPACING_MD, pady=(0, SPACING_LG)
        )
        self.progress_bar.set(0)

        # Card 3: Format Uniform
        self.format_card = ctk.CTkFrame(
            self.stats_frame,
            fg_color=FLUENT_SURFACE,
            corner_radius=RADIUS_LG,
            border_width=1,
            border_color=FLUENT_BORDER,
        )
        self.format_card.pack(side="right", fill="both", expand=True)

        self.format_status_label = ctk.CTkLabel(
            self.format_card,
            text="Yes",
            font=get_poppins_font(size=20, weight="bold"),
            text_color=FLUENT_SUCCESS,
        )
        self.format_status_label.pack(pady=(SPACING_LG, SPACING_MD))

        self.format_text_label = ctk.CTkLabel(
            self.format_card,
            text="Format Uniform",
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.format_text_label.pack(pady=(0, SPACING_MD))

        self.format_detail_label = ctk.CTkLabel(
            self.format_card,
            text="All tables consistent",
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.format_detail_label.pack(pady=(0, SPACING_LG))

    def update_results(self, result: AnalysisResult) -> None:
        """
        Update panel with analysis results.

        Args:
            result: AnalysisResult object
        """
        # Update total tables
        self.total_label.configure(text=str(result.total_tables))

        # Update tables to modify
        self.modify_number_label.configure(
            text=str(result.tables_to_modify)
        )

        # Update progress bar
        if result.total_tables > 0:
            progress = result.tables_to_modify / result.total_tables
            self.progress_bar.set(progress)
        else:
            self.progress_bar.set(0)

        # Update format uniform status
        if result.format_uniform:
            self.format_status_label.configure(
                text="Yes", text_color=FLUENT_SUCCESS
            )
            self.format_detail_label.configure(
                text="All tables consistent"
            )
        else:
            self.format_status_label.configure(
                text="No", text_color="#FF6F00"
            )
            self.format_detail_label.configure(
                text="Formats vary"
            )

    def clear_results(self) -> None:
        """Clear all results display."""
        self.total_label.configure(text="0")
        self.modify_number_label.configure(text="0")
        self.progress_bar.set(0)
        self.format_status_label.configure(
            text="Yes", text_color=FLUENT_SUCCESS
        )
        self.format_detail_label.configure(
            text="All tables consistent"
        )

