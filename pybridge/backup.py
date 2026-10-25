
import pyxel
from ledmatrix import LEDMatrix

led = LEDMatrix("COM31")

pyxel.init(64, 16, title="LED Matrix")
pyxel.load("my_resource.pyxres")

def update():
    pass

def draw():
    led.clear()

    # Gesamten Bildausschnitt aus Bildbank 0 anzeigen
    led.blt(0, 0, 0, 0, 0, 64, 16)

    led.show()

pyxel.run(update, draw)
