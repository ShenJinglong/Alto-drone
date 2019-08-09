# -*- coding: utf-8 -*-

import cv2
import numpy as np

from BaseFSM import base_fsm

from tools import math_tools
from tools import img_tools

from alto_status import alto_params

import global_params
import macro

if global_params.USE_VD:
    import V_Display as vd

class alto_turn_2_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        alto_turn_2(flight)

    def exit_state(self, flight):
        pass

alto_turn_2_counter = 0

def alto_turn_2(flight):
    global alto_turn_2_counter

    ret, frame = flight.read_camera()
    if not ret: return

    after_process_img = img_tools.image_pre_process(frame)
    lines = cv2.HoughLines(after_process_img, 1, np.pi / 180, 50, 0, 0)
    lines_class = math_tools.lineClassifier(lines)
    lines_params = math_tools.lineFit(lines_class)
    lines_params = math_tools.remove_horizontal_line(lines_params)
    for line in lines_params: img_tools.drawHoughLine(frame, line, (0, 0, 255))

    if len(lines_params) == 1:
        flight.median_filter.add_number_c1(math_tools.getLineWithY(lines_params[0], 120)[0])
        flight.median_filter.add_number_c2(math_tools.getLineAngleY(lines_params[0]))
    else:
        flight.median_filter.add_number_c1(global_params.IMAGE_CENTER_X - 30)
        flight.median_filter.add_number_c2(0)

    flight_angle = 110
    dst_point_x = flight.median_filter.get_result_number_c1() + 30
    path_angle = flight.median_filter.get_result_number_c2() + 100
    speed_x, speed_y = flight.get_speed()
    data_to_send = {
        'mode': 'go_y',
        'flight_angle': flight_angle,
        'dst_point_x': dst_point_x,
        'speed_x': speed_x,
        'speed_y': speed_y,
        'path_angle': path_angle
    }
    flight.send(data_to_send)
    cv2.circle(frame, (int(dst_point_x), 120), 5, (255, 255, 0), -1)

    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    alto_turn_2_counter += 1

    if alto_turn_2_counter == 90:
        alto_turn_2_counter = 0
        flight.next_state = macro.ALTO_BREAK_2
        print('>>> [!] ALTO_TURN_2 -> ALTO_BREAK_2')
    
