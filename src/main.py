"""Main entry point for PDF Table Title Fixer application."""

import sys
import customtkinter as ctk

from src.gui.main_window import MainWindow


def main() -> None:
    """Run the application."""
    # Create and run main window
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()

