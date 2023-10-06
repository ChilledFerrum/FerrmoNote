import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QScrollArea
from src.ferrmo_buttons import FerrmoButton
from src.ferrmo_notes import FerrmoNote
from PyQt6.QtWidgets import QSizePolicy
from src.main_board_ui import ScrollableTransparentBackground

menuColor = "#171924"


class Ferrmo(QWidget):
    def __init__(self, size):
        super().__init__()
        self.mainFrame = None  # Entire App Frame

        self.mainFrameUI = None  # Main Frame UI Contains Note History
        self.scroll_area = QScrollArea()  # Scroll area for mainFrameUI

        self.gridLayout = None  # Grid Layout to hold Note History
        self.setWindowTitle("Ferrmo")
        self.width = size[0]
        self.height = size[1]
        self.gradient_start = (0, 0, 0)
        self.gradient_end = (142, 142, 142)

        # Refresh with each update
        self.update()

        self.openedUIs = dict({
            "viewNotes": False,
            "addNotes": False,
            "searchNote": False,
            "saveNotes": False,
            "deleteNotes": False,
            "settings": False,
        })
        # Main Layout
        self.mainLayout = None
        self.appInit()

        # Side Bar Content
        self.sideBar_minHeight = 50
        self.frameSideBar = None
        self.notesList = []

        self.buttonViewNotes = None
        self.buttonAddNote = None
        self.buttonSearchNote = None
        self.buttonSaveNotes = None
        self.buttonDeleteNote = None
        self.buttonSettings = None
        self.buttonExit = None

        self.createMainUI()

        self.currentNote = None

    def appInit(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # self.mainFrame = GradientBackground(self, self.width, self.height, self.gradient_start, self.gradient_end)
        # self.mainFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Set size policy

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        center_x = screen_geometry.width() // 2
        center_y = screen_geometry.height() // 2
        offset_x = center_x - int(self.width / 2) - 100
        offset_y = center_y - int(self.height / 2)

        self.setGeometry(offset_x, offset_y, self.width, self.height)
        self.setWindowOpacity(0.93)
        # self.updateBackground()

    def createMainUI(self):
        # Side Bar Content
        self.frameSideBar = QWidget(self)
        self.frameSideBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Set size policy

        self.frameSideBar.setMinimumHeight(self.sideBar_minHeight)
        self.frameSideBar.setMaximumHeight(self.sideBar_minHeight)
        self.frameSideBar.setStyleSheet(f"background-color: {menuColor};")

        # Main Frame Initializing
        self.gridLayout = QGridLayout()
        self.mainFrameUI = ScrollableTransparentBackground(self.width - 30, self.height - self.sideBar_minHeight - 30,
                                                           self.gridLayout, self.gradient_start, self.gradient_end,
                                                           self)
        self.notesList = []

        buttonLayout = QHBoxLayout()
        self.buttonViewNotes = FerrmoButton(self.frameSideBar,
                                            text="View Notes",
                                            font_size=10,
                                            bg=menuColor, pressedColor="#036194")
        self.buttonViewNotes.clicked.connect(self.viewNotes)
        buttonLayout.addWidget(self.buttonViewNotes)

        self.buttonAddNote = FerrmoButton(self.frameSideBar,
                                          text="Add Notes",
                                          font_size=10,
                                          bg=menuColor, pressedColor="#069647")
        self.buttonAddNote.clicked.connect(self.addNote)
        buttonLayout.addWidget(self.buttonAddNote)

        self.buttonSearchNote = FerrmoButton(self.frameSideBar,
                                             text="Search Note",
                                             font_size=10,
                                             bg=menuColor, pressedColor="#036194")
        self.buttonSearchNote.clicked.connect(self.searchNote)
        buttonLayout.addWidget(self.buttonSearchNote)

        self.buttonSaveNotes = FerrmoButton(self.frameSideBar,
                                            text="Save Notes",
                                            font_size=10,
                                            bg=menuColor, pressedColor="#069647")
        self.buttonSaveNotes.clicked.connect(self.saveNote)
        buttonLayout.addWidget(self.buttonSaveNotes)

        self.buttonDeleteNote = FerrmoButton(self.frameSideBar,
                                             text="Delete Note",
                                             font_size=10,
                                             bg=menuColor, pressedColor='#940303')
        self.buttonDeleteNote.clicked.connect(self.deleteNote)
        buttonLayout.addWidget(self.buttonDeleteNote)

        self.buttonSettings = FerrmoButton(self.frameSideBar,
                                           text="Settings",
                                           bg=menuColor, pressedColor="#036194")
        self.buttonSettings.clicked.connect(self.settings)
        buttonLayout.addWidget(self.buttonSettings)

        self.buttonExit = FerrmoButton(self.frameSideBar,
                                       text="Exit",
                                       font_size=17,
                                       bg=menuColor, pressedColor="orange")
        self.buttonExit.clicked.connect(self.exit)
        buttonLayout.addWidget(self.buttonExit)

        self.frameSideBar.setContentsMargins(0, 0, 0, 0)
        self.frameSideBar.setLayout(buttonLayout)

        self.mainLayout.addWidget(self.mainFrameUI)
        self.mainLayout.addWidget(self.frameSideBar)

    def viewNotes(self, event):
        self.update_notes()
        print("Clicked View Notes!")

    def addNote(self, event):
        new_Note = FerrmoNote(self)

        new_Note.createNote(width=80, height=80)
        if self.notesList:
            new_Note.id = self.notesList[-1].id + 1
        else:
            new_Note.id = 0
        new_Note.changeName()

        self.notesList.append(new_Note)
        print("Clicked add Note!")

    def searchNote(self, event):
        print("Clicked Search Note!")

    def saveNote(self, event):
        print("Clicked Save Note!")

    def deleteNote(self, event):
        print("Clicked Delete Note!")

    def settings(self, event):
        print("Clicked Settings!")

    def exit(self, event):
        print("Clicked Exit!")
        sys.exit(1)

    # def

    def update_notes(self):
        x = -80
        y = 0

        col_count = 0
        row_count = 0
        for note in self.notesList:
            note.grid_pos = (row_count, col_count)
            col_count += 1
            if col_count == 6:
                col_count = 0
                row_count += 1

        for note in self.notesList:
            if note.grid_pos[1] > note.grid_pos[0] == 0:
                y += 110
                x = 0
            else:
                x += 80
            if not note.isVisible():
                note.re_pos(x, y)
                note.show()

            self.gridLayout.addWidget(note, note.grid_pos[0], note.grid_pos[1])
        self.mainFrameUI.setLayout(self.gridLayout)

    """
        EVENTS
    """
    def resizeEvent(self, event):
        # self.mainFrameUI.updateGradient(self.width, self.height, self.gradient_start, self.gradient_end)
        pass