from PyQt6.QtWidgets import QScrollArea, QVBoxLayout
from PyQt6.QtCore import Qt
from style_util import GradientBackground


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

