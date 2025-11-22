"""PDF modification module for applying table title changes."""

import os
import re
from typing import List, Optional, TYPE_CHECKING, Any, Dict

import fitz  # PyMuPDF

from src.core.models import Modification, FormatInfo
from src.utils.constants import DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE
from src.utils.exceptions import ModificationError

if TYPE_CHECKING:
    from fitz import Document, Page, Rect, Font


class PDFModifier:
    """Modifies PDF files to apply table title changes."""

    def __init__(self) -> None:
        """Initialize the modifier."""
        self.applied_count = 0
        self.font_cache: Dict[str, str] = {}  # Cache: key -> fontname registered

    def apply_modifications(
        self,
        pdf_path: str,
        output_path: str,
        modifications: List[Modification],
        custom_format: Optional[FormatInfo] = None,
    ) -> int:
        """
        Apply modifications to PDF file.

        Args:
            pdf_path: Input PDF path
            output_path: Output PDF path
            modifications: List of modifications to apply
            custom_format: Optional custom format to apply

        Returns:
            Number of modifications applied

        Raises:
            ModificationError: If modification fails
        """
        self.applied_count = 0

        try:
            doc = fitz.open(pdf_path)
            
            for mod in modifications:
                if not mod.needs_modification():
                    continue

                self._apply_single_modification(
                    doc, mod, custom_format
                )

            doc.save(output_path)
            doc.close()

            return self.applied_count
        except Exception as e:
            raise ModificationError(
                f"Error modifying PDF: {e}"
            ) from e

    def _apply_single_modification(
        self,
        doc: Any,  # fitz.Document
        mod: Modification,
        custom_format: Optional[FormatInfo],
    ) -> None:
        """
        Apply a single modification to the PDF.

        Args:
            doc: PyMuPDF Document object
            mod: Modification to apply
            custom_format: Optional custom format
        """
        page_num = mod.page - 1  # 0-indexed
        if page_num >= len(doc):
            return

        page = doc[page_num]

        # Find title location
        rect = self._find_title_rect(page, mod.original_title)
        if not rect:
            return

        # Get format to use
        format_info = custom_format or mod.format_info
        if not format_info:
            format_info = FormatInfo(
                font_name=DEFAULT_FONT_NAME,
                font_size=DEFAULT_FONT_SIZE,
                is_bold=False,
                is_italic=False,
            )
        
        # Apply modification (font will be loaded AFTER redaction)
        self._replace_text(
            page, rect, mod.modified_title, format_info
        )
        self.applied_count += 1

    def _find_title_rect(
        self, page: Any, title: str  # fitz.Page
    ) -> Optional[Any]:  # fitz.Rect
        """
        Find rectangle containing the title text.

        Args:
            page: PyMuPDF Page object
            title: Title text to find

        Returns:
            Rectangle if found, None otherwise
        """
        # Try exact match first
        instances = page.search_for(title)
        if instances:
            return instances[0]

        # Try with period if title doesn't have one
        if '.' not in title.split(' ', 2)[1] if len(title.split(' ')) > 1 else False:
            title_with_period = re.sub(
                r'(Cuadro|Tabla)\s+(\d+)\s+',
                r'\1 \2. ',
                title,
                flags=re.IGNORECASE
            )
            instances = page.search_for(title_with_period)
            if instances:
                return instances[0]
        
        # Try without period if title has one
        title_no_period = re.sub(
            r'(Cuadro|Tabla)\s+(\d+)\.\s+',
            r'\1 \2 ',
            title,
            flags=re.IGNORECASE
        )
        if title_no_period != title:
            instances = page.search_for(title_no_period)
            if instances:
                return instances[0]

        # Try to find by table number (with flexible period/space)
        match = re.search(
            r'(Cuadro|Tabla)\s+(\d+)', title, re.IGNORECASE
        )
        if match:
            table_type = match.group(1).capitalize()
            table_num = match.group(2)
            
            # Try both formats: with and without period
            for base_title in [
                f"{table_type} {table_num}.",
                f"{table_type} {table_num}",
            ]:
                base_instances = page.search_for(base_title)
                if base_instances:
                    # Expand rectangle to include full title
                    base_rect = base_instances[0]
                    x0, y0, x1, y1 = base_rect
                    expanded = fitz.Rect(x0, y0 - 2, x1 + 300, y1 + 2)  # type: ignore

                    # Check if full title is in expanded area
                    area_text = page.get_text("text", clip=expanded)
                    title_normalized = re.sub(r'\s+', ' ', title)
                    area_normalized = re.sub(r'\s+', ' ', area_text)

                    if title_normalized.lower() in area_normalized.lower():
                        return expanded

        return None

    def _replace_text(
        self,
        page: Any,  # fitz.Page
        rect: Any,  # fitz.Rect
        new_text: str,
        format_info: FormatInfo,
    ) -> None:
        """
        Replace text in rectangle with new text.

        Args:
            page: PyMuPDF Page object
            rect: Rectangle to replace
            new_text: New text to insert
            format_info: Format information
        """
        # Remove old text FIRST
        # This is important: redaction clears font registrations
        page.add_redact_annot(rect)
        page.apply_redactions()

        # Load font AFTER redaction (redaction clears font registrations)
        self._load_font_if_needed(page, format_info)
        
        # Get font name to use (may be loaded font or base font)
        font_name = self._get_font_name(format_info)

        # Calculate insertion point
        x0, y0, x1, y1 = rect
        insert_point = fitz.Point(x0, y0 + (y1 - y0) * 0.75)
        
        # Insert new text
        try:
            page.insert_text(
                insert_point,
                new_text,
                fontsize=format_info.font_size,
                fontname=font_name,
                color=format_info.color,
            )
        except Exception:
            # Fallback to default font
            page.insert_text(
                insert_point,
                new_text,
                fontsize=format_info.font_size,
                fontname=DEFAULT_FONT_NAME,
                color=format_info.color,
            )

    def _get_font_name(self, format_info: FormatInfo) -> str:
        """
        Get font name to use for insert_text.

        Args:
            format_info: Format information

        Returns:
            Font name string (registered fontname or base font)
        """
        font_name_lower = format_info.font_name.lower()
        
        # Create cache key that includes bold/italic state
        cache_key = f"{font_name_lower}_{format_info.is_bold}_{format_info.is_italic}"
        
        # Check if font was loaded (in cache) - this is the preferred method
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        # Use base font mapping as fallback
        font_map = {
            "times": "tiro",
            "times new roman": "tiro",
            "arial": "helv",
            "helvetica": "helv",
            "courier": "cour",
            "courier new": "cour",
        }

        for key, value in font_map.items():
            if key in font_name_lower:
                return value

        return DEFAULT_FONT_NAME

    def _load_font_if_needed(
        self, page: Any, format_info: FormatInfo  # fitz.Page
    ) -> None:
        """
        Load font from system if needed.

        Args:
            page: PyMuPDF Page object
            format_info: Format information
        """
        font_name_lower = format_info.font_name.lower()
        
        # Create cache key that includes bold/italic state
        cache_key = f"{font_name_lower}_{format_info.is_bold}_{format_info.is_italic}"
        
        # Note: We always register the font because apply_redactions() 
        # clears font registrations. The cache helps us know which 
        # font file to load, but we must register it on the page.
        
        # Map font names to Windows font file names
        font_file_map = {
            "times new roman": {
                "normal": "times.ttf",
                "bold": "timesbd.ttf",
                "italic": "timesi.ttf",
                "bold_italic": "timesbi.ttf",
            },
            "arial": {
                "normal": "arial.ttf",
                "bold": "arialbd.ttf",
                "italic": "ariali.ttf",
                "bold_italic": "arialbi.ttf",
            },
            "calibri": {
                "normal": "calibri.ttf",
                "bold": "calibrib.ttf",
                "italic": "calibrii.ttf",
                "bold_italic": "calibriz.ttf",
            },
            "helvetica": {
                "normal": "arial.ttf",  # Helvetica maps to Arial on Windows
                "bold": "arialbd.ttf",
                "italic": "ariali.ttf",
                "bold_italic": "arialbi.ttf",
            },
            "verdana": {
                "normal": "verdana.ttf",
                "bold": "verdanab.ttf",
                "italic": "verdanai.ttf",
                "bold_italic": "verdanaz.ttf",
            },
        }
        
        # Determine font variant based on bold/italic
        if format_info.is_bold and format_info.is_italic:
            variant = "bold_italic"
        elif format_info.is_bold:
            variant = "bold"
        elif format_info.is_italic:
            variant = "italic"
        else:
            variant = "normal"
        
        # Try to find and load font
        font_paths = [
            r"C:\Windows\Fonts",
            r"C:\WINNT\Fonts",
        ]
        
        # Find matching font in map
        font_files = None
        for font_key in font_file_map:
            if font_key in font_name_lower:
                font_files = font_file_map[font_key]
                break
        
        if not font_files:
            return  # Font not in map, will use base font
        
        font_file = font_files.get(variant, font_files["normal"])
        
        # Try to load font from system
        for font_path in font_paths:
            full_path = os.path.join(font_path, font_file)
            if os.path.exists(full_path):
                try:
                    # Create unique font name for this variant
                    # Replace spaces with hyphens (PyMuPDF doesn't allow spaces in fontname)
                    font_name_safe = font_name_lower.replace(" ", "-")
                    font_variant_name = f"{font_name_safe}-{variant}"
                    # Register font on the page
                    # Note: We always register because apply_redactions() clears fonts
                    page.insert_font(fontname=font_variant_name, fontfile=full_path)
                    # Cache the fontname and file path for future use
                    self.font_cache[cache_key] = font_variant_name
                    return
                except Exception:
                    # Continue to next path if this one fails
                    continue
        
        # If font file not found, try normal variant
        if variant != "normal":
            font_file = font_files["normal"]
            for font_path in font_paths:
                full_path = os.path.join(font_path, font_file)
                if os.path.exists(full_path):
                    try:
                        # Replace spaces with hyphens (PyMuPDF doesn't allow spaces)
                        font_name_safe = font_name_lower.replace(" ", "-")
                        font_variant_name = f"{font_name_safe}-normal"
                        page.insert_font(fontname=font_variant_name, fontfile=full_path)
                        self.font_cache[cache_key] = font_variant_name
                        return
                    except Exception:
                        continue

