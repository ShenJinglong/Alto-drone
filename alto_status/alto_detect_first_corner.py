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

class alto_detect_first_corner_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        alto_detect_first_corner(flight)

    def exit_state(self, flight):
        pass

alto_detect_first_corner_counter = 0

def alto_detect_first_corner(flight):
    global alto_detect_first_corner_counter

    ret, frame = flight.read_camera()
    if not ret: return

    after_process_img = img_tools.image_pre_process(frame)
    lines = cv2.HoughLines(after_process_img, 1, np.pi / 180, 30, 0, 0)
    lines_class = math_tools.lineClassifier(lines)
    lines_params = math_tools.lineFit(lines_class)
    for line in lines_params: img_tools.drawHoughLine(frame, line, (0, 0, 255))

    if len(lines_params) > 1:
        cross_points = math_tools.findCrossPoint(lines_params)

        for i in range(len(cross_points)):
            cv2.circle(frame, cross_points[i], 3, (0, 255, 0), -1)

        if len(cross_points) == 1 and cross_points[0][0] < global_params.IMAGE_WIDTH / 2:
            alto_detect_first_corner_counter += 1
            flight.median_filter.add_number_c1(global_params.IMAGE_CENTER_Y - 30)
            flight.median_filter.add_number_c2(0)
        else:
            alto_detect_first_corner_counter = 0
            flight.median_filter.add_number_c1(global_params.IMAGE_CENTER_Y - 30)
            flight.median_filter.add_number_c2(0)
    elif len(lines_params) == 1 and lines_params[0][1] < 2.2 and lines_params[0][1] > 0.8:
        alto_detect_first_corner_counter = 0
        flight.median_filter.add_number_c1(math_tools.getLineWithX(lines_params[0], 0)[1])
        flight.median_filter.add_number_c2(math_tools.getLineAngleX(lines_params[0]))
    else:
        alto_detect_first_corner_counter = 0
        flight.median_filter.add_number_c1(global_params.IMAGE_CENTER_Y - 30)
        flight.median_filter.add_number_c2(0)

    speed_x, speed_y = flight.get_speed()
    flight_angle = global_params.FLY_ANGLE_N
    dst_point_y = flight.median_filter.get_result_number_c1() + 30
    path_angle = flight.median_filter.get_result_number_c2()
    data_to_send = {
        'mode': 'go_x',
        'flight_angle': flight_angle,
        'dst_point_y': dst_point_y,
        'speed_x': speed_x,
        'speed_y': speed_y,
        'path_angle': path_angle
    }
    flight.send(data_to_send)
    cv2.circle(frame, (0, int(dst_point_y)), 3, (255, 255, 0), -1)

    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    if alto_detect_first_corner_counter == alto_params.ALTO_DETECT_FIRST_CORNER_NUM:
        alto_detect_first_corner_counter = 0
        flight.next_state = macro.ALTO_STOP_TO_FIRST_CORNER
        print('>>> [!] ALTO_DETECT_FIRST_CORNER -> ALTO_STOP_TO_FIRST_CORNER')
    
