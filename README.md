Pyxel LED Matrix Bridge

Control a 64×16 WS2812 LED matrix with Python, Pyxel and an Arduino Mega over USB Serial.

Turn your LED matrix into a tiny pixel-art display! Draw sprites in the Pyxel Editor, create animations, scroll through larger worlds and display everything on real LEDs.

Features

64×16 RGB LED display (1024 WS2812 LEDs)

Four chained 16×16 LED panels

Arduino Mega 2560 controller

USB Serial communication with Python (PySerial)

Pyxel's original 16-color palette

Python drawing API inspired by Pyxel

Sprite rendering from Pyxel image banks

Load .pyxres resources created with pyxel edit

Camera scrolling using the arrow keys

Double-buffered workflow: draw first, then show()

No Wi-Fi or internet connection required

Hardware

Component

Description

Controller

Arduino Mega 2560

Display

4 × 16×16 WS2812 LED panels

Resolution

64×16 pixels

LED count

1024

Data pin

D6

Communication

USB Serial

Power

External regulated 5V LED power supply

Important: 1024 WS2812 LEDs can draw substantial current at high brightness. Use a suitably rated external 5V supply, connect the Arduino and LED supply grounds together, and avoid powering the panels directly from the Arduino.

Project structure

panel/
├── LEDMatrix.h
├── panel.ino
└── pybridge/
    ├── pybridge.ino
    ├── LEDMatrix.h
    ├── ledmatrix.py
    ├── main.py
    ├── test.py
    └── my_resource.pyxres

LEDMatrix.h contains the physical LED mapping and drawing functions.

pybridge.ino receives frames over Serial and forwards them to the LED panels.

ledmatrix.py provides the Python drawing API.

main.py demonstrates Pyxel resource loading and camera scrolling.

Installation

1. Arduino

Install the Arduino AVR core and Adafruit NeoPixel library:

arduino-cli core install arduino:avr
arduino-cli lib install "Adafruit NeoPixel"

Compile and upload the firmware from the pybridge directory:

arduino-cli compile --fqbn arduino:avr:mega .
arduino-cli upload -p COM31 --fqbn arduino:avr:mega .

Replace COM31 with your Arduino's serial port.

2. Python

Requires Python 3 and the following dependencies:

pip install pyserial pyxel

Find your Arduino's serial port:

python -m serial.tools.list_ports -v

Configure the correct port and matching baud rate in your Python code.

Quick Start

from ledmatrix import LEDMatrix

led = LEDMatrix("COM31")

led.clear()

led.pixel(10, 5, 8)
led.rect(20, 2, 12, 10, 11)
led.line(0, 15, 63, 15, 10)

led.show()
led.close()

Colors are indexed from 0 to 15, following the original Pyxel palette.

Python Drawing API

Method

Description

led.clear(color=0)

Clear the framebuffer

led.pixel(x, y, color)

Set a pixel

led.pset(x, y, color)

Alias for pixel()

led.pget(x, y)

Read a framebuffer pixel

led.rect(x, y, w, h, color)

Draw a filled rectangle

led.rectb(x, y, w, h, color)

Draw a rectangle outline

led.line(x0, y0, x1, y1, color)

Draw a line

led.blt(x, y, img, u, v, w, h, colkey=None)

Draw a Pyxel sprite

led.show()

Transfer framebuffer to Arduino

led.close()

Close the serial connection

Drawing commands update a local Python framebuffer. The LEDs are updated only when led.show() is called.

Using Pyxel Resources

Create pixel art with the Pyxel Editor:

pyxel edit my_resource.pyxres

Load your artwork and display image bank 0:

import pyxel
from ledmatrix import LEDMatrix

pyxel.init(64, 16)
pyxel.load("my_resource.pyxres")

led = LEDMatrix("COM31")

led.clear()
led.blt(0, 0, 0, 0, 0, 64, 16)
led.show()

led.close()

The .pyxres file stores your Pyxel resources, including image banks.

Camera Scrolling

The LED display shows only 64×16 pixels, but a Pyxel image bank can contain a much larger world.

