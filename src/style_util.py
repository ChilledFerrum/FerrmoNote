from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout,
                             QPushButton)
from PyQt6.QtGui import (QPainter, QColor, QLinearGradient,
                         QFont, QIcon)
from PyQt6.QtCore import QPointF, QTimer, Qt, QSize


class GradientBackground(QWidget):
    def __init__(self, width, height, gradientStart, gradientEnd):
        super().__init__()
        self.startColor = gradientStart
        self.endColor = gradientEnd
        self.width = width
        self.height = height

    def updateGradient(self, width, height, gradientStart,
                       gradientEnd):  # is called, 1) When App is Resized. 2) When App is instantiated
        # Updates the fields of the GradientBackground class and initiates a repaint event
        self.width = width
        self.height = height
        self.startColor = gradientStart
        self.endColor = gradientEnd
        self.setContentsMargins(0, 0, 0, 0)
        self.repaint()

    def paintEvent(self, event):  # Main Paint or Repaint event of the background
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        start_point = QPointF(self.rect().left(), self.rect().top())
        end_point = QPointF(self.rect().left(), self.rect().bottom())
        gradient = QLinearGradient(start_point, end_point)
        sr, sg, sb = self.startColor
        er, eg, eb = self.endColor
        gradient.setColorAt(0.0, QColor(sr, sg, sb))
        gradient.setColorAt(0.50, QColor(er, eg, eb))
        gradient.setColorAt(1, QColor(sr, sg, sb))
        painter.fillRect(self.rect(), gradient)

    def resizeEvent(self, event):  # Main Event Function, is called, 1) When App is Resized. 2) When App is instantiated
        self.updateGradient(self.width, self.height, self.startColor, self.endColor)
        super().resizeEvent(event)


class Message(QWidget):
    def __init__(self, title, message, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QGridLayout())
        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet("font-size: 18px; font-weight: bold; padding: 0; text-align:center;")
        self.messageLabel = QLabel(message, self)
        self.messageLabel.setStyleSheet("font-size: 12px; font-weight: normal; padding: 0; text-align: center;")

        # Button
        self.buttonClose = QPushButton(self)
        self.buttonClose.setIcon(QIcon("style/close_icon.png"))
        self.buttonClose.setFlat(True)
        self.buttonClose.setFixedSize(32, 32)
        self.buttonClose.setIconSize(QSize(16, 16))

        self.layout().addWidget(self.titleLabel)
        self.layout().addWidget(self.messageLabel, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.layout().addWidget(self.buttonClose, 0, 1, alignment=Qt.AlignmentFlag.AlignHCenter)


class Notification(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent=None)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.mainLayout = QVBoxLayout(self)

    def setNotify(self, title, description, color, timeout):
        self.m = Message(title, description)
        self.mainLayout.addWidget(self.m, alignment=Qt.AlignmentFlag.AlignHCenter)
        r, g, b = color
        self.setStyleSheet(f"background: rgb({r}, {g}, {b}); padding: 0;")
        self.m.buttonClose.clicked.connect(self.onClicked)
        self.show()
        QTimer.singleShot(timeout, self.closeMe)

    def closeMe(self):
        self.close()
        self.m.close()

    def onClicked(self):
        self.close()


class FerrmoLabel(QLabel):
    def __init__(self, text="", font_family="Segoe UI", font_size=10, color="#000000", is_bold=False):
        super().__init__()
        font = QFont(font_family, font_size)
        font.setBold(is_bold)
        self.setFont(font)
        self.setText(text)
        self.setColor(color)

    def setColor(self, color):
        self.setStyleSheet(f"color:{color}")
    # def stylize_Label(self):
    #     style_sheet = """
    #
    #     """
