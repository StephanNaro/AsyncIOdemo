// SPDX-License-Identifier: GPL-3.0-or-later
#include <Servo.h>
#include "Breadboard.h"
#include "comms.h"
#include "commsIO.h"

// This Arduino sketch is the backend to the GUI

Servo servo;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
  SwitchOffRGBLEDs();

  servo.attach(SERVO);

  pinMode(TACTILE, INPUT_PULLUP);

  Serial.begin(commsBaudRate);
  Serial.setTimeout(commsTimeout);
}

void loop() {
  recvWithStartEndMarkers();

  if (commsNewData == true) {
    if (msgLEDon == commsTheMessage) {
      digitalWrite(LED_BUILTIN, HIGH);
    } else if (msgLEDoff == commsTheMessage) {
      digitalWrite(LED_BUILTIN, LOW);
    } else if (msgSetServoAngle == String(commsTheMessage).substring(0, lenMsgSetServoAngle)) {
      servo.write(String(commsTheMessage).substring(lenMsgSetServoAngle).toInt());
      delay(100);
    } else if (msgSetRedLEDValue == String(commsTheMessage).substring(0, lenMsgSetRedLEDValue)) {
      analogWrite(redLED, String(commsTheMessage).substring(lenMsgSetRedLEDValue).toInt());
    } else if (msgSetGreenLEDValue == String(commsTheMessage).substring(0, lenMsgSetGreenLEDValue)) {
      analogWrite(greenLED, String(commsTheMessage).substring(lenMsgSetGreenLEDValue).toInt());
    } else if (msgSetBlueLEDValue == String(commsTheMessage).substring(0, lenMsgSetBlueLEDValue)) {
      analogWrite(blueLED, String(commsTheMessage).substring(lenMsgSetBlueLEDValue).toInt());
    } else if (msgTurnOffRGBLEDs == commsTheMessage) {
      SwitchOffRGBLEDs();
    }
    commsNewData = false;
  }
  HandleTactileButton();
  HandlePotentiometer();
}

void HandleTactileButton(void) {
  static unsigned long counter = 0;
  static unsigned long lastDebounceTime = 0;
  static int lastButtonState = HIGH;
  static int buttonState;

  int reading = digitalRead(TACTILE);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      if (buttonState == HIGH) {
        /* I prefer tallying on the Arduino and sending the current count because
           if only a simple "Button pushed" message is sent, it can be lost in transmission (or whatever),
           which will cause the receiver to be out of sync
        */
        counter++;
        sendWithStartEndMarkers(msgButtonPressedCount + counter);
      }
    }
  }
  lastButtonState = reading;
}

void HandlePotentiometer(void) {
  static int old = 0;
  int current, jitterMax, jitterMin;

  current = analogRead(POTENTIOMETER);
  jitterMax = current + jitterTolerance;      // Potentiometers jitter
  jitterMin = current - jitterTolerance;
  if (current != old) {
    if ((old <= jitterMin) || (old >= jitterMax)) {
      sendWithStartEndMarkers(msgPotentiometerReading + String(current));
      old = current;
    }
  }
}
