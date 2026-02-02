from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication

import sys

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
button = QPushButton("Click Me")
layout.addWidget(button)
window.setLayout(layout)
window.show()

sys.exit(app.exec())