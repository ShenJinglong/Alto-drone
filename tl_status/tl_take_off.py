# -*- coding: utf-8 -*-

import cv2
import numpy as np

from BaseFSM import base_fsm

from tools import img_tools
from tools import math_tools

import global_params
from tl_status import tl_params

if global_params.USE_VD:
    import V_Display as vd

class tl_take_off_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        tl_take_off(flight)

    def exit_state(self, flight):
        pass

tl_take_off_counter = 0

def tl_take_off(flight):
    global tl_take_off_counter

    ret, frame = flight.read_camera()
    if not ret: return

    after_process_img = img_tools.image_pre_process(frame)
    # cv2.imshow('eee', after_process_img)
    lines = cv2.HoughLines(after_process_img, 1, np.pi / 180, 90, 0, 0)
    lines_class = math_tools.lineClassifier(lines)
    lines_params = math_tools.lineFit(lines_class)
    lines_params = math_tools.remove_horizontal_line(lines_params)
    for line in lines_params: img_tools.drawHoughLine(frame, line, (0, 0, 255))

    print(flight.get_speed())

    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    tl_take_off_counter += 1
    if tl_take_off_counter == tl_params.TL_TAKE_OFF_NUM:
        tl_take_off_counter = 0