from src.app_ui import Ferrmo
from PyQt6.QtWidgets import QApplication
import sys


def main():
    size = [800, 800]
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Ferrmo(size)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
