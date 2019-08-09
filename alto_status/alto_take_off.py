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

class alto_take_off_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        alto_take_off(flight)

    def exit_state(self, flight):
        pass

alto_take_off_counter = 0

def alto_take_off(flight):
    global alto_take_off_counter

    ret, src_frame = flight.read_camera()
    if not ret: return
    frame = src_frame.copy()

    after_process_img = img_tools.image_pre_process(frame)
    lines = cv2.HoughLines(after_process_img, 1, np.pi / 180, 50, 0, 0)
    lines_class = math_tools.lineClassifier(lines)
    lines_params = math_tools.lineFit(lines_class)
    lines_params = math_tools.remove_vertical_line(lines_params)
    for line in lines_params: img_tools.drawHoughLine(frame, line, (0, 0, 255))
    
    if len(lines_params) == 1:
        flight.median_filter.add_number_c1(math_tools.getLineWithX(lines_params[0], 0)[1])
        flight.median_filter.add_number_c2(math_tools.getLineAngleX(lines_params[0]))
        alto_take_off_counter += 1
    else:
        flight.median_filter.add_number_c1(global_params.IMAGE_CENTER_Y - 30)
        flight.median_filter.add_number_c2(0)

    flight_angle = global_params.FLY_ANGLE_N
    dst_point_y = flight.median_filter.get_result_number_c1() + 30
    path_angle = flight.median_filter.get_result_number_c2() + 100
    speed_x, speed_y = flight.get_speed()
    data_to_send = {
        'mode': 'go_x',
        'flight_angle': flight_angle,
        'dst_point_y': dst_point_y,
        'speed_x': speed_x,
        'speed_y': speed_y,
        'path_angle': path_angle
    }
    flight.send(data_to_send)
    cv2.circle(frame, (0, int(dst_point_y)), 5, (255, 255, 0), -1)
    
    # cv2.imshow('ss', pole_buttom_roi_th)
    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    print(alto_take_off_counter)

    if alto_take_off_counter == alto_params.ALTO_TAKE_OFF_NUM:
        alto_take_off_counter = 0
        flight.next_state = macro.ALTO_GO
        print('>>> [!] ALTO_TAKE_OFF -> ALTO_GO')

