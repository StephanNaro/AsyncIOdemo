// SPDX-License-Identifier: GPL-3.0-or-later
#ifndef COMMS_H
#define COMMS_H

// This is a header file for the Arduino sketch

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
