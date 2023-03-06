#!/usr/bin/env python

import sys
import time
import signal
import subprocess

import RPi.GPIO as gpio

# es gibt zwei PIN Nummerierungs Schemata

# 1. BOARD
#   wie die Zahlen die auf dem Pinout des Raspberry PI stehen
#   (aus meiner Sicht zu bevorzugen, wenn man es nicht anders braucht)

# 2. BCM (Broadcom SOC channel)
#   pin nummerierung nach nummer des verbundenen chip pins .....
#   (aus meiner Sicht hier nicht zu bevorzugen)

# Das Script aus dem Netz verwendet BCM !
# D.h. es ist möglich, dass du das falsch gesteckt hast!


# wie lange das display anbleiben soll in sekunden
COUNTDOWN = 60

# pfade zu scripten
DISPLAY_ON_SCRIPT = ""
DISPLAY_OFF_SCRIPT = ""


def ctrl_c_handler(sig, frame):
    # gpio.cleanup() wurde in dem anderen Script vergessen!
    # wenn gpio.cleanup() nicht aufgerufen wird,
    # kann das zu problemen beim nächsten aufruf führen
    gpio.cleanup()
    sys.exit(0)

#def rising_handler(pin):
#    global COUNTDOWN
#    COUNTDOWN = STAY_ON_TIME

if __name__ == "__main__":
    signal.signal(signal.SIGINT, ctrl_c_handler)
    print("drücke STRG+C um dieses Script zu beenden")
    
    PIR_PIN = 25    # 22 on the board
    gpio.setmode(gpio.BCM)
    gpio.setup(PIR_PIN, gpio.IN)
    gpio.add_event_detect(PIR_PIN, gpio.RISING)

    turned_on = gpio.input(PIR_PIN)
    countdown = 0

    while True:
        if gpio.event_detected(PIR_PIN):
            countdown = COUNTDOWN
            if not turned_on:
                subprocess.call(f"sh {DISPLAY_ON_SCRIPT}", shell=True)
                turned_on = True
        else:
            countdown -= 1
        if countdown == 0 and turned_on:
            subprocess.call(f"sh {DISPLAY_OFF_SCRIPT}", shell=True)
            turned_on = False
        time.sleep(1)
