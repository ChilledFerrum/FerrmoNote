import sys

from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout,
                             QWidget, QGridLayout)
from PyQt6.QtCore import QRect
from src.ferrmo_buttons import FerrmoButton
# Notifications Credit to Axel Schneider
from src.style_util import Notification
from src.ferrmo_widgets import AddButtonWidget
import pandas as pd
from src.main_board_ui import MainFrameUI
from src.ferrmo_notes import FerrmoNote

menuColor = "#171924"


class Ferrmo(QWidget):
    def __init__(self, size):
        super().__init__()

        self.mainFrame = None  # Entire App Frame

        self.saved_state = None
        print("Active")
        self.mainFrameUI = None  # Main Frame UI Contains Note History
        self.notification = None  # Pop-up Notifications
        self.gridLayout = None  # Grid Layout to hold Note History
        self.setWindowTitle("Ferrmo")
        self.width = size[0]
        self.height = size[1]
        self.gradient_start = (0, 0, 0)
        self.gradient_end = (142, 142, 142)

        # Refresh with each update
        self.update()

        # Main Layout
        self.mainLayout = None
        self.appInit()

        # Side Bar Content
        self.sideBar_minHeight = 50
        self.frameSideBar = None
        self.notesList = []

        self.buttonViewNote = None
        self.buttonAddNote = None
        self.buttonSearchNote = None
        self.buttonSaveNotes = None
        self.buttonLoadNotes = None
        self.buttonDeleteNote = None
        self.buttonSettings = None
        self.buttonExit = None

        self.createMainUI()

        self.currentNote = None

    def appInit(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        center_x = screen_geometry.width() // 2
        center_y = screen_geometry.height() // 2
        offset_x = center_x - int(self.width / 2) - 100
        offset_y = center_y - int(self.height / 2)

        self.setGeometry(offset_x, offset_y, self.width, self.height)
        self.setWindowOpacity(0.93)

    def createMainUI(self):
        # Side Bar Content
        self.setup_frameSideBar()

        self.gridLayout = QGridLayout()

        # Main Frame Initializing
        self.mainFrameUI = MainFrameUI(self, self.width,
                                       self.height,
                                       self.gradient_start,
                                       self.gradient_end)

        self.init_menu_buttons()
        self.setup_menu_button_connections()
        buttonLayout = self.add_menu_button_widgets()

        self.frameSideBar.setLayout(buttonLayout)

        self.mainLayout.addWidget(self.mainFrameUI)
        self.mainLayout.addWidget(self.frameSideBar)

    def showNotification(self, title, description, color=(36, 94, 189), timeout=3000):
        self.notification = Notification()
        self.notification.setNotify(title, description, color, timeout)
        r = QRect(self.x() + round(self.width / 2) - round(self.notification.width() / 2),
                  self.y() + 26, self.notification.m.messageLabel.width() + 30,
                  self.notification.m.messageLabel.height())
        self.notification.setGeometry(r)

    def viewNote(self):
        pass

    def addNote(self, event):
        add_button_widget = AddButtonWidget(self, self.gradient_start, self.gradient_end)
        self.mainLayout.insertWidget(1, add_button_widget)

    def searchNote(self, event):
        print("Clicked Search Note!")

    def saveNote(self, event):
        print("Clicked Save Note!")

    def deleteNote(self, event):  # Deletes Note
        for note in self.notesList:
            if note.selected:
                print(f"Deleted Note {note.id}")
                note.selected = False
                note.delete_note_data()
                self.notesList.remove(note)
                note.deleteLater()
                self.update_notes(clear_data=False)
                return
        self.showNotification("Warning!", "<b>No Note Selected</b>", color=(255, 140, 0))

    def loadNotes(self, event):
        notes_data = pd.read_json('data/note_data.json')

        if len(notes_data) > 0:
            if self.notesList:
                self.notesList = []
            for index, row in notes_data.iterrows():
                new_Note = FerrmoNote(self.mainFrameUI)  # Init Note
                note_info = [row['datetime'], row['_id'], row['Category'], row['note_title'], row['text_contents']]
                new_Note.set_contents(note_info)  # Store Note Info
                new_Note.createNote()  # Create Note
                self.notesList.append(new_Note)  # Append to active note list
            self.update_notes()
            self.showNotification("Loaded Notes", f"Loaded {len(self.notesList)} notes")
        else:
            self.showNotification("Warning!", "<b>No notes to load<b><br/>\n note_data.json Empty", color=(255, 140, 0))

    def settings(self, event):
        print("Clicked Settings!")

    def exit(self, event):
        print("Clicked Exit!")
        sys.exit(1)

    def init_menu_buttons(self):
        self.buttonViewNote = FerrmoButton(self.frameSideBar,
                                           text="View Note",
                                           font_size=10,
                                           bg=menuColor, pressedColor="#036194")
        self.buttonAddNote = FerrmoButton(self.frameSideBar,
                                          text="Add Notes",
                                          font_size=10,
                                          bg=menuColor, pressedColor="#069647")
        self.buttonSearchNote = FerrmoButton(self.frameSideBar,
                                             text="Search Note",
                                             font_size=10,
                                             bg=menuColor, pressedColor="#036194")
        self.buttonSaveNotes = FerrmoButton(self.frameSideBar,
                                            text="Save Notes",
                                            font_size=10,
                                            bg=menuColor, pressedColor="#069647")
        self.buttonLoadNotes = FerrmoButton(self.frameSideBar,
                                            text="Load Notes",
                                            font_size=10,
                                            bg=menuColor, pressedColor="#036194")
        self.buttonDeleteNote = FerrmoButton(self.frameSideBar,
                                             text="Delete Note",
                                             font_size=10,
                                             bg=menuColor, pressedColor='#940303')
        self.buttonSettings = FerrmoButton(self.frameSideBar,
                                           text="Settings",
                                           bg=menuColor, pressedColor="#036194")
        self.buttonExit = FerrmoButton(self.frameSideBar,
                                       text="Exit",
                                       font_size=17,
                                       bg=menuColor, pressedColor="orange")

    def setup_frameSideBar(self):
        self.frameSideBar = QWidget(self)

        self.frameSideBar.setMinimumHeight(self.sideBar_minHeight)
        self.frameSideBar.setMaximumHeight(self.sideBar_minHeight)
        self.frameSideBar.setStyleSheet(f"background-color: {menuColor};")

    def setup_menu_button_connections(self):
        self.buttonViewNote.clicked.connect(self.viewNote)
        self.buttonAddNote.clicked.connect(self.addNote)
        self.buttonSearchNote.clicked.connect(self.searchNote)
        self.buttonSaveNotes.clicked.connect(self.saveNote)
        self.buttonLoadNotes.clicked.connect(self.loadNotes)
        self.buttonDeleteNote.clicked.connect(self.deleteNote)
        self.buttonSettings.clicked.connect(self.settings)
        self.buttonExit.clicked.connect(self.exit)

    def add_menu_button_widgets(self):
        buttonLayout = QHBoxLayout()  # Define Horizontal menu Layout
        buttonLayout.addWidget(self.buttonViewNote)
        buttonLayout.addWidget(self.buttonAddNote)
        buttonLayout.addWidget(self.buttonSearchNote)
        buttonLayout.addWidget(self.buttonSaveNotes)
        buttonLayout.addWidget(self.buttonLoadNotes)
        buttonLayout.addWidget(self.buttonDeleteNote)
        buttonLayout.addWidget(self.buttonSettings)
        buttonLayout.addWidget(self.buttonExit)
        return buttonLayout

    """
        Backend Processing Utilities
    """

    def update_notes(self, clear_data=True):
        x = -60
        y = 0
        col_count = 0
        row_count = 0
        for note in self.notesList:
            note.grid_pos = (row_count, col_count)
            col_count += 1
            if col_count == 3:
                col_count = 0
                row_count += 1

        for note in self.notesList:
            if note.grid_pos[1] > note.grid_pos[0] == 0:
                y += 80
                x = 0
            else:
                x += 60
            if not note.isVisible():
                note.re_pos(x, y)
                note.show()

        self.mainFrameUI.display_notes(self.notesList, clear_data)

    """
        EVENTS
    """

    def resizeEvent(self, event):
        self.mainFrameUI.gradient_background.updateGradient(self.width, self.height, self.gradient_start,
                                                            self.gradient_end)
