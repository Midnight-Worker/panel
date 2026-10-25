#include "LEDMatrix.h"
#include <avr/pgmspace.h>

#define LED_PIN 6
#define BAUDRATE 115200

LEDMatrix matrix(LED_PIN);

// Original-Pyxel-Farbpalette
const uint32_t palette[16] PROGMEM = {
    0x000000, 0x2B335F, 0x7E2072, 0x19959C,
    0x8B4852, 0x395C98, 0xA9C1FF, 0xEEEEEE,
    0xD4186C, 0xD38441, 0xE9C35B, 0x70C6A9,
    0x7696DE, 0xA3A3A3, 0xFF9798, 0xEDC7B0
};

uint16_t framePos = 0;
bool receivingFrame = false;

void setup() {
    Serial.begin(BAUDRATE);
    matrix.begin(20);
}

void loop() {
    while (Serial.available()) {
        uint8_t data = Serial.read();

        // Bilddaten empfangen
        if (receivingFrame) {
            int x = framePos % MATRIX_WIDTH;
            int y = framePos / MATRIX_WIDTH;

            uint32_t color = pgm_read_dword(
                &palette[data & 0x0F]
            );

            matrix.pixel(x, y, color);
            framePos++;

            if (framePos == MATRIX_LEDS) {
                receivingFrame = false;
            }

            continue;
        }

        // Befehle empfangen
        switch (data) {
            case 'F':
                framePos = 0;
                receivingFrame = true;
                break;

            case 'S':
                matrix.show();
                Serial.write('K');
                break;

            case 'C':
                matrix.clear();
                break;
        }
    }
}
