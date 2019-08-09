# -*- coding: utf-8 -*-

import cv2
import numpy as np

from BaseFSM import base_fsm

import global_params
from alto_status import alto_params
import macro

from tools import math_tools
from tools import img_tools

if global_params.USE_VD:
    import V_Display as vd

class alto_stop_to_first_corner_fsm(base_fsm):
    def enter_state(self, flight):
        flight.median_filter.refresh()

    def exec_state(self, flight):
        alto_stop_to_first_corner(flight)

    def exit_state(self, flight):
        pass

alto_stop_to_first_corner_counter = 0

def alto_stop_to_first_corner(flight):
    global alto_stop_to_first_corner_counter

    ret, frame = flight.read_camera()
    if not ret: return

    after_process_img = img_tools.image_pre_process(frame)
    lines = cv2.HoughLines(after_process_img, 1, np.pi / 180, 50, 0, 0)
    lines_class = math_tools.lineClassifier(lines)
    lines_params = math_tools.lineFit(lines_class)
    for line in lines_params: img_tools.drawHoughLine(frame, line, (0, 0, 255))

    if len(lines_params) > 1:
        cross_points = math_tools.findCrossPoint(lines_params)

        for i in range(len(cross_points)):
            cv2.circle(frame, cross_points[i], 3, (0, 255, 0), -1)

        if len(cross_points) == 1:
            flight.median_filter.add_point_c1(cross_points[0])
        else:
            flight.median_filter.add_point_c1([global_params.IMAGE_CENTER_X - 30, global_params.IMAGE_CENTER_Y - 30])
    else:
        flight.median_filter.add_point_c1([global_params.IMAGE_CENTER_X - 30, global_params.IMAGE_CENTER_Y - 30])

    dst_point_x, dst_point_y = flight.median_filter.get_result_point_c1()
    dst_point_x += 30
    dst_point_y += 30
    # dst_point_x = (dst_point_x - 80) / 2 + 80
    # dst_point_y = (dst_point_y - 60) / 2 + 60
    speed_x, speed_y = flight.get_speed()
    data_to_send = {
        'mode': 'stop_tp',
        'dst_point_x': dst_point_x,
        'dst_point_y': dst_point_y,
        'speed_x': speed_x,
        'speed_y': speed_y
    }
    flight.send(data_to_send)
    cv2.circle(frame, (int(dst_point_x), int(dst_point_y)), 3, (255, 255, 0), -1)

    if global_params.USE_VD:
        vd.show(frame)
    else:
        cv2.imshow('frame', frame)

    alto_stop_to_first_corner_counter += 0
    if alto_stop_to_first_corner_counter == alto_params.ALTO_STOP_TO_FIRST_CORNER_NUM:
        alto_stop_to_first_corner_counter = 0
        flight.next_state = macro.ALTO_DETECT_SECOND_CORNER
        print('>>> [!] ALTO_STOP_TO_FIRST_CORNER -> ALTO_DETECT_SECOND_CORNER')
    