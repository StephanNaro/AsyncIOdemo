
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QProgressBar, QLabel, QVBoxLayout, QFrame
import comms, commsIO

class PotentiometerWidget(QFrame):
    units = ' Volts'

    def __init__(self):
        super().__init__()

        heading = QLabel("Potentiometer Value", alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.valueProgressBar = QProgressBar()
        self.valueProgressBar.setRange(0, 1023)
        self.valueText = QLabel("N/A" + self.units, alignment=Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(heading)
        layout.addWidget(self.valueProgressBar)
        layout.addWidget(self.valueText)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    @Slot(int)
    def msgReceived(self, value):
        self.valueProgressBar.setValue(value)
        volts = value * 5 / 1024
        self.valueText.setText(f'{volts:.2f}' + self.units)
