import time
from ledmatrix import LEDMatrix

led = LEDMatrix("COM31")

try:
    x = 0
    dx = 1

    while True:
        led.clear()

        # Bewegtes Quadrat
        led.rect(x, 4, 8, 8, 8)

        # Grüne Bodenlinie
        led.line(0, 15, 63, 15, 11)

        led.show()

        x += dx

        if x >= 56 or x <= 0:
            dx = -dx

        time.sleep(0.03)

except KeyboardInterrupt:
    led.clear()
    led.show()

finally:
    led.close()
