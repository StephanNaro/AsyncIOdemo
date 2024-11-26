import serial
import comms

CONST_PORT = 'COM6'

CONST_lenMsgButtonPressedCount = len(comms.CONST_msgButtonPressedCount)
CONST_lenMsgPotentiometerReading = len(comms.CONST_msgPotentiometerReading)


arduino = serial.Serial(CONST_PORT, comms.CONST_commsBaudRate, 								timeout=comms.CONST_commsTimeout/10)


def sendWithStartEndMarkers(message):
    wrapped = comms.CONST_msgStartMarker + message + comms.CONST_msgEndMarker
    arduino.write(bytes(wrapped, 'utf-8'))

def recvWithStartEndMarkers():
    message = ""
    rc = arduino.read().decode()
    if (rc == comms.CONST_msgStartMarker):
        rc = arduino.read().decode()
        while (rc != comms.CONST_msgEndMarker):
            message += rc
            rc = arduino.read().decode()

    return message
