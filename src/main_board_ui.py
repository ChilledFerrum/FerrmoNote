from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt
from src.style_util import GradientBackground


class MainFrameUI(QWidget):
    def __init__(self, parent, width, height, gradientStart, gradientEnd):
        super().__init__(parent)
        self.delta = 0
        self._parent = parent
        self._width = width
        self._height = height
        self.startColor = gradientStart
        self.endColor = gradientEnd

        self.scroll_area_locations = 0

        self.gradient_background = GradientBackground(width, height, gradientStart, gradientEnd)

        self.mainFrameUI_layout = QVBoxLayout()
        self.notes_grid_layout = QGridLayout()
        self.mainFrameUI_content_widget = GradientBackground(width, height, gradientStart, gradientEnd)

        self.initUI()

    def initUI(self):
        self.mainFrameUI_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainFrameUI_layout)
        self.mainFrameUI_content_widget.setLayout(self.notes_grid_layout)
        scroll = QScrollArea()
        scroll.setWidget(self.mainFrameUI_content_widget)
        scroll.setWidgetResizable(True)
        self.mainFrameUI_layout.addWidget(scroll)

    def unselect_note(self):
        for note in self._parent.notesList:
            if note.selected:
                note.button_unselect_UI()
                break

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
        scroll.verticalScrollBar().setValue(self.scroll_area_locations + self.delta)
        self.mainFrameUI_layout.addWidget(scroll)

    def clear_mainFrameUI_layout(self):
        while self.mainFrameUI_layout.count():
            item = self.mainFrameUI_layout.takeAt(0)
            item.widget().deleteLater()

    def clear_content_grid(self):
        while self.notes_grid_layout.count():
            item = self.notes_grid_layout.takeAt(0)
            item.widget().deleteLater()

    def wheelEvent(self, event):
        scroll = self.mainFrameUI_layout.itemAt(0).widget()
        current_scroll_pos = scroll.verticalScrollBar().value()
        self.scroll_area_locations = current_scroll_pos
        self.delta = event.angleDelta().y()
