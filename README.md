# What

A demonstration of interaction between an Arduino and a PC via a COM port (most likely a USB cable).

The GUI can instruct the Arduino to do 3 things and it can display 2 types of data received from the Arduino:
- Set a servo angle;
- Set the brightness on three (red, green, and blue) LEDs or turn them off;
- Toggle the Arduino's onboard LED on / off;
- Display a tally of presses of a tactile button switch;
- Display the level and voltage of a potentiometer.



# Inspiration

I don't remember whether I went looking for something or if a YouTube suggestion looked interesting, but I started this project by following along with this playlist: [Arduino GUI Using C#](https://www.youtube.com/playlist?list=PLDxm-EGn62t7indrQcJGBchHJCJqTWdGP) on the Byte Me channel.



# Additional resources

I wasn't going to bother with a 10-day free trial of Qt for C++ (and anyway I already had a little familiarity with Pyside6) so I decided to write it in python, which meant that a few things had to be done differently. For some of those things I needed to search DuckDuckGo and YouTube for solutions, among them:
## Asynchronous serial monitoring:
- [Serial Input Basics on Arduino](https://forum.arduino.cc/t/serial-input-basics-updated/382007)
- [Monitoring the COM port in the background while running a GUI](https://www.youtube.com/watch?v=HKgk4i8u8nk) (this took me a whole day to find)
- [Ending a Thread](https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread)



# Wiring

Since the videos in the inspiration did not include wiring diagrams, I set things up my own way.

One thing that did not work the way Byte Me had wired it was the tactile button switch. I don't know how to express this as an engineer would, but:
- two and two pins of the switch are permanently connected even while the button isn't pressed
- so if we call one pair A1 and A2, and the other pair B1 and B2
- then on the breadboard I connected
	- A1 to 5V;
	- B1 via a 10 kΩ resistor to GND;
	- and B2 to pin 4 on the Arduino.

For the rest of the wiring please see the accompanying photo and the Breadboard.h file.



# TO DO

It looks like I can use QGroupBox to make the GUI look more like in the playlist, thus better, but I don't feel like figuring that out too. If anyone cares to show me how, I'd probably appreciate it.
