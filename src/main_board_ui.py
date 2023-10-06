from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout
from PyQt6.QtGui import QPainter, QColor, QLinearGradient
from PyQt6.QtCore import QPointF, Qt


class ScrollableTransparentBackground(QScrollArea):
    def __init__(self, width, height, layout, gradientStart, gradientEnd, parent=None):
        super().__init__(parent)
        self.startColor = gradientStart
        self.endColor = gradientEnd

        self.gradient_background = GradientBackground(self, width, height, layout, gradientStart, gradientEnd)
        self.gradient_background.setLayout(layout)

        self.gradient_background.setFixedSize(width, height)
        self.setWidget(self.gradient_background)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setLayout(QVBoxLayout())  # Set layout for ScrollableTransparentBackground

    def resizeEvent(self, event):
        print("Changed")
        self.gradient_background.setFixedSize(self.width(), self.height())
        self.gradient_background.updateGradient(self.width(), self.height(), self.startColor, self.endColor)

        super().resizeEvent(event)


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
