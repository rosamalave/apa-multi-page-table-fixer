"""Format detection and analysis module."""

from typing import List, Optional, TYPE_CHECKING, Any

import fitz  # PyMuPDF

from src.core.models import FormatInfo, TableInfo
from src.utils.constants import (
    DEFAULT_FONT_NAME,
    DEFAULT_FONT_SIZE,
    DEFAULT_COLOR,
)
from src.utils.exceptions import FormatDetectionError

if TYPE_CHECKING:
    from fitz import Page


class FormatAnalyzer:
    """Analyzes format information from PDF table titles."""

    def __init__(self) -> None:
        """Initialize the format analyzer."""
        self.format_info_cache: dict[int, FormatInfo] = {}

    def extract_format(
        self, pdf_path: str, table: TableInfo
    ) -> FormatInfo:
        """
        Extract format information for a table title.

        Args:
            pdf_path: Path to PDF file
            table: TableInfo object

        Returns:
            FormatInfo with detected format

        Raises:
            FormatDetectionError: If format cannot be detected
        """
        try:
            doc = fitz.open(pdf_path)
            page = doc[table.page - 1]  # 0-indexed

            # Method 1: Try to find text using search_for (more reliable)
            format_info = self._find_format_by_search(page, table)
            
            # Method 2: Fallback to text dictionary search
            if format_info.font_name == DEFAULT_FONT_NAME:
                text_dict = page.get_text("rawdict")
                format_info = self._find_table_format(
                    text_dict, table.full_title
                )

            doc.close()
            return format_info
        except Exception as e:
            raise FormatDetectionError(
                f"Error extracting format: {e}"
            ) from e

    def _find_format_by_search(
        self, page: Any, table: TableInfo  # fitz.Page
    ) -> FormatInfo:
        """
        Find format by searching for table title text on page.

        Args:
            page: PyMuPDF Page object
            table: TableInfo object

        Returns:
            FormatInfo object
        """
        import re
        
        # Try to find the table title on the page
        title = table.full_title
        instances = page.search_for(title)
        
        if not instances:
            # Try without period
            title_no_period = title.rstrip('.')
            instances = page.search_for(title_no_period)
        
        if not instances:
            # Try to find by table number
            match = re.search(r'(Cuadro|Tabla)\s+(\d+)', title, re.IGNORECASE)
            if match:
                table_type = match.group(1)
                table_num = match.group(2)
                base_title = f"{table_type} {table_num}"
                instances = page.search_for(base_title)
        
        if instances:
            # Get the rectangle where the text was found
            rect = instances[0]
            
            # Expand rectangle slightly to capture full text
            expanded_rect = fitz.Rect(
                rect.x0 - 5,
                rect.y0 - 2,
                rect.x1 + 5,
                rect.y1 + 2
            )
            
            # Get text in rawdict format for that area
            text_dict = page.get_text("rawdict", clip=expanded_rect)
            
            # Since we found the rectangle using search_for, we know this is the right area
            # Collect all spans with valid format info
            valid_spans = []
            for block in text_dict.get("blocks", []):
                if "lines" not in block:
                    continue
                for line in block["lines"]:
                    for span in line.get("spans", []):
                        font_name = span.get("font", "")
                        font_size = span.get("size", 0)
                        
                        # Only use spans with valid font info
                        if font_name and font_size > 0:
                            valid_spans.append(span)
            
            # Use the first valid span (usually the main format)
            if valid_spans:
                return self._create_format_info(valid_spans[0])
        
        # Return default if not found
        return FormatInfo(
            font_name=DEFAULT_FONT_NAME,
            font_size=DEFAULT_FONT_SIZE,
            is_bold=False,
            is_italic=False,
            color=DEFAULT_COLOR,
        )

    def _find_table_format(
        self, text_dict: dict, title: str
    ) -> FormatInfo:
        """
        Find format information in text dictionary.

        Args:
            text_dict: Raw text dictionary from PyMuPDF
            title: Table title to search for

        Returns:
            FormatInfo object
        """
        import re
        
        title_lower = title.lower()
        # Extract table number and type from title
        match = re.search(r'(cuadro|tabla)\s+(\d+)', title_lower)
        table_type = match.group(1) if match else None
        table_num = match.group(2) if match else None
        
        # Collect all spans that might contain the table title
        candidate_spans = []
        
        for block in text_dict.get("blocks", []):
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = ""
                line_spans = []
                
                # Collect all spans in the line
                for span in line.get("spans", []):
                    span_text = span.get("text", "")
                    line_text += span_text
                    line_spans.append(span)
                
                line_text_lower = line_text.lower()
                
                # Check if this line contains table title information
                if table_type and table_num:
                    # Look for "Cuadro X" or "Tabla X" pattern
                    pattern = f"{table_type}\\s+{table_num}"
                    if re.search(pattern, line_text_lower):
                        # Use the first span that contains the table type/number
                        for span in line_spans:
                            span_text_lower = span.get("text", "").lower()
                            if table_type in span_text_lower and table_num in span_text_lower:
                                candidate_spans.append(span)
                                break
                        # If no individual span matches, use first span of the line
                        if not candidate_spans and line_spans:
                            candidate_spans.append(line_spans[0])
                
                # Also check for full title match
                if title_lower in line_text_lower:
                    for span in line_spans:
                        span_text_lower = span.get("text", "").lower()
                        if any(term in span_text_lower for term in ["cuadro", "tabla"]):
                            candidate_spans.append(span)
        
        # Return format from first candidate span, or default
        if candidate_spans:
            return self._create_format_info(candidate_spans[0])
        
        # Return default if not found
        return FormatInfo(
            font_name=DEFAULT_FONT_NAME,
            font_size=DEFAULT_FONT_SIZE,
            is_bold=False,
            is_italic=False,
            color=DEFAULT_COLOR,
        )

    def _create_format_info(self, span: dict) -> FormatInfo:
        """
        Create FormatInfo from span dictionary.

        Args:
            span: Span dictionary from PyMuPDF

        Returns:
            FormatInfo object
        """
        font_name = span.get("font", DEFAULT_FONT_NAME)
        font_size = span.get("size", DEFAULT_FONT_SIZE)
        flags = span.get("flags", 0)

        # Check bold and italic flags
        is_bold = bool(flags & 16)  # Bit 4 indicates bold
        is_italic = bool(flags & 1)  # Bit 0 indicates italic

        # Extract color if available
        color = span.get("color", DEFAULT_COLOR)
        if isinstance(color, int):
            # Convert single int to RGB tuple
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            color = (r, g, b)

        # Normalize font name
        font_name = self._normalize_font_name(font_name)

        return FormatInfo(
            font_name=font_name,
            font_size=font_size,
            is_bold=is_bold,
            is_italic=is_italic,
            color=color,
        )

    def _normalize_font_name(self, font_name: str) -> str:
        """
        Normalize font name to common names.

        Args:
            font_name: Raw font name from PDF

        Returns:
            Normalized font name
        """
        font_lower = font_name.lower()
        
        # Map common font variations
        font_mapping = {
            "times": "Times New Roman",
            "times-roman": "Times New Roman",
            "timesnewroman": "Times New Roman",
            "timesnewromanps": "Times New Roman",
            "timesnewromanpsmt": "Times New Roman",
            "helvetica": "Helvetica",
            "helv": "Helvetica",
            "arial": "Arial",
            "arialmt": "Arial",
            "calibri": "Calibri",
            "calibrimt": "Calibri",
            "verdana": "Verdana",
        }
        
        # Check for partial matches
        for key, value in font_mapping.items():
            if key in font_lower:
                return value
        
        # Return original if no mapping found
        return font_name

    def check_uniformity(
        self, formats: List[FormatInfo]
    ) -> bool:
        """
        Check if all formats are uniform.

        Args:
            formats: List of FormatInfo objects

        Returns:
            True if all formats are the same
        """
        if not formats:
            return True

        first_format = formats[0]
        return all(f == first_format for f in formats)

    def get_common_format(
        self, formats: List[FormatInfo]
    ) -> Optional[FormatInfo]:
        """
        Get the most common format from a list.

        Args:
            formats: List of FormatInfo objects

        Returns:
            Most common FormatInfo or None if list is empty
        """
        if not formats:
            return None

        # Count occurrences of each format
        format_counts: dict[FormatInfo, int] = {}
        for fmt in formats:
            format_counts[fmt] = format_counts.get(fmt, 0) + 1

        # Return the most common format
        return max(format_counts.items(), key=lambda x: x[1])[0]

