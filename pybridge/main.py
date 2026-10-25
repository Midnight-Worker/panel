import pyxel
from ledmatrix import LEDMatrix

WIDTH = 64
HEIGHT = 16

LEVEL_WIDTH = 256
LEVEL_HEIGHT = 256

led = LEDMatrix("COM31")

pyxel.init(WIDTH, HEIGHT, title="LED Camera", fps=30)
pyxel.load("my_resource.pyxres")

cam_x = 0
cam_y = 0

dirty = True


def update():
    global cam_x, cam_y, dirty

    old_x = cam_x
    old_y = cam_y

    # Pfeiltasten mit Wiederholung beim Halten
    if pyxel.btnp(pyxel.KEY_LEFT, 10, 2):
        cam_x -= 1

    if pyxel.btnp(pyxel.KEY_RIGHT, 10, 2):
        cam_x += 1

    if pyxel.btnp(pyxel.KEY_UP, 10, 2):
        cam_y -= 1

    if pyxel.btnp(pyxel.KEY_DOWN, 10, 2):
        cam_y += 1

    # Kamera innerhalb der Bildbank halten
    cam_x = max(0, min(cam_x, LEVEL_WIDTH - WIDTH))
    cam_y = max(0, min(cam_y, LEVEL_HEIGHT - HEIGHT))

    # Nur bei Bewegung neue Daten senden
    if cam_x != old_x or cam_y != old_y:
        dirty = True

    if pyxel.btnp(pyxel.KEY_ESCAPE):
        pyxel.quit()


def draw():
    global dirty

    # Vorschau im Pyxel-Fenster
    pyxel.cls(0)
    pyxel.blt(0, 0, 0, cam_x, cam_y, WIDTH, HEIGHT)

    # LED-Matrix nur aktualisieren, wenn nötig
    if dirty:
        led.clear()

        led.blt(
            0, 0,          # Zielposition
            0,             # Bildbank 0
            cam_x, cam_y,  # Kamera-Ausschnitt
            WIDTH, HEIGHT
        )

        led.show()
        dirty = False


try:
    pyxel.run(update, draw)
finally:
    led.close()
