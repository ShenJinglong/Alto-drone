# -*- coding: utf-8 -*-

import cv2
import numpy as np

from BaseFSM import base_fsm

from tools import img_tools
from tools import math_tools

import macro

import global_params
from tl_status import tl_params

if global_params.USE_VD:
    import V_Display as vd

class rect_test_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        rect_test(flight)

    def exit_state(self, flight):
        pass


def rect_test(flight):
    ret, frame = flight.read_camera()
    if not ret: return

    after_process_img = img_tools.image_pre_process(frame)
    lines = cv2.HoughLines(after_process_img, 1, np.pi / 180, 50, 0, 0)
    lines_class = math_tools.lineClassifier(lines)
    lines_params = math_tools.lineFit(lines_class)
    lines_params = math_tools.remove_vertical_line(lines_params)
    for line in lines_params: img_tools.drawHoughLine(frame, line, (0, 0, 255))


    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)