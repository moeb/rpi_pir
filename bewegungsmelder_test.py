#!/usr/bin/env python

import sys
import signal
import datetime

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

def ctrl_c_handler(sig, frame):
    # gpio.cleanup() wurde in dem anderen Script vergessen!
    # wenn gpio.cleanup() nicht aufgerufen wird,
    # kann das zu problemen beim nächsten aufruf führen
    gpio.cleanup()
    sys.exit(0)

def rising_handler(pin):
    print(datetime.datetime.now().time(), "angegangen")

def falling_handler(pin):
    print(datetime.datetime.now().time(), "ausgegangen")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, ctrl_c_handler)
    print("drücke STRG+C um dieses Script zu beenden")
    
    PIR_PIN = 25    # 22 on the board
    gpio.setmode(gpio.BCM)
    gpio.setup(PIR_PIN, gpio.IN)

    # bouncetime verhindert prellen
    gpio.add_event_detect(PIR_PIN, gpio.FALLING, callback=falling_handler, bouncetime=200)
    gpio.add_event_detect(PIR_PIN, gpio,RISING, callback=rising_handler, bouncetime=200)

    while True:
        time.sleep(0.1)