We can navigate through a 256×256 pixel image using a virtual camera.

import pyxel
from ledmatrix import LEDMatrix

WIDTH = 64
HEIGHT = 16

led = LEDMatrix("COM31")

pyxel.init(WIDTH, HEIGHT, fps=30)
pyxel.load("my_resource.pyxres")

cam_x = 0
cam_y = 0
dirty = True

def update():
    global cam_x, cam_y, dirty

    old = (cam_x, cam_y)

    if pyxel.btnp(pyxel.KEY_LEFT, 10, 2):
        cam_x -= 1
    if pyxel.btnp(pyxel.KEY_RIGHT, 10, 2):
        cam_x += 1
    if pyxel.btnp(pyxel.KEY_UP, 10, 2):
        cam_y -= 1
    if pyxel.btnp(pyxel.KEY_DOWN, 10, 2):
        cam_y += 1

    cam_x = max(0, min(cam_x, 256 - WIDTH))
    cam_y = max(0, min(cam_y, 256 - HEIGHT))

    if (cam_x, cam_y) != old:
        dirty = True

    if pyxel.btnp(pyxel.KEY_ESCAPE):
        pyxel.quit()

def draw():
    global dirty

    pyxel.cls(0)
    pyxel.blt(0, 0, 0, cam_x, cam_y, WIDTH, HEIGHT)

    if dirty:
        led.clear()
        led.blt(0, 0, 0, cam_x, cam_y, WIDTH, HEIGHT)
        led.show()
        dirty = False

try:
    pyxel.run(update, draw)
finally:
    led.close()

Use the arrow keys to move around the world. Press Escape to quit.

Only changed camera views are transmitted to the Arduino.

Serial Protocol

The Arduino firmware implements a simple binary serial protocol.

Command

Description

F

Start receiving a new frame

1024 bytes

One palette index per pixel

S

Display the received frame

C

Clear Arduino framebuffer

K

Acknowledgement sent by Arduino after S

Each frame contains 1024 bytes, ordered row by row.

The transfer format uses one byte per pixel, although only four bits are needed for the 16-color palette.

The baud rate must match on both sides. For example, both Arduino and Python can be configured for 115200 baud.

LED Mapping

Four 16×16 panels are arranged horizontally:

+----------+----------+----------+----------+
| Panel 0  | Panel 1  | Panel 2  | Panel 3  |
|  16x16   |  16x16   |  16x16   |  16x16   |
+----------+----------+----------+----------+

              Total: 64x16

Each panel uses a serpentine (zigzag) wiring pattern.

The first row runs from right to left, the next from left to right, alternating on each row.

The mapping is implemented in LEDMatrix.h and can be adapted for other panel arrangements.

Performance

A complete frame consists of 1024 bytes.

Approximate hardware timings:

WS2812 refresh: 30.8 ms for 1024 LEDs

Serial transfer at 115200 baud: approximately 88.9 ms

Serial transfer at 500000 baud: approximately 20.5 ms

These are theoretical timings, excluding software overhead and communication delays. Actual frame rates depend on the board, serial connection and firmware.

The Python bridge waits for an acknowledgement after show().

Troubleshooting

Could not open COM port

Check the available ports:

python -m serial.tools.list_ports -v

Make sure the Arduino Serial Monitor is closed.

Timeout: Keine Bestätigung vom Arduino

Verify that the bridge firmware is uploaded, the baud rates match and the selected COM port is correct.

Incorrect pixel positions

Check the panel order and serpentine mapping in LEDMatrix.h.

No image from Pyxel Editor

Make sure the resource is loaded and the artwork is stored in the expected image bank and coordinates.

Future Ideas

Framebuffer mirroring directly from Pyxel

Dirty rectangle updates

Packed 4-bit color transmission

Tilemap rendering and scrolling

Sprite animation

Keyboard-controlled LED games

Higher frame rates through protocol optimization

Support for additional display sizes

Dependencies

Pyxel

PySerial

Adafruit NeoPixel

Arduino CLI

License

No license has been specified yet.

Made for experimenting with pixel art, retro games, Python and real hardware.
