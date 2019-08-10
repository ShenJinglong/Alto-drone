# -*- coding: utf-8 -*-

import numpy as np
import cv2

import global_params
import macro
from alto_status import alto_params

from tools import math_tools
from tools import img_tools

from BaseFSM import base_fsm

if global_params.USE_VD:
    import V_Display as vd

class alto_brake_2_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()
    
    def exec_state(self, flight):
        alto_brake_2(flight)
    
    def exit_state(self, flight):
        pass

alto_brake_2_counter = 0
delay_counter = 0

def alto_brake_2(flight):
    global alto_brake_2_counter
    global delay_counter

    ret, frame = flight.read_camera()
    if ret != True: return

    speed_x, speed_y = flight.get_speed()

    if delay_counter >= 0:
        data_to_send = {
            'mode': 'brake',
            'speed_x': speed_x,
            'speed_y': speed_y
        }
        flight.send(data_to_send)
        alto_brake_2_counter += 1
        print('brake')
    else:
        delay_counter += 1
        print('delay')

    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    if alto_brake_2_counter == 10:
        alto_brake_2_counter = 0
        delay_counter = 0
        flight.next_state = macro.ALTO_BACK
        print(' >>> [!] ALTO_BREAK_2 -> ALTO_BACK')