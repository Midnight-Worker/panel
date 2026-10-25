import time
import serial


class LEDMatrix:
    WIDTH = 64
    HEIGHT = 16

    def __init__(self, port="COM6", baudrate=115200):
        self.ser = serial.Serial(
            port,
            baudrate,
            timeout=3,
            write_timeout=3
        )

        self.buffer = bytearray(
            self.WIDTH * self.HEIGHT
        )

        # Arduino startet beim Öffnen des Ports neu
        time.sleep(2)
        self.ser.reset_input_buffer()

    def clear(self, color=0):
        self.buffer[:] = bytes([color & 15]) * len(
            self.buffer
        )

    def pixel(self, x, y, color):
        x, y = int(x), int(y)

        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            self.buffer[y * self.WIDTH + x] = color & 15

    # Alias wie Pyxel
    pset = pixel

    def pget(self, x, y):
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            return self.buffer[y * self.WIDTH + x]
        return 0

    def rect(self, x, y, w, h, color):
        for py in range(y, y + h):
            for px in range(x, x + w):
                self.pixel(px, py, color)

    def rectb(self, x, y, w, h, color):
        for px in range(x, x + w):
            self.pixel(px, y, color)
            self.pixel(px, y + h - 1, color)

        for py in range(y, y + h):
            self.pixel(x, py, color)
            self.pixel(x + w - 1, py, color)

    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)

        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        error = dx + dy

        while True:
            self.pixel(x0, y0, color)

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * error

            if e2 >= dy:
                error += dy
                x0 += sx

            if e2 <= dx:
                error += dx
                y0 += sy

    def blt(self, x, y, img, u, v, w, h, colkey=None):
        """
        Kopiert ein Pyxel-Sprite in den LED-Bildspeicher.

        img: Pyxel-Bildbank (0, 1, 2 usw.)
             oder ein pyxel.Image-Objekt
        """
        import pyxel

        source = (
            pyxel.images[img]
            if isinstance(img, int)
            else img
        )

        for iy in range(abs(h)):
            for ix in range(abs(w)):
                sx = u + ix * (1 if w >= 0 else -1)
                sy = v + iy * (1 if h >= 0 else -1)

                color = source.pget(sx, sy)

                if colkey is not None and color == colkey:
                    continue

                self.pixel(x + ix, y + iy, color)

    def show(self):
        # Komplettes Bild übertragen
        self.ser.write(b"F")
        self.ser.write(self.buffer)
        self.ser.write(b"S")
        self.ser.flush()

        # Warten, bis der Arduino die LEDs aktualisiert hat
        answer = self.ser.read(1)

        if answer != b"K":
            raise TimeoutError(
                "Keine Bestätigung vom Arduino"
            )

    def close(self):
        self.ser.close()
