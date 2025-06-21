from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QLabel, QVBoxLayout, QFrame
import comms, commsIO

class TactileSwitchWidget(QFrame):
    spacer = '     '

    def __init__(self):
        super().__init__()

        heading = QLabel("Button Pressed", alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.counterText = QLabel("N/A" + self.spacer, alignment=Qt.AlignRight)

        layout = QVBoxLayout(self)
        layout.addWidget(heading)
        layout.addWidget(self.counterText)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    @Slot(int)
    def msgReceived(self, count):
        self.counterText.setText(str(count) + self.spacer)
