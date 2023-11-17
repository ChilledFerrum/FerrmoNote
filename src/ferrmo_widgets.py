from src.style_util import FerrmoLabel
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit,
                             QLineEdit)
from PyQt6.QtCore import Qt
from src.ferrmo_buttons import FerrmoButton
from src.ferrmo_notes import FerrmoNote
from src.style_util import GradientBackground
from datetime import datetime
import json


class AddButtonWidget(GradientBackground):
    def __init__(self, parent, gradient_start, gradient_end):
        super().__init__(parent.width, parent.height, gradient_start, gradient_end)
        self.submit_button = FerrmoButton(self, text="Submit", pressedColor="#069647")
        self.cancel_button = FerrmoButton(self, text="Cancel", pressedColor="#940303")

        self._parent = parent  # Used to create communication between parent and child widget
        self.new_button = False  # Used to communicate with parent class if a new button was submitted.

        self.out_dir = "data/"
        self.file_name = "note_data.json"

        self.layout = QVBoxLayout()
        self.note_name = QLineEdit()
        self.text_area = QPlainTextEdit()

        self.startColor = gradient_start
        self.endColor = gradient_end

        self.window_width = parent.width
        self.window_height = parent.height

        self.initUI()

    def initUI(self):
        text_area_style_sheet = """
        QPlainTextEdit {
            background-color: #f0f0f0;
            border: 1px solid #940303;
            font-family: Segoe UI;
            font-size: 15px;
            color: #333;
            border-radius: 8px;
        }
        QPlainTextEdit:focus {
            border: 2px solid #940303;
        }
        """

        self.text_area.setStyleSheet(text_area_style_sheet)
        self.note_name.setStyleSheet(text_area_style_sheet)
        self.setGeometry(0, 0, self.window_width, self.window_height)

        self.setup_addNote_window()

    def setup_addNote_window(self):
        self.setup_button_connections()  # Creates a link for each button's Function Triggers
        label = FerrmoLabel("Note Name:", font_family="Segoe UI", font_size=10, is_bold=True, color="#ffffff")

        note_name_widget = QWidget()
        note_name_layout = QHBoxLayout()

        # Window Layout Preparation
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_widget.setLayout(buttons_layout)

        # Add Widgets in Layout
        buttons_layout.addWidget(self.submit_button)
        buttons_layout.addWidget(self.cancel_button)
        note_name_layout.addWidget(label)
        note_name_layout.addWidget(self.note_name)
        note_name_widget.setLayout(note_name_layout)

        self.layout.addWidget(note_name_widget)
        self.layout.addWidget(self.text_area)
        self.layout.addWidget(buttons_widget)
        self.setLayout(self.layout)

    def submit_button_func(self):
        self.new_button = True
        new_Note = FerrmoNote(self._parent.mainFrameUI)  # Fixed incorrect parent reference
        new_Note.note_name = self.note_name.text()
        new_Note.contents = self.text_area.toPlainText()
        print(f"New Note Created [{self.note_name.text()}]\n{new_Note.contents}")

        new_Note.save_contents(self.prepare_contents())
        new_Note.createNote()
        if self._parent.notesList:
            new_Note.id = self._parent.notesList[-1].id + 1
        else:
            new_Note.id = 0

        new_Note.init_button_name()
        self._parent.notesList.append(new_Note)
        self._parent.update_notes(clear_data=False)  # Visualizes in parent frame MainFrameUI
        self._parent.showNotification(f"New Button Created", self.note_name.text())
        self.closeMe()


    def get_last_note_id(self):
        with open(self.out_dir + self.file_name, "r") as f:
            data = json.load(f)
            try:
                return data[-1].get('_id', 0) + 1
            except IndexError:
                return 0

    def prepare_contents(self):
        note_title = self.note_name.text()
        contents = {"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "_id": self.get_last_note_id(),
                    "Category": "Undefined",
                    "note_title": note_title,
                    "text_contents": self.text_area.toPlainText()}
        return contents

    def setup_button_connections(self):
        self.submit_button.clicked.connect(self.submit_button_func)
        self.cancel_button.clicked.connect(self.closeMe)

    def has_new_button(self):
        return self.new_button

    def delWidgets(self):
        self.submit_button.deleteLater()
        self.cancel_button.deleteLater()
        self.note_name.deleteLater()
        self.text_area.deleteLater()
        self.layout.deleteLater()

    def closeMe(self):
        self.close()
        self.delWidgets()
        widget = self._parent.mainLayout.takeAt(1).widget().deleteLater()
        del self

class ViewNote_Widget(GradientBackground):
    def __init__(self, parent, note, gradient_start, gradient_end):
        super().__init__(parent.width, parent.height, gradient_start, gradient_end)
        # Class data
        self.note = note
        self.parent = parent

        # Widget data
        self.title_label = None
        self.text_content = None
        self.exit_button = FerrmoButton(self, text="Done!", pressedColor="#006400")
        self.exit_button.clicked.connect(self.Done_button)

        self.widget_layout = QVBoxLayout()
        self.initWidget()

    def Done_button(self):
        self.closeMe()

    def initWidget(self):
        self.title_label = FerrmoLabel(self.note.note_name,
                                       font_size=15,
                                       color="WHITE",
                                       is_bold=True)

        self.text_content = FerrmoLabel(text=self.note.text_contents,
                                        font_family="sans-serif typefaces",
                                        font_size=10,
                                        color="WHITE")
        self.text_content.setWordWrap(True)
        self.setFixedSize(self.parent.mainFrameUI._width, self.parent.mainFrameUI._height-200)
        self.addWidgets()  # Adds widgets to the layout

    def addWidgets(self):
        self.widget_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.widget_layout.addWidget(self.text_content, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.widget_layout.addWidget(self.exit_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.widget_layout) # Vertical Box Layout

    def delWidgets(self):
        self.title_label.deleteLater()
        self.text_content.deleteLater()
        self.exit_button.deleteLater()
        self.widget_layout.deleteLater()

    def closeMe(self):
        self.close()
        self.delWidgets()
        self.parent.mainLayout.takeAt(1).widget().deleteLater()
        del self
