import os
from PyQt5.QtGui import QPalette, QColor

def resolve_path(relative_path):
    """
    Resolve the full path for a given relative path based on the script's directory.

    Args:
        relative_path (str): The relative path to resolve.

    Returns:
        str: The absolute path to the file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current file
    project_root = os.path.abspath(os.path.join(script_dir, os.pardir))  # Move up one level
    return os.path.join(project_root, relative_path)


def style_generate_resume_button(button):
    """Apply styles and initial properties to the generate resume button."""
    button.setEnabled(False)  # Initially disable the button
    button.setStyleSheet("""
        QPushButton:disabled {
            color: gray;
        }
    """)


def apply_dark_theme(app):
    """Apply a dark theme to the application."""
    dark_palette = QPalette()

    # Set palette colors
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    # dark_palette.setColor(QPalette.Highlight, QColor(35, 35, 35))  # Match the Window background
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setStyleSheet("""
        QRadioButton {
            color: white;  /* Text color for the label */
            background-color: transparent;  /* Transparent background for the rectangle */
            border: none;  /* Remove any border from the base rectangle */
        }
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border: 2px solid white;  /* White edge around the circle */
            background-color: gray;  /* Gray fill for the circle */
            border-radius: 8px;  /* Ensures the indicator is circular */
        }
        QRadioButton::indicator:checked {
            background-color: gray;  /* Keep the same gray color when checked */
            border: 2px solid white;  /* White border when checked */
        }
    """)
    app.setPalette(dark_palette)