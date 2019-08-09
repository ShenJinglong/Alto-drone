# -*- coding: utf-8 -*-

import cv2
import numpy as np

from BaseFSM import base_fsm

from tools import img_tools
from tools import math_tools

import global_params
from alto_status import alto_params
import macro

if global_params.USE_VD:
    import V_Display as vd

class alto_land_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        alto_land(flight)

    def exit_state(self, flight):
        pass

alto_land_counter = 0

def alto_land(flight):
    global alto_land_counter
    
    ret, frame = flight.read_camera()
    if not ret: return

    dst_point_x = 80
    dst_point_y = 60
    uart_buff = bytearray([0x55,               0xAA, 0x70, dst_point_x & 0xff,
                           dst_point_y & 0xff, 0x00, 0x00, 0x00,
                           0x00,               0x00, 0x00, 0xAA               ])
    flight.send(uart_buff)

    alto_land_counter += 1

    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    if alto_land_counter == alto_params.ALTO_LAND_NUM:
        alto_land_counter = 0
        flight.next_state = macro.ALTO_LAND
        print('>>> [!] ALTO_TURN -> ALTO_LAND')

