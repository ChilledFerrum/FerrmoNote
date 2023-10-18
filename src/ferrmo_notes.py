from PyQt6.QtWidgets import QToolButton, QLabel, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtGui import QIcon, QFont, QFontMetrics
from PyQt6.QtCore import QSize, Qt


class FerrmoNote(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # Note Info
        self.id = 0
        self.note = None
        self.selected = False
        self.file_path = ""
        self.name = QLabel()

        self.button_layout = QVBoxLayout(self)
        self.button = QToolButton(self)
        self.icon_label = QLabel()
        self.number = 0
        self.grid_pos = (0, 0)
        self.button.clicked.connect(self.button_select)
        self._parent = parent

        self._width = None
        self._height = None
        self.button.setCheckable(True)

    def createNote(self, width, height):

        icon = QIcon("style/note_leave.png")
        size = icon.pixmap(icon.availableSizes()[0])

        _width = size.width()
        _height = size.height()
        self._width = _width
        self._height = _height
        self.button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.icon_label.setPixmap(self.button.icon().pixmap(QSize(_width, _height)))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button.setIconSize(QSize(_width, _height))
        self.setFixedSize(_width, _height)
        self.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0);"
            # "border: 1px solid black;"
            "padding-left: 1px;"
        )

        font = QFont("Segoe UI", 9)
        font.setBold(True)


        self.icon_label.setFont(font)
        self.icon_label.setText(f"Button {self.id}")
        self.button.setIcon(QIcon("style/note_leave.png"))

        self.button_layout.addWidget(self.button)
        self.button_layout.addWidget(self.icon_label)
        self.setLayout(self.button_layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)


    def button_select(self):
        print(f"Button Selected {self.id}")
        self._parent.selected_button() # Removes current selected button
        self.selected = True
        self.button.setIcon(QIcon("style/note_selected.png"))

    def button_unselect(self):
        self.selected = False
        self.button.setIcon(QIcon("style/note_leave.png"))

    def changeName(self):
        font = QFont("Segoe UI", 9)
        font.setBold(True)
        font_metrics = QFontMetrics(font)
        text_bounding_rect = font_metrics.boundingRect(f"Button {self.id}")
        self.icon_label.setText(f"Button {self.id}")
        widget_width = max(self._width, text_bounding_rect.width())
        widget_height = self._height + text_bounding_rect.height()

        self.button.setIconSize(QSize(self._width, self._height))
        self.setFixedSize(widget_width, widget_height)
        print("Test")


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
