#pragma once

#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

// Vier Panels mit jeweils 16x16 Pixeln
#define PANEL_W 16
#define PANEL_H 16

#define PANELS_X 4
#define PANELS_Y 1

#define MATRIX_WIDTH  (PANEL_W * PANELS_X)
#define MATRIX_HEIGHT (PANEL_H * PANELS_Y)
#define MATRIX_LEDS   (MATRIX_WIDTH * MATRIX_HEIGHT)

// Farben
#define BLACK   0x000000
#define RED     0xFF0000
#define GREEN   0x00FF00
#define BLUE    0x0000FF
#define WHITE   0xFFFFFF
#define YELLOW  0xFFFF00
#define CYAN    0x00FFFF
#define MAGENTA 0xFF00FF

class LEDMatrix {
private:
    Adafruit_NeoPixel strip;

    // Logische X/Y-Koordinaten in LED-Nummern umrechnen
    int32_t xyToIndex(int x, int y) {
        if (x < 0 || x >= MATRIX_WIDTH ||
            y < 0 || y >= MATRIX_HEIGHT)
            return -1;

        // Welches Panel?
        int panelX = x / PANEL_W;
        int panelY = y / PANEL_H;

        int panel = panelY * PANELS_X + panelX;

        // Koordinaten innerhalb des Panels
        int localX = x % PANEL_W;
        int localY = y % PANEL_H;

        // Erste Zeile geht von RECHTS nach LINKS.
        // Zweite Zeile geht von LINKS nach RECHTS.
        if (localY % 2 == 0) {
            localX = PANEL_W - 1 - localX;
        }

        return (int32_t)panel * PANEL_W * PANEL_H
             + localY * PANEL_W + localX;
    }

public:
    LEDMatrix(uint8_t pin)
        : strip(MATRIX_LEDS, pin, NEO_GRB + NEO_KHZ800) {}

    void begin(uint8_t brightness = 20) {
        strip.begin();
        strip.setBrightness(brightness);
        clear();
        show();
    }

    int width() { return MATRIX_WIDTH; }
    int height() { return MATRIX_HEIGHT; }

    void pixel(int x, int y, uint32_t color) {
        int32_t i = xyToIndex(x, y);
        if (i >= 0)
            strip.setPixelColor((uint16_t)i, color);
    }

    void clear() {
        strip.clear();
    }

    void show() {
        strip.show();
    }

    void brightness(uint8_t value) {
        strip.setBrightness(value);
    }

    // Gefuelltes Rechteck
    void rect(int x, int y, int w, int h,
              uint32_t color) {
        for (int py = y; py < y + h; py++) {
            for (int px = x; px < x + w; px++) {
                pixel(px, py, color);
            }
        }
    }

    // Rechteckumrandung
    void drawRect(int x, int y, int w, int h,
                  uint32_t color) {
        for (int px = x; px < x + w; px++) {
            pixel(px, y, color);
            pixel(px, y + h - 1, color);
        }

        for (int py = y; py < y + h; py++) {
            pixel(x, py, color);
            pixel(x + w - 1, py, color);
        }
    }

    // Horizontale Linie
    void hline(int x, int y, int w, uint32_t color) {
        for (int i = 0; i < w; i++)
            pixel(x + i, y, color);
    }

    // Vertikale Linie
    void vline(int x, int y, int h, uint32_t color) {
        for (int i = 0; i < h; i++)
            pixel(x, y + i, color);
    }

    // Gesamtes Panel faerben (0 bis 3)
    void testPanel(int panel, uint32_t color) {
        if (panel < 0 || panel >= PANELS_X * PANELS_Y)
            return;

        int x = (panel % PANELS_X) * PANEL_W;
        int y = (panel / PANELS_X) * PANEL_H;

        rect(x, y, PANEL_W, PANEL_H, color);
    }
};
