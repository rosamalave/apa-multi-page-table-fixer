"""Data models for PDF table analysis and modification."""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TableInfo:
    """Information about a detected table/cuadro in the PDF."""

    page: int
    number: str
    description: str
    full_title: str
    position: int
    table_type: str  # "Cuadro" or "Tabla"

    def __post_init__(self) -> None:
        """Validate and normalize data after initialization."""
        if self.page < 1:
            raise ValueError("Page number must be >= 1")
        if not self.number.isdigit():
            raise ValueError("Table number must be numeric")
        if self.table_type not in ("Cuadro", "Tabla"):
            raise ValueError("Table type must be 'Cuadro' or 'Tabla'")


@dataclass
class FormatInfo:
    """Font and formatting information for table titles."""

    font_name: str
    font_size: float
    is_bold: bool
    is_italic: bool
    color: tuple[int, int, int] = (0, 0, 0)

    def __post_init__(self) -> None:
        """Validate format information."""
        if self.font_size <= 0:
            raise ValueError("Font size must be positive")
        if len(self.color) != 3 or not all(
            0 <= c <= 255 for c in self.color
        ):
            raise ValueError(
                "Color must be RGB tuple with values between 0-255"
            )

    def __eq__(self, other: object) -> bool:
        """Check if two FormatInfo objects are equal."""
        if not isinstance(other, FormatInfo):
            return False
        return (
            self.font_name == other.font_name
            and abs(self.font_size - other.font_size) < 0.1
            and self.is_bold == other.is_bold
            and self.is_italic == other.is_italic
        )

    def __hash__(self) -> int:
        """Make FormatInfo hashable for use as dictionary key."""
        # Round font_size to avoid floating point precision issues
        font_size_rounded = round(self.font_size, 1)
        return hash((
            self.font_name,
            font_size_rounded,
            self.is_bold,
            self.is_italic,
        ))


@dataclass
class Modification:
    """Represents a modification to apply to a table title."""

    page: int
    original_title: str
    modified_title: str
    repetition_number: Optional[int]
    total_repetitions: int
    format_info: Optional[FormatInfo] = None

    def __post_init__(self) -> None:
        """Validate modification data."""
        if self.page < 1:
            raise ValueError("Page number must be >= 1")
        if self.total_repetitions < 1:
            raise ValueError("Total repetitions must be >= 1")
        if (
            self.repetition_number is not None
            and (
                self.repetition_number < 1
                or self.repetition_number > self.total_repetitions
            )
        ):
            raise ValueError(
                "Repetition number must be between 1 and total_repetitions"
            )

    def needs_modification(self) -> bool:
        """Check if this modification actually needs to be applied."""
        return self.repetition_number is not None


@dataclass
class AnalysisResult:
    """Complete result of PDF analysis."""

    all_tables: List[TableInfo]
    modifications: List[Modification]
    format_uniform: bool
    format_info: Optional[FormatInfo] = None
    total_tables: int = 0
    tables_to_modify: int = 0

    def __post_init__(self) -> None:
        """Validate and calculate derived values."""
        self.total_tables = len(self.all_tables)
        self.tables_to_modify = sum(
            1 for m in self.modifications if m.needs_modification()
        )

    def get_tables_by_number(self, number: str) -> List[TableInfo]:
        """Get all tables with a specific number."""
        return [t for t in self.all_tables if t.number == number]

