"""Help panel component with dynamic content and icons."""

import customtkinter as ctk
from typing import Optional

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
    SPACING_XL,
    RADIUS_MD,
    RADIUS_LG,
)
from src.gui.themes.fonts import get_poppins_font
from src.utils.i18n import get_text


class HelpPanel(ctk.CTkFrame):
    """Help panel with dynamic content and icons."""

    def __init__(self, parent, **kwargs) -> None:
        """
        Initialize help panel component.

        Args:
            parent: Parent widget
            **kwargs: Additional frame arguments
        """
        # Set default card style with rounded corners and border
        kwargs.setdefault("fg_color", FLUENT_SURFACE)
        kwargs.setdefault("corner_radius", RADIUS_LG)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", FLUENT_BORDER)
        super().__init__(parent, **kwargs)

        # Create scrollable frame for content
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=SPACING_LG, pady=SPACING_LG)

        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create and layout widgets."""
        # Title section
        self._create_title_section()

        # Quick start section
        self._create_quick_start_section()

        # Features section
        self._create_features_section()

        # Format options section
        self._create_format_options_section()

        # Troubleshooting section
        self._create_troubleshooting_section()

        # Tips section
        self._create_tips_section()

    def _create_title_section(self) -> None:
        """Create title section with icon."""
        title_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(SPACING_LG, SPACING_MD), padx=SPACING_LG)

        # Icon
        icon_label = ctk.CTkLabel(
            title_frame,
            text="❓",
            font=get_poppins_font(size=24),
        )
        icon_label.pack(side="left", padx=(0, SPACING_MD))

        # Title
        self.title_label = ctk.CTkLabel(
            title_frame,
            text=get_text("help.title", "Help & Documentation"),
            font=get_poppins_font(size=20, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        self.title_label.pack(side="left")

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.scrollable_frame,
            text=get_text(
                "help.subtitle",
                "Learn how to use the PDF Table Title Fixer"
            ),
            font=get_poppins_font(size=12),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        self.subtitle_label.pack(
            pady=(0, SPACING_XL), padx=0, anchor="w"
        )

    def _create_quick_start_section(self) -> None:
        """Create quick start guide section."""
        section_card = self._create_section_card(
            "🚀",
            get_text("help.quick_start.title", "Quick Start Guide"),
            get_text(
                "help.quick_start.subtitle",
                "Get started in 3 simple steps"
            ),
        )

        steps = [
            (
                "1️⃣",
                get_text("help.quick_start.step1.title", "Select Your PDF"),
                get_text(
                    "help.quick_start.step1.desc",
                    "Click 'Browse Files' or drag and drop your PDF "
                    "document into the upload area."
                ),
            ),
            (
                "2️⃣",
                get_text("help.quick_start.step2.title", "Review Analysis"),
                get_text(
                    "help.quick_start.step2.desc",
                    "The application will automatically detect all table "
                    "titles and identify which ones need modification."
                ),
            ),
            (
                "3️⃣",
                get_text("help.quick_start.step3.title", "Apply Changes"),
                get_text(
                    "help.quick_start.step3.desc",
                    "Choose your formatting preferences and click "
                    "'Apply Modifications' to save the corrected PDF."
                ),
            ),
        ]

        for icon, title, desc in steps:
            self._create_info_item(section_card, icon, title, desc)

    def _create_features_section(self) -> None:
        """Create features section."""
        section_card = self._create_section_card(
            "✨",
            get_text("help.features.title", "Key Features"),
            get_text(
                "help.features.subtitle",
                "What makes this tool special"
            ),
        )

        features = [
            (
                "🔍",
                get_text("help.features.auto_detect.title", "Automatic Detection"),
                get_text(
                    "help.features.auto_detect.desc",
                    "Automatically finds all table titles in your PDF "
                    "document, even across multiple pages."
                ),
            ),
            (
                "📊",
                get_text("help.features.apa_compliant.title", "APA Compliant"),
                get_text(
                    "help.features.apa_compliant.desc",
                    "Ensures your table titles follow APA 7th edition "
                    "formatting standards for multi-page tables."
                ),
            ),
            (
                "🎨",
                get_text("help.features.format_preserve.title", "Format Preservation"),
                get_text(
                    "help.features.format_preserve.desc",
                    "Option to keep original formatting or customize "
                    "font, size, bold, and italic styles."
                ),
            ),
            (
                "⚡",
                get_text("help.features.fast.title", "Fast Processing"),
                get_text(
                    "help.features.fast.desc",
                    "Quick analysis and modification of large PDF "
                    "documents with multiple tables."
                ),
            ),
        ]

        for icon, title, desc in features:
            self._create_info_item(section_card, icon, title, desc)

    def _create_format_options_section(self) -> None:
        """Create format options explanation section."""
        section_card = self._create_section_card(
            "🎨",
            get_text("help.format_options.title", "Format Options"),
            get_text(
                "help.format_options.subtitle",
                "Understanding formatting controls"
            ),
        )

        format_items = [
            (
                "✅",
                get_text(
                    "help.format_options.keep_original.title",
                    "Keep Original Format"
                ),
                get_text(
                    "help.format_options.keep_original.desc",
                    "When enabled, preserves the exact formatting "
                    "(font, size, style) of the original table titles. "
                    "This option is only available when all detected "
                    "tables have uniform formatting."
                ),
            ),
            (
                "🔤",
                get_text("help.format_options.font.title", "Font Family"),
                get_text(
                    "help.format_options.font.desc",
                    "Choose from common academic fonts: Times New "
                    "Roman, Arial, Calibri, Helvetica, Verdana, or "
                    "Courier New."
                ),
            ),
            (
                "📏",
                get_text("help.format_options.size.title", "Font Size"),
                get_text(
                    "help.format_options.size.desc",
                    "Select the font size in points (pt). Common sizes "
                    "for academic documents are 10, 11, or 12 pt."
                ),
            ),
            (
                "💪",
                get_text("help.format_options.bold.title", "Bold & Italic"),
                get_text(
                    "help.format_options.bold.desc",
                    "Toggle bold and italic styles for table titles. "
                    "These options work independently and can be combined."
                ),
            ),
        ]

        for icon, title, desc in format_items:
            self._create_info_item(section_card, icon, title, desc)

    def _create_troubleshooting_section(self) -> None:
        """Create troubleshooting section."""
        section_card = self._create_section_card(
            "🔧",
            get_text("help.troubleshooting.title", "Troubleshooting"),
            get_text(
                "help.troubleshooting.subtitle",
                "Common issues and solutions"
            ),
        )

        issues = [
            (
                "❌",
                get_text(
                    "help.troubleshooting.no_tables.title",
                    "No Tables Detected"
                ),
                get_text(
                    "help.troubleshooting.no_tables.desc",
                    "Ensure your PDF contains tables with titles in the "
                    "format 'Table X' or 'Cuadro X' followed by a "
                    "description. The titles must be on separate lines."
                ),
            ),
            (
                "⚠️",
                get_text(
                    "help.troubleshooting.format_not_detected.title",
                    "Format Not Detected"
                ),
                get_text(
                    "help.troubleshooting.format_not_detected.desc",
                    "If format detection fails, you can still customize "
                    "the formatting manually using the format options. "
                    "The 'Keep original format' checkbox will be disabled."
                ),
            ),
            (
                "📄",
                get_text(
                    "help.troubleshooting.large_file.title",
                    "Large File Processing"
                ),
                get_text(
                    "help.troubleshooting.large_file.desc",
                    "For very large PDFs (50MB+), processing may take "
                    "longer. The application will show progress updates "
                    "during analysis."
                ),
            ),
            (
                "💾",
                get_text(
                    "help.troubleshooting.save_issues.title",
                    "Save File Issues"
                ),
                get_text(
                    "help.troubleshooting.save_issues.desc",
                    "Make sure you have write permissions in the output "
                    "directory. The application will create a new file "
                    "with '_fixed' suffix."
                ),
            ),
        ]

        for icon, title, desc in issues:
            self._create_info_item(section_card, icon, title, desc)

    def _create_tips_section(self) -> None:
        """Create tips and best practices section."""
        section_card = self._create_section_card(
            "💡",
            get_text("help.tips.title", "Tips & Best Practices"),
            get_text(
                "help.tips.subtitle",
                "Get the most out of the application"
            ),
        )

        tips = [
            (
                "📝",
                get_text("help.tips.backup.title", "Always Backup"),
                get_text(
                    "help.tips.backup.desc",
                    "Keep a backup of your original PDF before applying "
                    "modifications. The application creates a new file, "
                    "but it's good practice to have backups."
                ),
            ),
            (
                "👀",
                get_text("help.tips.review.title", "Review Before Applying"),
                get_text(
                    "help.tips.review.desc",
                    "Check the analysis results and preview the format "
                    "before clicking 'Apply Modifications' to ensure "
                    "everything looks correct."
                ),
            ),
            (
                "📚",
                get_text("help.tips.apa_guide.title", "APA Guidelines"),
                get_text(
                    "help.tips.apa_guide.desc",
                    "For multi-page tables, APA 7th edition requires "
                    "titles to include page numbering: 'Table X. Title "
                    "(1/3)', 'Table X. Title (2/3)', etc."
                ),
            ),
            (
                "🔄",
                get_text("help.tips.history.title", "Track Changes"),
                get_text(
                    "help.tips.history.desc",
                    "Use the 'Changes' section to view a history of "
                    "all modifications made to your documents, including "
                    "details about what was changed."
                ),
            ),
        ]

        for icon, title, desc in tips:
            self._create_info_item(section_card, icon, title, desc)

    def _create_section_card(
        self, icon: str, title: str, subtitle: str
    ) -> ctk.CTkFrame:
        """
        Create a section card with title and subtitle.

        Args:
            icon: Icon emoji
            title: Section title
            subtitle: Section subtitle

        Returns:
            Frame container for section content
        """
        card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=FLUENT_SURFACE,
            corner_radius=RADIUS_MD,
            border_width=1,
            border_color=FLUENT_BORDER,
        )
        card.pack(
            fill="x", padx=0, pady=(0, SPACING_LG)
        )

        # Title frame
        title_frame = ctk.CTkFrame(card, fg_color="transparent")
        title_frame.pack(
            fill="x", pady=(SPACING_MD, SPACING_SM), padx=SPACING_MD
        )

        # Icon
        icon_label = ctk.CTkLabel(
            title_frame,
            text=icon,
            font=get_poppins_font(size=20),
        )
        icon_label.pack(side="left", padx=(0, SPACING_MD))

        # Title
        title_label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=get_poppins_font(size=16, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
        )
        title_label.pack(side="left")

        # Subtitle
        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
        )
        subtitle_label.pack(
            anchor="w", padx=SPACING_MD, pady=(0, SPACING_MD)
        )

        return card

    def _create_info_item(
        self, parent: ctk.CTkFrame, icon: str, title: str, description: str
    ) -> None:
        """
        Create an info item with icon, title, and description.

        Args:
            parent: Parent frame (the section card)
            icon: Icon emoji
            title: Item title
            description: Item description
        """
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(
            fill="x", padx=SPACING_MD, pady=(0, SPACING_MD)
        )

        # Icon
        icon_label = ctk.CTkLabel(
            item_frame,
            text=icon,
            font=get_poppins_font(size=18),
            width=30,
        )
        icon_label.pack(side="left", padx=(0, SPACING_MD), anchor="n")

        # Content frame
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=get_poppins_font(size=13, weight="bold"),
            text_color=FLUENT_TEXT_PRIMARY,
            anchor="w",
        )
        title_label.pack(anchor="w", pady=(0, SPACING_SM))

        # Description - use CTkTextbox for native text wrapping support
        # CTkTextbox has built-in wrap support and is perfect for long text
        desc_textbox = ctk.CTkTextbox(
            content_frame,
            height=1,  # Start with minimal height, will adjust
            wrap="word",  # Wrap at word boundaries
            fg_color="transparent",
            border_width=0,
            font=get_poppins_font(size=11),
            text_color=FLUENT_TEXT_SECONDARY,
            activate_scrollbars=False,  # CRITICAL: Disable scrollbars
        )
        desc_textbox.pack(anchor="w", fill="x", expand=False)
        
        # Insert text
        desc_textbox.insert("0.0", description)
        
        # Make it read-only (like a label)
        desc_textbox.configure(state="disabled")
        
        # Calculate and set appropriate height to show all content
        def adjust_height() -> None:
            """Adjust textbox height to fit all content without scrollbar."""
            try:
                # Force update to get accurate measurements
                content_frame.update_idletasks()
                item_frame.update_idletasks()
                parent.update_idletasks()
                desc_textbox.update_idletasks()
                
                # Get the actual number of lines after wrapping
                # end-1c gives us the last position (line.column format)
                end_index = desc_textbox.index("end-1c")
                line_count = int(end_index.split(".")[0])
                
                # Use dlineinfo to get actual pixel height of content
                # This is more accurate than estimating
                try:
                    # Get bounding box of last line
                    bbox = desc_textbox.dlineinfo(f"{line_count}.0")
                    if bbox:
                        # bbox format: (x, y, width, height, baseline)
                        # y is top of line, height is line height
                        last_line_y = bbox[1]
                        last_line_height = bbox[3]
                        # Total content height = y position of last line + its height
                        content_pixel_height = last_line_y + last_line_height
                        
                        # Add padding for textbox borders and spacing
                        padding = 14  # Balanced padding - enough to prevent cutting
                        final_height = int(content_pixel_height) + padding
                    else:
                        # Fallback: estimate based on line count
                        line_height = 19  # Balanced line height
                        padding = 14
                        final_height = (line_count * line_height) + padding
                except Exception:
                    # Fallback: estimate based on line count
                    line_height = 19  # Balanced line height
                    padding = 14
                    final_height = (line_count * line_height) + padding
                
                # Ensure minimum height
                min_height = 28
                final_height = max(final_height, min_height)
                
                # Add small margin to ensure no cutting
                final_height = int(final_height * 1.08)  # 8% extra margin
                
                # Configure height to show all content
                desc_textbox.configure(height=final_height)
                
                # Force update to ensure layout is correct
                desc_textbox.update_idletasks()
                
                # Verify: check if content is fully visible
                try:
                    # Get the last visible line
                    visible_end = desc_textbox.index("@0,{}".format(desc_textbox.winfo_height()))
                    actual_end = desc_textbox.index("end-1c")
                    if visible_end < actual_end:
                        # Content is cut off, increase height
                        current_height = desc_textbox.winfo_height()
                        desc_textbox.configure(height=int(current_height * 1.3))
                except Exception:
                    pass
            except Exception:
                pass  # Silently fail if adjustment fails
        
        # Adjust height multiple times to ensure it works
        # Start after a short delay to let textbox render first
        item_frame.after(50, adjust_height)
        item_frame.after(150, adjust_height)
        item_frame.after(300, adjust_height)
        item_frame.after(500, adjust_height)
        
        # Also adjust on resize
        def on_configure(event) -> None:
            """Handle resize to recalculate height."""
            if event.widget == content_frame or event.widget == parent:
                adjust_height()
        
        content_frame.bind("<Configure>", on_configure)
        parent.bind("<Configure>", on_configure)

    def refresh_texts(self) -> None:
        """Refresh all texts after language change."""
        # Recreate all widgets in scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self._create_widgets()

