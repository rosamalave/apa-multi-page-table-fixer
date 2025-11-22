"""Loading panel component with circular progress indicator."""

import math
from typing import Optional

import customtkinter as ctk
import tkinter as tk

from src.gui.themes.fluent_theme import (
    FLUENT_BACKGROUND,
    FLUENT_PRIMARY,
    FLUENT_TEXT_PRIMARY,
    FLUENT_TEXT_SECONDARY,
    SPACING_LG,
    SPACING_MD,
    RADIUS_MD,
)
from src.gui.themes.fonts import get_poppins_font


class LoadingPanel(ctk.CTkFrame):
    """Loading panel with circular progress indicator."""

    def __init__(self, parent) -> None:
        """
        Initialize loading panel.

        Args:
            parent: Parent widget
        """
        super().__init__(
            parent,
            fg_color=FLUENT_BACKGROUND,
            corner_radius=RADIUS_MD,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Current message and progress
        self.current_message = "Initializing analysis..."
        self.current_progress = 0  # 0-100

        # Create centered container
        self._create_centered_container()

    def _create_centered_container(self) -> None:
        """Create centered container for progress and message."""
        # Container frame that will be centered and expand horizontally
        container = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        container.grid(
            row=0,
            column=0,
            sticky="ew",  # Expand horizontally
        )
        container.grid_columnconfigure(0, weight=1)

        # Inner frame for centering content vertically
        inner_frame = ctk.CTkFrame(
            container, fg_color="transparent"
        )
        inner_frame.grid(
            row=0,
            column=0,
            sticky="",
        )
        inner_frame.grid_columnconfigure(0, weight=1)

        # Create progress circle
        self._create_progress_circle(inner_frame)
        
        # Create message label
        self._create_message_label(inner_frame)

    def _create_progress_circle(self, parent) -> None:
        """Create circular progress indicator using Canvas."""
        progress_frame = ctk.CTkFrame(
            parent, fg_color="transparent"
        )
        progress_frame.pack(pady=(0, SPACING_LG * 3))

        # Canvas size (much larger for better visibility)
        canvas_size = 250
        self.canvas = tk.Canvas(
            progress_frame,
            width=canvas_size,
            height=canvas_size,
            bg=FLUENT_BACKGROUND,
            highlightthickness=0,
        )
        self.canvas.pack()

        # Store canvas dimensions
        self.canvas_size = canvas_size
        self.center_x = canvas_size // 2
        self.center_y = canvas_size // 2
        self.radius = 100  # Radius of the progress circle
        self.line_width = 18  # Thickness of the progress ring

        # Colors
        self.progress_color = FLUENT_PRIMARY  # Blue for progress
        self.background_color = "#E5E5E5"  # Light gray for background

        # Draw initial circle
        self._draw_progress_circle(0)

    def _draw_progress_circle(self, progress: float) -> None:
        """
        Draw circular progress indicator.

        Args:
            progress: Progress value from 0 to 100
        """
        # Clear canvas
        self.canvas.delete("all")

        # Clamp progress between 0 and 100
        progress = max(0, min(100, progress))

        # Calculate angle for progress (start from top, clockwise)
        # 0% = -90 degrees (top), 100% = 270 degrees (full circle)
        start_angle = -90  # Start from top
        extent_angle = (progress / 100) * 360  # Extent in degrees

        # Draw background circle (full circle in light gray)
        self.canvas.create_arc(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            start=start_angle,
            extent=360,
            outline=self.background_color,
            width=self.line_width,
            style=tk.ARC,
        )

        # Draw progress arc (blue, only if progress > 0)
        if progress > 0:
            self.canvas.create_arc(
                self.center_x - self.radius,
                self.center_y - self.radius,
                self.center_x + self.radius,
                self.center_y + self.radius,
                start=start_angle,
                extent=extent_angle,
                outline=self.progress_color,
                width=self.line_width,
                style=tk.ARC,
            )

        # Draw percentage text in center (larger font)
        percentage_text = f"{int(progress)}%"
        self.canvas.create_text(
            self.center_x,
            self.center_y,
            text=percentage_text,
            font=("Poppins", 40, "bold"),
            fill=self.progress_color,
        )

    def _create_message_label(self, parent) -> None:
        """Create message label."""
        # Message frame with padding to prevent edge cutoff
        message_frame = ctk.CTkFrame(
            parent, fg_color="transparent"
        )
        message_frame.pack(fill="x", padx=SPACING_LG * 2)
        message_frame.grid_columnconfigure(0, weight=1)

        self.message_label = ctk.CTkLabel(
            message_frame,
            text=self.current_message,
            font=get_poppins_font(size=18),
            text_color=FLUENT_TEXT_PRIMARY,
            wraplength=2000,  # Very large wraplength to prevent cutoff
            justify="center",  # Center align text
            anchor="center",  # Center anchor
        )
        self.message_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=SPACING_LG * 2,
        )

    def update_progress(self, progress: float) -> None:
        """
        Update progress value (0-100).

        Args:
            progress: Progress value from 0 to 100
        """
        self.current_progress = progress
        self._draw_progress_circle(progress)

    def update_message(self, message: str, progress: Optional[float] = None) -> None:
        """
        Update progress message and optionally progress value.

        Args:
            message: New progress message
            progress: Optional progress value (0-100)
        """
        self.current_message = message
        
        # Update text directly without wraplength restriction
        # The label will expand naturally within its container
        self.message_label.configure(text=message)

        if progress is not None:
            self.update_progress(progress)

    def show(self) -> None:
        """Show loading panel."""
        self.grid()
        # Reset progress to 0 when showing
        self.update_progress(0)

    def hide(self) -> None:
        """Hide loading panel."""
        self.grid_remove()
