"""Main application window."""

import threading
from pathlib import Path
from typing import Optional
from tkinter import messagebox, filedialog

import customtkinter as ctk

from src.gui.components.file_selector import FileSelector
from src.gui.components.results_panel import ResultsPanel
from src.gui.components.format_controls import FormatControls
from src.gui.themes.fluent_theme import (
    apply_fluent_theme,
    FLUENT_PRIMARY,
    FLUENT_SECONDARY,
    FLUENT_BACKGROUND,
    FLUENT_HOVER,
    FLUENT_TEXT_PRIMARY,
    FLUENT_TEXT_SECONDARY,
    SPACING_MD,
    SPACING_LG,
    RADIUS_MD,
)
from src.gui.themes.fonts import get_poppins_font
from src.rules.table_title_rule import TableTitleRule
from src.core.models import AnalysisResult, FormatInfo
from src.utils.exceptions import (
    PDFReadError,
    FormatDetectionError,
    ModificationError,
    ValidationError,
)


class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize main window."""
        super().__init__()

        # Apply theme
        apply_fluent_theme(self)

        # Window configuration
        self.title("PDF Table Title Fixer")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Initialize rule
        self.rule = TableTitleRule()

        # Current state
        self.current_result: Optional[AnalysisResult] = None
        self.selected_file: Optional[Path] = None

        # Create UI
        self._create_sidebar()
        self._create_main_content()

    def _create_sidebar(self) -> None:
        """Create left sidebar navigation."""
        self.sidebar = ctk.CTkFrame(
            self, width=220, corner_radius=0, fg_color=FLUENT_BACKGROUND
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        # Logo/Title with icon
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(SPACING_LG, SPACING_MD), padx=SPACING_MD)

        # Icon placeholder (using emoji, can be replaced with image)
        icon_label = ctk.CTkLabel(
            logo_frame,
            text="📄",
            font=get_poppins_font(size=32),
        )
        icon_label.pack()

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="PDF Fixer",
            font=get_poppins_font(size=20, weight="bold"),
            text_color=FLUENT_PRIMARY,
        )
        self.logo_label.pack(pady=(0, SPACING_MD))

        self.subtitle_label = ctk.CTkLabel(
            self.sidebar,
            text="Table Editor",
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.subtitle_label.pack(pady=(0, SPACING_LG))

        # Navigation buttons
        nav_items = [
            ("🏠", "Home", self._show_home, True),
            ("📄", "Documents", lambda: None, False),
            ("🔄", "History", lambda: None, False),
            ("⚙️", "Settings", lambda: None, False),
            ("❓", "Help", lambda: None, False),
        ]

        self.nav_buttons = []
        for icon, text, command, is_active in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}  {text}",
                command=command,
                fg_color=FLUENT_PRIMARY if is_active else "transparent",
                hover_color=FLUENT_SECONDARY if is_active else FLUENT_HOVER,
                corner_radius=RADIUS_MD,
                anchor="w",
                font=get_poppins_font(size=13),
                text_color=FLUENT_TEXT_PRIMARY if not is_active else "white",
            )
            btn.pack(fill="x", padx=SPACING_MD, pady=(0, SPACING_MD))
            self.nav_buttons.append(btn)

        # Help section at bottom
        help_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color=FLUENT_PRIMARY,
            corner_radius=RADIUS_MD,
        )
        help_frame.pack(side="bottom", fill="x", padx=SPACING_MD, pady=SPACING_MD)

        help_title = ctk.CTkLabel(
            help_frame,
            text="Need Help?",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white",
        )
        help_title.pack(pady=(SPACING_MD, SPACING_MD), padx=SPACING_MD)

        help_text = ctk.CTkLabel(
            help_frame,
            text="View our documentation for guides and tutorials.",
            font=get_poppins_font(size=10),
            text_color="white",
            wraplength=180,
        )
        help_text.pack(pady=(0, SPACING_MD), padx=SPACING_MD)

    def _create_main_content(self) -> None:
        """Create main content area with scrollbar."""
        # Create scrollable frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=SPACING_LG, pady=SPACING_LG)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
        )
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # File selector
        self.file_selector = FileSelector(self.scrollable_frame)
        self.file_selector.set_callback(self._on_file_selected)
        self.file_selector.grid(
            row=0, column=0, sticky="ew", padx=SPACING_MD, pady=(SPACING_MD, SPACING_LG)
        )

        # Results panel
        self.results_panel = ResultsPanel(self.scrollable_frame)
        self.results_panel.grid(
            row=1, column=0, sticky="ew", padx=SPACING_MD, pady=(0, SPACING_LG)
        )

        # Format controls
        self.format_controls = FormatControls(self.scrollable_frame)
        self.format_controls.set_format_callback(self._on_format_changed)
        self.format_controls.grid(
            row=2, column=0, sticky="ew", padx=SPACING_MD, pady=(0, SPACING_LG)
        )

        # Apply button
        self.apply_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Apply Modifications",
            command=self._apply_modifications,
            fg_color=FLUENT_PRIMARY,
            hover_color=FLUENT_SECONDARY,
            corner_radius=RADIUS_MD,
            font=get_poppins_font(size=14, weight="bold"),
            state="disabled",
            height=45,
        )
        self.apply_button.grid(
            row=3, column=0, sticky="ew", padx=SPACING_MD, pady=(0, SPACING_LG)
        )

    def _show_home(self) -> None:
        """Show home view (currently same as main)."""
        pass

    def _on_file_selected(self, file_path: Path) -> None:
        """
        Handle file selection.

        Args:
            file_path: Selected PDF file path
        """
        self.selected_file = file_path
        self._analyze_pdf(file_path)

    def _analyze_pdf(self, file_path: Path) -> None:
        """
        Analyze PDF file in background thread.

        Args:
            file_path: Path to PDF file
        """
        # Disable controls during analysis
        self.apply_button.configure(state="disabled")
        self.file_selector.browse_button.configure(state="disabled")

        def analyze_thread() -> None:
            try:
                result = self.rule.analyze(str(file_path))
                self.after(0, self._on_analysis_complete, result)
            except Exception as e:
                self.after(0, self._on_analysis_error, str(e))

        thread = threading.Thread(target=analyze_thread, daemon=True)
        thread.start()

    def _on_analysis_complete(self, result: AnalysisResult) -> None:
        """
        Handle analysis completion.

        Args:
            result: AnalysisResult object
        """
        self.current_result = result
        self.results_panel.update_results(result)

        # Set detected format in format controls
        self.format_controls.set_detected_format(result.format_info)

        # Enable format controls based on uniformity
        # Temporarily disable format callback to avoid interference
        original_callback = self.format_controls.format_callback
        self.format_controls.format_callback = None
        
        if result.format_uniform:
            self.format_controls.keep_original_checkbox.configure(
                state="normal"
            )
        else:
            self.format_controls.keep_original_checkbox.configure(
                state="disabled"
            )
            self.format_controls.keep_original_var.set(False)
            self.format_controls._on_keep_original_changed()
        
        # Re-enable format callback
        self.format_controls.format_callback = original_callback

        # Enable apply button if there are modifications
        # Do this AFTER all format control updates to ensure state is correct
        if result.tables_to_modify > 0:
            self.apply_button.configure(state="normal")
        else:
            self.apply_button.configure(state="disabled")

        # Re-enable file selector
        self.file_selector.browse_button.configure(state="normal")

    def _on_analysis_error(self, error_message: str) -> None:
        """
        Handle analysis error.

        Args:
            error_message: Error message
        """
        messagebox.showerror("Analysis Error", f"Error analyzing PDF:\n{error_message}")
        self.results_panel.clear_results()
        self.format_controls.set_detected_format(None)  # Clear detected format
        self.apply_button.configure(state="disabled")
        self.file_selector.browse_button.configure(state="normal")

    def _on_format_changed(self, format_info: Optional[FormatInfo]) -> None:
        """
        Handle format change.

        Args:
            format_info: New format info or None
        """
        # Format change doesn't require immediate action
        # But ensure apply button is still enabled if we have modifications
        if self.current_result and self.current_result.tables_to_modify > 0:
            self.apply_button.configure(state="normal")

    def _apply_modifications(self) -> None:
        """Apply modifications to PDF."""
        if not self.selected_file or not self.current_result:
            return

        # Get output path
        output_path = filedialog.asksaveasfilename(
            title="Save Modified PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )

        if not output_path:
            return

        # Get format info
        format_info = self.format_controls.get_format_info()

        # Disable button during processing
        self.apply_button.configure(state="disabled", text="Processing...")

        def apply_thread() -> None:
            try:
                modifications = [
                    m for m in self.current_result.modifications
                    if m.needs_modification()
                ]

                success = self.rule.apply_with_format(
                    str(self.selected_file),
                    output_path,
                    modifications,
                    format_info,
                )

                self.after(0, self._on_modification_complete, success)
            except Exception as e:
                self.after(0, self._on_modification_error, str(e))

        thread = threading.Thread(target=apply_thread, daemon=True)
        thread.start()

    def _on_modification_complete(self, success: bool) -> None:
        """
        Handle modification completion.

        Args:
            success: Whether modification was successful
        """
        self.apply_button.configure(
            state="normal", text="Apply Modifications"
        )

        if success:
            messagebox.showinfo(
                "Success",
                "PDF modifications applied successfully!"
            )
        else:
            messagebox.showwarning(
                "Warning",
                "Some modifications may not have been applied."
            )

    def _on_modification_error(self, error_message: str) -> None:
        """
        Handle modification error.

        Args:
            error_message: Error message
        """
        self.apply_button.configure(
            state="normal", text="Apply Modifications"
        )
        messagebox.showerror(
            "Modification Error",
            f"Error modifying PDF:\n{error_message}"
        )

