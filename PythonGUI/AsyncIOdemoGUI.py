import sys
from PySide6.QtCore import Qt, QThread, Signal, Slot, QObject
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLayout
import ServoWidget, RGBLEDWidget, OnboardLEDWidget, TactileSwitchWidget, PotentiometerWidget
import comms, commsIO

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GUI for Arduino Async IO demo')

        # Create GUI elements
        heading = QLabel("Arduino GUI demo", alignment=Qt.AlignHCenter | Qt.AlignTop)
        heading.setStyleSheet('font-size: 30px')
        servoWidget = ServoWidget.ServoWidget()
        rgbLEDWidget = RGBLEDWidget.RGBLEDWidget()
        ledWidget = OnboardLEDWidget.OnboardLEDWidget()
        self.tactileSwitchWidget = TactileSwitchWidget.TactileSwitchWidget()
        self.potentiometerWidget = PotentiometerWidget.PotentiometerWidget()

        # Set up layout
        layout = QGridLayout()
        layout.addWidget(heading, 0, 0, 1, 2)
        layout.addWidget(servoWidget, 1, 0)
        layout.addWidget(ledWidget, 1, 1)
        layout.addWidget(rgbLEDWidget, 2, 0, 3, 1)
        layout.addWidget(self.tactileSwitchWidget, 2, 1)
        layout.addWidget(self.potentiometerWidget, 3, 1, 2, 1)
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)

        # Set up thread and worker
        self.thread = QThread()
        self.worker = commsIO.CommsWorker(commsIO.CONST_PORT, comms.CONST_commsBaudRate)
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.thread.started.connect(self.worker.start)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.buttonPressedSignal.connect(self.tactileSwitchWidget.msgReceived)
        self.worker.potentiometerSignal.connect(self.potentiometerWidget.msgReceived)
        self.worker.errorSignal.connect(self.handleWorkerError)

        # Connect widget signals for sending messages
        servoWidget.servoAngleSignal.connect(self.worker.sendMessage)
        rgbLEDWidget.redValueSignal.connect(self.worker.sendMessage)
        rgbLEDWidget.greenValueSignal.connect(self.worker.sendMessage)
        rgbLEDWidget.blueValueSignal.connect(self.worker.sendMessage)
        rgbLEDWidget.turnOffSignal.connect(self.worker.sendMessage)
        ledWidget.ledStateSignal.connect(self.worker.sendMessage)

        # Start the thread
        self.thread.start()

    @Slot(str)
    def handleWorkerError(self, error_message):
        """Display serial port errors on the console."""
        print(error_message)

    def closeEvent(self, event):
        """Handle window close event to clean up the thread."""
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
