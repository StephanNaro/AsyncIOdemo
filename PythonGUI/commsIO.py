from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtSerialPort import QSerialPort
import comms

CONST_PORT = 'COM4'

CONST_lenMsgButtonPressedCount = len(comms.CONST_msgButtonPressedCount)
CONST_lenMsgPotentiometerReading = len(comms.CONST_msgPotentiometerReading)

def sendWithStartEndMarkers(serial_port, message):
    """Send a message with start and end markers using the provided QSerialPort."""
    wrapped = comms.CONST_msgStartMarker + message + comms.CONST_msgEndMarker
    serial_port.write(wrapped.encode('ascii'))

class CommsWorker(QObject):
    buttonPressedSignal = Signal(int)
    potentiometerSignal = Signal(int)
    errorSignal = Signal(str)
    finished = Signal()

    def __init__(self, port_name, baud_rate):
        super().__init__()
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.serial = None
        self.buffer = ""
        self.isRunning = True

    @Slot()
    def start(self):
        """Initialize and open the serial port in the worker thread."""
        self.serial = QSerialPort()
        self.serial.setPortName(self.port_name)
        self.serial.setBaudRate(self.baud_rate)
        self.serial.readyRead.connect(self.handleReadyRead)
        self.serial.errorOccurred.connect(self.handleSerialError)

        if not self.serial.open(QSerialPort.ReadWrite):
            self.errorSignal.emit(f"Failed to open port {self.port_name}: {self.serial.errorString()}")
            self.finished.emit()
            return

    @Slot()
    def handleReadyRead(self):
        """Process incoming serial data."""
        while self.serial.bytesAvailable() and self.isRunning:
            # Read all available data
            data = self.serial.readAll().data().decode('ascii', errors='ignore')
            self.buffer += data
            # Process complete messages
            while comms.CONST_msgStartMarker in self.buffer and comms.CONST_msgEndMarker in self.buffer:
                start_idx = self.buffer.find(comms.CONST_msgStartMarker) + len(comms.CONST_msgStartMarker)
                end_idx = self.buffer.find(comms.CONST_msgEndMarker)
                if end_idx < start_idx:
                    # Malformed message, clear up to end marker
                    self.buffer = self.buffer[end_idx + len(comms.CONST_msgEndMarker):]
                    continue
                msg = self.buffer[start_idx:end_idx]
                self.buffer = self.buffer[end_idx + len(comms.CONST_msgEndMarker):]
                # Process the message
                if msg.startswith(comms.CONST_msgButtonPressedCount):
                    try:
                        value = int(msg[CONST_lenMsgButtonPressedCount:])
                        self.buttonPressedSignal.emit(value)
                    except ValueError:
                        print(f"Invalid button count: {msg}")
                elif msg.startswith(comms.CONST_msgPotentiometerReading):
                    try:
                        value = int(msg[CONST_lenMsgPotentiometerReading:])
                        self.potentiometerSignal.emit(value)
                    except ValueError:
                        print(f"Invalid potentiometer value: {msg}")

    @Slot(str)
    def sendMessage(self, message):
        """Send a message to the Arduino."""
        if self.isRunning and self.serial and self.serial.isOpen():
            sendWithStartEndMarkers(self.serial, message)

    @Slot()
    def handleSerialError(self, error):
        """Handle serial port errors."""
        if error != QSerialPort.NoError:
            self.errorSignal.emit(f"Serial error: {self.serial.errorString()}")
            self.stop()

    def stop(self):
        """Stop the worker and close the serial port."""
        self.isRunning = False
        if self.serial:
            self.serial.close()
        self.finished.emit()
