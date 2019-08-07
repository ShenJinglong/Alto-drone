# -*- coding: utf-8 -*-

import time

import global_params
import macro

from BaseFSM import base_fsm

if global_params.RASPBERRY_MODE:
    import RPi.GPIO as GPIO

class mode_selector_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        mode_selector(flight)

    def exit_state(self, flight):
        pass

if global_params.RASPBERRY_MODE:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(global_params.MODE_PIN_1, GPIO.IN)
    GPIO.setup(global_params.MODE_PIN_2, GPIO.IN)
    GPIO.setup(global_params.MODE_PIN_3, GPIO.IN)
    GPIO.setup(global_params.MODE_PIN_4, GPIO.IN)
    GPIO.setup(12, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(13, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(17, GPIO.OUT, initial = GPIO.HIGH)

def mode_selector(flight):
    if global_params.RASPBERRY_MODE:
        v1 = GPIO.input(global_params.MODE_PIN_1)
        v2 = GPIO.input(global_params.MODE_PIN_2)
        v3 = GPIO.input(global_params.MODE_PIN_3)
        v4 = GPIO.input(global_params.MODE_PIN_4)
        if v4 and v3 and v2 and v1:
            show_error()
        elif v4 and v3 and v2 and not v1:
            show_error()
        elif v4 and v3 and not v2 and v1:
            show_error()
        else:
            show_error()
    else:
        flight.next_state = macro.TL_TAKE_OFF
        flight.main_mode = 0x90

def show_mode(blink_time):
    for i in range(blink_time):
        GPIO.output(17, 0)
        time.sleep(0.5)
        GPIO.output(17, 1)
        time.sleep(0.5)

def show_error():
    GPIO.output(12, 0)
    time.sleep(0.5)
    GPIO.output(12, 1)
    time.sleep(0.5)