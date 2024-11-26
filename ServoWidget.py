from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QFrame
import comms, commsIO

class ServoWidget(QFrame):
    def __init__(self):
        super().__init__()

        heading = QLabel("Set Servo Angle", alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.line_edit = QLineEdit()
        self.button = QPushButton("Send Angle")
        self.button.clicked.connect(self.button_clicked)

        layout = QGridLayout(self)
        layout.addWidget(heading, 0, 0, 1 ,2)
        layout.addWidget(self.line_edit, 1, 0)
        layout.addWidget(self.button, 1, 1)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def button_clicked(self):
        commsIO.sendWithStartEndMarkers(comms.CONST_msgSetServoAngle + self.line_edit.text())
