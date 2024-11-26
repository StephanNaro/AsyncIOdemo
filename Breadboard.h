// This is a header file for the Arduino sketch

const byte SERVO = 3;
const byte redLED = 5;
const byte greenLED = 6;
const byte blueLED = 11;
const byte TACTILE = 4;
const byte POTENTIOMETER = A0;


// These values do not make the results completely dbounced and jitter-free,
// but since this is only a demo I haven't bothered deciding what would be a reasonably
// error-free experience
const unsigned long debounceDelay = 50;
const int jitterTolerance = 4;


void SwitchOffRGBLEDs() {
  digitalWrite(redLED, LOW);
  digitalWrite(greenLED, LOW);
  digitalWrite(blueLED, LOW);
}
