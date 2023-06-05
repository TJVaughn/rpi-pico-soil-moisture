import time
import random
import math
import gc

import board
import digitalio
import analogio
import neopixel

SOIL_SENSOR_PIN = board.GP27
SOIL_POWER_PIN = board.GP7

CAP_SENSOR_SIGNAL = analogio.AnalogIn(SOIL_SENSOR_PIN)
CAP_SENSOR_POWER = digitalio.DigitalInOut(SOIL_POWER_PIN)
CAP_SENSOR_POWER.direction = digitalio.Direction.OUTPUT
CAP_SENSOR_POWER.value = False


SENSOR_MAX = 547
SENSOR_MIN = 275
AUTO_CALIBRATE = False
CALIBRATE_COUNT = 0
READING_DELAY = 1
NUM_PIXELS = 16
START = True
START_INTERVAL = 0.3

BLUE = [0, 0, 255]
BLUE_GREEN = [0, 255, 255]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]
ORANGE = [255, 127, 0]
RED = [255,0,0]


pixels = neopixel.NeoPixel(board.GP2, NUM_PIXELS, auto_write=False)
pixels.brightness = 0.5

def change_pixels(a):
    for i in range(NUM_PIXELS):
        pixels[i] = (a[0], a[1], a[2])
    pixels.show()

def set_pixels_by_percent(pct):
    if(pct > 90 and pct < 101):
        change_pixels(BLUE)
    elif (pct > 80):
        change_pixels(BLUE_GREEN)
    elif (pct > 60):
        change_pixels(GREEN)
    elif(pct > 40):
        change_pixels(ORANGE)
    elif(pct > 20):
        change_pixels(YELLOW)
    else:
        change_pixels(RED)

while True:
    print("RUNNING")
    if START:
        change_pixels(RED)
        time.sleep(START_INTERVAL)
        change_pixels(ORANGE)
        time.sleep(START_INTERVAL)
        change_pixels(GREEN)
        time.sleep(START_INTERVAL)
        change_pixels(BLUE_GREEN)
        time.sleep(START_INTERVAL)
        change_pixels(BLUE)
        time.sleep(START_INTERVAL)
        START = False

    if AUTO_CALIBRATE:
        print("CALIBRATE")
        CAP_SENSOR_POWER.value = True
        value = round(CAP_SENSOR_SIGNAL.value / 100)
        CAP_SENSOR_POWER.value = False

        print("value", value)

        if value > SENSOR_MAX:
            SENSOR_MAX = value

        if value < SENSOR_MIN:
            SENSOR_MIN = value

        if(CALIBRATE_COUNT > 99):
            print("\n---------------------")
            print("MIN", SENSOR_MIN)
            print("MAX", SENSOR_MAX)
            print("---------------------\n")
            time.sleep(5)

            AUTO_CALIBRATE = False
        CALIBRATE_COUNT += 1
        time.sleep(0.2)
    else:
        value = round(CAP_SENSOR_SIGNAL.value / 100)

        CAP_SENSOR_POWER.value = True

        percent = round(((value - SENSOR_MIN) / (SENSOR_MAX - SENSOR_MIN)) * 100) - 100
        if(percent < 0):
            percent *= -1
        print("Percent:", percent)


        CAP_SENSOR_POWER.value = True
        value = round(CAP_SENSOR_SIGNAL.value / 100)
        print("value", value)

        set_pixels_by_percent(percent)
        time.sleep(READING_DELAY)

