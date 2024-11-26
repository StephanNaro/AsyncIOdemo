from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QFrame
import comms, commsIO

class OnboardLEDWidget(QFrame):
    def __init__(self):
        super().__init__()

        heading = QLabel("Toggle onboard LED", alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.button = QPushButton("On")
        self.button.setCheckable(True)
        self.button.toggled.connect(self.button_toggled)

        layout = QVBoxLayout(self)
        layout.addWidget(heading)
        layout.addWidget(self.button)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def button_toggled(self):
        if self.button.isChecked():
            commsIO.sendWithStartEndMarkers(comms.CONST_msgLEDon)
            self.button.setText("Off")
        else:
            commsIO.sendWithStartEndMarkers(comms.CONST_msgLEDoff)
            self.button.setText("On")
