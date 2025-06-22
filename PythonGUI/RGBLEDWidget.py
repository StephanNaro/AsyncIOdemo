# SPDX-License-Identifier: GPL-3.0-or-later
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QLabel, QSlider, QPushButton, QGridLayout, QFrame
import comms, commsIO

class RGBLEDWidget(QFrame):
    redValueSignal = Signal(str)    # Emits "SetRedLEDValue: <value>"
    greenValueSignal = Signal(str)  # Emits "SetGreenLEDValue: <value>"
    blueValueSignal = Signal(str)   # Emits "SetBlueLEDValue: <value>"
    turnOffSignal = Signal(str)     # Emits "TurnOffRGBLEDs"

    def __init__(self):
        super().__init__()

        heading = QLabel("RGB LED Values", alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.redSlider = QSlider(Qt.Orientation.Horizontal)
        self.redSlider.setRange(0, 255)
        self.redButton = QPushButton("Send Red Value")
        self.redButton.setStyleSheet('QPushButton {color: red;}')
        self.redButton.clicked.connect(self.redButton_clicked)
        self.greenSlider = QSlider(Qt.Orientation.Horizontal)
        self.greenSlider.setRange(0, 255)
        self.greenButton = QPushButton("Send Green Value")
        self.greenButton.setStyleSheet('QPushButton {color: green;}')
        self.greenButton.clicked.connect(self.greenButton_clicked)
        self.blueSlider = QSlider(Qt.Orientation.Horizontal)
        self.blueSlider.setRange(0, 255)
        self.blueButton = QPushButton("Send Blue Value")
        self.blueButton.setStyleSheet('QPushButton {color: blue;}')
        self.blueButton.clicked.connect(self.blueButton_clicked)
        self.offButton = QPushButton("Turn Off RGB LEDs")
        self.offButton.clicked.connect(self.offButton_clicked)

        layout = QGridLayout(self)
        layout.addWidget(heading, 0, 0, 1, 2)
        layout.addWidget(self.redSlider, 1, 0)
        layout.addWidget(self.redButton, 1, 1)
        layout.addWidget(self.greenSlider, 2, 0)
        layout.addWidget(self.greenButton, 2, 1)
        layout.addWidget(self.blueSlider, 3, 0)
        layout.addWidget(self.blueButton, 3, 1)
        layout.addWidget(self.offButton, 4, 1)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    @Slot()
    def redButton_clicked(self):
        value = str(self.redSlider.value())
        self.redValueSignal.emit(comms.CONST_msgSetRedLEDValue + value)

    @Slot()
    def greenButton_clicked(self):
        value = str(self.greenSlider.value())
        self.greenValueSignal.emit(comms.CONST_msgSetGreenLEDValue + value)

    @Slot()
    def blueButton_clicked(self):
        value = str(self.blueSlider.value())
        self.blueValueSignal.emit(comms.CONST_msgSetBlueLEDValue + value)

    @Slot()
    def offButton_clicked(self):
        self.turnOffSignal.emit(comms.CONST_msgTurnOffRGBLEDs)
