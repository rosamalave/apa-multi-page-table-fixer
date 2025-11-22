"""Main application window."""

import threading
from pathlib import Path
from typing import Optional, List
from tkinter import messagebox, filedialog
import tkinter as tk

import customtkinter as ctk

from src.gui.components.file_selector import FileSelector
from src.gui.components.results_panel import ResultsPanel
from src.gui.components.format_controls import FormatControls
from src.gui.components.loading_panel import LoadingPanel
from src.gui.components.settings_panel import SettingsPanel
from src.gui.components.changes_panel import ChangesPanel
from src.gui.components.help_panel import HelpPanel
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
from src.utils.i18n import set_language, get_text
from src.utils.config import get_config_value, load_config
from src.utils.history import (
    create_history_entry,
    save_modification_history,
)


class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        """Initialize main window."""
        super().__init__()

        # Apply theme
        apply_fluent_theme(self)

        # Window configuration
        self.title(get_text("app.title", "PDF Table Title Fixer"))
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Set window icon (must be done before mainloop)
        self._set_window_icon()

        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Initialize rule
        self.rule = TableTitleRule()

        # Current state
        self.current_result: Optional[AnalysisResult] = None
        self.selected_file: Optional[Path] = None
        self.current_view = "home"  # Current view: "home" or "settings"

        # Load configuration and set language
        config = load_config()
        language = config.get("language", "en")
        set_language(language)

        # Create UI
        self._create_sidebar()
        self._create_main_content()

    def _set_window_icon(self) -> None:
        """Set window icon from image file."""
        try:
            # For Windows: Set AppUserModelID to ensure icon shows in taskbar
            try:
                import ctypes
                # Set unique app ID for Windows taskbar
                app_id = 'rosamalave.apa-multi-page-table-fixer.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    app_id
                )
            except Exception:
                pass  # Not Windows or ctypes not available
            
            # Get the path to the icon file
            # Use logo_apa_fixerr.ico (sharper quality)
            ico_path = Path(__file__).parent / "img" / "logo_apa_fixerr.ico"
            png_path = Path(__file__).parent / "img" / "logo_apa_fixer.png"
            
            # Try .ico first (better for Windows taskbar and window)
            if ico_path.exists():
                # Use absolute path for iconbitmap (required for Windows)
                icon_path_abs = str(ico_path.absolute())
                # Use iconbitmap for .ico files (works for taskbar and window)
                # Access underlying Tk widget for CustomTkinter
                try:
                    # Get the underlying Tk window
                    tk_window = self._root
                    if tk_window:
                        tk_window.iconbitmap(icon_path_abs)
                    else:
                        self.iconbitmap(icon_path_abs)
                except Exception:
                    # Fallback to direct call
                    self.iconbitmap(icon_path_abs)
            elif png_path.exists():
                # Fallback to PNG for window icon only
                icon_image = tk.PhotoImage(file=str(png_path))
                self.iconphoto(False, icon_image)
                # Keep reference to prevent garbage collection
                self.icon_image = icon_image
        except Exception:
            # Silently fail if icon cannot be loaded
            pass

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
            ("🏠", get_text("sidebar.home", "Home"), self._show_home, True),
            ("🔄", get_text("sidebar.changes", "Changes"), self._show_changes, False),
            ("⚙️", get_text("sidebar.settings", "Settings"), self._show_settings, False),
            ("❓", get_text("sidebar.help", "Help"), self._show_help, False),
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

        self.help_title = ctk.CTkLabel(
            help_frame,
            text=get_text("sidebar.need_help", "Need Help?"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white",
        )
        self.help_title.pack(pady=(SPACING_MD, SPACING_MD), padx=SPACING_MD)

        self.help_text = ctk.CTkLabel(
            help_frame,
            text=get_text(
                "sidebar.help_text",
                "View our documentation for guides and tutorials."
            ),
            font=get_poppins_font(size=10),
            text_color="white",
            wraplength=180,
        )
        self.help_text.pack(pady=(0, SPACING_MD), padx=SPACING_MD)

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

        # Loading panel (hidden by default)
        # Place it directly in main_frame to occupy full space
        self.loading_panel = LoadingPanel(self.main_frame)
        self.loading_panel.grid(
            row=0, column=0, sticky="nsew", padx=0, pady=0
        )
        self.loading_panel.grid_remove()  # Hide initially

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
            text=get_text("button.apply", "Apply Modifications"),
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

        # Settings panel (hidden by default, in main_frame not scrollable)
        self.settings_panel = SettingsPanel(
            self.main_frame,
            language_callback=self._on_language_changed
        )
        self.settings_panel.grid(
            row=0, column=0, sticky="nsew", padx=SPACING_LG, pady=SPACING_LG
        )
        self.settings_panel.grid_remove()  # Hide initially

        # Changes panel (hidden by default, in main_frame not scrollable)
        self.changes_panel = ChangesPanel(self.main_frame)
        self.changes_panel.grid(
            row=0, column=0, sticky="nsew", padx=SPACING_LG, pady=SPACING_LG
        )
        self.changes_panel.grid_remove()  # Hide initially

        # Help panel (hidden by default, in main_frame not scrollable)
        self.help_panel = HelpPanel(self.main_frame)
        self.help_panel.grid(
            row=0, column=0, sticky="nsew", padx=SPACING_LG, pady=SPACING_LG
        )
        self.help_panel.grid_remove()  # Hide initially

    def _reset_scroll_position(self) -> None:
        """Reset scroll position to top."""
        def reset_scroll() -> None:
            """Reset scroll after widget update."""
            try:
                # CTkScrollableFrame uses _parent_canvas internally
                # Reset scroll position to top (0.0 = top, 1.0 = bottom)
                if hasattr(self.scrollable_frame, '_parent_canvas'):
                    canvas = self.scrollable_frame._parent_canvas
                    if canvas:
                        canvas.yview_moveto(0.0)
            except (AttributeError, Exception):
                pass
        
        # Update widget first, then reset scroll
        self.scrollable_frame.update_idletasks()
        # Use after to ensure scroll reset happens after layout update
        self.after(10, reset_scroll)

    def _show_home(self) -> None:
        """Show home view."""
        self.current_view = "home"
        self._update_nav_buttons(0)  # Home is index 0

        # Reset scroll position
        self._reset_scroll_position()

        # Hide other views, show main content
        self.settings_panel.grid_remove()
        self.changes_panel.grid_remove()
        self.help_panel.grid_remove()
        self.scrollable_frame.grid()
        self.file_selector.grid()
        self.results_panel.grid()
        self.format_controls.grid()
        self.apply_button.grid()

    def _show_settings(self) -> None:
        """Show settings view."""
        self.current_view = "settings"
        self._update_nav_buttons(2)  # Settings is index 2

        # Reset scroll position
        self._reset_scroll_position()

        # Hide other views, show settings
        self.scrollable_frame.grid_remove()
        self.changes_panel.grid_remove()
        self.help_panel.grid_remove()
        self.settings_panel.grid()

    def _show_changes(self) -> None:
        """Show changes view."""
        self.current_view = "changes"
        self._update_nav_buttons(1)  # Changes is index 1

        # Hide other views, show changes
        self.scrollable_frame.grid_remove()
        self.settings_panel.grid_remove()
        self.help_panel.grid_remove()
        self.changes_panel.grid()
        # Refresh history when showing
        self.changes_panel.refresh_history()

    def _show_help(self) -> None:
        """Show help view."""
        self.current_view = "help"
        self._update_nav_buttons(3)  # Help is index 3

        # Reset scroll position
        self._reset_scroll_position()

        # Hide other views, show help
        self.scrollable_frame.grid_remove()
        self.settings_panel.grid_remove()
        self.changes_panel.grid_remove()
        self.help_panel.grid()

    def _update_nav_buttons(self, active_index: int) -> None:
        """
        Update navigation buttons active state.

        Args:
            active_index: Index of active button
        """
        for idx, btn in enumerate(self.nav_buttons):
            is_active = idx == active_index
            btn.configure(
                fg_color=FLUENT_PRIMARY if is_active else "transparent",
                hover_color=FLUENT_SECONDARY if is_active else FLUENT_HOVER,
                text_color=FLUENT_TEXT_PRIMARY if not is_active else "white",
            )

    def _on_language_changed(self, language_code: str) -> None:
        """
        Handle language change.

        Args:
            language_code: New language code
        """
        # Update all UI texts
        self._refresh_ui_texts()

    def _refresh_ui_texts(self) -> None:
        """Refresh all UI texts after language change."""
        # Update window title
        self.title(get_text("app.title", "PDF Table Title Fixer"))

        # Update apply button
        self.apply_button.configure(
            text=get_text("button.apply", "Apply Modifications")
        )

        # Update sidebar help section
        self.help_title.configure(
            text=get_text("sidebar.need_help", "Need Help?")
        )
        self.help_text.configure(
            text=get_text(
                "sidebar.help_text",
                "View our documentation for guides and tutorials."
            )
        )

        # Update navigation buttons
        nav_texts = [
            get_text("sidebar.home", "Home"),
            get_text("sidebar.changes", "Changes"),
            get_text("sidebar.settings", "Settings"),
            get_text("sidebar.help", "Help"),
        ]
        icons = ["🏠", "🔄", "⚙️", "❓"]
        for idx, btn in enumerate(self.nav_buttons):
            btn.configure(text=f"{icons[idx]}  {nav_texts[idx]}")

        # Update all components
        self.file_selector.refresh_texts()
        self.results_panel.refresh_texts()
        self.format_controls.refresh_texts()
        self.changes_panel.refresh_texts()
        self.settings_panel.refresh_texts()
        self.help_panel.refresh_texts()

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
        # Hide main content and show loading panel
        self._show_loading()

        # Disable controls during analysis
        self.apply_button.configure(state="disabled")
        self.file_selector.browse_button.configure(state="disabled")

        def progress_callback(
            message: str, progress: Optional[float] = None
        ) -> None:
            """Update progress message and value in UI thread."""
            self.after(
                0, self.loading_panel.update_message, message, progress
            )

        def analyze_thread() -> None:
            try:
                result = self.rule.analyze(
                    str(file_path), progress_callback=progress_callback
                )
                self.after(0, self._on_analysis_complete, result)
            except Exception as e:
                self.after(0, self._on_analysis_error, str(e))

        thread = threading.Thread(target=analyze_thread, daemon=True)
        thread.start()

    def _show_loading(self) -> None:
        """Show loading panel and hide main content."""
        # Hide scrollable frame (main content)
        self.scrollable_frame.grid_remove()

        # Show loading panel (occupies full main_frame)
        self.loading_panel.show()

    def _hide_loading(self) -> None:
        """Hide loading panel and show main content."""
        # Hide loading panel
        self.loading_panel.hide()

        # Show scrollable frame (main content)
        self.scrollable_frame.grid()

    def _on_analysis_complete(self, result: AnalysisResult) -> None:
        """
        Handle analysis completion.

        Args:
            result: AnalysisResult object
        """
        # Hide loading and show main content
        self._hide_loading()

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
        # Hide loading and show main content
        self._hide_loading()

        messagebox.showerror(
            get_text("dialog.analysis_error", "Analysis Error"),
            get_text(
                "dialog.analysis_error.message",
                "Error analyzing PDF:\n{message}"
            ).format(message=error_message)
        )
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
        self.apply_button.configure(
            state="disabled",
            text=get_text("button.processing", "Processing...")
        )

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

                # Save to history if successful
                if success:
                    self._save_to_history(
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

    def _save_to_history(
        self,
        input_file: str,
        output_file: str,
        modifications: List,
        format_info: Optional[FormatInfo],
    ) -> None:
        """
        Save modification to history.

        Args:
            input_file: Input PDF path
            output_file: Output PDF path
            modifications: List of modifications applied
            format_info: Format information applied
        """
        try:
            # Convert format_info to dict
            format_dict = None
            if format_info:
                format_dict = {
                    "font_name": format_info.font_name,
                    "font_size": format_info.font_size,
                    "is_bold": format_info.is_bold,
                    "is_italic": format_info.is_italic,
                    "color": format_info.color,
                }

            # Convert modifications to list of dicts
            modifications_detail = []
            for mod in modifications:
                modifications_detail.append({
                    "page": mod.page,
                    "original_title": mod.original_title,
                    "modified_title": mod.modified_title,
                    "repetition_number": mod.repetition_number,
                    "total_repetitions": mod.total_repetitions,
                })

            # Create and save history entry
            history_entry = create_history_entry(
                input_file=input_file,
                output_file=output_file,
                tables_modified=len(modifications),
                format_applied=format_dict,
                modifications_detail=modifications_detail,
            )
            save_modification_history(history_entry)
        except Exception:
            pass  # Silently fail if history can't be saved

    def _on_modification_complete(self, success: bool) -> None:
        """
        Handle modification completion.

        Args:
            success: Whether modification was successful
        """
        self.apply_button.configure(
            state="normal",
            text=get_text("button.apply", "Apply Modifications")
        )

        if success:
            messagebox.showinfo(
                get_text("dialog.modification_success", "Success"),
                get_text(
                    "dialog.modification_success.message",
                    "PDF modifications applied successfully!"
                )
            )
            # Refresh changes panel if visible
            if self.current_view == "changes":
                self.changes_panel.refresh_history()
        else:
            messagebox.showwarning(
                get_text("dialog.modification_warning", "Warning"),
                get_text(
                    "dialog.modification_warning.message",
                    "Some modifications may not have been applied."
                )
            )

    def _on_modification_error(self, error_message: str) -> None:
        """
        Handle modification error.

        Args:
            error_message: Error message
        """
        self.apply_button.configure(
            state="normal",
            text=get_text("button.apply", "Apply Modifications")
        )
        messagebox.showerror(
            get_text("dialog.modification_error", "Modification Error"),
            get_text(
                "dialog.modification_error.message",
                "Error modifying PDF:\n{message}"
            ).format(message=error_message)
        )

