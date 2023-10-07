from src.ui import Ferrmo
from PyQt6.QtWidgets import QApplication
import sys

def main():
    size = [700, 800]
    app = QApplication(sys.argv)
    window = Ferrmo(size)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
