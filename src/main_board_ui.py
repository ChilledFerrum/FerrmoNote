from PyQt6.QtWidgets import QScrollArea, QVBoxLayout
from PyQt6.QtCore import Qt
from src.style_util import GradientBackground


class ScrollableTransparentBackground(QScrollArea):
    def __init__(self, width, height, layout, gradientStart, gradientEnd, parent=None):
        super().__init__(parent)
        self.startColor = gradientStart
        self.endColor = gradientEnd

        self.gradient_background = GradientBackground(self, width, height, layout, gradientStart, gradientEnd)
        # Set the grid layout as the layout of ScrollableTransparentBackground
        self.setLayout(layout)

        self.gradient_background.setFixedSize(width, height)
        self.setWidget(self.gradient_background)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def resizeEvent(self, event): # RESIZES BACKGROUND DURING APP RESIZE EVENT
        self.gradient_background.setFixedSize(self.width(), self.height())
        self.gradient_background.updateGradient(self.width(), self.height(), self.startColor, self.endColor)

        super().resizeEvent(event)
