from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QLinearGradient
from PyQt6.QtCore import QPointF


class GradientBackground(QWidget):
    def __init__(self, parent, width, height, layout, gradientStart, gradientEnd):
        super().__init__(parent)

        self.setGeometry(15, 15, width, height)
        self.parent = parent
        self.width = width
        self.height = height
        self.startColor = gradientStart
        self.endColor = gradientEnd

        self.setLayout(layout)

    def updateGradient(self, width, height, gradientStart, gradientEnd):
        self.width = width
        self.height = height
        self.startColor = gradientStart
        self.endColor = gradientEnd

        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        start_point = QPointF(self.rect().left() - 100, self.rect().top())
        end_point = QPointF(self.rect().left() - 100, self.rect().bottom())
        gradient = QLinearGradient(start_point, end_point)
        sr, sg, sb = self.startColor
        er, eg, eb = self.endColor
        gradient.setColorAt(0.0, QColor(sr, sg, sb))
        gradient.setColorAt(0.50, QColor(er, eg, eb))
        gradient.setColorAt(1, QColor(sr, sg, sb))
        painter.fillRect(self.rect(), gradient)

    def resizeEvent(self, event):
        self.updateGradient(self.width, self.height, self.startColor, self.endColor)
        super().resizeEvent(event)
