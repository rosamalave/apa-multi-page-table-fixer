"""APA rule for table title numbering across pages."""

from typing import List, Optional, Callable, Union

from src.core.analyzer import PDFAnalyzer
from src.core.formatter import FormatAnalyzer
from src.core.modifier import PDFModifier
from src.core.models import (
    AnalysisResult,
    Modification,
    TableInfo,
    FormatInfo,
)
from src.rules.base_rule import BaseRule


class TableTitleRule(BaseRule):
    """Rule for fixing table titles that span multiple pages."""

    def __init__(self) -> None:
        """Initialize the table title rule."""
        super().__init__(
            name="Table Title Numbering",
            description=(
                "Adds page numbering to table titles that "
                "repeat across consecutive pages (e.g., "
                "Table 1. Title (1/3), Table 1. Title (2/3))"
            ),
        )
        self.analyzer = PDFAnalyzer()
        self.format_analyzer = FormatAnalyzer()
        self.modifier = PDFModifier()

    def analyze(
        self,
        pdf_path: str,
        progress_callback: Optional[
            Callable[[str, Optional[float]], None]
        ] = None,
    ) -> AnalysisResult:
        """
        Analyze PDF for table title issues.

        Args:
            pdf_path: Path to PDF file
            progress_callback: Optional callback for progress updates
                (message: str, progress: Optional[float])

        Returns:
            AnalysisResult with detected issues
        """
        if progress_callback:
            progress_callback("Reading PDF document...", 10)

        # Detect all tables
        tables = self.analyzer.analyze(pdf_path)

        if progress_callback:
            progress_callback(
                f"Found {len(tables)} table(s). Analyzing repetitions...",
                30,
            )

        # Find consecutive repetitions
        repetitions = self.analyzer.find_consecutive_repetitions(tables)

        if progress_callback:
            progress_callback("Creating modifications...", 50)

        # Create modifications
        modifications = self._create_modifications(
            tables, repetitions, pdf_path, progress_callback
        )

        if progress_callback:
            progress_callback("Extracting format information...", 80)

        # Extract format information
        format_info = self._extract_format_info(tables, pdf_path)

        if progress_callback:
            progress_callback("Checking format uniformity...", 90)

        # Check uniformity (this can be slow, so we'll optimize it)
        format_uniform = self._check_format_uniformity(
            tables, pdf_path, progress_callback
        )

        if progress_callback:
            progress_callback("Analysis complete!", 100)

        return AnalysisResult(
            all_tables=tables,
            modifications=modifications,
            format_uniform=format_uniform,
            format_info=format_info,
        )

    def _create_modifications(
        self,
        tables: List[TableInfo],
        repetitions: List[tuple[TableInfo, int]],
        pdf_path: str,
        progress_callback: Optional[
            Callable[[str, Optional[float]], None]
        ] = None,
    ) -> List[Modification]:
        """
        Create modifications from detected repetitions.

        Args:
            tables: All detected tables
            repetitions: List of (table, count) tuples
            pdf_path: Path to PDF for format extraction
            progress_callback: Optional callback for progress updates

        Returns:
            List of Modification objects
        """
        modifications = []
        table_index = 0
        total_repetitions = len(repetitions)

        for rep_idx, (table, count) in enumerate(repetitions):
            if progress_callback and rep_idx % 5 == 0:
                # Calculate progress between 50% and 80%
                progress = 50 + (rep_idx / total_repetitions) * 30
                progress_callback(
                    f"Processing table {rep_idx + 1}/{total_repetitions}...",
                    progress,
                )
            if count > 1:
                # Need to add numbering
                for i in range(count):
                    current_table = tables[table_index + i]
                    format_info = self.format_analyzer.extract_format(
                        pdf_path, current_table
                    )

                    modified_title = (
                        f"{current_table.full_title} "
                        f"({i + 1}/{count})"
                    )

                    mod = Modification(
                        page=current_table.page,
                        original_title=current_table.full_title,
                        modified_title=modified_title,
                        repetition_number=i + 1,
                        total_repetitions=count,
                        format_info=format_info,
                    )
                    modifications.append(mod)
            else:
                # No modification needed
                format_info = self.format_analyzer.extract_format(
                    pdf_path, table
                )

                mod = Modification(
                    page=table.page,
                    original_title=table.full_title,
                    modified_title=table.full_title,
                    repetition_number=None,
                    total_repetitions=1,
                    format_info=format_info,
                )
                modifications.append(mod)

            table_index += count

        return modifications

    def _extract_format_info(
        self, tables: List[TableInfo], pdf_path: str
    ) -> Optional[FormatInfo]:
        """
        Extract common format information from tables.

        Args:
            tables: List of tables
            pdf_path: Path to PDF

        Returns:
            Common FormatInfo or None
        """
        if not tables:
            return None

        formats = [
            self.format_analyzer.extract_format(pdf_path, table)
            for table in tables[:10]  # Sample first 10
        ]

        return self.format_analyzer.get_common_format(formats)

    def _check_format_uniformity(
        self,
        tables: List[TableInfo],
        pdf_path: str,
        progress_callback: Optional[
            Callable[[str, Optional[float]], None]
        ] = None,
    ) -> bool:
        """
        Check if all table formats are uniform.

        Args:
            tables: List of tables
            pdf_path: Path to PDF
            progress_callback: Optional callback for progress updates

        Returns:
            True if formats are uniform
        """
        if not tables:
            return True

        # Optimize: sample tables instead of checking all
        # For large documents, checking all tables can be very slow
        sample_size = min(20, len(tables))  # Check up to 20 tables
        tables_to_check = tables[:sample_size]

        formats = []
        for idx, table in enumerate(tables_to_check):
            formats.append(
                self.format_analyzer.extract_format(pdf_path, table)
            )
            # Update progress if callback provided
            if progress_callback and idx % 5 == 0:
                progress = 90 + int((idx / sample_size) * 10)
                progress_callback(
                    f"Checking format uniformity... ({idx + 1}/{sample_size})",
                    progress,
                )

        return self.format_analyzer.check_uniformity(formats)

    def apply(
        self,
        pdf_path: str,
        output_path: str,
        modifications: List[Modification],
    ) -> bool:
        """
        Apply modifications to PDF.

        Args:
            pdf_path: Input PDF path
            output_path: Output PDF path
            modifications: List of modifications

        Returns:
            True if successful
        """
        return self.apply_with_format(pdf_path, output_path, modifications)

    def apply_with_format(
        self,
        pdf_path: str,
        output_path: str,
        modifications: List[Modification],
        custom_format: Optional[FormatInfo] = None,
    ) -> bool:
        """
        Apply modifications with custom format.

        Args:
            pdf_path: Input PDF path
            output_path: Output PDF path
            modifications: List of modifications
            custom_format: Optional custom format

        Returns:
            True if successful
        """
        try:
            count = self.modifier.apply_modifications(
                pdf_path, output_path, modifications, custom_format
            )
            return count > 0
        except Exception:
            return False

    def validate(self, modification: Modification) -> bool:
        """
        Validate a modification.

        Args:
            modification: Modification to validate

        Returns:
            True if valid
        """
        if modification.page < 1:
            return False
        if not modification.original_title:
            return False
        if not modification.modified_title:
            return False
        if (
            modification.repetition_number is not None
            and (
                modification.repetition_number < 1
                or modification.repetition_number
                > modification.total_repetitions
            )
        ):
            return False

        return True

