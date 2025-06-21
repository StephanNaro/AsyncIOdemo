from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QLabel, QSlider, QPushButton, QGridLayout, QFrame
import comms, commsIO

class ServoWidget(QFrame):
    servoAngleSignal = Signal(str)  # Emits "SetServoAngle: <value>"

    def __init__(self):
        super().__init__()

        heading = QLabel("Set Servo Angle", alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 180)
        self.button = QPushButton("Send Angle")
        self.button.clicked.connect(self.button_clicked)

        layout = QGridLayout(self)
        layout.addWidget(heading, 0, 0, 1, 2)
        layout.addWidget(self.slider, 1, 0)
        layout.addWidget(self.button, 1, 1)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    @Slot()
    def button_clicked(self):
        angle = str(self.slider.value())
        self.servoAngleSignal.emit(comms.CONST_msgSetServoAngle + angle)
