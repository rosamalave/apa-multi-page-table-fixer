"""Changes panel component for viewing modification history."""

import customtkinter as ctk
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from src.gui.themes.fluent_theme import (
    FLUENT_PRIMARY,
    FLUENT_TEXT_PRIMARY,
    FLUENT_TEXT_SECONDARY,
    FLUENT_SURFACE,
    FLUENT_BACKGROUND,
    FLUENT_BORDER,
    FLUENT_HOVER,
    SPACING_SM,
    SPACING_MD,
    SPACING_LG,
    RADIUS_MD,
    RADIUS_LG,
)
from src.gui.themes.fonts import get_poppins_font
from src.utils.i18n import get_text
from src.utils.history import load_all_history, ModificationHistory


class ChangesPanel(ctk.CTkFrame):
    """Component for viewing modification history."""

    def __init__(self, parent, **kwargs) -> None:
        """
        Initialize changes panel component.

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
        
        # Store current details entry
        self.current_details_entry: Optional[ModificationHistory] = None
        
        self._create_widgets()
        self._load_history()

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        # Title with icon
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(SPACING_LG, SPACING_MD), padx=SPACING_LG)

        # Icon
        icon_label = ctk.CTkLabel(
            title_frame,
            text="🔄",
            font=get_poppins_font(size=20),
        )
        icon_label.pack(side="left", padx=(0, SPACING_MD))

        # Title
        self.title_label = ctk.CTkLabel(
            title_frame,
            text=get_text("changes.title", "Changes"),
            font=get_poppins_font(size=18, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.title_label.pack(side="left")

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self,
            text=get_text("changes.subtitle", "History of applied modifications"),
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.subtitle_label.pack(pady=(0, SPACING_LG), padx=SPACING_LG, anchor="w")

        # History list container
        # Container for history list and details view
        self.content_container = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        self.content_container.pack(
            fill="both", expand=True, padx=SPACING_LG, pady=(0, SPACING_LG)
        )

        # History list container
        self.history_container = ctk.CTkFrame(
            self.content_container, fg_color="transparent"
        )
        self.history_container.pack(
            fill="both", expand=True
        )

        # Details view container (initially hidden)
        self.details_container = ctk.CTkFrame(
            self.content_container, fg_color="transparent"
        )
        # Don't pack initially - will be shown when details are viewed

    def _load_history(self) -> None:
        """Load and display modification history."""
        # Clear existing items
        for widget in self.history_container.winfo_children():
            widget.destroy()

        history = load_all_history()

        if not history:
            # Show empty state
            self._show_empty_state()
            return

        # Display history items
        for idx, entry in enumerate(history):
            self._create_history_item(entry, idx)

    def _show_empty_state(self) -> None:
        """Show empty state when no history exists."""
        empty_frame = ctk.CTkFrame(
            self.history_container, fg_color="transparent"
        )
        empty_frame.pack(expand=True, fill="both", pady=SPACING_LG * 2)

        empty_label = ctk.CTkLabel(
            empty_frame,
            text=get_text("changes.no_changes", "No modifications yet"),
            font=get_poppins_font(size=16, weight="bold"),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        empty_label.pack(pady=(0, SPACING_MD))

        desc_label = ctk.CTkLabel(
            empty_frame,
            text=get_text(
                "changes.no_changes.desc",
                "Modified documents will appear here after processing"
            ),
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
            wraplength=500,
        )
        desc_label.pack()

    def _create_history_item(
        self, entry: ModificationHistory, index: int
    ) -> None:
        """
        Create a history item card.

        Args:
            entry: ModificationHistory entry
            index: Item index
        """
        # Card frame
        card = ctk.CTkFrame(
            self.history_container,
            fg_color=FLUENT_BACKGROUND,
            corner_radius=RADIUS_MD,
            border_width=1,
            border_color=FLUENT_BORDER,
        )
        card.pack(fill="x", pady=(0, SPACING_MD))

        # Card content
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=SPACING_LG, pady=SPACING_MD)

        # File name (top)
        file_name = Path(entry.input_file).name
        file_label = ctk.CTkLabel(
            content_frame,
            text=file_name,
            font=get_poppins_font(size=14, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
            anchor="w",
        )
        file_label.pack(fill="x", pady=(0, SPACING_SM))

        # Info row
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=(0, SPACING_MD))

        # Date
        try:
            dt = datetime.fromisoformat(entry.timestamp)
            date_str = dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            date_str = entry.timestamp

        date_label = ctk.CTkLabel(
            info_frame,
            text=f"📅 {date_str}",
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        date_label.pack(side="left", padx=(0, SPACING_LG))

        # Tables modified
        tables_label = ctk.CTkLabel(
            info_frame,
            text=f"📊 {entry.tables_modified} {get_text('changes.tables_modified', 'Tables Modified')}",
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        tables_label.pack(side="left", padx=(0, SPACING_LG))

        # Format info
        if entry.format_applied:
            format_str = self._format_format_info(entry.format_applied)
            format_label = ctk.CTkLabel(
                info_frame,
                text=f"🎨 {format_str}",
                font=get_poppins_font(size=11),
                text_color=FLUENT_TEXT_SECONDARY,
            )
            format_label.pack(side="left")

        # Details button
        details_button = ctk.CTkButton(
            content_frame,
            text=get_text("changes.details", "Details"),
            command=lambda e=entry: self._show_details(e),
            fg_color=FLUENT_PRIMARY,
            hover_color="#106EBE",
            corner_radius=RADIUS_MD,
            font=get_poppins_font(size=12),
            width=100,
            height=30,
        )
        details_button.pack(anchor="e", pady=(SPACING_SM, 0))

    def _format_format_info(self, format_info: Dict[str, Any]) -> str:
        """
        Format format information for display.

        Args:
            format_info: Format dictionary

        Returns:
            Formatted string
        """
        parts = []
        if format_info.get("font_name"):
            parts.append(format_info["font_name"])
        if format_info.get("font_size"):
            parts.append(f"{format_info['font_size']}pt")
        if format_info.get("is_bold"):
            parts.append("Bold")
        if format_info.get("is_italic"):
            parts.append("Italic")
        
        return " • ".join(parts) if parts else get_text(
            "changes.details.original_format", "Original Format"
        )

    def _show_details(self, entry: ModificationHistory) -> None:
        """
        Show detailed modification information in the same panel.

        Args:
            entry: ModificationHistory entry
        """
        # Store current entry
        self.current_details_entry = entry
        
        # Hide history list, show details immediately
        self.history_container.pack_forget()
        
        # Clear details container
        for widget in self.details_container.winfo_children():
            widget.destroy()
        
        # Pack details container
        self.details_container.pack(fill="both", expand=True)
        
        # Force update to show container immediately
        self.details_container.update_idletasks()

        # Card container for details (rounded frame like other views)
        details_card = ctk.CTkFrame(
            self.details_container,
            fg_color=FLUENT_SURFACE,
            corner_radius=RADIUS_LG,
            border_width=1,
            border_color=FLUENT_BORDER,
        )
        details_card.pack(fill="both", expand=True, padx=SPACING_MD, pady=SPACING_MD)

        # Scrollable content for details
        scrollable = ctk.CTkScrollableFrame(
            details_card, fg_color=FLUENT_SURFACE
        )
        scrollable.pack(fill="both", expand=True, padx=SPACING_LG, pady=SPACING_LG)

        # Back button and title frame
        header_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, SPACING_LG))

        # Back button with hover effects - width proportional to text
        back_button_text = "← " + get_text("changes.details.back", "Back")
        # Calculate approximate width based on text length
        # Rough estimate: ~8 pixels per character + padding
        estimated_width = len(back_button_text) * 8 + 20
        back_button = ctk.CTkButton(
            header_frame,
            text=back_button_text,
            command=self._show_history_list,
            fg_color="transparent",
            hover_color=FLUENT_PRIMARY,  # Blue highlight color on hover
            corner_radius=RADIUS_MD,
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_PRIMARY,  # Black text by default
            anchor="center",  # Center text in button
            width=estimated_width,  # Proportional to text content
        )
        # Bind hover events to change both background and text color
        def on_enter(event):
            # Change to blue background with white text
            back_button.configure(
                fg_color=FLUENT_PRIMARY,
                text_color="white"
            )
        def on_leave(event):
            # Change back to transparent with black text
            back_button.configure(
                fg_color="transparent",
                text_color=FLUENT_TEXT_PRIMARY
            )
        
        # Bind to both Enter and Leave events
        back_button.bind("<Enter>", on_enter)
        back_button.bind("<Leave>", on_leave)
        # Also bind to the button's internal canvas if available
        try:
            if hasattr(back_button, 'canvas'):
                back_button.canvas.bind("<Enter>", on_enter)
                back_button.canvas.bind("<Leave>", on_leave)
        except Exception:
            pass
        
        # Pack button without fill to keep it proportional to text
        back_button.pack(side="left", padx=(0, SPACING_MD), fill="none")

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text=get_text("changes.details.title", "Modification Details"),
            font=get_poppins_font(size=20, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        title_label.pack(side="left")

        # File information section
        self._create_info_section(
            scrollable,
            get_text("changes.details.input_file", "Input File:"),
            entry.input_file,
        )
        self._create_info_section(
            scrollable,
            get_text("changes.details.output_file", "Output File:"),
            entry.output_file,
        )

        # Date
        try:
            dt = datetime.fromisoformat(entry.timestamp)
            date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            date_str = entry.timestamp
        self._create_info_section(
            scrollable,
            get_text("changes.details.timestamp", "Date & Time:"),
            date_str,
        )

        # Tables count
        self._create_info_section(
            scrollable,
            get_text("changes.details.tables_count", "Tables Modified:"),
            str(entry.tables_modified),
        )

        # Format applied
        format_str = (
            self._format_format_info(entry.format_applied)
            if entry.format_applied
            else get_text("changes.details.original_format", "Original Format")
        )
        self._create_info_section(
            scrollable,
            get_text("changes.details.format_applied", "Format Applied:"),
            format_str,
        )

        # Modifications detail - create in batches for better performance
        if entry.modifications_detail:
            mod_label = ctk.CTkLabel(
                scrollable,
                text=get_text("changes.details.modifications", "Modifications:"),
                font=get_poppins_font(size=14, weight="bold"),
                text_color=FLUENT_TEXT_PRIMARY,
            )
            mod_label.pack(pady=(SPACING_LG, SPACING_MD), anchor="w")
            
            # Force update to show label immediately
            scrollable.update_idletasks()
            
            # Create modifications in batches for better performance
            self._create_modifications_batch(scrollable, entry, 0)


    def _create_info_section(
        self, parent: ctk.CTkFrame, label: str, value: str
    ) -> None:
        """
        Create an information section.

        Args:
            parent: Parent widget
            label: Label text
            value: Value text
        """
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, SPACING_MD))

        label_widget = ctk.CTkLabel(
            frame,
            text=label,
            font=get_poppins_font(size=12, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
            anchor="w",
        )
        label_widget.pack(side="left", padx=(0, SPACING_MD))

        value_widget = ctk.CTkLabel(
            frame,
            text=value,
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
            anchor="w",
            wraplength=500,
        )
        value_widget.pack(side="left", fill="x", expand=True)

    def _create_modification_item(
        self, parent: ctk.CTkFrame, mod: Dict[str, Any]
    ) -> None:
        """
        Create a modification detail item.

        Args:
            parent: Parent widget
            mod: Modification dictionary
        """
        # Card for modification
        card = ctk.CTkFrame(
            parent,
            fg_color=FLUENT_SURFACE,
            corner_radius=RADIUS_MD,
            border_width=1,
            border_color=FLUENT_BORDER,
        )
        card.pack(fill="x", pady=(0, SPACING_MD))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=SPACING_MD, pady=SPACING_MD)

        # Page number
        page_label = ctk.CTkLabel(
            content,
            text=get_text("changes.details.page", "Page {page}").format(
                page=mod.get("page", "?")
            ),
            font=get_poppins_font(size=13, weight="bold"),
            text_color=FLUENT_PRIMARY,
        )
        page_label.pack(anchor="w", pady=(0, SPACING_SM))

        # Original title
        orig_frame = ctk.CTkFrame(content, fg_color="transparent")
        orig_frame.pack(fill="x", pady=(0, SPACING_SM))

        orig_label = ctk.CTkLabel(
            orig_frame,
            text=get_text("changes.details.original", "Original:"),
            font=get_poppins_font(size=11, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
            anchor="w",
        )
        orig_label.pack(side="left", padx=(0, SPACING_MD))

        orig_value = ctk.CTkLabel(
            orig_frame,
            text=mod.get("original_title", ""),
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
            anchor="w",
            wraplength=500,
        )
        orig_value.pack(side="left", fill="x", expand=True)

        # Modified title
        mod_frame = ctk.CTkFrame(content, fg_color="transparent")
        mod_frame.pack(fill="x")

        mod_label = ctk.CTkLabel(
            mod_frame,
            text=get_text("changes.details.modified", "Modified:"),
            font=get_poppins_font(size=11, weight="bold"),
            text_color=FLUENT_PRIMARY,
            anchor="w",
        )
        mod_label.pack(side="left", padx=(0, SPACING_MD))

        mod_value = ctk.CTkLabel(
            mod_frame,
            text=mod.get("modified_title", ""),
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_PRIMARY,
            anchor="w",
            wraplength=500,
        )
        mod_value.pack(side="left", fill="x", expand=True)

    def _create_modifications_batch(
        self, scrollable: ctk.CTkScrollableFrame, entry: ModificationHistory, start_idx: int
    ) -> None:
        """
        Create modifications in batches for better performance.
        
        Args:
            scrollable: Scrollable frame
            entry: ModificationHistory entry
            start_idx: Starting index for modifications
        """
        # Process modifications in batches of 10
        batch_size = 10
        end_idx = min(start_idx + batch_size, len(entry.modifications_detail))
        
        for i in range(start_idx, end_idx):
            self._create_modification_item(scrollable, entry.modifications_detail[i])
        
        # Force update after batch
        scrollable.update_idletasks()
        
        # Continue with next batch if needed
        if end_idx < len(entry.modifications_detail):
            self.after(10, lambda: self._create_modifications_batch(
                scrollable, entry, end_idx
            ))

    def refresh_texts(self) -> None:
        """Refresh all texts after language change."""
        self.title_label.configure(
            text=get_text("changes.title", "Changes")
        )
        self.subtitle_label.configure(
            text=get_text("changes.subtitle", "History of applied modifications")
        )
        # Reload history to update all texts
        self._load_history()

    def _show_history_list(self) -> None:
        """Show history list and hide details."""
        self.details_container.pack_forget()
        self.history_container.pack(fill="both", expand=True)
        self.current_details_entry = None

    def refresh_history(self) -> None:
        """Refresh history display."""
        # If showing details, refresh them; otherwise refresh list
        if hasattr(self, 'current_details_entry') and self.current_details_entry:
            # Re-show details with current entry
            self._show_details(self.current_details_entry)
        else:
            self._load_history()

