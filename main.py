from app.resume_view import ResumeApp
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from app.utils import apply_dark_theme



def main():
    app = QApplication(sys.argv)

    # Apply the dark theme
    apply_dark_theme(app)

    window = ResumeApp()
    window.resize(900, 1500)  # Default size; adjust as needed
    window.move(100, 100)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
