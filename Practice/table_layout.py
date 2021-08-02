import sys

from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
    QSizePolicy,
)

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGridLayout Example")
        # Create a QGridLayout instance
        layout = QGridLayout()
        # Add widgets to the layout
        alignment = Qt.AlignHCenter | Qt.AlignVCenter
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)

        for i in range(9):

            b = QPushButton(f"Button at ({i//3}, {i%3})")
            b.setSizePolicy(sizePolicy)
            b = layout.addWidget(b, i // 3, i % 3, alignment)

            # layout.addWidget(QPushButton("Button at (0, 1)"), 0, 1, alignment)
            # layout.addWidget(QPushButton("Button at (0, 2)"), 0, 2, alignment)
            # layout.addWidget(QPushButton("Button at (1, 0)"), 1, 0, alignment)
            # layout.addWidget(QPushButton("Button at (1, 1)"), 1, 1, alignment)
            # layout.addWidget(QPushButton("Button at (1, 2)"), 1, 2, alignment)
            # layout.addWidget(QPushButton("Button at (2, 0)"), 2, 0, alignment)
            # layout.addWidget(QPushButton("Button at (2, 1)"), 2, 1, alignment)
            # layout.addWidget(QPushButton("Button at (2, 2)"), 2, 2, alignment)
        # Set the layout on the application's window
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
