from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


class FerrmoNote(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        # Note Info
        self.id = 0
        self.note = None
        self.selected = False
        self.file_path = ""
        self.name = ""
        self.number = 0
        self.grid_pos = (0, 0)
        self.clicked.connect(self.button_clicked)
        self.setStyleSheet(
            "QPushButton { text-align: center;"
            "font: bold 20px;}"
        )
        self._parent = parent
        self.setFlat(True)

        self.setIcon(QIcon("stype/NoteIcon2.png"))

    def createNote(self, width, height):
        self.setGeometry(200, 200, width, height)
        self.setIcon(QIcon("style/NoteIcon2.png"))
        self.setIconSize(QSize(width, height))
        self.setStyleSheet(f"background-color: rgba(255, 255, 255, 0);")

    def button_clicked(self):
        print("Clicked ", self.id)
        self.selected = True

    def changeName(self):
        self.setText(f"Button {self.id}")

    def re_pos(self, off_x, off_y):
        self.move(50 + off_x, 50 + off_y)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def enterEvent(self, event):
        self.setIcon(QIcon("style/NoteIcon.png"))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(QIcon("style/NoteIcon2.png"))
        super().leaveEvent(event)
