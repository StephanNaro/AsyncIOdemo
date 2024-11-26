#ifndef COMMS_H                 // This is a header file for the Arduino sketch
#define COMMS_H

const long commsBaudRate = 115200;
const long commsTimeout = 1;

const char msgStartMarker = '<';
const char msgEndMarker = '>';

const String msgSetServoAngle = "SetServoAngle: ";
const String msgSetRedLEDValue = "SetRedLEDValue: ";
const String msgSetGreenLEDValue = "SetGreenLEDValue: ";
const String msgSetBlueLEDValue = "SetBlueLEDValue: ";
const String msgTurnOffRGBLEDs = "TurnOffRGBLEDs";
const String msgLEDon = "SwitchLEDon";
const String msgLEDoff = "SwitchLEDoff";
const String msgButtonPressedCount = "ButtonPressedCount: ";
const String msgPotentiometerReading = "PotentiometerReading: ";

#endif