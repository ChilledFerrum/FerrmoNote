import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Widget with Layout")
        self.setGeometry(100, 100, 400, 400)

        # Create a QVBoxLayout to hold widgets
        self.layout = QVBoxLayout()
        self.labels = []

        # Create labels to add to the layout
        self.add_labels()

        # Create a button to update the layout
        update_button = QPushButton("Update Layout")
        update_button.clicked.connect(self.update_layout)
        self.layout.addWidget(update_button)

        self.setLayout(self.layout)

    def add_labels(self):
        for i in range(5):
            label = QLabel(f"Label {i}")
            self.layout.addWidget(label)
            self.labels.append(label)

    def clear_layout(self):
        # Remove all items from the layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def update_layout(self):
        # Clear the existing contents from the layout
        self.clear_layout()

        # Add new or updated widgets
        update_button = QPushButton("Update Layout")
        update_button.clicked.connect(self.update_layout)
        for i in range(5):
            updated_label = QLabel(f"Updated Label {i}")
            self.layout.addWidget(updated_label)
            self.layout.addWidget(update_button)
            self.labels.append(updated_label)


def main():
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()