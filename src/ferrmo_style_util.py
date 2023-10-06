from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QLinearGradient
from PyQt6.QtCore import QPointF, Qt


class GradientBackground(QWidget):
    def __init__(self, parent, width, height, gradientStart, gradientEnd):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.startColor = gradientStart
        self.endColor = gradientEnd

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Convert the coordinates to QPointF objects
        start_point = QPointF(self.rect().left()-100, self.rect().top())
        end_point = QPointF(self.rect().left()-100, self.rect().bottom())
        gradient = QLinearGradient(start_point, end_point)
        sr, sg, sb = self.startColor
        er, eg, eb = self.endColor
        gradient.setColorAt(0.0, QColor(sr, sg, sb))# start
        gradient.setColorAt(0.50, QColor(er, eg, eb))# end
        gradient.setColorAt(1, QColor(sr, sg, sb))# start
        painter.fillRect(self.rect(), gradient)
