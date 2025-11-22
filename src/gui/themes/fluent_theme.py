"""Fluent Design theme colors and styles."""

# Fluent Design Color Palette
FLUENT_PRIMARY = "#264cce"  # Custom Blue
FLUENT_SECONDARY = "#1e3aa3"  # Darker Blue
FLUENT_SUCCESS = "#107C10"  # Green
FLUENT_WARNING = "#FFB900"  # Yellow
FLUENT_ERROR = "#D13438"  # Red
FLUENT_BACKGROUND = "#FFFFFF"  # White background
FLUENT_SURFACE = "#FFFFFF"  # White cards
FLUENT_TEXT_PRIMARY = "#1a1a1a"  # Dark text for contrast
FLUENT_TEXT_SECONDARY = "#666666"  # Medium Gray
FLUENT_ACRYLIC_LIGHT = "rgba(255, 255, 255, 0.7)"  # Acrylic light

# Additional colors
FLUENT_BORDER = "#E5E5E5"  # Light border
FLUENT_HOVER = "#F5F5F5"  # Hover state
FLUENT_SELECTED = "#E8E8E8"  # Selected state
FLUENT_SHADOW = "#000000"  # Shadow color
COMBOBOX_BUTTON = "#e8f0ff"  # Light blue for dropdown button
COMBOBOX_DROPDOWN = "#1a237e"  # Navy blue for dropdown background

# Spacing constants (in pixels)
SPACING_XS = 4
SPACING_SM = 8
SPACING_MD = 16
SPACING_LG = 24
SPACING_XL = 32

# Border radius (in pixels)
RADIUS_SM = 4
RADIUS_MD = 8
RADIUS_LG = 12
RADIUS_XL = 16

# Font sizes
FONT_SIZE_SM = 12
FONT_SIZE_MD = 14
FONT_SIZE_LG = 16
FONT_SIZE_XL = 20

# Shadow effects (for card elevation)
SHADOW_SM = "0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24)"
SHADOW_MD = "0 3px 6px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.12)"
SHADOW_LG = "0 10px 20px rgba(0, 0, 0, 0.15), 0 3px 6px rgba(0, 0, 0, 0.10)"

# Font family - Poppins (fallback to system fonts)
FONT_FAMILY = "Poppins"
FONT_FALLBACK = ["Segoe UI", "Arial", "sans-serif"]


def get_theme_colors() -> dict[str, str]:
    """
    Get all theme colors as a dictionary.

    Returns:
        Dictionary with color names and values
    """
    return {
        "primary": FLUENT_PRIMARY,
        "secondary": FLUENT_SECONDARY,
        "success": FLUENT_SUCCESS,
        "warning": FLUENT_WARNING,
        "error": FLUENT_ERROR,
        "background": FLUENT_BACKGROUND,
        "surface": FLUENT_SURFACE,
        "text_primary": FLUENT_TEXT_PRIMARY,
        "text_secondary": FLUENT_TEXT_SECONDARY,
        "border": FLUENT_BORDER,
        "hover": FLUENT_HOVER,
        "selected": FLUENT_SELECTED,
    }


def get_font(family: str = None, size: int = 12, weight: str = "normal") -> tuple:
    """
    Get font tuple with Poppins fallback.

    Args:
        family: Font family name
        size: Font size
        weight: Font weight (normal, bold)

    Returns:
        Font tuple for CTkFont
    """
    import customtkinter as ctk
    
    if family is None:
        family = FONT_FAMILY
    
    # Try Poppins, fallback to system fonts
    try:
        # Check if Poppins is available
        test_font = ctk.CTkFont(family=family, size=size, weight=weight)
        return (family, size, weight)
    except:
        # Fallback to system fonts
        return (FONT_FALLBACK[0], size, weight)


def apply_fluent_theme(app) -> None:
    """
    Apply Fluent Design theme to CustomTkinter app.

    Args:
        app: CustomTkinter CTk instance
    """
    import customtkinter as ctk

    # Set appearance mode
    ctk.set_appearance_mode("light")

    # Set default color theme (will be customized)
    ctk.set_default_color_theme("blue")

    # Configure custom colors
    ctk.set_widget_scaling(1.0)
    ctk.set_window_scaling(1.0)
    
    # Set background color
    app.configure(fg_color=FLUENT_BACKGROUND)

