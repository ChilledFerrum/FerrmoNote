from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, QRect
from src.style_util import GradientBackground


class MainFrameUI(QWidget):
    def __init__(self, parent, width, height, gradientStart, gradientEnd):
        super().__init__(parent)
        self._width = width
        self._height = height
        self.startColor = gradientStart
        self.endColor = gradientEnd

        self.gradient_background = GradientBackground(width, height, gradientStart, gradientEnd)

        self.mainFrameUI_layout = QVBoxLayout()
        self.mainFrameUI_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainFrameUI_layout)
        self.mainFrameUI_content_widget = GradientBackground(width, height, gradientStart, gradientEnd)
        self.notes_grid_layout = QGridLayout()

        self.mainFrameUI_content_widget.setLayout(self.notes_grid_layout)
        scroll = QScrollArea()
        scroll.setWidget(self.mainFrameUI_content_widget)
        scroll.setWidgetResizable(True)
        self.mainFrameUI_layout.addWidget(scroll)

    def display_notes(self, notesList, clear_data=True):
        try:
            if clear_data:
                self.clear_content_grid()
            self.clear_mainFrameUI_layout()
        except RuntimeError:
            print("No Widgets inside")

        scroll = QScrollArea()
        for note in notesList:
            self.notes_grid_layout.addWidget(note, note.grid_pos[0], note.grid_pos[1])
        scroll.setWidget(self.mainFrameUI_content_widget)
        scroll.setWidgetResizable(True)
        self.mainFrameUI_layout.addWidget(scroll)

    def clear_mainFrameUI_layout(self):
        while self.mainFrameUI_layout.count():
            item = self.mainFrameUI_layout.takeAt(0)
            item.widget().deleteLater()

    def clear_content_grid(self):
        while self.notes_grid_layout.count():
            item = self.notes_grid_layout.takeAt(0)
            item.widget().deleteLater()