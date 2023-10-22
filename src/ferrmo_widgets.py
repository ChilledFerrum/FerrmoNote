from src.style_util import *
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit
from src.ferrmo_buttons import FerrmoButton
from src.ferrmo_notes import FerrmoNote


class AddButtonWidget(QWidget):
    def __init__(self, parent, gradient_start, gradient_end):
        super().__init__()
        self.submit_button = FerrmoButton(self, text="Submit", pressedColor="#069647")
        self.cancel_button = FerrmoButton(self, text="Cancel", pressedColor="#940303")

        self._parent = parent  # Used to create communication between parent and child widget
        self.new_button = False  # Used to communicate with parent class if a new button was submitted.
        self.text_area = QPlainTextEdit()
        self.startColor = gradient_start
        self.endColor = gradient_end
        self.window_width = 450
        self.window_height = 600
        self.layout = QVBoxLayout()
        self.gradient_background = GradientBackground(self, self.window_width, self.window_height,
                                                      self.layout,
                                                      self.startColor, self.endColor)
        self.initUI()

    def initUI(self):
        style_sheet = """
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
        self.text_area.setStyleSheet(style_sheet)

        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.layout.addWidget(self.gradient_background)
        self.setup_addNote_window()

    def setup_addNote_window(self):
        self.setup_button_connections()  # Creates a link for each button's Function Triggers

        # Window Layout Preparation
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_widget.setLayout(buttons_layout)

        # Add Widgets in Layout
        buttons_layout.addWidget(self.submit_button)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addWidget(self.text_area)
        self.layout.addWidget(buttons_widget)

    def cancel_button_func(self):
        self.close()

    def submit_button_func(self):
        self.new_button = True
        new_Note = FerrmoNote(self._parent)

        new_Note.createNote(width=80, height=80)
        if self._parent.notesList:
            new_Note.id = self._parent.notesList[-1].id + 1
        else:
            new_Note.id = 0

        new_Note.init_button_name()
        self._parent.notesList.append(new_Note)
        self._parent.update_notes()  # Visualizes in parent frame MainFrameUI
        self.close()

    def setup_button_connections(self):
        self.submit_button.clicked.connect(self.submit_button_func)
        self.cancel_button.clicked.connect(self.cancel_button_func)

    def has_new_button(self):
        return self.new_button

    def resizeEvent(self, event):

        self.gradient_background.setFixedSize(self.width(), self.height())
        self.gradient_background.updateGradient(self.width(), self.height(), self.startColor, self.endColor)
