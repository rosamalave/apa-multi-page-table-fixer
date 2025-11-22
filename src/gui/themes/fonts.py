"""Font utilities for Poppins font with fallback."""

import customtkinter as ctk


def get_poppins_font(size: int = 12, weight: str = "normal") -> ctk.CTkFont:
    """
    Get Poppins font with system fallback.

    Args:
        size: Font size
        weight: Font weight (normal, bold)

    Returns:
        CTkFont object
    """
    # Try Poppins first, fallback to system fonts
    try:
        return ctk.CTkFont(family="Poppins", size=size, weight=weight)
    except:
        # Fallback to Segoe UI (Windows) or system default
        return ctk.CTkFont(family="Segoe UI", size=size, weight=weight)

