from PyQt6.QtWidgets import QToolButton, QLabel, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtGui import QIcon, QFont, QFontMetrics
from src.ferrmo_buttons import FerrmoButton
from PyQt6.QtCore import QSize, Qt
import json


class FerrmoNote(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # Note Info
        self.id = 0
        self.note = None
        self.selected = False

        self.out_dir = "data/"
        self.file_name = "note_data.json"

        self.note_name = ""

        self.button_layout = QVBoxLayout(self)
        self.button = QToolButton(self)
        self.icon_label = QLabel()
        self.number = 0
        self.grid_pos = (0, 0)
        self.button.clicked.connect(self.button_select)
        self._parent = parent

        self.icon_width = None
        self.icon_height = None
        self.button.setCheckable(True)

    def createNote(self, width, height):

        icon = QIcon("style/note_leave.png")
        self.button.setIcon(icon)
        self.button.setIconSize(QSize(76, 92))
        size = icon.pixmap(icon.availableSizes()[0])

        self.icon_width = size.width()//2
        self.icon_height = size.height()//2

        self.button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.button.setStyleSheet("text-align: center;")
        self.icon_label.setWordWrap(True)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("border:1px solid black;")
        self.button.setIconSize(QSize(self.icon_width, self.icon_height))

        self.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0);"
            "border: 1px solid black;"
            "margin-left: 2px;"
        )

        font = QFont("Segoe UI", 9)
        font.setBold(True)
        self.icon_label.setFont(font)

        self.button.setIcon(QIcon("style/note_leave.png"))

        self.button_layout.addWidget(self.button)
        self.button_layout.addWidget(self.icon_label)
        self.setLayout(self.button_layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def init_button_name(self):
        self.icon_label.setText(self.note_name)
        self.icon_label.setWordWrap(True)
        self.icon_label.adjustSize()
        self.button.setIconSize(QSize(self.icon_width, self.icon_height))

    def set_contents(self, contents):
        file_path = self.out_dir+self.file_name
        try:
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            print(f"WARNING: Missing/Not Found File {self.file_name} at location {self.out_dir}")
            with open(file_path, 'w') as file:
                file.write("[]")
                print(f"Created new note data file at path {file_path}")
            existing_data = []
        existing_data.append(contents)

        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

    def button_select(self):
        self.button_unselect()  # Removes current selected button
        self.selected = True
        print(f"Button Selected {self.id}")

        font = QFont("Segoe UI", 10)
        font.setBold(True)
        self.icon_label.setFont(font)
        self.icon_label.setStyleSheet("color: rgb(0,255,0);")
        self.button.setIconSize(QSize(self.icon_width + 15, self.icon_height + 15))
        self.button.setFixedSize(self.icon_width+15, self.icon_height+15)
        self.button.setIcon(QIcon("style/note_selected.png"))

    # def unselect_selected_button(self):

    def button_unselect(self):
        self.selected = False
        font = QFont("Segoe UI", 9)
        font.setBold(True)
        self.icon_label.setFont(font)
        self.button.setIconSize(QSize(self.icon_width, self.icon_height))
        self.icon_label.setStyleSheet("color: rgb(0,0,0);")
        self.button.setIcon(QIcon("style/note_leave.png"))


    def re_pos(self, off_x, off_y):
        self.move(50 + off_x, 50 + off_y)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def enterEvent(self, event):
        if not self.selected:
            self.button.setIcon(QIcon("style/note_enter.png"))
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.selected:
            self.button.setIcon(QIcon("style/note_leave.png"))
        super().leaveEvent(event)
