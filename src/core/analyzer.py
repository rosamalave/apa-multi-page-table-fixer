"""PDF analysis module for detecting table titles."""

import re
from collections import defaultdict
from typing import List, Tuple, Optional, TYPE_CHECKING

import pdfplumber

from src.core.models import TableInfo
from src.utils.constants import TABLE_TITLE_PATTERN
from src.utils.exceptions import PDFReadError

if TYPE_CHECKING:
    from pdfplumber.page import Page


class PDFAnalyzer:
    """Analyzes PDF files to detect table titles."""

    def __init__(self) -> None:
        """Initialize the analyzer."""
        self.tables: List[TableInfo] = []

    def analyze(self, pdf_path: str) -> List[TableInfo]:
        """
        Analyze PDF and detect all table titles.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of detected TableInfo objects

        Raises:
            PDFReadError: If PDF cannot be read
        """
        self.tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    self._analyze_page(page, page_num)
        except Exception as e:
            raise PDFReadError(f"Error reading PDF: {e}") from e

        return self.tables

    def _analyze_page(
        self, page: "Page", page_num: int
    ) -> None:
        """
        Analyze a single page for table titles.

        Args:
            page: pdfplumber Page object
            page_num: Page number (1-indexed)
        """
        text = page.extract_text()
        if not text:
            return

        matches = TABLE_TITLE_PATTERN.finditer(text)
        for match in matches:
            table_info = self._create_table_info(match, page_num)
            self.tables.append(table_info)

    def _create_table_info(
        self, match: re.Match, page_num: int
    ) -> TableInfo:
        """
        Create TableInfo from regex match.

        Args:
            match: Regex match object
            page_num: Page number

        Returns:
            TableInfo object
        """
        table_type = match.group(1)
        number = match.group(2)
        description = match.group(3).strip()
        description = re.sub(r'\s+', ' ', description)
        table_type_cap = table_type.capitalize()
        
        # Preserve original format: check if original had a period
        # The regex pattern uses (?:\.|\s+) which matches either period or space
        # We need to check the actual matched text to see which one was used
        matched_text = match.group(0)
        # Find the position of the number in the matched text
        number_pos = matched_text.find(str(number))
        if number_pos != -1:
            # Get the character(s) immediately after the number
            after_number_start = number_pos + len(str(number))
            if after_number_start < len(matched_text):
                after_number = matched_text[after_number_start:after_number_start + 2]
                # Check if there's a period immediately after the number
                has_period = after_number.strip().startswith('.')
            else:
                has_period = False
        else:
            has_period = False
        
        if has_period:
            full_title = f"{table_type_cap} {number}. {description}"
        else:
            full_title = f"{table_type_cap} {number} {description}"

        return TableInfo(
            page=page_num,
            number=number,
            description=description,
            full_title=full_title,
            position=match.start(),
            table_type=table_type_cap,
        )

    def find_consecutive_repetitions(
        self, tables: List[TableInfo]
    ) -> List[Tuple[TableInfo, int]]:
        """
        Find tables that repeat consecutively across pages.

        Args:
            tables: List of TableInfo objects

        Returns:
            List of tuples (TableInfo, repetition_count)
        """
        repetitions = []
        i = 0

        while i < len(tables):
            current = tables[i]
            count = 1
            j = i + 1

            while (
                j < len(tables)
                and tables[j].full_title == current.full_title
                and tables[j].page == current.page + count
            ):
                count += 1
                j += 1

            repetitions.append((current, count))
            i += count

        return repetitions

    def group_by_number(
        self, tables: List[TableInfo]
    ) -> dict[str, List[TableInfo]]:
        """
        Group tables by their number.

        Args:
            tables: List of TableInfo objects

        Returns:
            Dictionary mapping table numbers to lists of TableInfo
        """
        grouped = defaultdict(list)
        for table in tables:
            grouped[table.number].append(table)
        return dict(grouped)

