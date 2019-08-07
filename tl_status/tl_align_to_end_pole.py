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

class tl_align_to_end_pole_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        tl_align_to_end_pole(flight)

    def exit_state(self, flight):
        pass

tl_align_to_end_pole_counter = 0

def tl_align_to_end_pole(flight):
    global tl_align_to_end_pole_counter

    ret, frame = flight.read_camera()
    if not ret: return

    after_process_img = img_tools.image_pre_process(frame)
    # cv2.imshow('eee', after_process_img)
    lines = cv2.HoughLines(after_process_img, 1, np.pi / 180, 90, 0, 0)
    lines_class = math_tools.lineClassifier(lines)
    lines_params = math_tools.lineFit(lines_class)
    lines_params = math_tools.remove_horizontal_line(lines_params)
    for line in lines_params: img_tools.drawHoughLine(frame, line, (0, 0, 255))

    if len(lines_params) == 1:
        _x = math_tools.getLineWithY(lines_params[0], global_params.IMAGE_HEIGHT / 2)[0]
        if global_params.IMAGE_CENTER_X - 30 < _x and _x < global_params.IMAGE_CENTER_X + 30:
            tl_align_to_end_pole_counter += 1
        else:
            tl_align_to_end_pole_counter = 0
        flight.median_filter.add_number_c1(_x)
    else:
        tl_align_to_end_pole_counter = 0
        flight.median_filter.add_number_c1(global_params.IMAGE_WIDTH / 2)
    
    dst_point_x = flight.median_filter.get_result_number_c1()
    data_to_send = {
        'mode': 'stop_tp',
        'dst_point_x': dst_point_x
    }
    flight.send(data_to_send)

    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    if tl_align_to_end_pole_counter == tl_params.TL_ALIGN_TO_END_POLE_NUM:
        tl_align_to_end_pole_counter = 0