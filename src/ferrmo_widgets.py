from src.style_util import GradientBackground, FerrmoLabel
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit, QLineEdit, QLabel
from src.ferrmo_buttons import FerrmoButton
from src.ferrmo_notes import FerrmoNote
from datetime import datetime


class AddButtonWidget(QWidget):
    def __init__(self, parent, gradient_start, gradient_end):
        super().__init__(parent)
        self.submit_button = FerrmoButton(self, text="Submit", pressedColor="#069647")
        self.cancel_button = FerrmoButton(self, text="Cancel", pressedColor="#940303")

        self._parent = parent  # Used to create communication between parent and child widget
        self.new_button = False  # Used to communicate with parent class if a new button was submitted.

        self.note_name = QLineEdit()
        self.text_area = QPlainTextEdit()

        self.startColor = gradient_start
        self.endColor = gradient_end

        self.window_width = parent.mainFrame_width
        self.window_height = parent.mainFrame_height
        self.layout = QVBoxLayout()

        # self.gradient_background = GradientBackground(self, self.window_width, self.window_height,
        #                                               self.layout,
        #                                                 self.startColor, self.endColor)

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
        # self.layout.addWidget(self.gradient_background)
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

    def cancel_button_func(self):
        self.close()

    def submit_button_func(self):
        self.new_button = True
        new_Note = FerrmoNote(self._parent)
        new_Note.note_name = self.note_name.text()
        new_Note.contents = self.text_area.toPlainText()
        print(f"New Note Created [{self.note_name.text()}]\n{new_Note.contents}")

        new_Note.set_contents(self.prepare_contents())
        new_Note.createNote(width=80, height=80)
        if self._parent.notesList:
            new_Note.id = self._parent.notesList[-1].id + 1
        else:
            new_Note.id = 0

        new_Note.init_button_name()
        self._parent.notesList.append(new_Note)
        self._parent.update_notes()  # Visualizes in parent frame MainFrameUI

        self.close()

    def prepare_contents(self):
        note_title = self.note_name.text()
        note_title = note_title.replace(" ", "_")
        contents = {"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Category": "Undefined",
                    "note_title": note_title,
                    "text_contents": self.text_area.toPlainText()}
        return contents

    def setup_button_connections(self):
        self.submit_button.clicked.connect(self.submit_button_func)
        self.cancel_button.clicked.connect(self.cancel_button_func)

    def has_new_button(self):
        return self.new_button

    # def resizeEvent(self, event):
    #
    #     self.gradient_background.setFixedSize(self.width(), self.height())
    #     self.gradient_background.updateGradient(self.width(), self.height(), self.startColor, self.endColor)
