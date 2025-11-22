"""Custom exceptions for PDF processing."""


class PDFProcessingError(Exception):
    """Base exception for PDF processing errors."""

    pass


class PDFReadError(PDFProcessingError):
    """Raised when PDF cannot be read."""

    pass


class FormatDetectionError(PDFProcessingError):
    """Raised when format detection fails."""

    pass


class ModificationError(PDFProcessingError):
    """Raised when PDF modification fails."""

    pass


class ValidationError(PDFProcessingError):
    """Raised when input validation fails."""

    pass

