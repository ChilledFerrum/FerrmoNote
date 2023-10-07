from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QFont


class FerrmoButton(QPushButton):
    def __init__(self, parent, text="Undefined", font_size=12, bg="#171924", width=80, height=30,
                 fg="white", pressedColor="#041f3d"):
        super().__init__(text, parent)
        self.pressedColor = pressedColor
        self.width = width
        self.height = height
        self.defaultColor = bg
        self.defaultFg = fg
        self.setFont(QFont("Arial", font_size, QFont.Weight.Bold))
        self.setStyleSheet(f"background-color: {bg}; color: {fg}; width: {width}px; height: {height}px;"
                           f"border: 2px; border-style: solid; border-color: {pressedColor}; border-radius:5px;")
        self.setFlat(True)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == QEvent.Type.MouseButtonPress:
                self.setStyleSheet(f"background-color: {self.pressedColor}; color: {self.defaultFg}; "
                                   f"width: {self.width}; height: {self.height};"
                                   f"border: 2px; border-style: solid;  border-color: {self.pressedColor}; border-radius:5px")
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self.setStyleSheet(f"background-color: {self.defaultColor}; color: {self.defaultFg}; "
                                   f"width: {self.width}; height: {self.height};"
                                   f"border: 2px; border-style: solid;  border-color: {self.pressedColor}; border-radius:5px;")

        return super().eventFilter(obj, event)
