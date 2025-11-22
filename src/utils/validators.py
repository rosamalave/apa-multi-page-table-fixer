"""Input validation functions."""

import os
from pathlib import Path
from typing import Optional

from src.utils.exceptions import ValidationError
from src.utils.constants import PDF_EXTENSION, MAX_FILE_SIZE_MB


def validate_pdf_path(file_path: str) -> Path:
    """
    Validate that the file path exists and is a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Path object if valid

    Raises:
        ValidationError: If path is invalid
    """
    if not file_path:
        raise ValidationError("File path cannot be empty")

    path = Path(file_path)

    if not path.exists():
        raise ValidationError(f"File does not exist: {file_path}")

    if not path.is_file():
        raise ValidationError(f"Path is not a file: {file_path}")

    if path.suffix.lower() != PDF_EXTENSION:
        raise ValidationError(
            f"File must be a PDF ({PDF_EXTENSION}): {file_path}"
        )

    # Check file size
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValidationError(
            f"File size ({size_mb:.2f} MB) exceeds maximum "
            f"({MAX_FILE_SIZE_MB} MB)"
        )

    return path


def validate_output_path(file_path: str, overwrite: bool = False) -> Path:
    """
    Validate output file path.

    Args:
        file_path: Path for output file
        overwrite: Whether to allow overwriting existing files

    Returns:
        Path object if valid

    Raises:
        ValidationError: If path is invalid
    """
    if not file_path:
        raise ValidationError("Output file path cannot be empty")

    path = Path(file_path)

    if path.exists() and not overwrite:
        raise ValidationError(
            f"File already exists: {file_path}. "
            "Set overwrite=True to allow overwriting."
        )

    # Check if parent directory exists and is writable
    parent = path.parent
    if not parent.exists():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ValidationError(
                f"Cannot create output directory: {e}"
            ) from e

    if not os.access(parent, os.W_OK):
        raise ValidationError(
            f"Output directory is not writable: {parent}"
        )

    return path


def validate_font_size(size: float) -> float:
    """
    Validate font size value.

    Args:
        size: Font size to validate

    Returns:
        Validated font size

    Raises:
        ValidationError: If size is invalid
    """
    if size <= 0:
        raise ValidationError("Font size must be positive")
    if size > 72:
        raise ValidationError("Font size cannot exceed 72 points")
    return size


def validate_page_number(page: int, max_pages: int) -> int:
    """
    Validate page number.

    Args:
        page: Page number to validate
        max_pages: Maximum number of pages in document

    Returns:
        Validated page number

    Raises:
        ValidationError: If page number is invalid
    """
    if page < 1:
        raise ValidationError("Page number must be >= 1")
    if page > max_pages:
        raise ValidationError(
            f"Page number ({page}) exceeds document pages ({max_pages})"
        )
    return page

