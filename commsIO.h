// SPDX-License-Identifier: GPL-3.0-or-later
#include "comms.h"

// This is a header file for the Arduino sketch

// comms.h is kept separate from commsIO.h so comms.h can be script-converted to comms.py for AsyncIOdemoGUI.py

const byte numChars = 32;
char commsTheMessage[numChars];

const int lenMsgSetServoAngle = msgSetServoAngle.length();
const int lenMsgSetRedLEDValue = msgSetRedLEDValue.length();
const int lenMsgSetGreenLEDValue = msgSetGreenLEDValue.length();
const int lenMsgSetBlueLEDValue = msgSetBlueLEDValue.length();


boolean commsNewData = false;

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char rc;
 
    while (Serial.available() > 0 && commsNewData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != msgEndMarker) {
                commsTheMessage[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                commsTheMessage[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                commsNewData = true;
            }
        }

        else if (rc == msgStartMarker) {
            recvInProgress = true;
        }
    }
}

void sendWithStartEndMarkers(String msg) {
  Serial.print(msgStartMarker + msg + msgEndMarker);
}
