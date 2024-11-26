import sys, threading
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLayout, QGridLayout
import ServoWidget, RGBLEDWidget, OnboardLEDWidget, TactileSwitchWidget, PotentiometerWidget
import comms, commsIO

CONST_PORT = 'COM6'

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GUI for Arduino Async IO demo')

        heading = QLabel("Arduino GUI demo",
                      alignment=Qt.AlignHCenter | Qt.AlignTop)
        heading.setStyleSheet('font-size: 30px')
        servoWidget = ServoWidget.ServoWidget()
        rgbLEDWidget = RGBLEDWidget.RGBLEDWidget()
        ledWidget = OnboardLEDWidget.OnboardLEDWidget()
        self.tactileSwitchWidget = TactileSwitchWidget.TactileSwitchWidget()
        self.potentiometerWidget = PotentiometerWidget.PotentiometerWidget()

        layout = QGridLayout()
        layout.addWidget(heading, 0, 0, 1, 2)
        layout.addWidget(servoWidget, 1, 0)
        layout.addWidget(ledWidget, 1, 1)
        layout.addWidget(rgbLEDWidget, 2, 0, 3, 1)
        layout.addWidget(self.tactileSwitchWidget, 2, 1)
        layout.addWidget(self.potentiometerWidget, 3, 1, 2, 1)
        layout.setSizeConstraint(QLayout.SetFixedSize);
        self.setLayout(layout)

        self.thread = threading.Thread(target=self.commsMonitorThread)
        self.thread.start()

    def commsMonitorThread(self):
        # Much, if not all, of this should be moved into commsIO.recvWithStartEndMarkers(),
        # but I am not in the mood for figuring out the necessary signalling or whatever it would take
        self._stopMonitorThread = False
        self._monitorThreadIsRunning = True;
        while not self._stopMonitorThread:
            msg = commsIO.recvWithStartEndMarkers()
            if (comms.CONST_msgButtonPressedCount == msg[:commsIO.CONST_lenMsgButtonPressedCount]):
                    self.tactileSwitchWidget.msgReceived(msg[commsIO.CONST_lenMsgButtonPressedCount:])
            elif (comms.CONST_msgPotentiometerReading == msg[:commsIO.CONST_lenMsgPotentiometerReading]):
                    self.potentiometerWidget.msgReceived(int(msg[commsIO.CONST_lenMsgPotentiometerReading:]))

        self._monitorThreadIsRunning = False

    def stopMonitorThread(self):
        self._stopMonitorThread = True
        while self._monitorThreadIsRunning:
            ...


if __name__ == "__main__":
    app = QApplication([])

    window = MyWidget()
    window.show()

    exit_code = app.exec()
    window.stopMonitorThread()
    sys.exit(exit_code)
