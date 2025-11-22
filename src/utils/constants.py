"""Constants used throughout the application."""

import re

# Regex pattern for detecting table titles
# Matches both "Tabla 1. xxx" and "Tabla 1 xxx" formats
TABLE_TITLE_PATTERN = re.compile(
    r'(Cuadro|Tabla)\s+(\d+)(?:\.|\s+)([^\n]+?)(?:\n|$)',
    re.IGNORECASE | re.MULTILINE
)

# Default format values
DEFAULT_FONT_NAME = "helv"
DEFAULT_FONT_SIZE = 11.0
DEFAULT_COLOR = (0, 0, 0)  # Black

# Supported font names for PDF modification
SUPPORTED_FONTS = [
    "helv",  # Helvetica
    "tiro",  # Times Roman
    "cour",  # Courier
    "times",  # Times (if loaded)
]

# Common font sizes for academic documents
COMMON_FONT_SIZES = [8, 9, 10, 11, 12, 14, 16]

# Common font families
COMMON_FONT_FAMILIES = [
    "Times New Roman",
    "Arial",
    "Calibri",
    "Helvetica",
    "Courier New",
]

# File extensions
PDF_EXTENSION = ".pdf"
MAX_FILE_SIZE_MB = 50

# UI constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

