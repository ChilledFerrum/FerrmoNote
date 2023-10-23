from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QFont
from PyQt6.QtCore import QPointF


class GradientBackground(QWidget):
    def __init__(self, parent, width, height, layout, gradientStart, gradientEnd):
        super().__init__(parent)

        self.setGeometry(0, 0, width, height)
        self.parent = parent
        self.width = width
        self.height = height
        self.startColor = gradientStart
        self.endColor = gradientEnd
        #
        # self.setLayout(layout)

    def updateGradient(self, width, height, gradientStart, gradientEnd): # is called, 1) When App is Resized. 2) When App is instantiated
        # Updates the fields of the GradientBackground class and initiates a repaint event
        self.width = width
        self.height = height
        self.startColor = gradientStart
        self.endColor = gradientEnd

        self.repaint()

    def paintEvent(self, event): # Main Paint or Repaint event of the background
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

