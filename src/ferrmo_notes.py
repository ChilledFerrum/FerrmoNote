import json

from PyQt6.QtCore import QSize, Qt, QRect
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (QToolButton, QLabel, QVBoxLayout, QWidget,
                             QSizePolicy)

from src.style_util import Notification


class FerrmoNote(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.notification = None
        self._parent = parent
        self.out_dir = "data/"
        self.file_name = "note_data.json"

        # Note Info
        self.datetime = ""
        self.id = 0
        self.category = ""
        self.note_name = ""
        self.text_contents = ""

        self.note = None
        self.selected = False

        self.button_layout = QVBoxLayout(self)
        self.note_button_widget = QToolButton(self)
        self.note_label_widget = QLabel()
        self.number = 0
        self.grid_pos = (0, 0)
        self.icon_width = None
        self.icon_height = None
        self.note_button_widget.setCheckable(True)

    def createNote(self, width=80, height=80):

        icon = QIcon("style/note_leave.png")
        self.note_button_widget.setIcon(icon)

        size = icon.pixmap(icon.availableSizes()[0])
        self.icon_width = size.width() // 2 + 2
        self.icon_height = size.height() // 2

        self.note_button_widget.setFixedSize(self.icon_width, self.icon_height+2)
        self.note_button_widget.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.note_button_widget.setStyleSheet("text-align: center; border: 0px solid black;")
        self.note_button_widget.setGeometry(-15, -15, self.icon_width, self.icon_height)
        self.note_button_widget.setIconSize(QSize(self.icon_width, self.icon_height))

        font = QFont("Segoe UI", 9)
        font.setBold(True)
        self.note_label_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.note_label_widget.setFont(font)
        self.note_button_widget.setIcon(QIcon("style/note_leave.png"))

        self.button_layout.addWidget(self.note_label_widget, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.button_layout.addWidget(self.note_button_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(self.button_layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.note_button_widget.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon, )
        self.init_button_name()

    def set_contents(self, info):
        self.datetime, self.id, self.category, \
            self.note_name, self.text_contents = info

    def init_button_name(self):
        self.note_label_widget.setText(self.note_name)
        self.note_label_widget.setWordWrap(True)
        self.note_label_widget.setMaximumWidth(self.icon_width + 50)
        self.note_label_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.setMinimumSize(self.sizeHint()) # Used to 

        self.note_button_widget.setIconSize(QSize(self.icon_width, self.icon_height))
        self.note_button_widget.setToolTip(self.note_name)
        self.note_button_widget.clicked.connect(self.note_button)

    def save_contents(self, contents):
        file_path = self.out_dir + self.file_name
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

    def note_button(self):
        self._parent.unselect_note()  # Uses higher level widget reference to communicate with lower level widget.
        self.button_select_UI()

    def showNotification(self, title, description, color=(36, 94, 189), border_color=(255, 255, 255), timeout=1000000):
        self.notification = Notification()
        self.notification.setNotify(title, description, color, border_color, timeout, use_exit_button=False)
        notif_popup = QRect(self._parent._parent.x() + self._parent._parent.width - self.notification.width(),
                            self._parent._parent.y() + self._parent._parent.sideBar_minHeight - 10,
                            self.notification.m.messageLabel.width(), self.notification.m.messageLabel.height())
        self.notification.setGeometry(notif_popup)

    def delete_note_data(self):
        file_path = self.out_dir + self.file_name
        with open(file_path, 'r') as f:
            data = json.load(f)
            data[:] = [row for row in data if int(row.get('_id')) != self.id]
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def setButtonFixedSize(self, width, height): # Sets note to Init. size
        self.icon_width = width
        self.icon_height = height

        self.note_button_widget.setIconSize(QSize(width, height))
        self.note_button_widget.setFixedSize(width, height)

    def button_select_UI(self): # Widget changes when selecting
        self.selected = True
        print(f"Button Selected {self.id}")

        font = QFont("Segoe UI", 10)
        font.setBold(True)
        self.note_label_widget.setFont(font)
        self.setButtonFixedSize(self.icon_width + 15, self.icon_height + 15)
        self.note_button_widget.setIcon(QIcon("style/note_selected.png"))

    def button_unselect_UI(self):
        self.selected = False
        font = QFont("Segoe UI", 9)
        font.setBold(True)
        self.note_label_widget.setFont(font)
        self.note_label_widget.setStyleSheet("color: rgb(255,255,255);")
                
        self.setButtonFixedSize(self.icon_width - 15, self.icon_height - 15)
        self.note_button_widget.setIcon(QIcon("style/note_leave.png"))

    def re_pos(self, off_x, off_y):
        self.move(50 + off_x, 50 + off_y)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def enterEvent(self, event):
        self.showNotification("Note Name:", f"<h3>{self.note_name}</h3>", color=(0, 60, 0), border_color=(255, 100, 0))
        if not self.selected:
            self.note_button_widget.setIcon(QIcon("style/note_enter.png"))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.notification.closeMe()
        if not self.selected:
            self.note_button_widget.setIcon(QIcon("style/note_leave.png"))
        super().leaveEvent(event)
